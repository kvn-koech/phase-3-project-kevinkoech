from models.orm import CarRentalORM
from datetime import datetime

def exit_program():
    print("Goodbye!")
    exit()

# Vehicle functions
def list_vehicles():
    vehicles = CarRentalORM.get_all('vehicles')
    for vehicle in vehicles:
        status = "Available" if vehicle['available'] else "Not Available"
        print(f"{vehicle['id']}: {vehicle['year']} {vehicle['make']} {vehicle['model']} - KES {vehicle['daily_rate']}/day - {status}")

def find_available_vehicles():
    vehicles = CarRentalORM.find_available_vehicles()
    for vehicle in vehicles:
        print(f"{vehicle['id']}: {vehicle['year']} {vehicle['make']} {vehicle['model']} - KES {vehicle['daily_rate']}/day")

def create_vehicle():
    print("Add New Vehicle:")
    make = input("Make: ")
    model = input("Model: ")
    year = int(input("Year: "))
    license_plate = input("License Plate: ")
    daily_rate = float(input("Daily Rate: "))
    color = input("Color: ")
    vehicle_type = input("Type: ")
    
    locations = CarRentalORM.get_all('locations')
    for loc in locations:
        print(f"{loc['id']}: {loc['name']}")
    
    location_id = int(input("Location ID: "))
    
    data = {
        'make': make, 'model': model, 'year': year,
        'license_plate': license_plate, 'daily_rate': daily_rate,
        'color': color, 'vehicle_type': vehicle_type,
        'location_id': location_id
    }
    
    vehicle_id = CarRentalORM.create('vehicles', data)
    print(f"Vehicle added! ID: {vehicle_id}")

def update_vehicle_status():
    list_vehicles()
    vehicle_id = int(input("Enter vehicle ID to update: "))
    new_status = input("Set as available? (y/n): ").lower()
    available = 1 if new_status == 'y' else 0
    CarRentalORM.update('vehicles', vehicle_id, {'available': available})
    print("Vehicle status updated!")

def find_vehicle_by_type():
    vehicle_type = input("Vehicle type: ")
    vehicles = CarRentalORM.find_vehicles_by_type(vehicle_type)
    for vehicle in vehicles:
        print(f"{vehicle['id']}: {vehicle['make']} {vehicle['model']} - KES {vehicle['daily_rate']}/day")

# Customer functions
def list_customers():
    customers = CarRentalORM.get_all('customers')
    for customer in customers:
        print(f"{customer['id']}: {customer['first_name']} {customer['last_name']} - {customer['email']}")

def create_customer():
    print("Add New Customer:")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    license_number = input("License: ")
    
    data = {
        'first_name': first_name, 'last_name': last_name,
        'email': email, 'phone': phone, 'license_number': license_number
    }
    
    customer_id = CarRentalORM.create('customers', data)
    print(f"Customer added! ID: {customer_id}")

def find_customer_by_email():
    email = input("Email: ")
    customer = CarRentalORM.find_customer_by_email(email)
    if customer:
        print(f"Found: {customer['first_name']} {customer['last_name']} - {customer['email']}")

# Rental functions
def list_rentals():
    rentals = CarRentalORM.get_all('rentals')
    for rental in rentals:
        customer = CarRentalORM.find_by_id('customers', rental['customer_id'])
        vehicle = CarRentalORM.find_by_id('vehicles', rental['vehicle_id'])
        if customer and vehicle:
            print(f"{rental['id']}: {customer['first_name']} - {vehicle['make']} {vehicle['model']} - {rental['status']}")

def find_active_rentals():
    rentals = CarRentalORM.find_active_rentals()
    for rental in rentals:
        print(f"{rental['id']}: {rental['first_name']} - {rental['make']} {rental['model']} - {rental['status']}")

def create_rental():
    print("Create Rental:")
    
    customers = CarRentalORM.get_all('customers')
    for customer in customers:
        print(f"{customer['id']}: {customer['first_name']} {customer['last_name']}")
    
    customer_id = int(input("Customer ID: "))
    
    vehicles = CarRentalORM.find_available_vehicles()
    for vehicle in vehicles:
        print(f"{vehicle['id']}: {vehicle['make']} {vehicle['model']} - KES {vehicle['daily_rate']}/day")
    
    vehicle_id = int(input("Vehicle ID: "))
    start_date = input("Start Date (YYYY-MM-DD): ")
    end_date = input("End Date (YYYY-MM-DD): ")
    
    vehicle = CarRentalORM.find_by_id('vehicles', vehicle_id)
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    days = (end - start).days
    total = days * vehicle['daily_rate']
    
    data = {
        'customer_id': customer_id, 'vehicle_id': vehicle_id,
        'start_date': start_date, 'end_date': end_date,
        'total_amount': total, 'status': 'active'
    }
    
    rental_id = CarRentalORM.create('rentals', data)
    print(f"Rental created! ID: {rental_id}, Total: KES {total}")

def process_return():
    rentals = CarRentalORM.find_active_rentals()
    for rental in rentals:
        print(f"{rental['id']}: {rental['first_name']} - {rental['make']} {rental['model']}")
    
    rental_id = int(input("Rental ID to return: "))
    
    CarRentalORM.update('rentals', rental_id, {
        'status': 'completed',
        'actual_return_date': datetime.now().strftime('%Y-%m-%d')
    })
    
    rental = CarRentalORM.find_by_id('rentals', rental_id)
    CarRentalORM.update('vehicles', rental['vehicle_id'], {'available': 1})
    
    print("Vehicle returned!")

# Location functions
def list_locations():
    locations = CarRentalORM.get_all('locations')
    for location in locations:
        print(f"{location['id']}: {location['name']} - {location['city']}")

def create_location():
    print("Add Location:")
    name = input("Name: ")
    address = input("Address: ")
    city = input("City: ")
    state = input("State: ")
    zip_code = input("ZIP: ")
    
    data = {
        'name': name, 'address': address,
        'city': city, 'state': state, 'zip_code': zip_code
    }
    
    location_id = CarRentalORM.create('locations', data)
    print(f"Location added! ID: {location_id}")

# Maintenance functions
def list_maintenance():
    records = CarRentalORM.get_all('maintenance_records')
    for record in records:
        vehicle = CarRentalORM.find_by_id('vehicles', record['vehicle_id'])
        if vehicle:
            print(f"{record['id']}: {vehicle['make']} {vehicle['model']} - {record['maintenance_type']}")

# Insurance functions
def list_insurance():
    policies = CarRentalORM.get_all('insurance')
    for policy in policies:
        vehicle = CarRentalORM.find_by_id('vehicles', policy['vehicle_id'])
        if vehicle:
            print(f"{policy['id']}: {vehicle['make']} {vehicle['model']} - {policy['provider']}")

# Reporting functions
def generate_revenue_report():
    data = CarRentalORM.get_revenue_report()
    if data:
        print(f"Total Revenue: KES {data['total_revenue'] or 0:,.2f}")
        print(f"Completed Rentals: {data['completed_rentals']}")

def generate_utilization_report():
    data = CarRentalORM.get_utilization_report()
    if data:
        print(f"Total Vehicles: {data['total_vehicles']}")
        print(f"Available: {data['available_vehicles']}")
        print(f"Rented: {data['rented_vehicles']}")