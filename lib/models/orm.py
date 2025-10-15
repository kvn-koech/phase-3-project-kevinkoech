from database import db
from datetime import datetime, timedelta

class CarRentalORM:
    
    # Generic CRUD operations
    @classmethod
    def create(cls, table, data):
        """Create a new record"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = db.execute_query(query, tuple(data.values()))
        return cursor.lastrowid
    
    @classmethod
    def delete(cls, table, record_id):
        """Delete a record by ID"""
        query = f"DELETE FROM {table} WHERE id = ?"
        db.execute_query(query, (record_id,))
    
    @classmethod
    def get_all(cls, table):
        """Get all records from a table"""
        query = f"SELECT * FROM {table}"
        return db.fetch_all(query)
    
    @classmethod
    def find_by_id(cls, table, record_id):
        """Find a record by ID"""
        query = f"SELECT * FROM {table} WHERE id = ?"
        return db.fetch_one(query, (record_id,))
    
    @classmethod
    def update(cls, table, record_id, data):
        """Update a record"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        params = tuple(data.values()) + (record_id,)
        db.execute_query(query, params)
    
    # Vehicle-specific operations
    @classmethod
    def find_available_vehicles(cls):
        """Find all available vehicles"""
        query = """
            SELECT v.*, l.name as location_name, l.city 
            FROM vehicles v 
            LEFT JOIN locations l ON v.location_id = l.id 
            WHERE v.available = 1 
            AND v.id NOT IN (
                SELECT vehicle_id FROM rentals 
                WHERE status IN ('active', 'reserved')
            )
        """
        return db.fetch_all(query)
    
    @classmethod
    def find_vehicles_by_type(cls, vehicle_type):
        """Find vehicles by type"""
        query = """
            SELECT v.*, l.name as location_name, l.city 
            FROM vehicles v 
            LEFT JOIN locations l ON v.location_id = l.id 
            WHERE v.vehicle_type = ? AND v.available = 1
            AND v.id NOT IN (
                SELECT vehicle_id FROM rentals 
                WHERE status IN ('active', 'reserved')
            )
        """
        return db.fetch_all(query, (vehicle_type,))
    
    @classmethod
    def find_vehicles_by_location(cls, location_id):
        """Find vehicles by location"""
        query = """
            SELECT v.*, l.name as location_name, l.city 
            FROM vehicles v 
            LEFT JOIN locations l ON v.location_id = l.id 
            WHERE v.location_id = ? AND v.available = 1
            AND v.id NOT IN (
                SELECT vehicle_id FROM rentals 
                WHERE status IN ('active', 'reserved')
            )
        """
        return db.fetch_all(query, (location_id,))
    
    # Customer-specific operations
    @classmethod
    def find_customer_by_email(cls, email):
        """Find customer by email"""
        query = "SELECT * FROM customers WHERE email = ?"
        return db.fetch_one(query, (email,))
    
    @classmethod
    def find_customer_by_license(cls, license_number):
        """Find customer by license number"""
        query = "SELECT * FROM customers WHERE license_number = ?"
        return db.fetch_one(query, (license_number,))
    
    # Rental-specific operations
    @classmethod
    def find_active_rentals(cls):
        """Find all active rentals"""
        query = """
            SELECT r.*, c.first_name, c.last_name, v.make, v.model, v.year 
            FROM rentals r
            JOIN customers c ON r.customer_id = c.id
            JOIN vehicles v ON r.vehicle_id = v.id
            WHERE r.status IN ('active', 'reserved')
        """
        return db.fetch_all(query)
    
    @classmethod
    def find_overdue_rentals(cls):
        """Find overdue rentals"""
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT r.*, c.first_name, c.last_name, v.make, v.model, v.year 
            FROM rentals r
            JOIN customers c ON r.customer_id = c.id
            JOIN vehicles v ON r.vehicle_id = v.id
            WHERE r.status = 'active' AND r.end_date < ?
        """
        return db.fetch_all(query, (today,))
    
    @classmethod
    def find_rentals_by_customer(cls, customer_id):
        """Find rentals by customer"""
        query = """
            SELECT r.*, v.make, v.model, v.year 
            FROM rentals r
            JOIN vehicles v ON r.vehicle_id = v.id
            WHERE r.customer_id = ?
        """
        return db.fetch_all(query, (customer_id,))
    
    # Maintenance-specific operations
    @classmethod
    def find_overdue_maintenance(cls):
        """Find overdue maintenance records"""
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT m.*, v.make, v.model, v.year 
            FROM maintenance_records m
            JOIN vehicles v ON m.vehicle_id = v.id
            WHERE m.next_maintenance_date < ? AND m.status != 'completed'
        """
        return db.fetch_all(query, (today,))
    
    @classmethod
    def find_scheduled_maintenance(cls):
        """Find scheduled maintenance"""
        query = """
            SELECT m.*, v.make, v.model, v.year 
            FROM maintenance_records m
            JOIN vehicles v ON m.vehicle_id = v.id
            WHERE m.status = 'scheduled'
        """
        return db.fetch_all(query)
    
    # Insurance-specific operations
    @classmethod
    def find_expiring_insurance(cls, days=30):
        """Find insurance policies expiring soon"""
        future_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')
        query = """
            SELECT i.*, v.make, v.model, v.year 
            FROM insurance i
            JOIN vehicles v ON i.vehicle_id = v.id
            WHERE i.end_date <= ? AND i.end_date >= ?
        """
        return db.fetch_all(query, (future_date, today))
    
    # Reporting operations
    @classmethod
    def get_revenue_report(cls):
        """Generate revenue report"""
        query = """
            SELECT 
                COUNT(*) as total_rentals,
                SUM(total_amount) as total_revenue,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_rentals,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_rentals
            FROM rentals
            WHERE total_amount IS NOT NULL
        """
        return db.fetch_one(query)
    
    @classmethod
    def get_utilization_report(cls):
        """Generate vehicle utilization report"""
        query = """
            SELECT 
                COUNT(*) as total_vehicles,
                SUM(available) as available_vehicles,
                COUNT(*) - SUM(available) as rented_vehicles
            FROM vehicles
        """
        return db.fetch_one(query)

# Utility functions
def calculate_rental_total(vehicle_daily_rate, start_date, end_date, actual_return_date=None):
    """Calculate rental total with potential late fees"""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Base rental days
    rental_days = (end - start).days
    base_cost = rental_days * vehicle_daily_rate
    
    # Late fees
    late_fee = 0
    if actual_return_date:
        actual_return = datetime.strptime(actual_return_date, '%Y-%m-%d')
        if actual_return > end:
            overdue_days = (actual_return - end).days
            late_fee = overdue_days * vehicle_daily_rate * 1.5  # 50% late fee
    
    return base_cost + late_fee

def is_vehicle_available(vehicle_id):
    """Check if a vehicle is available for rental"""
    query = """
        SELECT available FROM vehicles WHERE id = ?
        AND id NOT IN (
            SELECT vehicle_id FROM rentals 
            WHERE status IN ('active', 'reserved')
        )
    """
    result = db.fetch_one(query, (vehicle_id,))
    return result and result['available'] == 1

def can_customer_rent(customer_id):
    """Check if customer can rent (no active rentals)"""
    query = "SELECT COUNT(*) as active_count FROM rentals WHERE customer_id = ? AND status = 'active'"
    result = db.fetch_one(query, (customer_id,))
    return result and result['active_count'] == 0