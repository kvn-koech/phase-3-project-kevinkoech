#!/usr/bin/env python3

import click
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import *
from debug import DebugHelper, debug_menu

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
    click.echo(f"Vehicle added! ID: {vehicle_id}")

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
    click.echo(f"Customer added! ID: {customer_id}")

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
        click.echo("Vehicle not found!")
        return
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    days = (end - start).days
    
    if days <= 0:
        click.echo("Invalid date range!")
        return
    
    total = days * vehicle['daily_rate']
    
    data = {
        'customer_id': customer_id, 'vehicle_id': vehicle_id,
        'start_date': start_date, 'end_date': end_date,
        'total_amount': total, 'status': 'active'
    }
    
    rental_id = CarRentalORM.create('rentals', data)
    click.echo(f"Rental created! ID: {rental_id}, Total: KES {total:,.2f}")

# Debug commands
@cli.group()
def debug():
    """Debug utilities"""
    pass

@debug.command()
def setup_data():
    """Setup Kenyan sample data"""
    DebugHelper.setup_sample_data()

@debug.command()
def test_db():
    """Test database connection"""
    DebugHelper.test_database_connection()

@debug.command()
def stats():
    """Show database statistics"""
    DebugHelper.display_database_stats()

@debug.command()
def reset():
    """Reset database (DANGEROUS)"""
    if click.confirm('⚠️  WARNING: This will delete ALL data. Are you sure?'):
        DebugHelper.reset_database()

# Interactive mode
@cli.command()
def interactive():
    """Start interactive mode"""
    from main import main
    main()

if __name__ == '__main__':
    click.echo("🇰🇪 Kenyan Car Rental System")
    cli()