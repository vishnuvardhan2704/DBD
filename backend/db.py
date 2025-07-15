import sqlite3
from typing import List, Dict, Any, Optional
import os
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Database configuration
DB_PATH = os.getenv('ESG_DB_PATH', 'esg_recommender.db')

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

# --- Schema Creation ---
def create_tables():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            packaging TEXT,
            is_organic BOOLEAN,
            carbon_kg FLOAT,
            price FLOAT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            points INTEGER DEFAULT 0
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )''')
        conn.commit()

# --- Mock Data Insertion ---
def insert_mock_data():
    with get_db_connection() as conn:
        c = conn.cursor()
        # Only insert if table is empty
        c.execute('SELECT COUNT(*) FROM products')
        if c.fetchone()[0] == 0:
            products = [
                ('Regular Chicken Breast', 'Standard chicken breast', 'meat', 'plastic', 0, 3.2, 8.99),
                ('Organic Free-Range Chicken', 'Organic, free-range chicken', 'meat', 'paper', 1, 2.1, 12.99),
                ('Regular Ground Beef', 'Standard ground beef', 'meat', 'plastic', 0, 4.8, 10.99),
                ('Organic Grass-Fed Beef', 'Organic, grass-fed beef', 'meat', 'paper', 1, 3.2, 16.99),
                ('Regular Milk', 'Standard milk', 'dairy', 'plastic', 0, 1.9, 3.99),
                ('Organic Oat Milk', 'Organic oat milk', 'dairy', 'glass', 1, 0.8, 4.99),
                ('Regular Yogurt', 'Standard yogurt', 'dairy', 'plastic', 0, 1.2, 2.99),
                ('Organic Greek Yogurt', 'Organic Greek yogurt', 'dairy', 'glass', 1, 0.9, 5.99),
                ('White Rice', 'Standard white rice', 'grains', 'plastic', 0, 2.1, 2.49),
                ('Organic Brown Rice', 'Organic brown rice', 'grains', 'paper', 1, 1.8, 3.99)
            ]
            c.executemany('''INSERT INTO products (name, description, category, packaging, is_organic, carbon_kg, price)
                             VALUES (?, ?, ?, ?, ?, ?, ?)''', products)
        c.execute('SELECT COUNT(*) FROM users')
        if c.fetchone()[0] == 0:
            c.execute('INSERT INTO users (name, points) VALUES (?, ?)', ('Alice', 0))
        conn.commit()

# --- Product Helpers ---
def get_all_products() -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM products')
        rows = c.fetchall()
        keys = ['id', 'name', 'description', 'category', 'packaging', 'is_organic', 'carbon_kg', 'price']
        return [dict(zip(keys, row)) for row in rows]

def get_product_by_id(pid: int) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM products WHERE id=?', (pid,))
        row = c.fetchone()
        if row:
            keys = ['id', 'name', 'description', 'category', 'packaging', 'is_organic', 'carbon_kg', 'price']
            return dict(zip(keys, row))
    return None

# --- User Helpers ---
def get_user_by_name(name: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE name=?', (name,))
        row = c.fetchone()
        if row:
            keys = ['id', 'name', 'points']
            return dict(zip(keys, row))
    return None

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE id=?', (user_id,))
        row = c.fetchone()
        if row:
            keys = ['id', 'name', 'points']
            return dict(zip(keys, row))
    return None

def update_user_points(user_id: int, points: int):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('UPDATE users SET points=? WHERE id=?', (points, user_id))
        conn.commit()

# --- Cart Helpers ---
def add_to_cart(user_id: int, product_id: int, quantity: int = 1):
    if quantity < 1:
        return False, 'Quantity must be at least 1.'
    with get_db_connection() as conn:
        c = conn.cursor()
        # Check if already in cart
        c.execute('SELECT id, quantity FROM cart WHERE user_id=? AND product_id=?', (user_id, product_id))
        row = c.fetchone()
        if row:
            cart_id, old_qty = row
            c.execute('UPDATE cart SET quantity=? WHERE id=?', (old_qty + quantity, cart_id))
        else:
            c.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)', (user_id, product_id, quantity))
        conn.commit()
    return True, 'Added to cart.'

def get_cart(user_id: int) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''SELECT cart.id, products.name, products.category, products.packaging, products.is_organic, products.carbon_kg, products.price, cart.quantity
                     FROM cart JOIN products ON cart.product_id = products.id WHERE cart.user_id=?''', (user_id,))
        rows = c.fetchall()
        keys = ['cart_id', 'name', 'category', 'packaging', 'is_organic', 'carbon_kg', 'price', 'quantity']
        return [dict(zip(keys, row)) for row in rows]

def clear_cart(user_id: int):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('DELETE FROM cart WHERE user_id=?', (user_id,))
        conn.commit()

# --- Initialize DB on first run ---
def init_db():
    create_tables()
    insert_mock_data()