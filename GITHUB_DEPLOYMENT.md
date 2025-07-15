# 🚀 GitHub Deployment Guide - Your ESG Recommender

## 🎯 What We're Doing

You'll deploy your app in **2 steps**:
1. **Frontend** (React) → **Netlify** (connects to your GitHub repo)
2. **Backend** (Flask) → **Heroku** (connects to your GitHub repo)

Both will **automatically redeploy** whenever you push code to GitHub! 🔄

---

## 📱 Step 1: Deploy Frontend to Netlify via GitHub

### 1.1 Sign Up & Connect GitHub
1. Go to [netlify.com](https://netlify.com)
2. Click **"Sign up"** → **"GitHub"** (use your GitHub account)
3. Authorize Netlify to access your repositories

### 1.2 Create New Site
1. Click **"Add new site"** → **"Import from Git"**
2. Choose **"GitHub"** 
3. Find and select your **"DBD"** repository
4. Click on it

### 1.3 Configure Build Settings
Set these **exact settings**:
```
Base directory: frontend
Build command: npm run build  
Publish directory: frontend/build
```

### 1.4 Deploy!
1. Click **"Deploy site"**
2. Wait 2-3 minutes for build
3. You'll get a URL like: `https://adorable-unicorn-123456.netlify.app`

### 1.5 Add Environment Variable (Important!)
1. In Netlify dashboard → **"Site settings"** → **"Environment variables"**
2. Click **"Add variable"**
3. **Key**: `REACT_APP_API_URL`
4. **Value**: `https://your-backend-app.herokuapp.com` (we'll get this in Step 2)
5. Click **"Save"**

---

## ⚡ Step 2: Deploy Backend to Heroku via GitHub

### 2.1 Sign Up for Heroku
1. Go to [heroku.com](https://heroku.com)
2. Sign up for free account
3. **Important**: Add a payment method (required for free tier, won't be charged)

### 2.2 Create New App
1. Click **"New"** → **"Create new app"**
2. **App name**: `your-name-esg-backend` (must be unique)
3. **Region**: Choose closest to you
4. Click **"Create app"**

### 2.3 Connect to GitHub
1. In your Heroku app dashboard
2. Go to **"Deploy"** tab
3. **Deployment method** → Click **"GitHub"**
4. **Connect to GitHub** → Authorize Heroku
5. Search for **"DBD"** repository → **"Connect"**

### 2.4 Configure Environment Variables
1. Go to **"Settings"** tab
2. Click **"Reveal Config Vars"**
3. Add these variables:

```
SECRET_KEY = your-super-secret-key-change-this-123
ESG_DB_PATH = esg_recommender.db
GEMINI_API_KEY = your-api-key-here (optional)
```

### 2.5 Set Build Path
1. Still in **"Settings"** tab
2. **Buildpacks** → **"Add buildpack"**
3. Select **"Python"**
4. **Important**: We need to tell Heroku to look in the `backend` folder

Let me create a special file for this:

### 2.6 Deploy!
1. Go back to **"Deploy"** tab
2. **Manual deploy** section
3. Choose **"main"** branch
4. Click **"Deploy Branch"**
5. Wait for build (2-3 minutes)
6. Click **"View"** to see your API!

---

## 🔗 Step 3: Connect Frontend to Backend

### 3.1 Get Your Heroku URL
After Heroku deployment, you'll have a URL like:
`https://your-name-esg-backend.herokuapp.com`

### 3.2 Update Netlify Environment Variable
1. Go back to Netlify dashboard
2. **Site settings** → **"Environment variables"**  
3. Edit `REACT_APP_API_URL`
4. Set value to your Heroku URL (without `/api` at the end)
5. **Save**

### 3.3 Redeploy Frontend
1. **Site overview** → **"Deploys"**
2. Click **"Trigger deploy"** → **"Deploy site"**
3. Wait for rebuild

---

## 🎉 Step 4: Test Your Live App!

### 4.1 Test Backend API
Visit: `https://your-name-esg-backend.herokuapp.com/api/health`
Should show: `{"status": "ok"}`

### 4.2 Test Frontend
Visit your Netlify URL, should show your React app!

### 4.3 Test Full Integration
1. Try logging in as "Alice"
2. Add products to cart
3. Get AI recommendations
4. Check if everything works!

---

## 🔄 Auto-Deployment Setup (The Magic!)

### 4.1 Enable Auto-Deploy for Backend
1. In Heroku → **"Deploy"** tab
2. **Automatic deploys** section
3. Choose **"main"** branch
4. Click **"Enable Automatic Deploys"**

### 4.2 Auto-Deploy for Frontend
Netlify automatically deploys when you push to GitHub! ✨

### 4.3 Test Auto-Deploy
1. Make a small change to your code
2. Push to GitHub: `git push origin main`
3. Watch both Netlify and Heroku automatically rebuild!

---

## 🐛 Troubleshooting Common Issues

### ❌ "App not found" on Heroku
**Problem**: Heroku can't find your backend files
**Solution**: Make sure your backend files are in the `backend/` folder in your repo

### ❌ "Failed to fetch" in your app  
**Problem**: Frontend can't reach backend
**Solution**: 
1. Check your Heroku URL is working: `https://your-app.herokuapp.com/api/health`
2. Update `REACT_APP_API_URL` in Netlify
3. Redeploy frontend

### ❌ Netlify build fails
**Problem**: npm build errors
**Solution**:
1. Test locally: `cd frontend && npm run build`
2. Fix any errors
3. Push to GitHub

### ❌ Heroku build fails
**Problem**: Python dependencies issue
**Solution**: Check `backend/requirements.txt` has all needed packages

---

## 💡 Pro Tips

### Custom Domain (Optional)
1. Buy domain from Namecheap/GoDaddy
2. In Netlify: **"Domain settings"** → **"Add custom domain"**
3. Follow DNS setup instructions

### Monitoring Your Apps
- **Netlify**: Check build logs in dashboard
- **Heroku**: View logs with `heroku logs --tail -a your-app-name`
- Both services email you if deployment fails

### Free Tier Limits
- **Netlify**: 100GB bandwidth/month
- **Heroku**: 550 hours/month (enough for always-on small apps)
- **Tip**: Heroku apps "sleep" after 30 min of inactivity (first request takes a few seconds to wake up)

---

## 🎯 Quick Reference

### Your App URLs (After Deployment)
- **Frontend**: `https://your-site-name.netlify.app`
- **Backend**: `https://your-app-name.herokuapp.com`
- **API Health Check**: `https://your-app-name.herokuapp.com/api/health`

### Push New Changes
```bash
git add .
git commit -m "Your changes description"
git push origin main
# Both apps automatically redeploy! 🚀
```

### Check Deployment Status
- **Netlify**: Dashboard shows build progress
- **Heroku**: Dashboard → "Activity" tab shows deployments

---

## 🆘 Need Help?

**Common Commands**:
```bash
# Check what's staged for commit
git status

# Push your changes
git add .
git commit -m "Updated app"
git push origin main

# View your remote repository
git remote -v
```

**If Stuck**:
1. Check both Netlify and Heroku dashboards for error messages
2. Test your backend URL directly in browser
3. Check environment variables are set correctly
4. Look at build logs for specific errors

You've got this! 🚀 Both services have excellent documentation and your app is now set up for professional deployment!
