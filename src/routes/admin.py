from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import db, User
from ..models.application import Application
from ..models.job import Job

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Login do administrador"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Nom d\'utilisateur et mot de passe requis'
            }), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.is_admin or not check_password_hash(user.password_hash, password):
            return jsonify({
                'success': False,
                'message': 'Identifiants invalides'
            }), 401
        
        session['admin_id'] = user.id
        session['is_admin'] = True
        
        return jsonify({
            'success': True,
            'message': 'Connexion réussie',
            'user': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la connexion: {str(e)}'
        }), 500

@admin_bp.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Logout do administrador"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Déconnexion réussie'
    })

@admin_bp.route('/admin/check-auth', methods=['GET'])
def check_admin_auth():
    """Verificar se o usuário está autenticado como admin"""
    if session.get('is_admin'):
        user = User.query.get(session.get('admin_id'))
        if user and user.is_admin:
            return jsonify({
                'success': True,
                'authenticated': True,
                'user': user.to_dict()
            })
    
    return jsonify({
        'success': True,
        'authenticated': False
    })

@admin_bp.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    """Dashboard com estatísticas"""
    try:
        if not session.get('is_admin'):
            return jsonify({
                'success': False,
                'message': 'Accès non autorisé'
            }), 401
        
        # Estatísticas
        total_jobs = Job.query.count()
        active_jobs = Job.query.filter_by(is_active=True).count()
        total_applications = Application.query.count()
        pending_applications = Application.query.filter_by(status='En attente').count()
        
        # Candidaturas recentes
        recent_applications = Application.query.order_by(Application.applied_at.desc()).limit(10).all()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_jobs': total_jobs,
                'active_jobs': active_jobs,
                'total_applications': total_applications,
                'pending_applications': pending_applications
            },
            'recent_applications': [app.to_dict() for app in recent_applications]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors du chargement du dashboard: {str(e)}'
        }), 500

@admin_bp.route('/admin/create-admin', methods=['POST'])
def create_admin():
    """Criar usuário administrador (apenas para setup inicial)"""
    try:
        # Verificar se já existe admin
        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            return jsonify({
                'success': False,
                'message': 'Un administrateur existe déjà'
            }), 400
        
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({
                'success': False,
                'message': 'Tous les champs sont requis'
            }), 400
        
        # Verificar se usuário já existe
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': 'Nom d\'utilisateur déjà utilisé'
            }), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'message': 'Email déjà utilisé'
            }), 400
        
        # Criar admin
        admin = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Administrateur créé avec succès',
            'user': admin.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la création de l\'administrateur: {str(e)}'
        }), 500

