# Mini CRM

A lightweight Customer Relationship Management (CRM) system built using Flask and MySQL.  
It supports user authentication, role-based dashboards, and management of customers, products, and associations.

## 🚀 Features
- User & Admin login system
- Manage customers and products (CRUD)
- Link customers to products
- Role-based dashboards
- MySQL database integration
- Responsive UI with HTML templates

## ⚙️ Technologies Used
- Python (Flask)
- MySQL
- Jinja2 Templates
- HTML/CSS

## 📦 Setup Instructions
1. Clone this repo:
   ```bash
   git clone https://github.com/vanshsingh0819/mini_crm.git
   cd mini_crm

##Create and activate a virtual environment:

Windows:

 ```bash
  python -m venv venv
  venv\Scripts\activate
```
macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```


## Install project dependencies:

```bash
pip install -r requirements.txt
```

## Set up your MySQL database:

Create a database named mini_crm

Update database config in app/__init__.py with your:

host

user

password

database


##Run the Flask application:

```bash
python run.py
```

## Open in your browser:

```bash
http://localhost:5000
```

🛠 Technologies Used
Python 3

Flask

MySQL

Flask-MySQLdb

Jinja2 Templates

HTML/CSS

📁 Project Structure
crm_project/ 
│ ── app                                                      (folder) 
│             ├── __init__.py                      
│             ├── routes                                 (folder)                       
│              │            ├── auth.py              
│              │            ├── admin.py              
│              │            ├── user.py                
│              │            ├── association.py  
│              │            └──_ init__.py 
│              ├── templates                        (folder)  
│              │            ├── login.html 
│              │            ├── register.html 
│              │            ├── admin_dashboard.html 
│              │            ├── user_dashboard.html 
│              │            ├── customers.html 
│              │            ├── products.html 
│              │            ├── customer_details.html  
│              │            ├── product_details.html    
│              │            ├── associations.html     
│              │            ├── users.html 
│              │            ├── add_customer.html 
│              │            ├── add_product.html 
│              │            ├── welcome.html 
│              │            ├── product_user.html          
│              │            ├── customer_details.html  
│              │            ├── customers_details.html  
│              │            ├── customers_user.html 
│              │            ├── edit_ customer.html 
│              │            └── edit_ product.html 
├── .gitignore 
├── README.md 
├── requirement.txt 
├── run.py 
├── test_db.py 
└── wsgi.py 


🧾 License

This project is licensed under the MIT License.

Feel free to use and modify for educational or personal purposes.

🙌 Acknowledgements

Developed by Vansh Singh
Special thanks to the Flask and MySQL communities.


