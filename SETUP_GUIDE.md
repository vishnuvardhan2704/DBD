# 🚀 ESG Recommender - Quick Setup Guide

## Pre-Deployment Checklist

### ✅ **What's Been Cleaned Up:**
- ✅ Removed redundant files and configurations
- ✅ Consolidated API into single clean structure
- ✅ Configured for Render.com deployment
- ✅ Updated documentation and README
- ✅ Added proper environment variable handling
- ✅ Created build scripts and configuration files

### 📁 **Final Project Structure:**
```
esg-recommender/
├── api/                    # Backend (Flask)
│   ├── app.py             # Main application
│   ├── db.py              # Database operations
│   ├── recommender.py     # ESG algorithms
│   ├── gemini.py          # AI integration
│   └── requirements.txt   # Python dependencies
├── frontend/              # Frontend (React)
│   ├── src/App.js        # Main React app
│   ├── package.json      # Node dependencies
│   └── build/            # (Generated during build)
├── build.sh              # Build script
├── Procfile              # Process definition
├── render.yaml           # Deployment config
├── requirements.txt      # Root dependencies
├── .env.template         # Environment template
└── README.md            # Documentation
```

---

## 🚀 **Deployment Steps**

### **Step 1: Test Locally (Optional)**
```bash
# Run the setup test
python test_setup.py

# Start backend
cd api
pip install -r requirements.txt
python app.py

# Start frontend (new terminal)
cd frontend
npm install
npm start
```

### **Step 2: Deploy to Render.com**

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Clean codebase for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com)
   - Sign in with GitHub
   - Click "New" → "Web Service"
   - Connect your repository
   - Use these settings:
     - **Name**: `esg-recommender`
     - **Environment**: `Python 3`
     - **Build Command**: `./build.sh`
     - **Start Command**: `cd api && gunicorn --bind 0.0.0.0:$PORT app:app`

3. **Set Environment Variables**:
   ```bash
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key  # Optional
   ```

4. **Deploy**: Click "Create Web Service"

### **Step 3: Test Deployment**
- **Frontend**: `https://your-app.onrender.com/`
- **API Health**: `https://your-app.onrender.com/api/health`
- **API Products**: `https://your-app.onrender.com/api/products`

---

## 🔧 **Environment Variables**

### **Required:**
- `FLASK_ENV` = `production`
- `SECRET_KEY` = Any random string (Render can generate this)

### **Optional:**
- `GEMINI_API_KEY` = Your Google Gemini API key for AI features

### **How to Get Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your Render environment variables

---

## 🚨 **Troubleshooting**

### **Build Fails:**
- Check build logs in Render dashboard
- Ensure `build.sh` is executable
- Verify all dependencies are in requirements.txt

### **App Doesn't Start:**
- Check runtime logs in Render dashboard
- Verify environment variables are set
- Ensure database initializes properly

### **Frontend Not Loading:**
- Check if `api/static/` folder exists after build
- Verify build script completed successfully
- Check for any React build errors

### **API Errors:**
- Test endpoints individually
- Check Flask app logs
- Verify CORS configuration

---

## 📞 **Support**

If you encounter issues:
1. Check the build and runtime logs in Render dashboard
2. Review this setup guide
3. Test locally first to isolate issues
4. Create a GitHub issue if needed

---

**🎉 Ready to deploy? Your codebase is now clean and Render-ready!**
