#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import (
    exit_program,
    # Vehicle functions
    list_vehicles, create_vehicle, find_vehicle_by_type,
    find_available_vehicles, update_vehicle_status,
    # Customer functions
    list_customers, create_customer, find_customer_by_email,
    # Rental functions
    list_rentals, create_rental, find_active_rentals,
    process_return, 
    # Maintenance functions
    list_maintenance,
    # Location functions
    list_locations, create_location,
    # Insurance functions
    list_insurance,
    # Reporting functions
    generate_revenue_report, generate_utilization_report
)

def main():
    print("🇰🇪 Kenyan Car Rental System initialized!")
    print("Database tables created successfully.")
    
    while True:
        main_menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            vehicle_menu()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            rental_menu()
        elif choice == "4":
            maintenance_menu()
        elif choice == "5":
            location_menu()
        elif choice == "6":
            insurance_menu()
        elif choice == "7":
            reporting_menu()
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    print("\n" + "="*50)
    print("    🇰🇪 KENYAN CAR RENTAL MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Vehicle Management")
    print("2. Customer Management")
    print("3. Rental Management")
    print("4. Maintenance Management")
    print("5. Location Management")
    print("6. Insurance Management")
    print("7. Reports & Analytics")
    print("0. Exit Program")
    print("="*50)

def vehicle_menu():
    while True:
        print("\n--- VEHICLE MANAGEMENT ---")
        print("1. List all vehicles")
        print("2. List available vehicles")
        print("3. Add new vehicle")
        print("4. Find vehicles by type")
        print("5. Update vehicle status")
        print("6. Back to main menu")
        
        choice = input("> ")
        if choice == "1":
            list_vehicles()
        elif choice == "2":
            find_available_vehicles()
        elif choice == "3":
            create_vehicle()
        elif choice == "4":
            find_vehicle_by_type()
        elif choice == "5":
            update_vehicle_status()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def customer_menu():
    while True:
        print("\n--- CUSTOMER MANAGEMENT ---")
        print("1. List all customers")
        print("2. Add new customer")
        print("3. Find customer by email")
        print("4. Back to main menu")
        
        choice = input("> ")
        if choice == "1":
            list_customers()
        elif choice == "2":
            create_customer()
        elif choice == "3":
            find_customer_by_email()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def rental_menu():
    while True:
        print("\n--- RENTAL MANAGEMENT ---")
        print("1. List all rentals")
        print("2. List active rentals")
        print("3. Create new rental")
        print("4. Process vehicle return")
        print("5. Back to main menu")
        
        choice = input("> ")
        if choice == "1":
            list_rentals()
        elif choice == "2":
            find_active_rentals()
        elif choice == "3":
            create_rental()
        elif choice == "4":
            process_return()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def maintenance_menu():
    while True:
        print("\n--- MAINTENANCE MANAGEMENT ---")
        print("1. List all maintenance records")
        print("2. Back to main menu")
        
        choice = input("> ")
        if choice == "1":
            list_maintenance()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

def location_menu():
    while True:
        print("\n--- LOCATION MANAGEMENT ---")
        print("1. List all locations")
        print("2. Add new location")
        print("3. Back to main menu")
        
        choice = input("> ")
        if choice == "1":
            list_locations()
        elif choice == "2":
            create_location()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def insurance_menu():
    while True:
        print("\n--- INSURANCE MANAGEMENT ---")
        print("1. List all insurance policies")
        print("2. Back to main menu")
        
        choice = input("> ")
        if choice == "1":
            list_insurance()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

def reporting_menu():
    while True:
        print("\n--- REPORTS & ANALYTICS ---")
        print("1. Revenue Report")
        print("2. Vehicle Utilization Report")
        print("3. Back to main menu")
        
        choice = input("> ")
        if choice == "1":
            generate_revenue_report()
        elif choice == "2":
            generate_utilization_report()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()