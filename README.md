# DairyPro — Complete Dairy Management System

## Quick Start

### Requirements
- Python 3.8+
- pip

### Installation

1. Extract the project:
```bash
cd dairy_project
```

2. Install dependencies:
```bash
pip install django pillow
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create admin user (skip if using demo data):
```bash
python manage.py createsuperuser
```

5. Run the server:
```bash
python manage.py runserver
```

6. Open browser: http://127.0.0.1:8000


## Features
- ✅ Role-based login (Admin, Staff, Accountant)
- ✅ Farmer management (add/edit/delete/search)
- ✅ Milk collection recording (morning/evening shifts)
- ✅ Auto rate calculation based on fat/SNF
- ✅ Payment billing (weekly/monthly)
- ✅ Customer management
- ✅ Inventory tracking with low-stock alerts
- ✅ Daily, monthly, fat/SNF reports
- ✅ Dashboard with charts
- ✅ Profile management & password change
- ✅ Responsive design

## Rate Formula
`Rate = ₹25 + (Fat - 3.5) × ₹2.0 + (SNF - 8.5) × ₹1.5`  
Minimum: ₹15/litre

## Project Structure
```
dairy_project/
├── core/          # Auth, Dashboard, User Management, Rates
├── farmers/       # Farmer CRUD
├── milk_collection/  # Collections, Inventory
├── payments/      # Bills, Payments, Customers
├── reports/       # Daily, Monthly, Fat Reports
└── templates/     # HTML Templates
```
