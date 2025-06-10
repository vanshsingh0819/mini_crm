from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app import mysql
from functools import wraps
from MySQLdb.cursors import DictCursor  # For dict-style cursor

# Define the user blueprint
user_bp = Blueprint('user', __name__)

# Login required decorator for users only
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'user':
            flash("User access required. Please login.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# User dashboard route
@user_bp.route('/')
@login_required
def user_dashboard():
    username = session.get('username', 'User')
    return render_template('user_dashboard.html', username=username)

# Route to view all customers - READ ONLY
@user_bp.route('/customers')
@login_required
def view_customers():
    cur = mysql.connection.cursor(DictCursor)
    try:
        cur.execute("SELECT id, name, email, phone, address FROM customers")
        customers = cur.fetchall()
    finally:
        cur.close()
    return render_template('customers_user.html', customers=customers)

# Route to view single customer details (read-only)
@user_bp.route('/customers/<int:customer_id>')
@login_required
def customer_details(customer_id):
    cur = mysql.connection.cursor(DictCursor)
    customer = None
    try:
        cur.execute("SELECT id, name, email, phone, address FROM customers WHERE id = %s", (customer_id,))
        customer = cur.fetchone()
    finally:
        cur.close()
    if not customer:
        flash("Customer not found.", "danger")
        return redirect(url_for('user.view_customers'))
    return render_template('customers_details.html', customer=customer)

# Route to view all products - READ ONLY (no associations)
@user_bp.route('/products')
@login_required
def view_products():
    cur = mysql.connection.cursor(DictCursor)
    try:
        cur.execute("SELECT id, name, price, description, stock_quantity FROM products ORDER BY id")
        products = cur.fetchall()
    finally:
        cur.close()
    return render_template('product_user.html', products=products)

# Route to view single product details (read-only, no associated customers)
@user_bp.route('/products/<int:product_id>')
@login_required
def product_details(product_id):
    cur = mysql.connection.cursor(DictCursor)
    product = None
    try:
        cur.execute("SELECT id, name, price, description, stock_quantity FROM products WHERE id = %s", (product_id,))
        product = cur.fetchone()
    finally:
        cur.close()
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('user.view_products'))
    return render_template('products_details.html', product=product)

# Logout route (accepts GET or POST)
@user_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))
