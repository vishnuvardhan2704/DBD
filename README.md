# 🌱 ESG-based Sustainable Product Recommendation System

A **beautiful, modern, and professional** ESG product recommendation system built with **React + Flask**. Features a stunning Material-UI interface with real-time recommendations powered by Google's Gemini AI.

---

## ✨ Features

- **🎨 Beautiful React UI** - Modern Material-UI design with cards, dialogs, and animations
- **🤖 AI-Powered Recommendations** - Gemini AI explains why alternatives are more sustainable
- **📊 Carbon Points System** - Track your environmental impact
- **🛒 Smart Cart** - Add items with greener alternatives
- **📱 Responsive Design** - Works on desktop, tablet, and mobile
- **🔒 Secure API** - Flask backend with CORS support
- **💾 SQLite Database** - Easy to swap for MySQL/PostgreSQL

---

## 🚀 Quick Start

### 1. **Clone and Setup**
```bash
git clone <your-repo-url>
cd esg_recommender
```

### 2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

### 3. **Frontend Setup**
```bash
cd frontend
npm install
```

### 4. **Add Your Gemini API Key**
Create a `.env` file in the `backend` directory:
```
GEMINI_API_KEY=AIza...your_key_here
```

### 5. **Run the Application**

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Visit `http://localhost:3000` to see your beautiful ESG recommender! 🌱

---

## 🏗️ Architecture

```
esg_recommender/
├── backend/                 # Flask API
│   ├── app.py              # Main Flask app
│   ├── db.py               # Database helpers
│   ├── recommender.py      # ESG logic
│   ├── gemini.py           # Gemini AI integration
│   └── requirements.txt    # Python dependencies
├── frontend/               # React app
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   └── App.css         # Styles
│   └── package.json        # Node dependencies
└── README.md
```

---

## 🎯 How It Works

1. **User Login** - Enter your name (Alice is in the mock DB)
2. **Browse Products** - See ESG info (organic, packaging, carbon footprint)
3. **Add to Cart** - System checks for greener alternatives
4. **AI Recommendation** - Gemini explains why the alternative is better
5. **Accept/Decline** - Choose your preference
6. **Earn Points** - Get carbon points for sustainable choices
7. **View Cart** - See your selections and clear cart

---

## 🛠️ Customization

### **Add More Products**
Edit `backend/db.py` in the `insert_mock_data()` function.

### **Change ESG Rules**
Modify `backend/recommender.py` in the `calculate_sustainability_score()` function.

### **Update UI Theme**
Edit `frontend/src/App.js` for colors, fonts, and layout.

### **Switch to MySQL**
Replace SQLite connection in `backend/db.py` with MySQL connector.

---

## 📦 Dependencies

### **Backend (Python)**
- Flask - Web framework
- Flask-CORS - Cross-origin support
- google-generativeai - Gemini AI
- python-dotenv - Environment variables
- scikit-learn, scipy, numpy, pandas - Data processing

### **Frontend (React)**
- React - UI framework
- Material-UI - Component library
- @mui/icons-material - Icons
- @emotion/react, @emotion/styled - Styling

---

## 🔧 API Endpoints

- `GET /api/products` - Get all products
- `GET /api/users/<name>` - Get user by name
- `GET /api/cart/<user_id>` - Get user's cart
- `POST /api/cart` - Add item to cart
- `DELETE /api/cart/<user_id>` - Clear cart
- `POST /api/recommendation` - Get greener alternative
- `PUT /api/points/<user_id>` - Update user points

---

## 🎨 UI Features

- **Material Design** - Professional, modern interface
- **Responsive Cards** - Product display with ESG badges
- **Smart Dialogs** - Recommendation popups with AI explanations
- **Cart Drawer** - Slide-out cart with item management
- **Progress Indicators** - Loading states and animations
- **Snackbar Notifications** - User feedback and alerts
- **Color-coded Badges** - Organic, packaging, and carbon info

---

## 🔒 Security Notes

- API key stored in `.env` (never commit this file)
- CORS enabled for local development
- Input validation on all endpoints
- Error handling with user-friendly messages

---

## 🚀 Deployment

### **Heroku**
1. Add `Procfile` to backend
2. Set environment variables
3. Deploy backend and frontend separately

### **Vercel/Netlify**
1. Build React app: `npm run build`
2. Deploy frontend to Vercel/Netlify
3. Deploy backend to Heroku/Railway

### **Docker**
```dockerfile
# Backend
FROM python:3.9
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

# Frontend
FROM node:16
WORKDIR /app
COPY frontend/ .
RUN npm install
RUN npm run build
CMD ["npm", "start"]
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

MIT License - feel free to use this for your own projects!

---

**Made with ❤️ for a greener world** 🌱

*This system demonstrates how AI can help consumers make more sustainable choices while providing a beautiful, professional user experience.* 