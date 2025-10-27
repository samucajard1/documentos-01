import os
import uuid
import requests
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from ..models.user import db
from ..models.application import Application
from ..models.job import Job

application_bp = Blueprint('application', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, prefix):
    """Salvar arquivo com nome único"""
    if file and allowed_file(file.filename):
        # Gerar nome único
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_filename = f"{prefix}_{uuid.uuid4().hex}{ext}"
        
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        return unique_filename
    return None

@application_bp.route('/applications', methods=['POST'])
def create_application():
    """Criar nova candidatura"""
    try:
        # Verificar se a vaga existe
        job_id = request.form.get('job_id')
        if not job_id:
            return jsonify({
                'success': False,
                'message': 'ID de l\'offre requis'
            }), 400
        
        job = Job.query.get(job_id)
        if not job or not job.is_active:
            return jsonify({
                'success': False,
                'message': 'Offre non trouvée ou inactive'
            }), 404
        
        # Validar dados obrigatórios
        required_fields = ['first_name', 'last_name', 'birth_date', 'citizenship', 'email', 'phone', 'address']
        for field in required_fields:
            if not request.form.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Le champ {field} est requis'
                }), 400
        
        # Validar arquivos obrigatórios
        required_files = ['document_front', 'document_back', 'address_proof']
        for file_field in required_files:
            if file_field not in request.files:
                return jsonify({
                    'success': False,
                    'message': f'Le fichier {file_field} est requis'
                }), 400
        
        # Salvar arquivos
        document_front_filename = save_file(request.files['document_front'], 'doc_front')
        document_back_filename = save_file(request.files['document_back'], 'doc_back')
        address_proof_filename = save_file(request.files['address_proof'], 'addr_proof')
        
        if not all([document_front_filename, document_back_filename, address_proof_filename]):
            return jsonify({
                'success': False,
                'message': 'Erreur lors du téléchargement des fichiers. Formats acceptés: PNG, JPG, JPEG, PDF'
            }), 400
        
        # Converter data de nascimento
        try:
            birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Format de date de naissance invalide (YYYY-MM-DD requis)'
            }), 400
        
        # Criar candidatura
        application = Application(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            birth_date=birth_date,
            citizenship=request.form.get('citizenship'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            document_front_path=document_front_filename,
            document_back_path=document_back_filename,
            address_proof_path=address_proof_filename,
            job_id=job_id
        )
        
        db.session.add(application)
        db.session.commit()
        
        # Enviar notificação Pushcut
        try:
            pushcut_webhook = 'https://api.pushcut.io/FXvjCseOo1bOmzslKpkry/notifications/Doc%20coletado'
            notification_data = {
                'text': f'Nouvelle candidature reçue: {application.first_name} {application.last_name} pour {job.title}'
            }
            requests.post(pushcut_webhook, json=notification_data, timeout=5)
        except Exception as webhook_error:
            # Log the error but don't fail the application submission
            print(f'Erro ao enviar notificação Pushcut: {str(webhook_error)}')
        
        return jsonify({
            'success': True,
            'message': 'Candidature soumise avec succès',
            'application_id': application.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la soumission de la candidature: {str(e)}'
        }), 500

@application_bp.route('/applications', methods=['GET'])
def get_applications():
    """Obter todas as candidaturas (apenas admin)"""
    try:
        applications = Application.query.order_by(Application.applied_at.desc()).all()
        return jsonify({
            'success': True,
            'applications': [app.to_dict() for app in applications]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la récupération des candidatures: {str(e)}'
        }), 500

@application_bp.route('/applications/<int:app_id>', methods=['GET'])
def get_application(app_id):
    """Obter candidatura específica (apenas admin)"""
    try:
        application = Application.query.get_or_404(app_id)
        return jsonify({
            'success': True,
            'application': application.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la récupération de la candidature: {str(e)}'
        }), 500

@application_bp.route('/applications/<int:app_id>/status', methods=['PUT'])
def update_application_status(app_id):
    """Atualizar status da candidatura (apenas admin)"""
    try:
        application = Application.query.get_or_404(app_id)
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({
                'success': False,
                'message': 'Status requis'
            }), 400
        
        valid_statuses = ['En attente', 'Accepté', 'Refusé']
        if data['status'] not in valid_statuses:
            return jsonify({
                'success': False,
                'message': f'Status invalide. Options: {", ".join(valid_statuses)}'
            }), 400
        
        application.status = data['status']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Status mis à jour avec succès',
            'application': application.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la mise à jour du status: {str(e)}'
        }), 500

@application_bp.route('/applications/<int:app_id>/download/<file_type>', methods=['GET'])
def download_file(app_id, file_type):
    """Download de arquivos da candidatura (apenas admin)"""
    try:
        application = Application.query.get_or_404(app_id)
        
        file_mapping = {
            'document_front': application.document_front_path,
            'document_back': application.document_back_path,
            'address_proof': application.address_proof_path
        }
        
        if file_type not in file_mapping:
            return jsonify({
                'success': False,
                'message': 'Type de fichier invalide'
            }), 400
        
        filename = file_mapping[file_type]
        if not filename:
            return jsonify({
                'success': False,
                'message': 'Fichier non trouvé'
            }), 404
        
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'message': 'Fichier physique non trouvé'
            }), 404
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors du téléchargement: {str(e)}'
        }), 500

