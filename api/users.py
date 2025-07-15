"""
Vercel Serverless Function: User Management
URL: /api/users/[name]
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import urlparse, parse_qs

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

try:
    from db import init_db, get_user_by_name
except ImportError:
    def get_user_by_name(name):
        # Fallback user data
        if name.lower() == 'alice':
            return {"id": 1, "name": "Alice", "points": 0}
        return None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse URL to get username
            path = self.path
            # Expected format: /api/users/Alice
            parts = path.split('/')
            
            if len(parts) >= 4:
                username = parts[3]  # /api/users/Alice -> Alice
            else:
                username = 'Alice'  # Default user
            
            # Initialize database
            if 'init_db' in globals():
                init_db()
            
            # Get user by name
            user = get_user_by_name(username)
            
            if user:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(user).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {"error": "User not found"}
                self.wfile.write(json.dumps(error_response).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {"error": f"Failed to get user: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
