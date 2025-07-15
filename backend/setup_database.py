#!/usr/bin/env python3
"""
Database Configuration Script
Helps you switch between SQLite (local) and PostgreSQL (Supabase) databases
"""

import os
import shutil
from pathlib import Path

def setup_database_for_supabase():
    """Replace db.py with Supabase-compatible version"""
    backend_dir = Path(__file__).parent
    
    # Backup original db.py
    if (backend_dir / "db.py").exists():
        shutil.copy(backend_dir / "db.py", backend_dir / "db_sqlite_backup.py")
        print("✅ Backed up original db.py to db_sqlite_backup.py")
    
    # Replace with Supabase version
    if (backend_dir / "db_supabase.py").exists():
        shutil.copy(backend_dir / "db_supabase.py", backend_dir / "db.py")
        print("✅ Replaced db.py with Supabase-compatible version")
        print("✅ Your app now supports both SQLite (local) and PostgreSQL (Supabase)")
        print("")
        print("🎯 Next steps:")
        print("1. Set DATABASE_URL environment variable for Supabase")
        print("2. Deploy to Vercel")
        print("3. Your app will automatically use PostgreSQL in production!")
    else:
        print("❌ db_supabase.py not found")

def restore_sqlite_only():
    """Restore original SQLite-only db.py"""
    backend_dir = Path(__file__).parent
    
    if (backend_dir / "db_sqlite_backup.py").exists():
        shutil.copy(backend_dir / "db_sqlite_backup.py", backend_dir / "db.py")
        print("✅ Restored original SQLite-only db.py")
    else:
        print("❌ No SQLite backup found")

if __name__ == "__main__":
    print("🗄️  Database Configuration for ESG Recommender")
    print("")
    print("Choose your database setup:")
    print("1. Enable Supabase support (SQLite + PostgreSQL)")
    print("2. Restore SQLite only")
    print("3. Show current configuration")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        setup_database_for_supabase()
    elif choice == "2":
        restore_sqlite_only()
    elif choice == "3":
        # Check current configuration
        backend_dir = Path(__file__).parent
        with open(backend_dir / "db.py", "r") as f:
            content = f.read()
            if "psycopg2" in content:
                print("✅ Current: Supabase-compatible (supports both SQLite and PostgreSQL)")
            else:
                print("✅ Current: SQLite only")
    else:
        print("❌ Invalid choice")
