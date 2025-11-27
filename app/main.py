"""Data Pipeline API - Flask application for data transformation.

This module provides REST API endpoints for:
- Health checking
- Data transformation (ETL operations)
- Statistics reporting
"""

from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

processed_records = []

@app.route('/')
def home():
    """Return API information and available endpoints."""
    return jsonify({
        "service": "Data Pipeline API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "endpoints": ["/health", "/api/transform", "/api/stats"]
    })

@app.route('/health')
def health():
    """Health check endpoint for monitoring and load balancers."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/transform', methods=['POST'])
def transform():
    """Transform incoming data with ETL operations.
    
    Accepts JSON payload and applies transformations:
    - name: converted to uppercase
    - age: converted to integer
    
    Returns:
        JSON with original data, transformed data, and status.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    transformed = {
        "name": data.get("name", "").upper(),
        "age": int(data.get("age", 0)),
        "processed_at": datetime.now().isoformat(),
        "source": "data-pipeline-api"
    }
    
    processed_records.append(transformed)
    
    return jsonify({
        "status": "success",
        "original": data,
        "transformed": transformed
    })

@app.route('/api/stats')
def stats():
    """Return statistics for all processed records."""
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
    app.run(host='0.0.0.0', port=port, debug=True)
