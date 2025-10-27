import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from .models.user import db
from .models.job import Job
from .models.application import Application
from .routes.user import user_bp
from .routes.job import job_bp
from .routes.application import application_bp
from .routes.admin import admin_bp

app = Flask(__name__, static_folder='static')

# Configuração para produção
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['SESSION_COOKIE_SECURE'] = False  # Allow in development
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Configurar CORS
CORS(app, origins="*", supports_credentials=True)

# Criar diretório de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(job_bp, url_prefix='/api')
app.register_blueprint(application_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/admin-rh-airbus')
def admin_page():
    """Página do painel administrativo"""
    try:
        return send_from_directory('static', 'admin.html')
    except FileNotFoundError:
        return "admin.html not found", 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join('static', path)):
        return send_from_directory('static', path)
    else:
        try:
            return send_from_directory('static', 'index.html')
        except FileNotFoundError:
            return "index.html not found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

