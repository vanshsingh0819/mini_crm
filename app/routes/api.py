from flask import Blueprint, request, jsonify, Response
import xmltodict
import dicttoxml
import os
from app import mysql

api_bp = Blueprint('api', __name__)

API_KEY = os.getenv("API_KEY")

# Middleware for API key check
@api_bp.before_request
def check_api_key():
    key = request.headers.get('x-api-key')
    if key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401

# Helper function to return XML or JSON

def respond(data, status=200):
    if request.headers.get("Accept") == "application/xml":
        xml = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
        return Response(xml, mimetype="application/xml", status=status)
    return jsonify(data), status

# ------------------------------------
# GET /api/customers - All customers
# ------------------------------------
@api_bp.route('/customers', methods=['GET'])
def get_customers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email FROM customers")
    rows = cur.fetchall()
    cur.close()
    customers = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
    return respond(customers)

# ------------------------------------
# GET /api/customers/<id> - Single customer
# ------------------------------------
@api_bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email FROM customers WHERE id = %s", (id,))
    row = cur.fetchone()
    cur.close()
    if row:
        return respond({"id": row[0], "name": row[1], "email": row[2]})
    else:
        return respond({"error": "Customer not found"}, status=404)

# ------------------------------------
# POST /api/customers - Create customer (JSON)
# ------------------------------------
@api_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()
    return respond({"message": "Customer added", "name": name, "email": email}, status=201)

# ------------------------------------
# POST /api/customers/xml - Create customer (XML)
# ------------------------------------
@api_bp.route('/customers/xml', methods=['POST'])
def create_customer_xml():
    data = xmltodict.parse(request.data)
    name = data['customer'].get('name')
    email = data['customer'].get('email')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()
    return respond({"message": "XML customer added", "name": name, "email": email}, status=201)

# ------------------------------------
# PUT /api/customers/<id> - Update customer (JSON)
# ------------------------------------
@api_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    cur = mysql.connection.cursor()
    cur.execute("UPDATE customers SET name=%s, email=%s WHERE id=%s", (name, email, id))
    mysql.connection.commit()
    cur.close()
    return respond({"message": "Customer updated", "id": id, "name": name, "email": email})

# ------------------------------------
# PUT /api/customers/<id>/xml - Update customer (XML)
# ------------------------------------
@api_bp.route('/customers/<int:id>/xml', methods=['PUT'])
def update_customer_xml(id):
    data = xmltodict.parse(request.data)
    name = data['customer'].get('name')
    email = data['customer'].get('email')
    cur = mysql.connection.cursor()
    cur.execute("UPDATE customers SET name=%s, email=%s WHERE id=%s", (name, email, id))
    mysql.connection.commit()
    cur.close()
    return respond({"message": "XML customer updated", "id": id, "name": name, "email": email})

# ------------------------------------
# DELETE /api/customers/<id> - Delete customer
# ------------------------------------
@api_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customers WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return respond({"message": "Customer deleted", "id": id})