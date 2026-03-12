# 🛒 Grocery Go - E-commerce Web Application

Grocery Go is a full-featured e-commerce web application built with
Django, designed for grocery shopping with separate interfaces for
admin, end-users, and delivery personnel.

------------------------------------------------------------------------

## 🚀 Features

### 🔐 Multi-role Authentication

-   Separate login systems for:
    -   Admin
    -   End Users
    -   Delivery Personnel

### 🛠 Admin Dashboard

Admin can manage: - Products & Categories - Orders & Exchange Requests -
Users & Workers - Posters & Deliveries

### 🛍 End User Features

-   Browse products by categories
-   Shopping cart functionality
-   Order placement
-   Exchange requests

### 🚚 Delivery Management

-   Dedicated interface for delivery personnel
-   Delivery assignments
-   Delivery status updates
-   Delivery tracking

### 📱 Responsive Design

-   Mobile-friendly interface

### 🔄 Real-time Updates

-   Auto-reload functionality for live dashboard updates

------------------------------------------------------------------------

## 📋 Prerequisites

Before running the project make sure you have:

-   Python 3.8+
-   pip (Python package manager)
-   Virtual Environment (recommended)

------------------------------------------------------------------------

## 🛠 Tech Stack

### Backend

-   Django 5.0.6

### Database

-   SQLite (Development)
-   PostgreSQL (Production Ready)

### Frontend

-   HTML5
-   CSS3
-   JavaScript

### Additional Libraries

-   Pillow -- Image handling
-   python-decouple -- Environment variables
-   whitenoise -- Static files

------------------------------------------------------------------------

## 🏗 Project Structure

grocery_go/
│
├── E_mart/                     # Main Django application
│   ├── constants/              # Constant values and configurations
│   ├── migrations/             # Database migrations
│   ├── models/                 # Database models
│   ├── services/               # Business logic services
│   ├── static/                 # Static files (CSS, JS)
│   │   ├── css/
│   │   └── js/
│   │       ├── admin/
│   │       └── enduser/
│   ├── templates/              # HTML templates
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── delivery/
│   │   └── enduser/
│   ├── views/                  # View controllers
│   ├── urls.py                 # URL configurations
│   └── apps.py                 # App configuration
│
├── grocery_go/                 # Project configuration
├── manage.py                   # Django management script
└── requirements.txt            # Project dependencies

------------------------------------------------------------------------

## ⚡ Quick Start

### 1️⃣ Clone the Repository

git clone https://github.com/Subhammodak69/grocery_go.git cd grocery_go

### 2️⃣ Create Virtual Environment

python -m venv venv

Activate Environment

Windows: .`\venv`{=tex}`\Scripts`{=tex}`\activate`{=tex}

Mac/Linux: source venv/bin/activate

### 3️⃣ Install Dependencies

pip install -r requirements.txt

### 4️⃣ Setup Database

Create migrations: python manage.py makemigrations E_mart

Apply migrations: python manage.py migrate

### 5️⃣ Run Development Server

python manage.py runserver

Open in browser: http://127.0.0.1:8000

------------------------------------------------------------------------

## 🔑 Default Access

User Interface: /

Admin Dashboard: /admin-dashboard/

Delivery Portal: /delivery/

------------------------------------------------------------------------

## 📦 Dependencies

Main packages used:

-   Django 5.0.6
-   Pillow 10.3.0
-   python-decouple 3.8
-   whitenoise 6.6.0

For full list check requirements.txt

------------------------------------------------------------------------

## 🎯 Key Functionalities

### Admin Dashboard

-   Product CRUD operations
-   Category management
-   Order tracking and management
-   User and worker management
-   Exchange request handling
-   Delivery scheduling

### User Features

-   User registration and login
-   Product browsing and searching
-   Shopping cart
-   Order placement
-   Exchange requests

### Delivery Management

-   Delivery assignments
-   Status updates
-   Delivery tracking

------------------------------------------------------------------------

## 🤝 Contributing

1.  Fork the repository
2.  Create your feature branch

git checkout -b feature/AmazingFeature

3.  Commit your changes

git commit -m "Add AmazingFeature"

4.  Push to the branch

git push origin feature/AmazingFeature

5.  Open a Pull Request

------------------------------------------------------------------------

## 📝 License

This project is licensed under the MIT License.

------------------------------------------------------------------------

## 👨‍💻 Author

Subham Modak

GitHub: https://github.com/Subhammodak69

------------------------------------------------------------------------

## 🙏 Acknowledgments

-   Django Documentation
-   Bootstrap UI components
-   All contributors and testers

------------------------------------------------------------------------

## ⚠️ Production Notes

Before deploying to production:

-   Use environment variables for sensitive data
-   Configure a production database
-   Set DEBUG = False
-   Use proper static file serving
-   Implement proper security measures
