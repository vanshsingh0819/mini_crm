from flask import Flask, render_template
from flask_mysqldb import MySQL
from urllib.parse import urlparse
import os

mysql = MySQL()

def create_app():
    app = Flask(__name__, template_folder='templates')

    # Secret Key for sessions
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

    # ✅ Get database URL from environment variable
    db_url = os.getenv('DATABASE_URL')  # Recommended key for Render or Railway

    if db_url:
        try:
            result = urlparse(db_url)

            app.config['MYSQL_HOST'] = result.hostname
            app.config['MYSQL_USER'] = result.username
            app.config['MYSQL_PASSWORD'] = result.password
            app.config['MYSQL_DB'] = result.path.lstrip('/')
            app.config['MYSQL_PORT'] = result.port or 3306
        except Exception as e:
            raise ValueError(f"Invalid DATABASE_URL format: {e}")
    else:
        # 🔧 Local development fallback
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = '5432'
        app.config['MYSQL_DB'] = 'crm_project'
        app.config['MYSQL_PORT'] = 3306

    # 🔌 Initialize MySQL
    mysql.init_app(app)

    # 🔗 Import and register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.user import user_bp
    from app.routes.association import assoc_bp

    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(assoc_bp, url_prefix='/assoc')

    # 🌐 Home Route
    @app.route('/')
    def home():
        return render_template('welcome.html')

    return app
