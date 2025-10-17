#!/usr/bin/env python3

import click
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import *
from debug import debug_menu

@click.group()
def cli():
    """🇰🇪 Kenyan Car Rental Management System"""
    pass

# Vehicle commands
@cli.group()
def vehicles():
    """Manage vehicles"""
    pass

@vehicles.command()
def list():
    """List all vehicles"""
    list_vehicles()

@vehicles.command()
def available():
    """List available vehicles"""
    find_available_vehicles()

@vehicles.command()
@click.option('--make', prompt=True, help='Vehicle make')
@click.option('--model', prompt=True, help='Vehicle model')
@click.option('--year', prompt=True, type=int, help='Manufacturing year')
@click.option('--license-plate', prompt=True, help='License plate')
@click.option('--daily-rate', prompt=True, type=float, help='Daily rental rate')
@click.option('--color', prompt=True, help='Vehicle color')
@click.option('--type', prompt=True, help='Vehicle type')
@click.option('--location-id', prompt=True, type=int, help='Location ID')
def add(make, model, year, license_plate, daily_rate, color, type, location_id):
    """Add a new vehicle"""
    data = {
        'make': make, 'model': model, 'year': year,
        'license_plate': license_plate, 'daily_rate': daily_rate,
        'color': color, 'vehicle_type': type, 'location_id': location_id
    }
    vehicle_id = CarRentalORM.create('vehicles', data)
    click.echo(f" Vehicle added! ID: {vehicle_id}")

# Customer commands
@cli.group()
def customers():
    """Manage customers"""
    pass

@customers.command()
def list():
    """List all customers"""
    list_customers()

@customers.command()
@click.option('--first-name', prompt=True, help='First name')
@click.option('--last-name', prompt=True, help='Last name')
@click.option('--email', prompt=True, help='Email address')
@click.option('--phone', prompt=True, help='Phone number')
@click.option('--license', prompt=True, help='License number')
def add(first_name, last_name, email, phone, license):
    """Add a new customer"""
    data = {
        'first_name': first_name, 'last_name': last_name,
        'email': email, 'phone': phone, 'license_number': license
    }
    customer_id = CarRentalORM.create('customers', data)
    click.echo(f" Customer added! ID: {customer_id}")

# Rental commands
@cli.group()
def rentals():
    """Manage rentals"""
    pass

@rentals.command()
def list():
    """List all rentals"""
    list_rentals()

@rentals.command()
def active():
    """List active rentals"""
    find_active_rentals()

@rentals.command()
@click.option('--customer-id', prompt=True, type=int, help='Customer ID')
@click.option('--vehicle-id', prompt=True, type=int, help='Vehicle ID')
@click.option('--start-date', prompt=True, help='Start date (YYYY-MM-DD)')
@click.option('--end-date', prompt=True, help='End date (YYYY-MM-DD)')
def create(customer_id, vehicle_id, start_date, end_date):
    """Create a new rental"""
    from datetime import datetime
    
    vehicle = CarRentalORM.find_by_id('vehicles', vehicle_id)
    if not vehicle:
        click.echo(" Vehicle not found!")
        return
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    days = (end - start).days
    
    if days <= 0:
        click.echo(" Invalid date range!")
        return
    
    total = days * vehicle['daily_rate']
    
    data = {
        'customer_id': customer_id, 'vehicle_id': vehicle_id,
        'start_date': start_date, 'end_date': end_date,
        'total_amount': total, 'status': 'active'
    }
    
    rental_id = CarRentalORM.create('rentals', data)
    click.echo(f" Rental created! ID: {rental_id}, Total: KES {total:,.2f}")

# Debug commands
@cli.group()
def debug():
    """Debug utilities"""
    pass

@debug.command()
def setup_data():
    """Setup Kenyan sample data"""
    from debug import DebugHelper
    DebugHelper.setup_sample_data()

@debug.command()
def test_db():
    """Test database connection"""
    from debug import DebugHelper
    DebugHelper.test_database_connection()

@debug.command()
def stats():
    """Show database statistics"""
    from debug import DebugHelper
    DebugHelper.display_database_stats()

@debug.command()
def reset():
    """Reset database (DANGEROUS)"""
    from debug import DebugHelper
    if click.confirm('  WARNING: This will delete ALL data. Are you sure?'):
        DebugHelper.reset_database()

# Interactive mode (replaces main.py functionality)
@cli.command()
def interactive():
    """Start interactive menu mode"""
    click.echo("\n" + "="*60)
    click.echo("    🇰🇪 WELCOME TO KENYAN CAR RENTAL MANAGEMENT SYSTEM")
    click.echo("="*60)
    click.echo("Starting interactive mode...")
    click.echo("Type 'debug' for debug menu or '0' to exit")
    click.echo("="*60)
    
    while True:
        show_main_menu()
        choice = click.prompt(" Select option", type=str)
        
        if choice == "0":
            exit_program()
        elif choice == "1":
            vehicle_menu_interactive()
        elif choice == "2":
            customer_menu_interactive()
        elif choice == "3":
            rental_menu_interactive()
        elif choice == "4":
            maintenance_menu_interactive()
        elif choice == "5":
            location_menu_interactive()
        elif choice == "6":
            insurance_menu_interactive()
        elif choice == "7":
            reporting_menu_interactive()
        elif choice.lower() == "debug":
            debug_menu()
        else:
            click.echo(" Invalid choice. Please try again.")

def show_main_menu():
    """Display the main menu for interactive mode"""
    click.echo("\n" + "="*50)
    click.echo("    🇰🇪 KENYAN CAR RENTAL MANAGEMENT SYSTEM")
    click.echo("="*50)
    click.echo("1.  Vehicle Management")
    click.echo("2.  Customer Management")
    click.echo("3.  Rental Management")
    click.echo("4.  Maintenance Management")
    click.echo("5.  Location Management")
    click.echo("6.   Insurance Management")
    click.echo("7.  Reports & Analytics")
    click.echo("8.  Debug Menu (type 'debug')")
    click.echo("0.  Exit Program")
    click.echo("="*50)

# Interactive submenus (moved from main.py)
def vehicle_menu_interactive():
    while True:
        click.echo("\n" + "="*40)
        click.echo(" VEHICLE MANAGEMENT")
        click.echo("="*40)
        click.echo("1. List all vehicles")
        click.echo("2. List available vehicles")
        click.echo("3. Add new vehicle")
        click.echo("4. Find vehicles by type")
        click.echo("5. Update vehicle status")
        click.echo("6. Back to main menu")
        
        choice = click.prompt(" Select option", type=str)
        
        if choice == "1":
            click.echo("\n All Vehicles:")
            list_vehicles()
        elif choice == "2":
            click.echo("\n Available Vehicles:")
            find_available_vehicles()
        elif choice == "3":
            click.echo("\n Add New Vehicle:")
            create_vehicle()
        elif choice == "4":
            click.echo("\n Find Vehicles by Type:")
            find_vehicle_by_type()
        elif choice == "5":
            click.echo("\n Update Vehicle Status:")
            update_vehicle_status()
        elif choice == "6":
            break
        else:
            click.echo(" Invalid choice. Please try again.")

def customer_menu_interactive():
    while True:
        click.echo("\n" + "="*40)
        click.echo(" CUSTOMER MANAGEMENT")
        click.echo("="*40)
        click.echo("1. List all customers")
        click.echo("2. Add new customer")
        click.echo("3. Find customer by email")
        click.echo("4. Back to main menu")
        
        choice = click.prompt(" Select option", type=str)
        
        if choice == "1":
            click.echo("\n All Customers:")
            list_customers()
        elif choice == "2":
            click.echo("\n Add New Customer:")
            create_customer()
        elif choice == "3":
            click.echo("\n Find Customer by Email:")
            find_customer_by_email()
        elif choice == "4":
            break
        else:
            click.echo(" Invalid choice. Please try again.")

def rental_menu_interactive():
    while True:
        click.echo("\n" + "="*40)
        click.echo(" RENTAL MANAGEMENT")
        click.echo("="*40)
        click.echo("1. List all rentals")
        click.echo("2. List active rentals")
        click.echo("3. Create new rental")
        click.echo("4. Process vehicle return")
        click.echo("5. Back to main menu")
        
        choice = click.prompt(" Select option", type=str)
        
        if choice == "1":
            click.echo("\n All Rentals:")
            list_rentals()
        elif choice == "2":
            click.echo("\n Active Rentals:")
            find_active_rentals()
        elif choice == "3":
            click.echo("\n Create New Rental:")
            create_rental()
        elif choice == "4":
            click.echo("\n Process Vehicle Return:")
            process_return()
        elif choice == "5":
            break
        else:
            click.echo(" Invalid choice. Please try again.")

def maintenance_menu_interactive():
    while True:
        click.echo("\n" + "="*40)
        click.echo("🔧 MAINTENANCE MANAGEMENT")
        click.echo("="*40)
        click.echo("1. List all maintenance records")
        click.echo("2. Back to main menu")
        
        choice = click.prompt(" Select option", type=str)
        
        if choice == "1":
            click.echo("\n Maintenance Records:")
            list_maintenance()
        elif choice == "2":
            break
        else:
            click.echo(" Invalid choice. Please try again.")

def location_menu_interactive():
    while True:
        click.echo("\n" + "="*40)
        click.echo(" LOCATION MANAGEMENT")
        click.echo("="*40)
        click.echo("1. List all locations")
        click.echo("2. Add new location")
        click.echo("3. Back to main menu")
        
        choice = click.prompt(" Select option", type=str)
        
        if choice == "1":
            click.echo("\n All Locations:")
            list_locations()
        elif choice == "2":
            click.echo("\n Add New Location:")
            create_location()
        elif choice == "3":
            break
        else:
            click.echo(" Invalid choice. Please try again.")

def insurance_menu_interactive():
    while True:
        click.echo("\n" + "="*40)
        click.echo("  INSURANCE MANAGEMENT")
        click.echo("="*40)
        click.echo("1. List all insurance policies")
        click.echo("2. Back to main menu")
        
        choice = click.prompt(" Select option", type=str)
        
        if choice == "1":
            click.echo("\n Insurance Policies:")
            list_insurance()
        elif choice == "2":
            break
        else:
            click.echo(" Invalid choice. Please try again.")

def reporting_menu_interactive():
    while True:
        click.echo("\n" + "="*40)
        click.echo(" REPORTS & ANALYTICS")
        click.echo("="*40)
        click.echo("1. Revenue Report")
        click.echo("2. Vehicle Utilization Report")
        click.echo("3. Back to main menu")
        
        choice = click.prompt(" Select option", type=str)
        
        if choice == "1":
            click.echo("\n Revenue Report:")
            generate_revenue_report()
        elif choice == "2":
            click.echo("\n Vehicle Utilization Report:")
            generate_utilization_report()
        elif choice == "3":
            break
        else:
            click.echo(" Invalid choice. Please try again.")

if __name__ == '__main__':
    cli()