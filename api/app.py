from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import logging
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database and business logic modules
from db import init_db, get_all_products, get_user_by_name, get_user_by_id, add_to_cart, get_cart, clear_cart, update_user_points, get_product_by_id
from recommender import find_greener_alternative, estimate_carbon_savings
from gemini import get_gemini_reason

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-for-development')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("✅ ESG Recommender Backend initialized successfully")

# Initialize database
init_db()

def handle_errors(f):
    """Decorator for consistent error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return decorated_function

# Input validation helpers
def validate_json_data(data, required_fields):
    """Validate JSON request data"""
    if not data:
        return False, 'Missing JSON body'
    
    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'
    
    return True, None

# --- API Routes ---

@app.route('/', methods=['GET'])
@handle_errors
def serve_frontend():
    """Serve the React frontend"""
    return send_file('static/index.html')

@app.route('/api/', methods=['GET'])
@handle_errors
def api_root():
    """API root endpoint"""
    return jsonify({
        'message': 'ESG Recommender API', 
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'products': '/api/products',
            'cart': '/api/cart',
            'recommendation': '/api/recommendation'
        }
    })

# Frontend routes (catch-all for React Router)
@app.route('/<path:path>')
def serve_frontend_routes(path):
    """Serve frontend routes for React Router"""
    # Check if it's a static file
    if '.' in path and path.split('.')[-1] in ['js', 'css', 'png', 'jpg', 'ico', 'svg']:
        return send_from_directory('static', path)
    # Otherwise serve the React app
    return send_file('static/index.html')

@app.route('/api/health', methods=['GET'])
@handle_errors
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'ESG Recommender API is running'})

@app.route('/api/products', methods=['GET'])
@handle_errors
def get_products():
    """Get all products with ESG information"""
    products = get_all_products()
    return jsonify(products)

@app.route('/api/users/<name>', methods=['GET'])
@handle_errors
def get_user(name):
    """Get user by name"""
    user = get_user_by_name(name)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/cart', methods=['GET'])
@handle_errors
def get_user_cart():
    """Get cart items for a user"""
    user_id = request.args.get('user_id', default=1, type=int)
    cart_items = get_cart(user_id)
    return jsonify(cart_items)

@app.route('/api/cart', methods=['POST'])
@handle_errors
def add_to_user_cart():
    """Add item to cart"""
    data = request.get_json()
    is_valid, error_msg = validate_json_data(data, ['product_id'])
    
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    user_id = data.get('user_id', 1)
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    success, message = add_to_cart(user_id, product_id, quantity)
    
    if success:
        return jsonify({'message': message})
    else:
        return jsonify({'error': message}), 400

@app.route('/api/cart', methods=['DELETE'])
@handle_errors
def clear_user_cart():
    """Clear user's cart"""
    user_id = request.args.get('user_id', default=1, type=int)
    clear_cart(user_id)
    return jsonify({'message': 'Cart cleared successfully'})

@app.route('/api/recommendation', methods=['POST'])
@handle_errors
def get_recommendation():
    """Get AI-powered sustainability recommendation"""
    data = request.get_json()
    is_valid, error_msg = validate_json_data(data, ['product_id'])
    
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    product_id = data.get('product_id')
    
    # Get original product
    original_product = get_product_by_id(product_id)
    if not original_product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Find greener alternative
    alternative = find_greener_alternative(original_product)
    
    if alternative:
        # Calculate carbon savings
        carbon_saved = estimate_carbon_savings(original_product, alternative)
        points_awarded = int(carbon_saved * 10)  # 10 points per kg CO2 saved
        
        # Get AI explanation
        reason = get_gemini_reason(original_product, alternative)
        
        # Update user points (assuming user_id = 1 for demo)
        user_id = 1
        user = get_user_by_id(user_id)
        if user:
            new_points = user['points'] + points_awarded
            update_user_points(user_id, new_points)
        
        response = {
            'original': original_product,
            'alternative': alternative,
            'reason': reason,
            'carbon_saved': carbon_saved,
            'points_awarded': points_awarded
        }
        
        return jsonify(response)
    else:
        return jsonify({'error': 'No greener alternative found'}), 404

# --- Run Application ---

# For Render.com and production
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
