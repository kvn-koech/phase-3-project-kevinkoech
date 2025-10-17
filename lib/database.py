import sqlite3
from datetime import datetime
import click

class Database:
    def __init__(self, db_name='car_rental.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get database connection with proper error handling"""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.row_factory = sqlite3.Row
            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            click.echo(f"Database connection error: {e}")
            raise
    
    def init_database(self):
        """Initialize database tables with better constraints"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Locations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zip_code TEXT NOT NULL,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Vehicles table with better constraints
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vehicles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year INTEGER NOT NULL CHECK (year >= 1900 AND year <= 2025),
                    license_plate TEXT UNIQUE NOT NULL,
                    color TEXT,
                    vehicle_type TEXT CHECK(vehicle_type IN ('sedan', 'SUV', 'hatchback', 'minivan', 'pickup', 'luxury')),
                    daily_rate REAL NOT NULL CHECK (daily_rate > 0),
                    available BOOLEAN DEFAULT 1,
                    location_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE SET NULL
                )
            ''')
            
            # Customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    license_number TEXT UNIQUE NOT NULL,
                    date_of_birth TEXT,
                    is_vip BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Rentals table with status constraints
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rentals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    vehicle_id INTEGER NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    actual_return_date TEXT,
                    total_amount REAL CHECK (total_amount >= 0),
                    status TEXT DEFAULT 'reserved' CHECK (status IN ('reserved', 'active', 'completed', 'cancelled')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id) ON DELETE CASCADE,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles (id) ON DELETE CASCADE
                )
            ''')
            
            # Maintenance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS maintenance_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id INTEGER NOT NULL,
                    maintenance_type TEXT NOT NULL CHECK (maintenance_type IN ('routine', 'repair', 'inspection')),
                    description TEXT,
                    cost REAL CHECK (cost >= 0),
                    maintenance_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    next_maintenance_date TEXT,
                    status TEXT DEFAULT 'completed' CHECK (status IN ('scheduled', 'in-progress', 'completed')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles (id) ON DELETE CASCADE
                )
            ''')
            
            # Insurance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS insurance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id INTEGER NOT NULL,
                    provider TEXT NOT NULL,
                    policy_number TEXT UNIQUE NOT NULL,
                    coverage_type TEXT CHECK (coverage_type IN ('comprehensive', 'third-party', 'liability')),
                    premium REAL CHECK (premium >= 0),
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    deductible REAL CHECK (deductible >= 0),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles (id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
            click.echo("Database initialized successfully!")
            
        except sqlite3.Error as e:
            click.echo(f"Database initialization error: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_query(self, query, params=()):
        """Execute a query with proper error handling"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except sqlite3.Error as e:
            conn.rollback()
            click.echo(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def fetch_all(self, query, params=()):
        """Fetch all results from a query"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            click.echo(f"Database fetch error: {e}")
            return []
        finally:
            conn.close()
    
    def fetch_one(self, query, params=()):
        """Fetch one result from a query"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            click.echo(f"Database fetch error: {e}")
            return None
        finally:
            conn.close()

# Global database instance
db = Database()