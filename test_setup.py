import requests
import json

def test_backend():
    """Test if Flask backend is running"""
    try:
        response = requests.get('http://localhost:5000/api/products')
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Backend is running! Found {len(products)} products")
            return True
        else:
            print(f"❌ Backend error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Start with: cd backend && python app.py")
        return False

def test_user():
    """Test user login"""
    try:
        response = requests.get('http://localhost:5000/api/users/Alice')
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User 'Alice' found with {user['points']} points")
            return True
        else:
            print("❌ User 'Alice' not found")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running")
        return False

def test_recommendation():
    """Test recommendation API"""
    try:
        response = requests.post('http://localhost:5000/api/recommendation', 
                               json={'product_id': 1})
        if response.status_code == 200:
            data = response.json()
            if 'alternative' in data:
                print(f"✅ Recommendation working: {data['alternative']['name']}")
                return True
            else:
                print("✅ Recommendation API working (no alternative found)")
                return True
        else:
            print(f"❌ Recommendation error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running")
        return False

if __name__ == "__main__":
    print("🧪 Testing ESG Recommender Setup...")
    print("=" * 50)
    
    backend_ok = test_backend()
    user_ok = test_user()
    rec_ok = test_recommendation()
    
    print("=" * 50)
    if backend_ok and user_ok and rec_ok:
        print("🎉 All tests passed! Your ESG recommender is ready!")
        print("🌐 Open http://localhost:3000 in your browser")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("💡 Make sure both backend and frontend are running") 