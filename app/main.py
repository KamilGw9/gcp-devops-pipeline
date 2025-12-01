"""Crypto Tracker API - Real-time cryptocurrency prices and portfolio tracking."""

from flask import Flask, jsonify, request
import os
from datetime import datetime
import requests
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus metrics
requests_total = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('app_request_duration_seconds', 'Request duration')

# In-memory storage (w prawdziwej apce: baza danych)
alerts = []
portfolio = {}

# CoinGecko API base URL
COINGECKO_API = "https://api.coingecko.com/api/v3"


@app.route('/')
def home():
    """Return API information and available endpoints."""
    return jsonify({
        "service": "Crypto Tracker API",
        "version": os.getenv("APP_VERSION", "2.0.0"),
        "endpoints": {
            "GET /health": "Health check",
            "GET /metrics": "Prometheus metrics",
            "GET /api/crypto/<coin>": "Get price for specific coin (e.g., bitcoin, ethereum)",
            "GET /api/crypto/top10": "Get top 10 cryptocurrencies",
            "GET /api/crypto/compare? coins=btc,eth": "Compare multiple coins",
            "POST /api/portfolio/add": "Add coin to portfolio",
            "GET /api/portfolio": "View your portfolio with current values",
            "POST /api/alerts": "Set price alert",
            "GET /api/alerts": "View all alerts"
        }
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.route('/api/crypto/<coin>')
def get_coin_price(coin):
    """Get current price for a specific cryptocurrency."""
    requests_total.labels(method='GET', endpoint='/api/crypto').inc()
    
    try:
        response = requests.get(
            f"{COINGECKO_API}/simple/price",
            params={
                "ids": coin.lower(),
                "vs_currencies": "usd,eur,pln",
                "include_24hr_change": "true",
                "include_market_cap": "true"
            },
            timeout=10
        )
        data = response.json()
        
        if not data:
            return jsonify({"error": f"Coin '{coin}' not found"}), 404
        
        coin_data = data.get(coin.lower(), {})
        
        return jsonify({
            "coin": coin.lower(),
            "prices": {
                "usd": coin_data.get("usd"),
                "eur": coin_data.get("eur"),
                "pln": coin_data.get("pln")
            },
            "change_24h": coin_data.get("usd_24h_change"),
            "market_cap_usd": coin_data.get("usd_market_cap"),
            "timestamp": datetime.now().isoformat()
        })
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500


@app.route('/api/crypto/top10')
def get_top_10():
    """Get top 10 cryptocurrencies by market cap."""
    requests_total.labels(method='GET', endpoint='/api/crypto/top10').inc()
    
    try:
        response = requests.get(
            f"{COINGECKO_API}/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 10,
                "page": 1,
                "sparkline": "false"
            },
            timeout=10
        )
        data = response.json()
        
        coins = []
        for coin in data:
            coins.append({
                "rank": coin.get("market_cap_rank"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol").upper(),
                "price_usd": coin.get("current_price"),
                "change_24h": round(coin.get("price_change_percentage_24h", 0), 2),
                "market_cap": coin.get("market_cap")
            })
        
        return jsonify({
            "top_10": coins,
            "timestamp": datetime.now().isoformat()
        })
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500


@app.route('/api/crypto/compare')
def compare_coins():
    """Compare multiple cryptocurrencies."""
    coins_param = request.args.get('coins', 'bitcoin,ethereum')
    coin_ids = [c.strip().lower() for c in coins_param.split(',')]
    
    # Map common symbols to CoinGecko IDs
    symbol_map = {
        "btc": "bitcoin",
        "eth": "ethereum", 
        "sol": "solana",
        "ada": "cardano",
        "xrp": "ripple",
        "doge": "dogecoin",
        "dot": "polkadot",
        "matic": "matic-network",
        "link": "chainlink",
        "ltc": "litecoin"
    }
    
    coin_ids = [symbol_map.get(c, c) for c in coin_ids]
    
    try:
        response = requests.get(
            f"{COINGECKO_API}/simple/price",
            params={
                "ids": ",".join(coin_ids),
                "vs_currencies": "usd,pln",
                "include_24hr_change": "true"
            },
            timeout=10
        )
        data = response.json()
        
        comparison = []
        for coin_id in coin_ids:
            coin_data = data.get(coin_id, {})
            if coin_data:
                comparison.append({
                    "coin": coin_id,
                    "price_usd": coin_data.get("usd"),
                    "price_pln": coin_data.get("pln"),
                    "change_24h": round(coin_data.get("usd_24h_change", 0), 2)
                })
        
        return jsonify({
            "comparison": comparison,
            "timestamp": datetime.now().isoformat()
        })
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch data", "details": str(e)}), 500


@app.route('/api/portfolio/add', methods=['POST'])
def add_to_portfolio():
    """Add cryptocurrency to portfolio."""
    data = request.get_json()
    
    if not data or 'coin' not in data or 'amount' not in data:
        return jsonify({"error": "Required: coin, amount"}), 400
    
    coin = data['coin'].lower()
    amount = float(data['amount'])
    buy_price = data.get('buy_price')  # Optional
    
    if coin in portfolio:
        portfolio[coin]['amount'] += amount
    else:
        portfolio[coin] = {
            'amount': amount,
            'buy_price': buy_price,
            'added_at': datetime.now().isoformat()
        }
    
    return jsonify({
        "status": "success",
        "message": f"Added {amount} {coin.upper()} to portfolio",
        "portfolio": portfolio
    })


@app.route('/api/portfolio')
def get_portfolio():
    """Get portfolio with current values."""
    if not portfolio:
        return jsonify({
            "message": "Portfolio is empty",
            "hint": "POST /api/portfolio/add with {coin, amount}"
        })
    
    coin_ids = list(portfolio.keys())
    
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
        
        for coin, data in portfolio.items():
            coin_prices = prices.get(coin, {})
            value_usd = data['amount'] * coin_prices.get('usd', 0)
            value_pln = data['amount'] * coin_prices.get('pln', 0)
            total_usd += value_usd
            total_pln += value_pln
            
            holdings.append({
                "coin": coin,
                "amount": data['amount'],
                "current_price_usd": coin_prices.get('usd'),
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
        return jsonify({"error": "Failed to fetch prices", "details": str(e)}), 500


@app.route('/api/alerts', methods=['GET', 'POST'])
def manage_alerts():
    """Create or view price alerts."""
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or 'coin' not in data or 'target_price' not in data:
            return jsonify({"error": "Required: coin, target_price, direction (above/below)"}), 400
        
        alert = {
            "id": len(alerts) + 1,
            "coin": data['coin'].lower(),
            "target_price": float(data['target_price']),
            "direction": data.get('direction', 'above'),
            "created_at": datetime.now().isoformat(),
            "triggered": False
        }
        alerts.append(alert)
        
        return jsonify({
            "status": "success",
            "alert": alert
        })
    
    # GET - return all alerts
    return jsonify({"alerts": alerts})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)