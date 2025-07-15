# 🌱 ESG Product Recommendation System - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture) 
3. [File Structure](#file-structure)
4. [Quick Start](#quick-start)
5. [API Reference](#api-reference)
6. [Configuration](#configuration)
7. [Deployment](#deployment)
8. [Development](#development)
9. [Troubleshooting](#troubleshooting)

---

## Project Overview

The **ESG Product Recommendation System** is a full-stack web application that helps users make more sustainable shopping choices. It analyzes products based on Environmental, Social, and Governance (ESG) criteria and provides AI-powered recommendations for greener alternatives.

### Key Features
- 🎨 **Modern React UI** with Material-UI components
- 🤖 **AI-Powered Recommendations** using Google Gemini API
- 📊 **ESG Scoring System** with sustainability metrics
- 🛒 **Smart Shopping Cart** with alternative suggestions
- 📱 **Responsive Design** for all devices
- 🔒 **Production Ready** with Docker support

---

## Architecture

### System Architecture
```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐    SQL    ┌─────────────┐
│                 │    API Calls    │                 │  Queries  │             │
│  React Frontend │ ←─────────────→ │  Flask Backend  │ ←────────→│   SQLite    │
│   (Port 3000)   │                 │   (Port 5000)   │           │  Database   │
│                 │                 │                 │           │             │
└─────────────────┘                 └─────────────────┘           └─────────────┘
                                             │
                                             │ API Calls
                                             ▼
                                    ┌─────────────────┐
                                    │                 │
                                    │   Gemini AI     │
                                    │   (Optional)    │
                                    │                 │
                                    └─────────────────┘
```

### Component Breakdown

#### Frontend (React)
- **Technology**: React 19.1.0 + Material-UI 7.2.0
- **Purpose**: User interface and experience
- **Features**:
  - Product catalog with ESG badges
  - Shopping cart management
  - AI recommendation dialogs
  - User authentication (mock)
  - Responsive design

#### Backend (Flask)
- **Technology**: Flask 2.3.0 + Python 3.8+
- **Purpose**: Business logic and data management
- **Features**:
  - REST API endpoints
  - ESG scoring algorithm
  - Database operations
  - AI integration with Gemini
  - CORS handling

#### Database (SQLite)
- **Technology**: SQLite (easily replaceable with PostgreSQL/MySQL)
- **Purpose**: Data persistence
- **Tables**:
  - `products` - Product catalog with ESG data
  - `users` - User profiles and points
  - `cart` - Shopping cart items

#### AI Integration (Gemini)
- **Technology**: Google Generative AI
- **Purpose**: Generate explanations for sustainability recommendations
- **Fallback**: Works with dummy responses if no API key provided

---

## File Structure

```
esg_recommender/
├── 📁 backend/                    # Flask API Server
│   ├── 📄 app.py                 # Main Flask application (119 lines)
│   ├── 📄 db.py                  # Database operations (157 lines)
│   ├── 📄 recommender.py         # ESG scoring & recommendation logic (100+ lines)
│   ├── 📄 gemini.py              # Google Gemini AI integration (50 lines)
│   ├── 📄 requirements.txt       # Python dependencies (5 packages)
│   ├── 📄 .env.template          # Environment variables template
│   ├── 📄 .env                   # Environment variables (created from template)
│   ├── 📄 Dockerfile             # Backend container configuration
│   ├── 📄 Procfile               # Heroku deployment configuration
│   └── 📄 esg_recommender.db     # SQLite database (auto-created)
│
├── 📁 frontend/                   # React Application
│   ├── 📁 src/
│   │   ├── 📄 App.js             # Main React component (405 lines)
│   │   ├── 📄 App.css            # Application styles
│   │   └── 📄 index.js           # React entry point
│   ├── 📁 public/                # Static assets
│   ├── 📄 package.json           # Node.js dependencies
│   ├── 📄 Dockerfile             # Frontend container configuration
│   └── 📄 nginx.conf             # Production web server configuration
│
├── 📄 docker-compose.yml         # Multi-container orchestration
├── 📄 README.md                  # This documentation file
├── 📄 setup.py                   # Automated setup script
├── 📄 test_setup.py              # System validation tests
├── 📄 .gitignore                 # Git ignore rules
│
├── 🏃 start_backend.bat          # Windows backend starter
├── 🏃 start_backend.sh           # Linux/Mac backend starter
├── 🏃 start_frontend.bat         # Windows frontend starter
└── 🏃 start_frontend.sh          # Linux/Mac frontend starter
```

### Core Files Explained

#### `backend/app.py` (Main Flask Application)
- **Purpose**: Central Flask application with all API endpoints
- **Key Functions**:
  - `/api/health` - Health check
  - `/api/products` - Product catalog
  - `/api/recommendation` - AI recommendations
  - `/api/cart/*` - Cart management
  - `/api/users/*` - User management
- **Dependencies**: Flask, Flask-CORS, python-dotenv

#### `backend/db.py` (Database Operations)
- **Purpose**: All database interactions and setup
- **Key Functions**:
  - `init_db()` - Create tables and sample data
  - `get_all_products()` - Retrieve product catalog
  - `add_to_cart()` - Cart management
  - Context managers for safe database connections
- **Database Schema**: 3 tables (products, users, cart)

#### `backend/recommender.py` (ESG Logic)
- **Purpose**: Sustainability scoring and recommendation algorithms
- **Key Classes**:
  - `ESGScorer` - Advanced scoring system with configurable weights
  - Functions for finding alternatives and calculating carbon savings
- **Scoring Factors**: Organic certification, packaging type, carbon footprint, price efficiency

#### `backend/gemini.py` (AI Integration)
- **Purpose**: Google Gemini AI integration for explanations
- **Fallback**: Dummy responses if no API key provided
- **API**: Uses `google-generativeai` library

#### `frontend/src/App.js` (React Application)
- **Purpose**: Complete React application in single component
- **Features**: Material-UI interface, state management, API calls
- **Components**: Product cards, recommendation dialogs, shopping cart drawer

---

## Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** (for cloning)

### Option 1: Automated Setup (Recommended)
```bash
# 1. Clone repository
git clone <your-repo-url>
cd esg_recommender

# 2. Run automated setup
python setup.py
# This installs dependencies and creates configuration

# 3. Start services
start_backend.bat    # Windows Terminal 1
start_frontend.bat   # Windows Terminal 2

# Or for Linux/Mac
./start_backend.sh   # Terminal 1
./start_frontend.sh  # Terminal 2
```

### Option 2: Manual Setup
```bash
# 1. Backend setup
cd backend
pip install -r requirements.txt
cp .env.template .env  # Optional: edit to add Gemini API key

# 2. Frontend setup
cd ../frontend
npm install

# 3. Start backend (Terminal 1)
cd ../backend
python app.py

# 4. Start frontend (Terminal 2)
cd ../frontend
npm start
```

### Option 3: Docker (Production)
```bash
# 1. Create environment file
echo "SECRET_KEY=your-secret-key" > .env
echo "GEMINI_API_KEY=your-api-key" >> .env

# 2. Start with Docker Compose
docker-compose up --build
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api/
- **Health Check**: http://localhost:5000/api/health

---

## API Reference

### Base URL
```
http://localhost:5000/api
```

### Authentication
No authentication required (mock user system)

### Endpoints

#### Health Check
```http
GET /health
```
Returns server status.

**Response:**
```json
{"status": "ok"}
```

#### Products
```http
GET /products
```
Get all products with ESG information.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Organic Free-Range Chicken",
    "description": "Organic, free-range chicken",
    "category": "meat",
    "packaging": "paper",
    "is_organic": true,
    "carbon_kg": 2.1,
    "price": 12.99
  }
]
```

#### Users
```http
GET /users/{name}
```
Get user by name (mock authentication).

**Response:**
```json
{
  "id": 1,
  "name": "Alice",
  "points": 150
}
```

#### Shopping Cart
```http
GET /cart/{user_id}           # Get cart items
POST /cart                    # Add item to cart
DELETE /cart/{user_id}        # Clear cart
```

**Add to Cart Request:**
```json
{
  "user_id": 1,
  "product_id": 2,
  "quantity": 1
}
```

#### Recommendations
```http
POST /recommendation
```
Get AI-powered sustainable alternative.

**Request:**
```json
{
  "product_id": 1
}
```

**Response:**
```json
{
  "original": { /* product data */ },
  "alternative": { /* better product data */ },
  "reason": "AI explanation of why alternative is better",
  "carbon_saved": 1.1,
  "points_awarded": 11
}
```

### Error Responses
All endpoints return consistent error format:
```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (validation error)
- `404` - Resource not found
- `500` - Internal server error

---

## Configuration

### Environment Variables

Create `backend/.env` file:
```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-for-production
FLASK_DEBUG=true                           # Development mode

# Database (optional)
ESG_DB_PATH=esg_recommender.db

# Gemini AI (optional - works with dummy responses if not set)
GEMINI_API_KEY=your-gemini-api-key-here

# CORS (optional)
CORS_ORIGINS=http://localhost:3000

# Scoring (optional)
CARBON_POINTS_MULTIPLIER=10.0
```

### ESG Scoring Configuration

Edit `backend/recommender.py` to customize scoring:
```python
WEIGHTS = {
    'organic': 3.0,          # Organic certification weight
    'packaging': 2.0,        # Packaging impact weight  
    'carbon': 2.5,          # Carbon footprint weight
    'price_efficiency': 1.0  # Price efficiency weight
}

PACKAGING_SCORES = {
    'glass': 2,     # Best packaging
    'paper': 1.5,   # Good packaging
    'plastic': -1,  # Poor packaging
    'styrofoam': -2 # Worst packaging
}
```

---

## Deployment

### Development (Local)
```bash
# Backend (Terminal 1)
cd backend && python app.py

# Frontend (Terminal 2)
cd frontend && npm start
```

### Production Deployment

**📖 See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed step-by-step instructions!**

**Quick Summary**:
- **Frontend**: Deploy to Netlify (free, easy drag-and-drop)
- **Backend**: Deploy to Heroku, Railway, or Render (free tiers available)
- **Database**: SQLite works for small projects, upgrade to PostgreSQL for production

**5-Minute Deployment**:
1. `cd frontend && npm run build` 
2. Drag `build` folder to [netlify.com](https://netlify.com)
3. Deploy backend to Heroku with `git push heroku main`
4. Update frontend API URL and redeploy

#### Docker (Advanced)
```bash
# Full stack deployment
docker-compose up -d

# Scale services
docker-compose up -d --scale backend=2
```

---

## Development

### Adding New Products
Edit `backend/db.py` in the `insert_mock_data()` function:
```python
products = [
    ('Product Name', 'Description', 'category', 'packaging', is_organic, carbon_kg, price),
    # Add your products here
]
```

### Modifying ESG Rules
Edit `backend/recommender.py`:
```python
def calculate_sustainability_score(product):
    score = 0
    # Add your custom scoring logic
    return score
```

### UI Customization
Edit `frontend/src/App.js` for:
- Colors and theme
- Component layout
- New features

### Database Changes
For production, replace SQLite with PostgreSQL:
1. Update `backend/db.py` connection string
2. Install `psycopg2-binary`
3. Set `DATABASE_URL` environment variable

---

## Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies
pip install -r backend/requirements.txt

# Check port availability
netstat -an | findstr :5000  # Windows
lsof -i :5000                # Linux/Mac
```

#### Frontend Won't Start
```bash
# Check Node.js version
node --version  # Should be 16+

# Install dependencies
npm install

# Clear cache
npm start -- --reset-cache
```

#### "Connection Refused" Errors
- Backend not running on port 5000
- Check firewall settings
- Verify CORS configuration

#### API Key Issues
- Gemini API key not set (system works without it)
- Invalid API key format
- API rate limits exceeded

#### Database Errors
```bash
# Reset database
rm backend/esg_recommender.db
python backend/app.py  # Will recreate
```

### Performance Issues
- **Backend**: Use gunicorn with multiple workers
- **Frontend**: Run `npm run build` for production
- **Database**: Add indexes for large datasets

### Development Tips
```bash
# Reset everything
rm backend/esg_recommender.db
rm -rf frontend/node_modules
python setup.py

# Test API endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/products

# Monitor logs
tail -f backend/app.log  # If logging to file
```

---

## Project Statistics

- **Total Files**: 20 essential files (after cleanup)
- **Backend Code**: ~500 lines of Python
- **Frontend Code**: ~400 lines of JavaScript/JSX
- **Dependencies**: 5 Python packages, 15 npm packages
- **Database Tables**: 3 (products, users, cart)
- **API Endpoints**: 8 main endpoints
- **Docker Support**: Multi-container setup
- **Documentation**: Single comprehensive file

---

## License

MIT License - Free to use for personal and commercial projects.

---

**Made with ❤️ for a greener world** 🌱

*This system demonstrates how AI can help consumers make more sustainable choices while providing a beautiful, professional, and production-ready user experience.*
