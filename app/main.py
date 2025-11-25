from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

# Symulacja "bazy danych" w pamięci
processed_records = []

@app.route('/')
def home():
    return jsonify({
        "service": "Data Pipeline API",
        "version": os.getenv("APP_VERSION", "1.0. 0"),
        "endpoints": ["/health", "/api/transform", "/api/stats"]
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime. now().isoformat()
    })

@app.route('/api/transform', methods=['POST'])
def transform():
    """
    Prosty ETL - przyjmuje dane, transformuje, zwraca
    Przykład: {"name": "jan", "age": "25"} 
           -> {"name": "JAN", "age": 25, "processed_at": "... "}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # TRANSFORM: uppercase name, convert age to int
    transformed = {
        "name": data.get("name", ""). upper(),
        "age": int(data.get("age", 0)),
        "processed_at": datetime.now().isoformat(),
        "source": "data-pipeline-api"
    }
    
    # Zapisz do "bazy"
    processed_records.append(transformed)
    
    return jsonify({
        "status": "success",
        "original": data,
        "transformed": transformed
    })

@app.route('/api/stats')
def stats():
    """Statystyki przetworzonych danych"""
    if not processed_records:
        return jsonify({
            "total_records": 0,
            "message": "No data processed yet"
        })
    
    ages = [r["age"] for r in processed_records]
    
    return jsonify({
        "total_records": len(processed_records),
        "avg_age": sum(ages) / len(ages),
        "min_age": min(ages),
        "max_age": max(ages)
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0. 0.0.0', port=port, debug=True)
