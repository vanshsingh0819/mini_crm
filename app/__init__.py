from flask import Flask, render_template
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__, template_folder='templates')  # specify templates folder explicitly

    # Secret Key for sessions
    app.config['SECRET_KEY'] = 'c63ef16f23961fb9c8df40d425cb13305282748ba5fa41a0feac0447d4bf827b'

    # MySQL Configuration
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '5432'
    app.config['MYSQL_DB'] = 'crm_project'

    # Initialize MySQL
    mysql.init_app(app)

    # Import Blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.user import user_bp
    from app.routes.association import assoc_bp

    # Register Blueprints with URL prefixes
    app.register_blueprint(auth_bp, url_prefix='')          # Auth routes: /login, /register, etc.
    app.register_blueprint(admin_bp, url_prefix='/admin')   # Admin routes: /admin/...
    app.register_blueprint(user_bp, url_prefix='/user')     # User routes: /user/...
    app.register_blueprint(assoc_bp, url_prefix='/assoc')   # Association routes: /assoc/...

    # Home route
    @app.route('/')
    def home():
        return render_template('welcome.html')

    return app
