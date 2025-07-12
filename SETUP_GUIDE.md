# 🚀 Quick Setup Guide - ESG Recommender

## ✅ **Issues Fixed**
- ✅ Removed duplicate files causing import conflicts
- ✅ Fixed backend import paths
- ✅ Installed missing React dependencies
- ✅ Backend (Flask) is running on `http://localhost:5000`
- ✅ Frontend (React) is running on `http://localhost:3000`

## 🎯 **How to Use**

1. **Open your browser** and go to: `http://localhost:3000`

2. **Login** with name: `Alice` (this user exists in the database)

3. **Browse products** and click "Add to Cart"

4. **See AI recommendations** when greener alternatives are available

5. **Accept/decline** recommendations and earn carbon points

## 🔧 **If You Have Issues**

### **Backend Issues:**
```bash
cd backend
python app.py
```
Should show: "Running on http://127.0.0.1:5000"

### **Frontend Issues:**
```bash
cd frontend
npm start
```
Should open browser to `http://localhost:3000`

### **Test Everything:**
```bash
python test_setup.py
```
This will test all components and tell you what's working.

### **Database Issues:**
The SQLite database (`esg_recommender.db`) is automatically created.

### **Gemini API Issues:**
Create `backend/.env` file:
```
GEMINI_API_KEY=your_key_here
```
If no key, it will use dummy responses.

## 📁 **Correct File Structure**
```
esg_recommender/
├── backend/          # Flask API (port 5000)
│   ├── app.py        # Main Flask app
│   ├── db.py         # Database helpers
│   ├── recommender.py # ESG logic
│   ├── gemini.py     # Gemini AI integration
│   └── requirements.txt
├── frontend/         # React App (port 3000)
│   ├── src/
│   │   └── App.js    # Main React component
│   └── package.json
├── start_backend.bat # Windows backend starter
├── start_frontend.bat # Windows frontend starter
├── test_setup.py     # Test script
└── README.md         # Full documentation
```

## 🎨 **Features Working**
- ✅ Beautiful Material-UI interface
- ✅ Product catalog with ESG badges
- ✅ AI-powered recommendations
- ✅ Cart management
- ✅ Carbon points system
- ✅ Responsive design

## 🆘 **Need Help?**
- Backend logs: Check terminal running `python app.py`
- Frontend logs: Check terminal running `npm start`
- Browser console: F12 for JavaScript errors
- Run test: `python test_setup.py`

**Your ESG recommender is ready to use! 🌱** 