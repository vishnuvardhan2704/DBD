from flask import Flask, request, jsonify
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
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-for-development')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')}})

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
        if field not in data or data[field] is None:
            return False, f'Missing required field: {field}'
    
    return True, 'Valid'

def validate_positive_integer(value, field_name):
    """Validate positive integer values"""
    try:
        val = int(value)
        if val <= 0:
            return False, f'{field_name} must be positive'
        return True, val
    except (ValueError, TypeError):
        return False, f'{field_name} must be a valid integer'

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/products', methods=['GET'])
def get_products():
    products = get_all_products()
    return jsonify(products)

@app.route('/api/users/<name>', methods=['GET'])
def get_user(name):
    user = get_user_by_name(name)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/cart/<int:user_id>', methods=['GET'])
def get_user_cart(user_id):
    if not get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
    cart_items = get_cart(user_id)
    return jsonify(cart_items)

@app.route('/api/cart', methods=['POST'])
def add_item_to_cart():
    data = request.get_json()
    is_valid, msg = validate_json_data(data, ['user_id', 'product_id'])
    if not is_valid:
        return jsonify({'error': msg}), 400

    user_id = data['user_id']
    product_id = data['product_id']
    quantity = data.get('quantity', 1)

    is_valid, quantity = validate_positive_integer(quantity, 'Quantity')
    if not is_valid:
        return jsonify({'error': quantity}), 400

    if not get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
    if not get_product_by_id(product_id):
        return jsonify({'error': 'Product not found'}), 404
    ok, msg = add_to_cart(user_id, product_id, quantity)
    if not ok:
        return jsonify({'error': msg}), 400
    return jsonify({'message': msg})

@app.route('/api/cart/<int:user_id>', methods=['DELETE'])
def clear_user_cart(user_id):
    if not get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
    clear_cart(user_id)
    return jsonify({'message': 'Cart cleared'})

@app.route('/api/recommendation', methods=['POST'])
def get_recommendation():
    data = request.json
    product_id = data.get('product_id')
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    alternative = find_greener_alternative(product)
    if not alternative:
        return jsonify({'message': 'No greener alternative found'})
    reason = get_gemini_reason(product, alternative)
    carbon_saved = estimate_carbon_savings(product, alternative)
    return jsonify({
        'original': product,
        'alternative': alternative,
        'reason': reason,
        'carbon_saved': carbon_saved,
        'points_awarded': int(carbon_saved * float(os.getenv('CARBON_POINTS_MULTIPLIER', '10.0')))
    })

@app.route('/api/points/<int:user_id>', methods=['PUT'])
def update_points(user_id):
    data = request.json
    points = data.get('points')
    if not get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
    try:
        points = int(points)
    except Exception:
        return jsonify({'error': 'Points must be an integer'}), 400
    update_user_points(user_id, points)
    return jsonify({'message': 'Points updated'})

@app.route('/api/gemini_test', methods=['GET'])
def gemini_test():
    from gemini import get_gemini_api_key
    api_key = get_gemini_api_key()
    if not api_key:
        return jsonify({'error': 'GEMINI_API_KEY not set'}), 400
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = "Say hello from Gemini API."
        response = model.generate_content(prompt)
        return jsonify({'result': response.text.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    debug_mode = app.config.get('DEBUG', True)
    
    print("🚀 Starting ESG Recommender Backend...")
    print(f"🌐 Debug mode: {debug_mode}")
    print(f"📍 Server will be available at: http://localhost:5000")
    print(f"🔗 API endpoints: http://localhost:5000/api/")
    
    app.run(debug=debug_mode, port=5000, host='127.0.0.1')