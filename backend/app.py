from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db, get_all_products, get_user_by_name, get_user_by_id, add_to_cart, get_cart, clear_cart, update_user_points, get_product_by_id
from recommender import find_greener_alternative, estimate_carbon_savings
from gemini import get_gemini_reason
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize database
init_db()

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
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    if not user_id or not product_id:
        return jsonify({'error': 'user_id and product_id required'}), 400
    if not get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
    if not get_product_by_id(product_id):
        return jsonify({'error': 'Product not found'}), 404
    try:
        quantity = int(quantity)
    except Exception:
        return jsonify({'error': 'Quantity must be an integer'}), 400
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
        'points_awarded': int(carbon_saved * 10)
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
    app.run(debug=True, port=5000) 