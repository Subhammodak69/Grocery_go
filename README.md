# grocery_go
=>This is a E-commerce web application 

# git clone:
=> git clone https://github.com/Subhammodak69/grocery_go

# open and go to vscode:
=> cd grocery_go
    code .

# Made venv:
=> python -m venv venv

# Activate Scripts of venv:
=> .\venv\Scripts\Activate

# Install all requirements:
=> pip install -r requirements.txt

# Migration:
=>python manage.py makemigrations E_mart
    =>python manage.py migrate

# Runserver:
=> python manage.py runserver

# App File Structure:
"""
    => 📦E_mart
        ┣ 📂constants
        ┣ 📂migrations
        ┣ 📂models
        ┣ 📂services
        ┣ 📂static
        ┃ ┣ 📂css
        ┃ ┃ ┣ 📂admin
        ┃ ┃ ┣ 📂enduser
        ┃ ┃ ┗ 📜login.css
        ┃ ┣ 📂js
        ┃ ┃ ┣ 📂admin
        ┃ ┃ ┃ ┣ 📂category
        ┃ ┃ ┃ ┣ 📂delivery_or_pickup
        ┃ ┃ ┃ ┣ 📂exchange_request
        ┃ ┃ ┃ ┣ 📂order
        ┃ ┃ ┃ ┣ 📂poster
        ┃ ┃ ┃ ┣ 📂product
        ┃ ┃ ┃ ┣ 📂user
        ┃ ┃ ┃ ┣ 📂worker
        ┃ ┃ ┃ ┣ 📜admin_base.js
        ┃ ┃ ┃ ┣ 📜admin_login.js
        ┃ ┃ ┃ ┗ 📜home.js
        ┃ ┃ ┣ 📂enduser
        ┃ ┃ ┣ 📜active-nav.js
        ┃ ┃ ┣ 📜auto_reload.js
        ┃ ┃ ┣ 📜base.js
        ┃ ┃ ┣ 📜error_or_success.js
        ┃ ┃ ┣ 📜login.js
        ┃ ┃ ┣ 📜logout.js
        ┃ ┃ ┗ 📜signup.js
        ┣ 📂templates
        ┃ ┣ 📂admin
        ┃ ┃ ┣ 📂category
        ┃ ┃ ┣ 📂delivery_or_pickup
        ┃ ┃ ┣ 📂exchange_request
        ┃ ┃ ┣ 📂order
        ┃ ┃ ┣ 📂poster
        ┃ ┃ ┣ 📂product
        ┃ ┃ ┣ 📂user
        ┃ ┃ ┣ 📂worker
        ┃ ┃ ┣ 📜dashboard.html
        ┃ ┃ ┗ 📜home.html
        ┃ ┣ 📂auth
        ┃ ┣ 📂delivery
        ┃ ┗ 📂enduser
        ┣ 📂views
        ┣ 📜apps.py
        ┣ 📜urls.py
        ┗ 📜__init__.py

"""