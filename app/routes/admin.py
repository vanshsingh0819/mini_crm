from flask import Blueprint, session, redirect, url_for, flash, render_template, request
from functools import wraps
from app import mysql

admin_bp = Blueprint('admin', __name__)

# Admin login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash("Admin access required. Please login.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin Dashboard
@admin_bp.route('/')
@login_required
def admin_dashboard():
    username = session.get('username', 'Admin')

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    cur.close()

    return render_template(
        'admin_dashboard.html',
        username=username,
        total_users=total_users,
        total_customers=total_customers,
        total_products=total_products
    )

# Manage Users
@admin_bp.route('/users')
@login_required
def manage_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, role FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('users.html', users=users)

# View All Customers
@admin_bp.route('/customers')
@login_required
def manage_customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, phone, address FROM customers")
    customers = cur.fetchall()
    cur.close()
    return render_template('customers.html', customers=customers)

# Add Customer
@admin_bp.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)",
            (name, email, phone, address)
        )
        mysql.connection.commit()
        cur.close()

        flash("Customer added successfully.", "success")
        return redirect(url_for('admin.manage_customers'))

    return render_template('add_customer.html')

# Edit Customer
@admin_bp.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        cur.execute(
            "UPDATE customers SET name = %s, email = %s, phone = %s, address = %s WHERE id = %s",
            (name, email, phone, address, customer_id)
        )
        mysql.connection.commit()
        cur.close()

        flash("Customer updated successfully.", "success")
        return redirect(url_for('admin.manage_customers'))

    cur.execute("SELECT id, name, email, phone, address FROM customers WHERE id = %s", (customer_id,))
    customer = cur.fetchone()
    cur.close()

    if not customer:
        flash("Customer not found.", "danger")
        return redirect(url_for('admin.manage_customers'))

    return render_template('edit_customer.html', customer=customer)

# Delete Customer
@admin_bp.route('/customers/delete/<int:customer_id>', methods=['POST'])
@login_required
def delete_customer(customer_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect(url_for('admin.manage_customers'))

# Customer Details
@admin_bp.route('/customers/<int:customer_id>')
@login_required
def customer_details(customer_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, phone, address FROM customers WHERE id = %s", (customer_id,))
    customer = cur.fetchone()
    cur.close()

    if not customer:
        flash("Customer not found.", "danger")
        return redirect(url_for('admin.manage_customers'))

    return render_template('customer_details.html', customer=customer)

# Manage Products
@admin_bp.route('/products')
@login_required
def manage_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, price, description, stock_quantity FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('products.html', products=products)

# Product Details
@admin_bp.route('/products/<int:product_id>')
@login_required
def product_details(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, price, description, stock_quantity FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('admin.manage_products'))

    return render_template('product_details.html', product=product)

# Add Product
@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        stock_quantity = request.form['stock_quantity']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO products (name, price, description, stock_quantity) VALUES (%s, %s, %s, %s)",
            (name, price, description, stock_quantity)
        )
        mysql.connection.commit()
        cur.close()

        flash("Product added successfully.", "success")
        return redirect(url_for('admin.manage_products'))

    return render_template('add_product.html')

# Edit Product
@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        stock_quantity = request.form['stock_quantity']

        cur.execute(
            "UPDATE products SET name = %s, price = %s, description = %s, stock_quantity = %s WHERE id = %s",
            (name, price, description, stock_quantity, product_id)
        )
        mysql.connection.commit()
        cur.close()

        flash("Product updated successfully.", "success")
        return redirect(url_for('admin.manage_products'))

    cur.execute("SELECT id, name, price, description, stock_quantity FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('admin.manage_products'))

    return render_template('edit_product.html', product=product)

# Delete Product
@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
    mysql.connection.commit()
    cur.close()

    flash("Product deleted successfully.", "success")
    return redirect(url_for('admin.manage_products'))

# Manage Associations - List and show form
@admin_bp.route('/associations', methods=['GET'])
@login_required
def manage_associations():
    cur = mysql.connection.cursor()

    # Fetch existing associations with join to show customer and product names
    query = """
        SELECT cp.id, c.name AS customer_name, p.name AS product_name
        FROM customer_product cp
        JOIN customers c ON cp.customer_id = c.id
        JOIN products p ON cp.product_id = p.id
    """
    cur.execute(query)
    associations = cur.fetchall()

    # Fetch all customers and products for the dropdowns in the add form
    cur.execute("SELECT id, name FROM customers")
    customers = cur.fetchall()

    cur.execute("SELECT id, name FROM products")
    products = cur.fetchall()

    cur.close()

    return render_template('associations.html', associations=associations, customers=customers, products=products)

# Add new association
@admin_bp.route('/associations/add', methods=['POST'])
@login_required
def add_association():
    customer_id = request.form.get('customer_id')
    product_id = request.form.get('product_id')

    if not customer_id or not product_id:
        flash("Please select both customer and product.", "warning")
        return redirect(url_for('admin.manage_associations'))

    cur = mysql.connection.cursor()

    # Check if association already exists
    cur.execute(
        "SELECT id FROM customer_product WHERE customer_id = %s AND product_id = %s",
        (customer_id, product_id)
    )
    existing = cur.fetchone()
    if existing:
        flash("This association already exists.", "warning")
        cur.close()
        return redirect(url_for('admin.manage_associations'))

    # Insert new association
    cur.execute(
        "INSERT INTO customer_product (customer_id, product_id) VALUES (%s, %s)",
        (customer_id, product_id)
    )
    mysql.connection.commit()
    cur.close()

    flash("Association added successfully.", "success")
    return redirect(url_for('admin.manage_associations'))

# Delete association
@admin_bp.route('/associations/delete/<int:association_id>', methods=['POST'])
@login_required
def delete_association(association_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customer_product WHERE id = %s", (association_id,))
    mysql.connection.commit()
    cur.close()

    flash("Association deleted successfully.", "success")
    return redirect(url_for('admin.manage_associations'))

# Logout Route (POST method for safety)
@admin_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
