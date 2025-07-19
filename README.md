# 🌱 ESG Recommender - Sustainable Shopping Assistant

> **AI-powered sustainability recommendations for conscious consumers**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

---

## 📋 Overview

The **ESG Recommender** is a full-stack web application that helps users make more sustainable shopping decisions through:

- **ESG Scoring**: Environmental, Social, and Governance ratings for products
- **AI Recommendations**: Smart suggestions for greener alternatives using Google Gemini AI
- **Carbon Tracking**: Real-time environmental impact calculations
- **Gamification**: Points system to reward sustainable choices
- **Responsive Design**: Works perfectly on mobile and desktop

---

## 🏗️ Architecture

### **Technology Stack**
- **Frontend**: React.js with Material-UI
- **Backend**: Python Flask with Gunicorn
- **Database**: SQLite (with easy PostgreSQL upgrade path)
- **AI Integration**: Google Gemini API (optional)
- **Deployment**: Render.com
- **Styling**: Material-UI + Custom CSS

### **Project Structure**
```
esg-recommender/                    # 🧹 CLEAN & ORGANIZED
├── 📁 api/                        # Backend (Python Flask)
│   ├── app.py                     # Main Flask application
│   ├── db.py                      # Database operations
│   ├── recommender.py             # ESG scoring algorithms
│   ├── gemini.py                  # AI integration
│   ├── requirements.txt           # Python dependencies
│   └── esg_recommender.db         # SQLite database
│
├── 📁 frontend/                   # Frontend (React)
│   ├── src/
│   │   ├── App.js                 # Main React component
│   │   ├── App.css                # Styling
│   │   └── index.js               # Entry point
│   ├── public/                    # Static assets
│   └── package.json               # Node.js dependencies
│
├── 📄 Configuration Files
│   ├── .env.template              # Environment variables template
│   ├── .gitignore                 # Git ignore rules (prevents clutter)
│   ├── build.sh                   # Build script for Render
│   ├── Procfile                   # Process configuration
│   ├── render.yaml                # Render deployment config
│   └── requirements.txt           # Python dependencies (root)
│
└── 📚 Documentation
    ├── README.md                  # This documentation
    ├── SETUP_GUIDE.md             # Quick setup guide
    ├── PROJECT_STRUCTURE.md       # Clean structure overview
    └── test_setup.py              # Setup verification script
```

---

## 🚀 Deployment on Render.com

### **Option 1: One-Click Deploy**
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### **Option 2: Manual Deployment**

1. **Fork or clone this repository**
2. **Connect to Render.com**:
   - Go to [render.com](https://render.com)
   - Sign up/in with GitHub
   - Click "New" → "Web Service"
   - Connect your repository

3. **Configuration**:
   - **Name**: `esg-recommender`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd api && gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Instance Type**: `Free` (or upgrade as needed)

4. **Environment Variables**:
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = `your-secret-key-here`
   - `GEMINI_API_KEY` = `your-gemini-api-key` (optional, for AI features)

5. **Deploy**: Click "Create Web Service"

### **Environment Variables Setup**

In your Render dashboard, add these environment variables:

```bash
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
GEMINI_API_KEY=your-gemini-api-key-here  # Optional
```

To get a Gemini API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your Render environment variables

---

## 🔧 Local Development

### **Prerequisites**
- Python 3.9+
- Node.js 16+
- Git

### **Setup**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vishnuvardhan2704/DBD.git
   cd DBD
   ```

2. **Backend Setup**:
   ```bash
   cd api
   pip install -r requirements.txt
   python app.py
   ```

3. **Frontend Setup** (new terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Environment Variables**:
   ```bash
   cp .env.template .env
   # Edit .env with your values
   ```

### **Development URLs**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/api/health

---

## 📱 Features

### **Core Features**
- **Product Catalog**: Browse sustainable products with ESG ratings
- **Shopping Cart**: Add items with real-time sustainability scoring
- **AI Recommendations**: Get personalized suggestions for greener alternatives
- **Carbon Tracking**: Monitor your environmental impact
- **User Points**: Earn rewards for sustainable choices
- **Responsive Design**: Works on all devices

### **ESG Scoring System**
```python
ESG Score = (
    organic_bonus * 20 +           # Organic certification
    packaging_score * 15 +         # Sustainable packaging
    carbon_efficiency * 30 +       # Carbon per dollar
    price_efficiency * 25 +        # Value proposition
    category_bonus * 10            # Category-specific bonus
)
```

### **API Endpoints**
- `GET /api/health` - Health check
- `GET /api/products` - Product catalog
- `GET /api/cart` - User cart
- `POST /api/cart` - Add to cart
- `DELETE /api/cart` - Clear cart
- `POST /api/recommendation` - Get AI recommendations

---

## 🔒 Security & Best Practices

### **Security Features**
- **Environment Variables**: Secure API key storage
- **CORS Configuration**: Controlled cross-origin requests
- **Input Validation**: Sanitized user inputs
- **Error Handling**: Graceful error responses

### **Performance Optimizations**
- **Static File Serving**: Efficient asset delivery
- **Database Optimization**: Indexed queries
- **Caching**: Response caching for frequent requests
- **Minification**: Optimized frontend assets

---

## 🧪 Testing

### **Run Tests Locally**
```bash
# Backend tests
cd api
python -m pytest tests/

# Frontend tests
cd frontend
npm test
```

### **API Testing**
```bash
# Health check
curl https://your-app.onrender.com/api/health

# Get products
curl https://your-app.onrender.com/api/products

# Add to cart
curl -X POST https://your-app.onrender.com/api/cart \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

---

## 🔧 Customization

### **Adding New Products**
Edit `api/db.py` and modify the `seed_data()` function:

```python
def seed_data():
    products = [
        {
            "name": "Your Product",
            "category": "category",
            "price": 9.99,
            "esg_score": 85,
            "carbon_footprint": 0.5,
            "organic": True,
            "packaging": "minimal",
            "description": "Product description"
        }
    ]
```

### **Customizing ESG Scoring**
Edit `api/recommender.py` to modify the scoring algorithm:

```python
def calculate_esg_score(product):
    # Your custom scoring logic
    return score
```

### **UI Customization**
Edit `frontend/src/App.css` for styling changes or modify `frontend/src/App.js` for functionality changes.

---

## 🚧 Troubleshooting

### **Common Issues**

**Build Fails**:
- Make sure `build.sh` is executable: `chmod +x build.sh`
- Check that all dependencies are in `requirements.txt`

**Frontend Not Loading**:
- Verify build files exist in `api/static/`
- Check Render build logs for errors

**API Errors**:
- Check environment variables are set correctly
- Verify database initialization in logs

**AI Features Not Working**:
- Ensure `GEMINI_API_KEY` is set in environment variables
- Check API quota limits

### **Debug Mode**
Set `FLASK_ENV=development` in environment variables for detailed error messages.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- **Google Gemini AI** for intelligent recommendations
- **Material-UI** for beautiful React components
- **Render.com** for reliable hosting
- **Open Source Community** for inspiration and tools

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/vishnuvardhan2704/DBD/issues)
- **Documentation**: This README
- **Community**: [Discussions](https://github.com/vishnuvardhan2704/DBD/discussions)

---

**🌱 Ready to make shopping more sustainable? Deploy now!**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
