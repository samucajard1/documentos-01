import os
import sys
from werkzeug.security import generate_password_hash
from src.main import app
from src.models.user import db, User

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_admin():
    with app.app_context():
        # Verificar se já existe admin
        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            print(f"Admin já existe: {existing_admin.username}")
            return
        
        # Criar admin com as credenciais fornecidas
        admin = User(
            username='Admin2025',
            email='admin@airbus-careers.fr',
            password_hash=generate_password_hash('#AdminLasanha'),
            is_admin=True
        )
        
        db.session.add(admin)
        db.session.commit()
        print(f"Admin criado com sucesso: {admin.username}")

if __name__ == '__main__':
    init_admin()
