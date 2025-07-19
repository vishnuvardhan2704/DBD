# 🚀 ESG Recommender - Render.com Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Current Status
Your codebase is **READY** for deployment with:
- ✅ Clean project structure
- ✅ Flask backend configured for Render
- ✅ React frontend with build process
- ✅ Render.yaml configuration
- ✅ Build script (build.sh)
- ✅ Process file (Procfile)
- ✅ Environment variables template

---

## 🚀 Step-by-Step Deployment

### **Step 1: Push to GitHub** 
```bash
# Navigate to your project
cd "d:\DBD internship"

# Add all files
git add .

# Commit your changes
git commit -m "Deploy ESG Recommender to Render"

# Push to your repository
git push origin main
```

### **Step 2: Deploy on Render.com**

#### **Option A: One-Click Deploy (Recommended)**
1. Go to your GitHub repository
2. Click on this deploy button in your README:
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

#### **Option B: Manual Setup**
1. **Go to [render.com](https://render.com)**
2. **Sign in** with your GitHub account
3. **Click "New"** → **"Web Service"**
4. **Connect your repository**: Select "DBD" repository
5. **Use these exact settings**:

```yaml
Name: esg-recommender
Environment: Python 3
Region: Oregon (recommended)
Branch: main
Build Command: ./build.sh
Start Command: cd api && gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 60 app:app
```

### **Step 3: Environment Variables**
In your Render dashboard, add these environment variables:

**Required:**
- `FLASK_ENV` = `production`
- `SECRET_KEY` = `your-secret-key-here` (or let Render generate)

**Optional (for AI features):**
- `GEMINI_API_KEY` = `your-google-gemini-api-key`

### **Step 4: Deploy**
1. Click **"Create Web Service"**
2. Wait for the build to complete (5-10 minutes)
3. Your app will be available at: `https://your-app-name.onrender.com`

---

## 🔧 Configuration Details

### **Your render.yaml Configuration:**
```yaml
services:
  - type: web
    name: esg-recommender
    env: python
    region: oregon
    plan: free
    buildCommand: "./build.sh"
    startCommand: "cd api && gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 60 app:app"
    healthCheckPath: /api/health
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: GEMINI_API_KEY
        sync: false
```

### **Build Process (build.sh):**
1. Builds React frontend (`npm install && npm run build`)
2. Moves build files to `api/static/` for Flask to serve
3. Installs Python dependencies
4. Sets up the application

### **Runtime Process (Procfile):**
- Starts Gunicorn server with Flask app
- Serves both frontend and API from single service

---

## 🧪 Testing Your Deployment

Once deployed, test these endpoints:

### **Frontend:**
- **App**: `https://your-app.onrender.com/`
- Should load the React application

### **Backend API:**
- **Health Check**: `https://your-app.onrender.com/api/health`
- **Products**: `https://your-app.onrender.com/api/products`
- **API Root**: `https://your-app.onrender.com/api/`

### **Test Commands:**
```bash
# Health check
curl https://your-app.onrender.com/api/health

# Get products
curl https://your-app.onrender.com/api/products

# Test frontend
# Visit https://your-app.onrender.com/ in browser
```

---

## 🚨 Troubleshooting

### **Build Fails:**
1. Check build logs in Render dashboard
2. Ensure `build.sh` is executable
3. Verify all dependencies are in `requirements.txt`

### **App Won't Start:**
1. Check runtime logs in Render dashboard
2. Verify environment variables are set
3. Ensure database initializes properly

### **Frontend Not Loading:**
1. Check if `api/static/` folder exists after build
2. Verify build script completed successfully
3. Check for React build errors in logs

### **API Errors:**
1. Test endpoints individually
2. Check Flask app logs in Render
3. Verify CORS configuration

### **Common Solutions:**
- **Build timeout**: The free tier has build time limits
- **Memory issues**: Free tier has 512MB RAM limit
- **Static files**: Ensure build.sh copies files correctly

---

## 🎯 Environment Variables Setup

### **Required Variables:**
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
```

### **Optional Variables:**
```bash
GEMINI_API_KEY=your-gemini-api-key  # For AI recommendations
```

### **How to get Gemini API Key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API key"
4. Copy the key and add to Render environment variables

---

## 📊 Deployment Timeline

| Step | Time | Description |
|------|------|-------------|
| 1 | 2 min | Push to GitHub |
| 2 | 1 min | Setup Render service |
| 3 | 1 min | Configure environment |
| 4 | 5-10 min | Build & deploy |
| **Total** | **10-15 min** | **Complete deployment** |

---

## 🎉 Success Indicators

You'll know your deployment is successful when:
- ✅ Build completes without errors
- ✅ Health check endpoint responds with 200
- ✅ Frontend loads at your Render URL
- ✅ API endpoints return data
- ✅ React app can communicate with Flask backend

---

## 📞 Support

If you encounter issues:
1. **Check Render logs** (build and runtime)
2. **Review this guide** step by step
3. **Test locally** first: `python test_setup.py`
4. **Create GitHub issue** if problems persist

---

**🚀 Ready to deploy? Your app is configured and ready to go live!**

**Next Action:** Push to GitHub and click the deploy button!
