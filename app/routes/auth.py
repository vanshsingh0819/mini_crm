from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql
import re

auth_bp = Blueprint('auth', __name__)

def is_valid_email(email):
    """Validate email format using regex."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Check if all fields are filled
        if not username or not email or not password or not role:
            flash('All fields are required!', 'danger')
            return redirect(url_for('auth.register'))

        # Validate email format
        if not is_valid_email(email):
            flash('Invalid email format!', 'danger')
            return redirect(url_for('auth.register'))

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
            existing_user = cur.fetchone()

            if existing_user:
                flash('Username or Email already exists!', 'danger')
                return redirect(url_for('auth.register'))

            hashed_password = generate_password_hash(password)

            cur.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_password, role)
            )
            mysql.connection.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if both fields are filled
        if not username or not password:
            flash('Username and password are required!', 'danger')
            return redirect(url_for('auth.login'))

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT id, username, password_hash, role FROM users WHERE username=%s", (username,))
            user = cur.fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            flash(f'Welcome back, {user[1]}!', 'success')

            if user[3] == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('user.user_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

# Logout only via POST for security
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
