# 🚀 Supabase Backend Deployment Guide

## 🎯 Why Supabase for Your Backend?

**Supabase = Firebase Alternative + PostgreSQL + Edge Functions**
- ✅ **Free tier**: 500MB database, 2GB bandwidth
- ✅ **Built-in PostgreSQL**: No separate database needed
- ✅ **Edge Functions**: Your Flask API runs globally
- ✅ **Real-time**: Built-in real-time features
- ✅ **Auth**: Built-in user authentication (optional)

---

## 📋 Deployment Options

### Option 1: Supabase Edge Functions (Recommended)
Deploy your Flask API as serverless functions

### Option 2: Supabase + Vercel  
Use Supabase for database, Vercel for Flask API

### Option 3: Full Supabase (Advanced)
Replace Flask with Supabase's built-in API

Let's start with **Option 1** (easiest):

---

## 🔧 Option 1: Supabase Edge Functions

### Step 1: Install Supabase CLI
```bash
# Install Supabase CLI
npm install -g supabase

# Login to Supabase
supabase login
```

### Step 2: Initialize Supabase Project
```bash
# In your project root
supabase init

# Create new Supabase project
supabase projects create your-esg-app

# Link to your project
supabase link --project-ref your-project-ref
```

### Step 3: Create Edge Function
```bash
# Create function for your API
supabase functions new esg-api
```

### Step 4: Deploy
```bash
# Deploy your function
supabase functions deploy esg-api

# Your API will be available at:
# https://your-project-ref.supabase.co/functions/v1/esg-api
```

---

## 🔧 Option 2: Supabase Database + Vercel API (Easier!)

This is actually **easier** and works great with your existing Flask code!

### Step 1: Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. **"New project"**
3. **Name**: `esg-recommender`
4. **Database password**: Generate strong password
5. **Region**: Choose closest to you
6. Click **"Create new project"**

### Step 2: Set Up Database
1. In Supabase dashboard → **"SQL Editor"**
2. Run this SQL to create your tables:

```sql
-- Create products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    packaging TEXT,
    is_organic BOOLEAN,
    carbon_kg FLOAT,
    price FLOAT
);

-- Create users table  
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    points INTEGER DEFAULT 0
);

-- Create cart table
CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER DEFAULT 1
);

-- Insert sample data
INSERT INTO products (name, description, category, packaging, is_organic, carbon_kg, price) VALUES
('Regular Chicken Breast', 'Standard chicken breast', 'meat', 'plastic', false, 3.2, 8.99),
('Organic Free-Range Chicken', 'Organic, free-range chicken', 'meat', 'paper', true, 2.1, 12.99),
('Regular Ground Beef', 'Standard ground beef', 'meat', 'plastic', false, 4.8, 10.99),
('Organic Grass-Fed Beef', 'Organic, grass-fed beef', 'meat', 'paper', true, 3.2, 16.99),
('Regular Milk', 'Standard milk', 'dairy', 'plastic', false, 1.9, 3.99),
('Organic Oat Milk', 'Organic oat milk', 'dairy', 'glass', true, 0.8, 4.99),
('Regular Yogurt', 'Standard yogurt', 'dairy', 'plastic', false, 1.2, 2.99),
('Organic Greek Yogurt', 'Organic Greek yogurt', 'dairy', 'glass', true, 0.9, 5.99),
('White Rice', 'Standard white rice', 'grains', 'plastic', false, 2.1, 2.49),
('Organic Brown Rice', 'Organic brown rice', 'grains', 'paper', true, 1.8, 3.99);

-- Insert sample user
INSERT INTO users (name, points) VALUES ('Alice', 0);
```

### Step 3: Get Database URL
1. In Supabase dashboard → **"Settings"** → **"Database"**
2. Copy **"Connection string"**
3. Replace `[YOUR-PASSWORD]` with your database password
4. Save this URL - you'll need it!

### Step 4: Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. **"New Project"** → Import from GitHub
3. Select your **"DBD"** repository
4. **Root Directory**: `backend`
5. **Framework**: Other
6. **Environment Variables**:
   ```
   DATABASE_URL = your-supabase-connection-string
   SECRET_KEY = your-secret-key-123
   GEMINI_API_KEY = your-api-key (optional)
   ```
7. Click **"Deploy"**

---

## 🔧 Option 3: Full Supabase (Replace Flask)

**Advanced**: Use Supabase's built-in API instead of Flask

### Benefits:
- ✅ **No backend code needed**
- ✅ **Auto-generated REST API**
- ✅ **Real-time subscriptions**
- ✅ **Built-in authentication**

### How it works:
1. Create tables in Supabase
2. Supabase automatically creates REST API
3. Your React app calls Supabase directly
4. No Flask needed!

### API Examples:
```javascript
// Get all products
const { data } = await supabase.from('products').select('*')

// Add to cart
const { data } = await supabase.from('cart').insert({
  user_id: 1,
  product_id: 2,
  quantity: 1
})

// Get user cart
const { data } = await supabase
  .from('cart')
  .select('*, products(*)')
  .eq('user_id', userId)
```

---

## 🎯 Which Option Should You Choose?

### **Option 2: Supabase + Vercel** (Recommended for you!)
**Why**: Keep your existing Flask code, just change database
- ✅ Minimal code changes
- ✅ Keep your Flask logic
- ✅ Easy to understand
- ✅ Free deployment

### **Option 1: Edge Functions** (If you want serverless)
**Why**: For scale and performance
- ✅ Serverless (pay per use)
- ✅ Global edge deployment
- ✅ Modern architecture

### **Option 3: Full Supabase** (If you want to learn something new)
**Why**: Simplest long-term
- ✅ No backend maintenance
- ✅ Auto-generated API
- ✅ Real-time features

---

## 🔄 Migration Steps (Option 2)

I'll help you migrate your existing Flask app to use Supabase database:

### 1. Update Database Connection
Replace SQLite with PostgreSQL connection

### 2. Update SQL Queries  
Minor syntax changes for PostgreSQL

### 3. Deploy to Vercel
Your Flask app runs on Vercel, connects to Supabase

### 4. Update Frontend
Point your React app to new Vercel URL

---

## 💡 Pro Tips

### Cost Comparison
- **Supabase**: 500MB DB + 2GB bandwidth (free)
- **Heroku**: 10k rows + 550 hours (free)
- **Vercel**: 100GB bandwidth + serverless functions (free)

### Performance
- **Supabase**: Global edge network
- **PostgreSQL**: More powerful than SQLite
- **Vercel**: Fast serverless functions

### Scaling
- **Supabase**: Real-time features built-in
- **PostgreSQL**: Handles millions of rows
- **Vercel**: Auto-scales with traffic

---

## 🚀 Ready to Start?

**Easiest path** (5 minutes):
1. Create Supabase project
2. Run SQL to create tables
3. Deploy Flask to Vercel with Supabase database URL
4. Update frontend API URL

**Want me to help you with the migration?** I can:
1. Update your `db.py` for PostgreSQL
2. Create the Supabase setup
3. Configure Vercel deployment
4. Test everything works

Let me know which option you prefer! 🎯
