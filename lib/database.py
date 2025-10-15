import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='car_rental.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Locations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                phone TEXT
            )
        ''')
        
        # Vehicles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                license_plate TEXT UNIQUE NOT NULL,
                color TEXT,
                vehicle_type TEXT,
                daily_rate REAL NOT NULL,
                available BOOLEAN DEFAULT 1,
                location_id INTEGER,
                FOREIGN KEY (location_id) REFERENCES locations (id)
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
                is_vip BOOLEAN DEFAULT 0
            )
        ''')
        
        # Rentals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                vehicle_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                actual_return_date TEXT,
                total_amount REAL,
                status TEXT DEFAULT 'reserved',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
            )
        ''')
        
        # Maintenance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                maintenance_type TEXT NOT NULL,
                description TEXT,
                cost REAL,
                maintenance_date TEXT DEFAULT CURRENT_TIMESTAMP,
                next_maintenance_date TEXT,
                status TEXT DEFAULT 'completed',
                FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
            )
        ''')
        
        # Insurance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insurance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER NOT NULL,
                provider TEXT NOT NULL,
                policy_number TEXT UNIQUE NOT NULL,
                coverage_type TEXT,
                premium REAL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                deductible REAL,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=()):
        """Execute a query and return results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def fetch_all(self, query, params=()):
        """Fetch all results from a query"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def fetch_one(self, query, params=()):
        """Fetch one result from a query"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result

# Global database instance
db = Database()