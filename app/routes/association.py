from flask import Blueprint, render_template, flash
from app import mysql

assoc_bp = Blueprint('assoc', __name__)

@assoc_bp.route('/customer/<int:customer_id>/products')
def view_customer_products(customer_id):
    cur = mysql.connection.cursor()
    query = """
        SELECT p.id, p.name, p.price, p.description
        FROM products p
        JOIN customer_product cp ON p.id = cp.product_id
        WHERE cp.customer_id = %s
    """
    cur.execute(query, (customer_id,))
    products = cur.fetchall()
    cur.close()

    if not products:
        flash("No products found for this customer.", "info")

    return render_template('customer_products.html', products=products, customer_id=customer_id)

@assoc_bp.route('/product/<int:product_id>/customers')
def view_product_customers(product_id):
    cur = mysql.connection.cursor()
    query = """
        SELECT c.id, c.name, c.email, c.phone
        FROM customers c
        JOIN customer_product cp ON c.id = cp.customer_id
        WHERE cp.product_id = %s
    """
    cur.execute(query, (product_id,))
    customers = cur.fetchall()
    cur.close()

    if not customers:
        flash("No customers found for this product.", "info")

    return render_template('product_customers.html', customers=customers, product_id=product_id)
