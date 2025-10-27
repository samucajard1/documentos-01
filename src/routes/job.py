from flask import Blueprint, request, jsonify
from ..models.user import db
from ..models.job import Job

job_bp = Blueprint('job', __name__)

@job_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """Obter todas as vagas ativas"""
    try:
        jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
        return jsonify({
            'success': True,
            'jobs': [job.to_dict() for job in jobs]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la récupération des offres: {str(e)}'
        }), 500

@job_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Obter uma vaga específica"""
    try:
        job = Job.query.get_or_404(job_id)
        return jsonify({
            'success': True,
            'job': job.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la récupération de l\'offre: {str(e)}'
        }), 500

@job_bp.route('/jobs', methods=['POST'])
def create_job():
    """Criar nova vaga (apenas admin)"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['title', 'description', 'location', 'department', 'contract_type', 'experience_level', 'requirements']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Le champ {field} est requis'
                }), 400
        
        job = Job(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            department=data['department'],
            contract_type=data['contract_type'],
            experience_level=data['experience_level'],
            requirements=data['requirements'],
            benefits=data.get('benefits', ''),
            salary_range=data.get('salary_range', '')
        )
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Offre créée avec succès',
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la création de l\'offre: {str(e)}'
        }), 500

@job_bp.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Atualizar vaga (apenas admin)"""
    try:
        job = Job.query.get_or_404(job_id)
        data = request.get_json()
        
        # Atualizar campos
        for field in ['title', 'description', 'location', 'department', 'contract_type', 'experience_level', 'requirements', 'benefits', 'salary_range', 'is_active']:
            if field in data:
                setattr(job, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Offre mise à jour avec succès',
            'job': job.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la mise à jour de l\'offre: {str(e)}'
        }), 500

@job_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Deletar vaga (apenas admin)"""
    try:
        job = Job.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Offre supprimée avec succès'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Erreur lors de la suppression de l\'offre: {str(e)}'
        }), 500

