#!/usr/bin/env python3

"""
Debug helper for the Car Rental System - Kenyan Edition
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.orm import CarRentalORM, calculate_rental_total, is_vehicle_available, can_customer_rent
from database import db
from datetime import datetime, timedelta

class DebugHelper:
    
    @staticmethod
    def setup_sample_data():
        """Create sample data with Kenyan examples"""
        print("Setting up sample data with Kenyan locations...")
        
        # Check if sample data already exists
        existing_locations = CarRentalORM.get_all('locations')
        existing_vehicles = CarRentalORM.get_all('vehicles')
        
        if len(existing_locations) >= 3 or len(existing_vehicles) >= 5:
            print("WARNING: Sample data already exists!")
            print("To avoid duplicates, please:")
            print("1. Use option 5 to reset database first, OR")
            print("2. Continue with current data (some records may fail)")
            
            choice = input("Continue anyway? (y/N): ").lower()
            if choice != 'y':
                print("Sample data setup cancelled.")
                return
        
        # Create sample locations in Kenyan cities
        locations_data = [
            {'name': 'Nairobi CBD Branch', 'address': 'Kenyatta Avenue, ICEA Building', 'city': 'Nairobi', 'state': 'Nairobi', 'zip_code': '00100', 'phone': '020-1234567'},
            {'name': 'JKIA Airport Branch', 'address': 'Jomo Kenyatta International Airport', 'city': 'Nairobi', 'state': 'Nairobi', 'zip_code': '00501', 'phone': '020-2345678'},
            {'name': 'Mombasa Branch', 'address': 'Moi Avenue, Nyali', 'city': 'Mombasa', 'state': 'Coast', 'zip_code': '80100', 'phone': '041-1234567'},
            {'name': 'Kisumu Branch', 'address': 'Oginga Odinga Road', 'city': 'Kisumu', 'state': 'Nyanza', 'zip_code': '40100', 'phone': '057-1234567'},
            {'name': 'Nakuru Branch', 'address': 'Kenyatta Avenue', 'city': 'Nakuru', 'state': 'Rift Valley', 'zip_code': '20100', 'phone': '051-1234567'}
        ]
        
        location_ids = []
        for location in locations_data:
            try:
                location_id = CarRentalORM.create('locations', location)
                location_ids.append(location_id)
                print(f"Created location: {location['name']} (ID: {location_id})")
            except Exception as e:
                print(f"Error creating location {location['name']}: {e}")
        
        # Create sample vehicles with Kenyan license plates
        vehicles_data = [
            {'make': 'Toyota', 'model': 'Noah', 'year': 2023, 'license_plate': 'KCA123A', 'color': 'White', 'vehicle_type': 'minivan', 'daily_rate': 3500.00, 'location_id': location_ids[0]},
            {'make': 'Toyota', 'model': 'Premio', 'year': 2022, 'license_plate': 'KDB456B', 'color': 'Silver', 'vehicle_type': 'sedan', 'daily_rate': 2500.00, 'location_id': location_ids[0]},
            {'make': 'Subaru', 'model': 'Forester', 'year': 2023, 'license_plate': 'KCC789C', 'color': 'Blue', 'vehicle_type': 'SUV', 'daily_rate': 4500.00, 'location_id': location_ids[1]},
            {'make': 'Land Rover', 'model': 'Discovery', 'year': 2022, 'license_plate': 'KCD012D', 'color': 'Black', 'vehicle_type': 'SUV', 'daily_rate': 6000.00, 'location_id': location_ids[1]},
            {'make': 'Nissan', 'model': 'March', 'year': 2023, 'license_plate': 'KCE345E', 'color': 'Red', 'vehicle_type': 'hatchback', 'daily_rate': 1800.00, 'location_id': location_ids[2]},
            {'make': 'Toyota', 'model': 'Hilux', 'year': 2023, 'license_plate': 'KCF678F', 'color': 'White', 'vehicle_type': 'pickup', 'daily_rate': 4000.00, 'location_id': location_ids[2]},
            {'make': 'Mazda', 'model': 'CX-5', 'year': 2022, 'license_plate': 'KCG901G', 'color': 'Gray', 'vehicle_type': 'SUV', 'daily_rate': 3800.00, 'location_id': location_ids[3]},
            {'make': 'Toyota', 'model': 'Vitz', 'year': 2023, 'license_plate': 'KCH234H', 'color': 'Blue', 'vehicle_type': 'hatchback', 'daily_rate': 2000.00, 'location_id': location_ids[4]}
        ]
        
        vehicle_ids = []
        for vehicle in vehicles_data:
            try:
                vehicle_id = CarRentalORM.create('vehicles', vehicle)
                vehicle_ids.append(vehicle_id)
                print(f"Created vehicle: {vehicle['year']} {vehicle['make']} {vehicle['model']} - KES {vehicle['daily_rate']}/day (ID: {vehicle_id})")
            except Exception as e:
                print(f"Error creating vehicle {vehicle['license_plate']}: {e}")
        
        # Create sample customers with Kenyan names
        customers_data = [
            {'first_name': 'John', 'last_name': 'Kamau', 'email': 'john.kamau@email.com', 'phone': '0712-345678', 'license_number': 'A1234567', 'date_of_birth': '1985-03-15', 'is_vip': 1},
            {'first_name': 'Mary', 'last_name': 'Wanjiku', 'email': 'mary.wanjiku@email.com', 'phone': '0723-456789', 'license_number': 'B7654321', 'date_of_birth': '1990-07-22', 'is_vip': 0},
            {'first_name': 'James', 'last_name': 'Ochieng', 'email': 'james.ochieng@email.com', 'phone': '0734-567890', 'license_number': 'C1122334', 'date_of_birth': '1988-11-30', 'is_vip': 1},
            {'first_name': 'Grace', 'last_name': 'Akinyi', 'email': 'grace.akinyi@email.com', 'phone': '0745-678901', 'license_number': 'D4455667', 'date_of_birth': '1992-05-14', 'is_vip': 0},
            {'first_name': 'David', 'last_name': 'Mbugua', 'email': 'david.mbugua@email.com', 'phone': '0756-789012', 'license_number': 'E7788990', 'date_of_birth': '1987-09-10', 'is_vip': 1}
        ]
        
        customer_ids = []
        for customer in customers_data:
            try:
                customer_id = CarRentalORM.create('customers', customer)
                customer_ids.append(customer_id)
                print(f"Created customer: {customer['first_name']} {customer['last_name']} (ID: {customer_id})")
            except Exception as e:
                print(f"Error creating customer {customer['first_name']} {customer['last_name']}: {e}")
        
        # Create sample rentals
        today = datetime.now().date()
        rentals_data = [
            {'customer_id': customer_ids[0], 'vehicle_id': vehicle_ids[0], 'start_date': (today - timedelta(days=2)).strftime('%Y-%m-%d'), 'end_date': (today + timedelta(days=3)).strftime('%Y-%m-%d'), 'status': 'active', 'total_amount': 17500.00},
            {'customer_id': customer_ids[1], 'vehicle_id': vehicle_ids[2], 'start_date': (today - timedelta(days=5)).strftime('%Y-%m-%d'), 'end_date': (today - timedelta(days=1)).strftime('%Y-%m-%d'), 'status': 'completed', 'total_amount': 18000.00},
            {'customer_id': customer_ids[2], 'vehicle_id': vehicle_ids[4], 'start_date': (today + timedelta(days=2)).strftime('%Y-%m-%d'), 'end_date': (today + timedelta(days=7)).strftime('%Y-%m-%d'), 'status': 'reserved', 'total_amount': 9000.00}
        ]
        
        for rental in rentals_data:
            try:
                rental_id = CarRentalORM.create('rentals', rental)
                print(f"Created rental: Customer {rental['customer_id']} - Vehicle {rental['vehicle_id']} (ID: {rental_id})")
            except Exception as e:
                print(f"Error creating rental: {e}")
        
        print("\nKenyan Sample data setup completed successfully!")
        print(f"Created: {len(location_ids)} locations, {len(vehicle_ids)} vehicles, {len(customer_ids)} customers")
        print("Plus sample rentals")
        print("\nLocations: Nairobi CBD, JKIA, Mombasa, Kisumu, Nakuru")
        print("Vehicle types: Noah, Premio, Forester, Hilux, Vitz - popular in Kenya!")

    @staticmethod
    def test_database_connection():
        """Test database connection and table creation"""
        print("Testing database connection...")
        try:
            # Test connection by querying all tables
            tables = ['locations', 'vehicles', 'customers', 'rentals', 'maintenance_records', 'insurance']
            
            for table in tables:
                result = CarRentalORM.get_all(table)
                print(f" Table '{table}': {len(result)} records")
            
            print("Database connection test: PASSED")
            return True
            
        except Exception as e:
            print(f"Database connection test: FAILED - {e}")
            return False

    @staticmethod
    def display_database_stats():
        """Display database statistics"""
        print("\n" + "="*50)
        print("🇰🇪 KENYAN CAR RENTAL - DATABASE STATISTICS")
        print("="*50)
        
        tables = {
            'locations': 'Locations',
            'vehicles': 'Vehicles',
            'customers': 'Customers',
            'rentals': 'Rentals',
            'maintenance_records': 'Maintenance Records',
            'insurance': 'Insurance Policies'
        }
        
        for table, name in tables.items():
            count = len(CarRentalORM.get_all(table))
            print(f"{name}: {count}")
        
        # Additional stats
        available_vehicles = len(CarRentalORM.find_available_vehicles())
        active_rentals = len(CarRentalORM.find_active_rentals())
        
        print(f"\nAvailable Vehicles: {available_vehicles}")
        print(f"Active Rentals: {active_rentals}")
        
        # Revenue report
        revenue_data = CarRentalORM.get_revenue_report()
        if revenue_data:
            print(f"\nTotal Revenue: KES {revenue_data['total_revenue'] or 0:,.2f}")
            print(f"Completed Rentals: {revenue_data['completed_rentals']}")
            print(f"Active Rentals: {revenue_data['active_rentals']}")

    @staticmethod
    def run_all_tests():
        """Run all debug tests"""
        print("🇰🇪 Running Kenyan Car Rental System Tests")
        print("="*50)
        
        # Test 1: Database connection
        if DebugHelper.test_database_connection():
            print(" Database tests passed")
        else:
            print(" Database tests failed")
        
        # Display stats
        DebugHelper.display_database_stats()

    @staticmethod
    def reset_database():
        """Reset the database (DANGEROUS - for development only)"""
        confirm = input(" WARNING: This will delete ALL data. Type 'DELETE ALL' to confirm: ")
        if confirm == 'DELETE ALL':
            try:
                conn = db.get_connection()
                cursor = conn.cursor()
                
                # Drop all tables in correct order (respecting foreign keys)
                tables = ['insurance', 'maintenance_records', 'rentals', 'vehicles', 'customers', 'locations']
                
                for table in tables:
                    cursor.execute(f'DROP TABLE IF EXISTS {table}')
                    print(f"Dropped table: {table}")
                
                conn.commit()
                conn.close()
                
                # Reinitialize database
                db.init_database()
                print("Database reset completed successfully!")
                
            except Exception as e:
                print(f"Error resetting database: {e}")
        else:
            print("Database reset cancelled.")

def debug_menu():
    """Interactive debug menu"""
    while True:
        print("\n" + "="*50)
        print("🇰🇪 DEBUG MENU - Kenyan Car Rental System")
        print("="*50)
        print("1. Run All Tests")
        print("2. Setup Kenyan Sample Data")
        print("3. Test Database Connection")
        print("4. Display Database Statistics")
        print("5. Reset Database (DANGEROUS)")
        print("0. Exit Debug Menu")
        print("="*50)
        
        choice = input("Select option: ")
        
        if choice == "1":
            DebugHelper.run_all_tests()
        elif choice == "2":
            DebugHelper.setup_sample_data()
        elif choice == "3":
            DebugHelper.test_database_connection()
        elif choice == "4":
            DebugHelper.display_database_stats()
        elif choice == "5":
            DebugHelper.reset_database()
        elif choice == "0":
            print("Exiting debug menu...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # When run directly, show the debug menu
    debug_menu()