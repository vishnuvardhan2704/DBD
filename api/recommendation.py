"""
Vercel Serverless Function: AI Recommendations
URL: /api/recommendation
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

try:
    from db import init_db, get_product_by_id
    from recommender import find_greener_alternative, estimate_carbon_savings
    from gemini import get_gemini_reason
except ImportError:
    def get_product_by_id(pid):
        return {"id": pid, "name": "Sample Product", "carbon_kg": 2.0}
    def find_greener_alternative(product):
        return {"id": 99, "name": "Greener Alternative", "carbon_kg": 1.0}
    def estimate_carbon_savings(original, alternative):
        return 1.0
    def get_gemini_reason(original, alternative):
        return "This alternative is more sustainable due to better packaging and lower carbon footprint."

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Initialize database
            if 'init_db' in globals():
                init_db()
            
            product_id = data.get('product_id')
            if not product_id:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {"error": "product_id is required"}
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Get original product
            original_product = get_product_by_id(product_id)
            if not original_product:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {"error": "Product not found"}
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Find greener alternative
            alternative = find_greener_alternative(original_product)
            
            if alternative:
                # Calculate carbon savings
                carbon_saved = estimate_carbon_savings(original_product, alternative)
                points_awarded = int(carbon_saved * 10)  # 10 points per kg CO2 saved
                
                # Get AI explanation
                reason = get_gemini_reason(original_product, alternative)
                
                response = {
                    "original": original_product,
                    "alternative": alternative,
                    "reason": reason,
                    "carbon_saved": carbon_saved,
                    "points_awarded": points_awarded
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {"error": "No greener alternative found"}
                self.wfile.write(json.dumps(error_response).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {"error": f"Failed to get recommendation: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
