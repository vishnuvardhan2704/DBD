# 🌱 ESG Recommender - Sustainable Shopping Assistant

> **AI-powered sustainability recommendations for conscious consumers**

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/vishnuvardhan2704/DBD)

---

## 📋 **Overview**

The **ESG Recommender** is a full-stack web application that helps users make more sustainable shopping decisions through:

- **ESG Scoring**: Environmental, Social, and Governance ratings for products
- **AI Recommendations**: Smart suggestions for greener alternatives
- **Carbon Tracking**: Real-time environmental impact calculations
- **Gamification**: Points system to reward sustainable choices

### **Key Features:**
- 🛒 Interactive shopping cart with ESG insights
- 📊 Real-time sustainability metrics dashboard
- 🤖 AI-powered product recommendations (Google Gemini)
- 🏆 User scoring system and achievements
- 📱 Responsive design for all devices

---

## 🏗️ **Architecture**

### **Technology Stack:**
- **Frontend**: React.js with Material-UI
- **Backend**: Python Flask (Serverless Functions)
- **Database**: SQLite with in-memory fallback
- **AI Integration**: Google Gemini API
- **Deployment**: Vercel (Full-Stack)
- **Styling**: Material-UI + Custom CSS

### **System Architecture:**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Flask Backend  │    │   External APIs │
│                 │    │                 │    │                 │
│  ┌─────────────┐│    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│  │ App.js      ││────│ │ app.py      │ │────│ │ Gemini AI   │ │
│  │ (SPA)       ││    │ │ (REST API)  │ │    │ │ (Optional)  │ │
│  └─────────────┘│    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │ ┌─────────────┐ │    │                 │
│  ┌─────────────┐│    │ │ db.py       │ │    │                 │
│  │Material-UI  ││    │ │ (Database)  │ │    │                 │
│  │Components   ││    │ └─────────────┘ │    │                 │
│  └─────────────┘│    │ ┌─────────────┐ │    │                 │
│                 │    │ │recommender  │ │    │                 │
│                 │    │ │.py (ESG)    │ │    │                 │
│                 │    │ └─────────────┘ │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Data Flow:**

1. **User Interaction** → React Frontend
2. **API Requests** → Flask Backend (`/api/*`)
3. **Data Processing** → ESG Calculation Engine
4. **AI Enhancement** → Google Gemini (optional)
5. **Response** → JSON API Response
6. **UI Update** → React State Management

---

## 📁 **Project Structure**

```
esg-recommender/
├── 📁 api/                    # Backend (Python Flask)
│   ├── app.py                 # Main Flask application
│   ├── db.py                  # Database operations & schema
│   ├── recommender.py         # ESG scoring algorithms
│   ├── gemini.py              # AI integration module
│   └── requirements.txt       # Python dependencies
│
├── 📁 frontend/               # Frontend (React)
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css            # Styling
│   │   └── index.js           # Entry point
│   ├── public/                # Static assets
│   └── package.json           # Node.js dependencies
│
├── 📁 backend/                # Legacy folder (DB file only)
│   └── esg_recommender.db     # SQLite database
│
├── package.json               # Root build configuration
├── vercel.json                # Deployment configuration
├── .gitignore                 # Git ignore rules
└── README.md                  # This documentation
```

---

## 🔧 **Core Components**

### **Frontend (`frontend/src/App.js`)**
- **Single Page Application** built with React
- **Material-UI Components** for professional design
- **State Management** using React hooks
- **Responsive Layout** for mobile/desktop
- **Real-time Updates** for cart and recommendations

**Key Features:**
```javascript
// Main sections in App.js
├── Product Catalog (filterable by category)
├── Shopping Cart (persistent, ESG scoring)
├── Sustainability Dashboard (carbon footprint)
├── AI Recommendations (smart alternatives)
└── User Profile (points, achievements)
```

### **Backend (`api/app.py`)**
- **Flask REST API** with CORS enabled
- **Modular Endpoints** for different functionalities
- **Error Handling** and validation
- **Environment Configuration** for development/production

**API Endpoints:**
```python
GET  /api/health          # System health check
GET  /api/products        # Product catalog with ESG data
GET  /api/users/{name}    # User profile and points
GET  /api/cart            # Get current cart items
POST /api/cart            # Add item to cart
DELETE /api/cart          # Clear cart
POST /api/recommendation  # Get AI sustainability suggestions
```

### **Database Layer (`api/db.py`)**
- **SQLite Database** for development
- **In-memory Fallback** for serverless deployment
- **Schema Management** and data seeding
- **CRUD Operations** for all entities

**Database Schema:**
```sql
Products Table:
├── id (Primary Key)
├── name, category, price
├── esg_score, carbon_footprint
├── organic, packaging_type
└── description

Users Table:
├── id (Primary Key)
├── name, email
├── points, carbon_saved
└── preferences

Cart Table:
├── id (Primary Key)
├── product_id, quantity
└── created_at
```

### **ESG Engine (`api/recommender.py`)**
- **Multi-factor ESG Scoring** algorithm
- **Weighted Calculations** for different sustainability metrics
- **Product Comparison** and ranking
- **Carbon Footprint** calculations

**ESG Scoring Factors:**
```python
ESG Score = (
    organic_bonus * 20 +           # Organic certification
    packaging_score * 15 +         # Sustainable packaging
    carbon_efficiency * 30 +       # Carbon per dollar
    price_efficiency * 25 +        # Value proposition
    category_bonus * 10            # Category-specific bonus
)
```

### **AI Integration (`api/gemini.py`)**
- **Google Gemini API** integration
- **Graceful Fallback** when API unavailable
- **Smart Prompting** for product recommendations
- **Response Parsing** and validation

---

## 🚀 **Deployment Architecture**

### **Vercel Configuration:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    },
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/app.py"
    },
    {
      "src": "/static/(.*)",
      "dest": "/frontend/static/$1"
    },
    {
      "src": "/(.*\\.(js|css|png|jpg|ico|json))",
      "dest": "/frontend/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/index.html"
    }
  ]
}
```

### **Important Deployment Settings:**
When deploying to Vercel, make sure to:
1. **Leave Build Command EMPTY** (let Vercel auto-detect from frontend/package.json)
2. **Leave Output Directory EMPTY** (Vercel will use frontend/build automatically)
3. **Leave Install Command as default** (npm install)

### **Build Process:**
1. **Frontend Build**: React app compiled to static files
2. **Backend Deployment**: Python Flask as serverless function
3. **Asset Optimization**: Automatic CDN distribution
4. **Environment Variables**: Secure API key management

### **Scalability Features:**
- **Serverless Functions**: Auto-scaling backend
- **Global CDN**: Fast worldwide delivery
- **Database Flexibility**: Easy upgrade to PostgreSQL
- **API Rate Limiting**: Built-in request throttling

---

## ⚡ **Quick Start**

### **1. Local Development:**
```bash
# Clone repository
git clone https://github.com/vishnuvardhan2704/DBD.git
cd DBD

# Start backend
cd api
pip install -r requirements.txt
python app.py

# Start frontend (new terminal)
cd frontend
npm install
npm start
```

### **2. Deploy to Vercel:**
```bash
# Step 1: Commit and push your changes
git add .
git commit -m "Fix Vercel configuration for proper routing"
git push origin main

# Step 2: Deploy via GitHub (Recommended)
1. Go to vercel.com and sign in with GitHub
2. Click "New Project"
3. Import your "DBD" repository
4. IMPORTANT: In deployment settings:
   - Build Command: LEAVE EMPTY
   - Output Directory: LEAVE EMPTY
   - Install Command: LEAVE EMPTY (or npm install)
5. Click "Deploy"

# Alternative: Delete old project and redeploy if issues persist
```

### **🔧 Troubleshooting Deployment:**
If you're still getting 404 errors:
1. **Delete the old Vercel project** completely
2. **Import the repository again** as a fresh project
3. **Don't override any build settings** - let Vercel auto-detect
4. The `vercel.json` file will handle all configuration

### **3. Environment Variables (Optional):**
In Vercel Dashboard → Settings → Environment Variables:
```bash
GOOGLE_API_KEY=your_gemini_api_key  # For AI features
FLASK_ENV=production                # For production
```

---

## 🔍 **API Documentation**

### **Base URL**: `/api`

#### **Products Endpoint**
```http
GET /api/products
```
**Response:**
```json
[
  {
    "id": 1,
    "name": "Organic Bananas",
    "category": "fruits",
    "price": 3.99,
    "esg_score": 85,
    "carbon_footprint": 0.5,
    "organic": true,
    "packaging": "minimal"
  }
]
```

#### **Cart Operations**
```http
POST /api/cart
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

#### **AI Recommendations**
```http
POST /api/recommendation
Content-Type: application/json

{
  "user_preferences": {
    "sustainability_importance": 8,
    "price_sensitivity": 6
  },
  "current_cart": [...]
}
```

---

## 🛠️ **Development Guide**

### **Adding New Features:**

1. **Backend API Endpoint:**
   ```python
   # In api/app.py
   @app.route('/api/new-feature', methods=['POST'])
   def new_feature():
       # Implementation
       return jsonify({"status": "success"})
   ```

2. **Frontend Integration:**
   ```javascript
   // In frontend/src/App.js
   const callNewFeature = async () => {
     const response = await fetch('/api/new-feature', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify(data)
     });
     return response.json();
   };
   ```

### **Database Modifications:**
```python
# In api/db.py
def create_new_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS new_table (
            id INTEGER PRIMARY KEY,
            field1 TEXT,
            field2 INTEGER
        )
    ''')
```

### **ESG Algorithm Updates:**
```python
# In api/recommender.py
def calculate_new_metric(product):
    # Add new sustainability calculation
    return score
```

---

## 🎯 **Performance & Optimization**

### **Frontend Optimizations:**
- **Code Splitting**: Lazy loading of components
- **Memoization**: React.memo for expensive operations
- **Asset Optimization**: Compressed images and fonts
- **Caching**: Browser caching for static assets

### **Backend Optimizations:**
- **Database Indexing**: Optimized queries
- **Response Caching**: Redis for frequently accessed data
- **Connection Pooling**: Efficient database connections
- **Error Handling**: Graceful degradation

### **Monitoring:**
- **Vercel Analytics**: Built-in performance monitoring
- **Error Tracking**: Automatic error reporting
- **Usage Metrics**: API endpoint analytics
- **User Behavior**: Frontend interaction tracking

---

## 🔒 **Security & Best Practices**

### **Security Measures:**
- **Environment Variables**: Secure API key storage
- **CORS Configuration**: Controlled cross-origin requests
- **Input Validation**: Sanitized user inputs
- **Rate Limiting**: API abuse prevention

### **Code Quality:**
- **Modular Architecture**: Separation of concerns
- **Error Handling**: Comprehensive try-catch blocks
- **Documentation**: Inline code comments
- **Version Control**: Git best practices

---

## 📊 **Testing & Quality Assurance**

### **Testing Strategy:**
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint validation
- **E2E Tests**: Complete user flow testing
- **Performance Tests**: Load and stress testing

### **Code Quality Tools:**
- **ESLint**: JavaScript linting
- **Prettier**: Code formatting
- **Black**: Python code formatting
- **Git Hooks**: Pre-commit validation

---

## 🤝 **Contributing**

### **Development Workflow:**
1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/new-feature`
3. **Commit** changes: `git commit -m 'Add new feature'`
4. **Push** to branch: `git push origin feature/new-feature`
5. **Submit** pull request

### **Code Standards:**
- **Python**: PEP 8 formatting
- **JavaScript**: ES6+ standards
- **Comments**: Comprehensive documentation
- **Testing**: Unit tests for new features

---

## 📞 **Support & Contact**

### **Technical Support:**
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides and API docs
- **Community**: Developer discussions and help

### **Project Maintainer:**
- **GitHub**: [@vishnuvardhan2704](https://github.com/vishnuvardhan2704)
- **Repository**: [DBD](https://github.com/vishnuvardhan2704/DBD)

---

## 📝 **License**

This project is open source and available under the [MIT License](LICENSE).

---

## 🌟 **Acknowledgments**

- **Google Gemini AI** for intelligent recommendations
- **Material-UI** for beautiful React components
- **Vercel** for seamless deployment platform
- **Open Source Community** for inspiration and tools

---

**🚀 Ready to deploy? [Click here to deploy to Vercel](https://vercel.com/new/clone?repository-url=https://github.com/vishnuvardhan2704/DBD)**
