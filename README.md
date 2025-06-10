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
bash
Copy
Edit
mini_crm/
│
├── app/
│   ├── routes/               # Flask Blueprints (auth, user, admin)
│   ├── templates/            # HTML templates
│   └── __init__.py           # App factory + MySQL config
│
├── run.py                    # Entry point for the app
├── requirements.txt          # Python package requirements
├── README.md                 # Project documentation


🧾 License

This project is licensed under the MIT License.

Feel free to use and modify for educational or personal purposes.

🙌 Acknowledgements

Developed by Vansh Singh
Special thanks to the Flask and MySQL communities.


