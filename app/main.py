"""Crypto Tracker API - Real-time cryptocurrency prices and portfolio tracking."""

import json
import redis
import os
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# === Database configuration ===
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'postgres')
db_host = os.getenv('DB_HOST', 'postgres-postgresql')
db_name = os.getenv('DB_NAME', 'postgres')

# === conn string for SQLAlchemy ===
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class PortfolioItem(db.Model):
    """Model for portfolio items."""
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True)
    coin = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    buy_price = db.Column(db.Float, nullable=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

class PortfolioAlert(db.Model):
    """Model for portfolio alerts."""
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    coin = db.Column(db.String(20), nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    direction = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    triggered = db.Column(db.Boolean, default=False)

# === auto create tables if not exist ===
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")

# === redis config (caching only)===
redis_host = os.getenv('REDIS_HOST', 'redis-master')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', '')

try:
    cache = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True,
        socket_timeout=2
    )
    cache.ping()
    print(f"Connected to Redis: {redis_host}")
except redis.RedisError as e:
    print(f"Redis connection error: {e}")
    cache = None

# Prometheus metrics
requests_total = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('app_request_duration_seconds', 'Request duration')

# CoinGecko API base URL
COINGECKO_API = "https://api.coingecko.com/api/v3"

@app.route('/')
def home():
    """Return API information."""
    return jsonify({
        "service": "Crypto Tracker API (SQL Backend)",
        "version": os.getenv("APP_VERSION", "2.1.0"),
        "status": "active"
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    status = {"status": "healthy", "timestamp": datetime.now().isoformat()}

    try:
        db.session.execute(db.text('SELECT 1'))
        status["db"] = "connected"
    except Exception as e:
        status["db"] = f"error: {e}"
        status["status"] = "unhealthy"

    if cache:
        try:
            cache.ping()
            status["redis"] = "connected"
        except:
            status["redis"] = "disconnected"
    else:
        status["redis"] = "disabled"

    return jsonify(status)


@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/crypto/<coin>')
def get_coin_price(coin):
    """Get current price for a specific cryptocurrency (Uses Redis Cache)."""
    requests_total.labels(method='GET', endpoint='/api/crypto').inc()
    
    coin_lower = coin.lower()
    cache_key = f"price_{coin_lower}"

    if cache:
        try:
            cached_data = cache.get(cache_key)
            if cached_data:
                return jsonify(json.loads(cached_data))
        except redis.RedisError:
            pass

    try:
        response = requests.get(
            f"{COINGECKO_API}/simple/price",
            params={
                "ids": coin_lower,
                "vs_currencies": "usd,eur,pln",
                "include_24hr_change": "true",
                "include_market_cap": "true"
            },
            timeout=10
        )
        data = response.json()
        
        if not data:
            return jsonify({"error": f"Coin '{coin}' not found"}), 404
        
        coin_data = data.get(coin_lower, {})
        
        result = {
            "coin": coin_lower,
            "prices": {
                "usd": coin_data.get("usd"),
                "eur": coin_data.get("eur"),
                "pln": coin_data.get("pln")
            },
            "change_24h": coin_data.get("usd_24h_change"),
            "market_cap_usd": coin_data.get("usd_market_cap"),
            "timestamp": datetime.now().isoformat(),
            "source": "api" 
        }

        if cache:
            try:
                cache.setex(cache_key, 60, json.dumps(result))
            except redis.RedisError:
                pass

        return jsonify(result)

    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500


@app.route('/api/portfolio/add', methods=['POST'])
def add_to_portfolio():
    """Add cryptocurrency to portfolio (PERSISTENT)."""
    data = request.get_json()
    
    if not data or 'coin' not in data or 'amount' not in data:
        return jsonify({"error": "Required: coin, amount"}), 400
    
    coin = data['coin'].lower()
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Amount must be a valid number"}), 400
    
    # === SQL: Check if coin already exists in portfolio ===
    item = PortfolioItem.query.filter_by(coin=coin).first()
    
    if item:
        item.amount += amount
    else:
        new_item = PortfolioItem(coin=coin, amount=amount)
        db.session.add(new_item)
    
    try:
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": f"Added {amount} {coin.upper()} to persistent portfolio"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/api/portfolio')
def get_portfolio():
    """Get portfolio with current values."""
    # === SQL: Get current portfolio from DATABASE ===
    items = PortfolioItem.query.all()
    
    if not items:
        return jsonify({
            "message": "Portfolio is empty",
            "hint": "POST /api/portfolio/add with {coin, amount}"
        })
    
    coin_ids = [item.coin for item in items]
    portfolio_map = {item.coin: item.amount for item in items}
    
    # === API: Fetch current prices from CoinGecko (for valuation) ===
    try:
        response = requests.get(
            f"{COINGECKO_API}/simple/price",
            params={
                "ids": ",".join(coin_ids),
                "vs_currencies": "usd,pln"
            },
            timeout=10
        )
        prices = response.json()
        
        holdings = []
        total_usd = 0
        total_pln = 0
        
        for coin, amount in portfolio_map.items():
            coin_prices = prices.get(coin, {})
            current_usd = coin_prices.get('usd', 0)
            current_pln = coin_prices.get('pln', 0)
            
            value_usd = amount * current_usd
            value_pln = amount * current_pln
            
            total_usd += value_usd
            total_pln += value_pln
            
            holdings.append({
                "coin": coin,
                "amount": amount,
                "current_price_usd": current_usd,
                "value_usd": round(value_usd, 2),
                "value_pln": round(value_pln, 2)
            })
        
        return jsonify({
            "holdings": holdings,
            "total_value": {
                "usd": round(total_usd, 2),
                "pln": round(total_pln, 2)
            },
            "timestamp": datetime.now().isoformat()
        })
    except requests.RequestException as e:
        return jsonify({
            "error": "Failed to fetch live prices", 
            "holdings_only": portfolio_map
        }), 500


@app.route('/api/alerts', methods=['GET', 'POST'])
def manage_alerts():
    """Create or view price alerts (PERSISTENT)."""
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or 'coin' not in data or 'target_price' not in data:
            return jsonify({"error": "Required: coin, target_price"}), 400
        
        try:
            target_price = float(data['target_price'])
            if target_price <= 0:
                return jsonify({"error": "Target price must be greater than 0"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Target price must be a valid number"}), 400
        
        new_alert = PortfolioAlert(
            coin=data['coin'].lower(),
            target_price=target_price,
            direction=data.get('direction', 'above')
        )
        
        try:
            db.session.add(new_alert)
            db.session.commit()
            return jsonify({
                "status": "success",
                "alert_id": new_alert.id,
                "message": "Alert saved to database"
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    alerts_list = PortfolioAlert.query.all()
    return jsonify({
        "alerts": [{
            "id": a.id, 
            "coin": a.coin, 
            "target_price": a.target_price, 
            "direction": a.direction,
            "created_at": a.created_at.isoformat()
        } for a in alerts_list]
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)