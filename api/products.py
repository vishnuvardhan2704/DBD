"""
Vercel Serverless Function: Get All Products
URL: /api/products
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add current directory to path so we can import our modules
sys.path.append(os.path.dirname(__file__))

try:
    from db import init_db, get_all_products
except ImportError:
    # Fallback data if database import fails
    def get_all_products():
        return [
            {"id": 1, "name": "Organic Free-Range Chicken", "description": "Organic, free-range chicken", "category": "meat", "packaging": "paper", "is_organic": True, "carbon_kg": 2.1, "price": 12.99},
            {"id": 2, "name": "Organic Oat Milk", "description": "Organic oat milk", "category": "dairy", "packaging": "glass", "is_organic": True, "carbon_kg": 0.8, "price": 4.99}
        ]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Initialize database (creates tables if needed)
            if 'init_db' in globals():
                init_db()
            
            # Get all products
            products = get_all_products()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(products).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {"error": f"Failed to get products: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
