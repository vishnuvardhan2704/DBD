# 🚀 Easy Deployment Guide for Your ESG Recommender

## 📋 What You're Actually Doing

Think of deployment like **publishing your app to the internet**:

```
Your Computer (Development)          →          The Internet (Production)
┌─────────────────────┐                      ┌─────────────────────┐
│ React Frontend      │  ──Deploy──→         │ Netlify             │
│ (localhost:3000)    │                      │ (your-app.netlify)  │
└─────────────────────┘                      └─────────────────────┘

┌─────────────────────┐                      ┌─────────────────────┐
│ Flask Backend       │  ──Deploy──→         │ Heroku/Railway      │
│ (localhost:5000)    │                      │ (your-api.herokuapp)│
└─────────────────────┘                      └─────────────────────┘
```

**Why separate?**
- **Frontend** = What users see (HTML, CSS, JS) → **Static hosting** (Netlify)
- **Backend** = Server that processes data → **App hosting** (Heroku, Railway)

---

## 🌐 Deploy Frontend to Netlify (Easy Way)

### Option 1: Drag & Drop (Simplest)

**Step 1**: Build your React app
```bash
cd frontend
npm install
npm run build
```
This creates a `build` folder with your website files.

**Step 2**: Go to [netlify.com](https://netlify.com)
- Sign up with GitHub/email
- Click "Add new site" → "Deploy manually" 
- **Drag the entire `build` folder** into the box
- Done! Your frontend is live at `https://yourapp.netlify.app`

### Option 2: GitHub Integration (Recommended)

**Step 1**: Push your code to GitHub
```bash
# In your project root
git add .
git commit -m "Ready for deployment"
git push origin main
```

**Step 2**: Connect to Netlify
- Go to [netlify.com](https://netlify.com) → "Add new site" → "Import from Git"
- Connect your GitHub account
- Select your repository
- **Build settings**:
  ```
  Base directory: frontend
  Build command: npm run build
  Publish directory: frontend/build
  ```
- Click "Deploy site"

**Step 3**: Configure Environment Variables
- In Netlify dashboard → "Site settings" → "Environment variables"
- Add: `REACT_APP_API_URL` = `https://your-backend-url.herokuapp.com`

---

## ☁️ Deploy Backend Options

### Option 1: Heroku (Free tier available)

**Step 1**: Install Heroku CLI
- Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

**Step 2**: Prepare backend for Heroku
```bash
cd backend
heroku login
heroku create your-esg-backend
```

**Step 3**: Set environment variables
```bash
heroku config:set SECRET_KEY=your-super-secret-key
heroku config:set GEMINI_API_KEY=your-gemini-key  # Optional
```

**Step 4**: Deploy
```bash
git init  # If not already a git repo
git add .
git commit -m "Backend ready for Heroku"
heroku git:remote -a your-esg-backend
git push heroku main
```

### Option 2: Railway (Modern alternative)

**Step 1**: Go to [railway.app](https://railway.app)
- Sign up with GitHub
- Click "New Project" → "Deploy from GitHub repo"
- Select your repository

**Step 2**: Configure
- **Root directory**: `/backend`
- **Start command**: `python app.py`
- Add environment variables in Railway dashboard

### Option 3: Render (Another good option)

**Step 1**: Go to [render.com](https://render.com)
- Sign up and connect GitHub
- "New" → "Web Service"
- Select your repo

**Step 2**: Configure
- **Root directory**: `backend`
- **Build command**: `pip install -r requirements.txt`
- **Start command**: `python app.py`

---

## 🔧 Complete Deployment Workflow

### 1. Deploy Backend First
```bash
# Choose Heroku, Railway, or Render
# Get your backend URL (e.g., https://your-app.herokuapp.com)
```

### 2. Update Frontend Configuration
```bash
# Update netlify.toml with your backend URL
cd frontend
# Edit netlify.toml - replace "your-backend-url.herokuapp.com" with actual URL
```

### 3. Deploy Frontend
```bash
# Method A: Manual
npm run build
# Drag 'build' folder to Netlify

# Method B: Git integration
git add .
git commit -m "Updated API URL"
git push origin main
# Netlify auto-deploys
```

### 4. Test Your Live App
- Visit your Netlify URL
- Check if frontend loads
- Test API calls (add products to cart, get recommendations)

---

## 🐛 Common Deployment Issues & Fixes

### ❌ "Failed to fetch" Errors
**Problem**: Frontend can't reach backend
**Solution**: 
1. Check API URL in `netlify.toml`
2. Ensure backend is running (visit backend URL directly)
3. Check CORS settings in Flask app

### ❌ Build Fails on Netlify
**Problem**: npm build errors
**Solution**:
```bash
# Test build locally first
cd frontend
npm run build
# Fix any errors before deploying
```

### ❌ Environment Variables Not Working
**Problem**: `process.env.REACT_APP_API_URL` is undefined
**Solution**:
1. Variable must start with `REACT_APP_`
2. Set in Netlify dashboard under "Environment variables"
3. Redeploy after adding variables

### ❌ Database Errors in Production
**Problem**: SQLite file not found
**Solution**: Most hosting services provide database URLs
```python
# In backend/db.py, update for production
import os
DATABASE_URL = os.getenv('DATABASE_URL')  # Provided by hosting service
if DATABASE_URL:
    # Use PostgreSQL connection
else:
    # Use SQLite for development
```

---

## 💡 Pro Tips

### Free Hosting Limits
- **Netlify**: 100GB bandwidth/month, unlimited sites
- **Heroku**: 550-1000 dyno hours/month (enough for small projects)
- **Railway**: $5 credit/month (usually enough for small apps)

### Custom Domains
- Buy domain from Namecheap, GoDaddy, etc.
- In Netlify: "Domain settings" → "Add custom domain"
- In Heroku: `heroku domains:add yourdomain.com`

### HTTPS is Automatic
- Both Netlify and Heroku provide free SSL certificates
- Your app automatically gets `https://` URLs

### Monitoring
- Netlify: Check deploy logs in dashboard
- Heroku: `heroku logs --tail` to see live logs
- Both send email alerts for failed deployments

---

## 🎯 Quick Start Summary

**Fastest deployment (5 minutes)**:
1. `cd frontend && npm run build`
2. Drag `build` folder to netlify.com
3. Create free Heroku account
4. `cd backend && git push heroku main`
5. Update frontend with backend URL
6. Redeploy frontend

**Your app is now live!** 🎉

---

## 📞 Need Help?

**Common Questions**:
- **"My frontend loads but API calls fail"** → Check API URL in environment variables
- **"Build fails"** → Run `npm run build` locally to see errors
- **"Backend won't start"** → Check Heroku logs: `heroku logs --tail`
- **"Database empty"** → Backend recreates tables on first run

**Resources**:
- [Netlify Documentation](https://docs.netlify.com/)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [React Deployment Guide](https://create-react-app.dev/docs/deployment/)

You got this! 🚀
