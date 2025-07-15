"""
Vercel Serverless Function: Shopping Cart Management
URL: /api/cart
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import urlparse, parse_qs

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

try:
    from db import init_db, add_to_cart, get_cart, clear_cart
except ImportError:
    def add_to_cart(user_id, product_id, quantity=1):
        return True, "Added to cart (fallback)"
    def get_cart(user_id):
        return []
    def clear_cart(user_id):
        pass

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse URL to get user_id
            query = urlparse(self.path).query
            params = parse_qs(query)
            user_id = int(params.get('user_id', [1])[0])
            
            # Initialize database
            if 'init_db' in globals():
                init_db()
            
            # Get cart items
            cart_items = get_cart(user_id)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(cart_items).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {"error": f"Failed to get cart: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Initialize database
            if 'init_db' in globals():
                init_db()
            
            # Add item to cart
            user_id = data.get('user_id', 1)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            
            if not product_id:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {"error": "product_id is required"}
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            success, message = add_to_cart(user_id, product_id, quantity)
            
            if success:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {"message": message}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {"error": message}
                self.wfile.write(json.dumps(error_response).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {"error": f"Failed to add to cart: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_DELETE(self):
        try:
            # Parse URL to get user_id
            query = urlparse(self.path).query
            params = parse_qs(query)
            user_id = int(params.get('user_id', [1])[0])
            
            # Initialize database
            if 'init_db' in globals():
                init_db()
            
            # Clear cart
            clear_cart(user_id)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {"message": "Cart cleared"}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {"error": f"Failed to clear cart: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
