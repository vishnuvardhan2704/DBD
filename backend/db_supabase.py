import os
import sqlite3
import psycopg2
import psycopg2.extras
from typing import List, Dict, Any, Optional
import logging
from contextlib import contextmanager
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Database configuration - supports both SQLite and PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
DB_PATH = os.getenv('ESG_DB_PATH', 'esg_recommender.db')

def is_postgres():
    """Check if we're using PostgreSQL (Supabase) or SQLite"""
    return DATABASE_URL is not None and DATABASE_URL.startswith('postgresql')

@contextmanager
def get_db_connection():
    """Context manager for database connections - supports both SQLite and PostgreSQL"""
    conn = None
    try:
        if is_postgres():
            # PostgreSQL connection (Supabase)
            conn = psycopg2.connect(DATABASE_URL)
            conn.autocommit = False
        else:
            # SQLite connection (local development)
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            conn.row_factory = sqlite3.Row
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def execute_query(query: str, params: tuple = None, fetch: bool = False):
    """Execute query with proper parameter binding for both databases"""
    with get_db_connection() as conn:
        if is_postgres():
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
            conn.commit()
            return result
        else:
            conn.commit()
            return cursor.rowcount

# --- Schema Creation ---
def create_tables():
    """Create tables with syntax compatible for both SQLite and PostgreSQL"""
    if is_postgres():
        # PostgreSQL syntax
        queries = [
            '''CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                packaging TEXT,
                is_organic BOOLEAN,
                carbon_kg FLOAT,
                price FLOAT
            )''',
            '''CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                points INTEGER DEFAULT 0
            )''',
            '''CREATE TABLE IF NOT EXISTS cart (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )'''
        ]
    else:
        # SQLite syntax
        queries = [
            '''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                packaging TEXT,
                is_organic BOOLEAN,
                carbon_kg FLOAT,
                price FLOAT
            )''',
            '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                points INTEGER DEFAULT 0
            )''',
            '''CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )'''
        ]
    
    for query in queries:
        execute_query(query)

# --- Mock Data Insertion ---
def insert_mock_data():
    """Insert sample data if tables are empty"""
    # Check if products table has data
    products_count = execute_query('SELECT COUNT(*) FROM products', fetch=True)[0][0]
    
    if products_count == 0:
        products = [
            ('Regular Chicken Breast', 'Standard chicken breast', 'meat', 'plastic', False, 3.2, 8.99),
            ('Organic Free-Range Chicken', 'Organic, free-range chicken', 'meat', 'paper', True, 2.1, 12.99),
            ('Regular Ground Beef', 'Standard ground beef', 'meat', 'plastic', False, 4.8, 10.99),
            ('Organic Grass-Fed Beef', 'Organic, grass-fed beef', 'meat', 'paper', True, 3.2, 16.99),
            ('Regular Milk', 'Standard milk', 'dairy', 'plastic', False, 1.9, 3.99),
            ('Organic Oat Milk', 'Organic oat milk', 'dairy', 'glass', True, 0.8, 4.99),
            ('Regular Yogurt', 'Standard yogurt', 'dairy', 'plastic', False, 1.2, 2.99),
            ('Organic Greek Yogurt', 'Organic Greek yogurt', 'dairy', 'glass', True, 0.9, 5.99),
            ('White Rice', 'Standard white rice', 'grains', 'plastic', False, 2.1, 2.49),
            ('Organic Brown Rice', 'Organic brown rice', 'grains', 'paper', True, 1.8, 3.99)
        ]
        
        for product in products:
            execute_query(
                '''INSERT INTO products (name, description, category, packaging, is_organic, carbon_kg, price)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''' if is_postgres() else
                '''INSERT INTO products (name, description, category, packaging, is_organic, carbon_kg, price)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                product
            )
    
    # Check if users table has data
    users_count = execute_query('SELECT COUNT(*) FROM users', fetch=True)[0][0]
    
    if users_count == 0:
        execute_query(
            'INSERT INTO users (name, points) VALUES (%s, %s)' if is_postgres() else
            'INSERT INTO users (name, points) VALUES (?, ?)',
            ('Alice', 0)
        )

# --- Product Helpers ---
def get_all_products() -> List[Dict[str, Any]]:
    """Get all products from database"""
    rows = execute_query('SELECT * FROM products', fetch=True)
    keys = ['id', 'name', 'description', 'category', 'packaging', 'is_organic', 'carbon_kg', 'price']
    return [dict(zip(keys, row)) for row in rows]

def get_product_by_id(pid: int) -> Optional[Dict[str, Any]]:
    """Get product by ID"""
    query = 'SELECT * FROM products WHERE id=%s' if is_postgres() else 'SELECT * FROM products WHERE id=?'
    rows = execute_query(query, (pid,), fetch=True)
    
    if rows:
        keys = ['id', 'name', 'description', 'category', 'packaging', 'is_organic', 'carbon_kg', 'price']
        return dict(zip(keys, rows[0]))
    return None

# --- User Helpers ---
def get_user_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Get user by name"""
    query = 'SELECT * FROM users WHERE name=%s' if is_postgres() else 'SELECT * FROM users WHERE name=?'
    rows = execute_query(query, (name,), fetch=True)
    
    if rows:
        keys = ['id', 'name', 'points']
        return dict(zip(keys, rows[0]))
    return None

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    query = 'SELECT * FROM users WHERE id=%s' if is_postgres() else 'SELECT * FROM users WHERE id=?'
    rows = execute_query(query, (user_id,), fetch=True)
    
    if rows:
        keys = ['id', 'name', 'points']
        return dict(zip(keys, rows[0]))
    return None

def update_user_points(user_id: int, points: int):
    """Update user points"""
    query = 'UPDATE users SET points=%s WHERE id=%s' if is_postgres() else 'UPDATE users SET points=? WHERE id=?'
    execute_query(query, (points, user_id))

# --- Cart Helpers ---
def add_to_cart(user_id: int, product_id: int, quantity: int = 1):
    """Add item to cart or update quantity if already exists"""
    if quantity < 1:
        return False, 'Quantity must be at least 1.'
    
    # Check if item already in cart
    query = ('SELECT id, quantity FROM cart WHERE user_id=%s AND product_id=%s' if is_postgres() else
             'SELECT id, quantity FROM cart WHERE user_id=? AND product_id=?')
    rows = execute_query(query, (user_id, product_id), fetch=True)
    
    if rows:
        # Update existing item
        cart_id, old_qty = rows[0]
        query = 'UPDATE cart SET quantity=%s WHERE id=%s' if is_postgres() else 'UPDATE cart SET quantity=? WHERE id=?'
        execute_query(query, (old_qty + quantity, cart_id))
    else:
        # Add new item
        query = ('INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)' if is_postgres() else
                 'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)')
        execute_query(query, (user_id, product_id, quantity))
    
    return True, 'Added to cart.'

def get_cart(user_id: int) -> List[Dict[str, Any]]:
    """Get cart items for user with product details"""
    query = '''SELECT cart.id, products.name, products.category, products.packaging, 
               products.is_organic, products.carbon_kg, products.price, cart.quantity
               FROM cart JOIN products ON cart.product_id = products.id 
               WHERE cart.user_id=%s''' if is_postgres() else '''SELECT cart.id, products.name, products.category, products.packaging, 
               products.is_organic, products.carbon_kg, products.price, cart.quantity
               FROM cart JOIN products ON cart.product_id = products.id 
               WHERE cart.user_id=?'''
    
    rows = execute_query(query, (user_id,), fetch=True)
    keys = ['cart_id', 'name', 'category', 'packaging', 'is_organic', 'carbon_kg', 'price', 'quantity']
    return [dict(zip(keys, row)) for row in rows]

def clear_cart(user_id: int):
    """Clear all items from user's cart"""
    query = 'DELETE FROM cart WHERE user_id=%s' if is_postgres() else 'DELETE FROM cart WHERE user_id=?'
    execute_query(query, (user_id,))

# --- Initialize DB on first run ---
def init_db():
    """Initialize database - create tables and insert sample data"""
    create_tables()
    insert_mock_data()
    print(f"Database initialized successfully ({'PostgreSQL' if is_postgres() else 'SQLite'})")
