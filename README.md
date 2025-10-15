# Kenyan Car Rental System
A command-line interface (CLI) application for managing a car rental business in Kenya. Built with Python and SQLite for Phase 3 project requirements.

## Features
Vehicle Management: Add, list, and manage rental vehicles

Customer Management: Register and manage customers

Rental Management: Create rentals, process returns, track active rentals

Location Management: Manage multiple rental locations across Kenya

Maintenance Tracking: Track vehicle maintenance records

Insurance Management: Manage vehicle insurance policies

Reporting: Generate revenue and utilization reports

Kenyan Context
This system is tailored for the Kenyan market with:

Kenyan cities and locations (Nairobi, Mombasa, Kisumu, Nakuru)

Popular Kenyan vehicle models (Toyota Noah, Premio, Hilux, Vitz)

Kenyan license plate format

Pricing in Kenyan Shillings (KES)

Local insurance providers

## Project Structure
text
car-rental-system/
├── Pipfile
├── Pipfile.lock
├── README.md
└── lib/
    ├── cli.py              # Main CLI application
    ├── helpers.py          # Helper functions
    ├── database.py         # SQLite database setup
    ├── debug.py            # Debug and testing utilities
    └── models/
        ├── __init__.py     # Models package
        └── orm.py          # ORM operations
## Installation
Clone or download the project

bash
cd car-rental-system
Set up the virtual environment

bash
pipenv install
pipenv shell
Usage
Starting the Application
bash
python lib/cli.py
Setting Up Sample Data
bash
python lib/debug.py
Then choose option 2 to populate the database with Kenyan sample data.

## Main Menu Options
Vehicle Management - Manage rental vehicles

Customer Management - Handle customer records

Rental Management - Process rentals and returns

Maintenance Management - View maintenance records

Location Management - Manage rental locations

Insurance Management - View insurance policies

Reports & Analytics - Generate business reports

## Database Models
Vehicles: Rental cars with make, model, daily rate, availability

Customers: Client information with contact details

Rentals: Rental transactions with dates and totals

Locations: Rental branches across Kenya

Maintenance: Vehicle service records

Insurance: Vehicle insurance policies

## Technical Requirements Met
✅ CLI Application with interactive menus

✅ Object-Relational Mapping with SQLite

✅ One-to-Many Relationships (Customer→Rentals, Vehicle→Rentals, Location→Vehicles)

✅ CRUD Operations for all models

✅ Input Validation and error handling

✅ Property Methods for business logic

✅ Proper Project Structure with modular code

## Example Usage
Creating a Rental
Start the application: python lib/cli.py

Choose option 3 (Rental Management)

Select "Create new rental"

Choose a customer and available vehicle

Enter rental dates

System calculates total automatically

## Processing a Return
Go to Rental Management

Select "Process vehicle return"

Choose the rental to return

System updates status and makes vehicle available

Generating Reports
Go to Reports & Analytics

View revenue and utilization statistics

Track business performance

Development
Testing the System
bash
python lib/debug.py
Run comprehensive tests and setup sample data.

Database File
The application creates car_rental.db SQLite database automatically.

## Adding New Features
Add new functions in helpers.py

Update menu options in cli.py

Add ORM methods in models/orm.py

## License
This project was created for educational purposes as part of the Phase 3 requirements.



