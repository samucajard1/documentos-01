from src.models.user import db
from datetime import datetime

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Dados pessoais
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    citizenship = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    
    # Documentos (caminhos dos arquivos)
    document_front_path = db.Column(db.String(255), nullable=False)
    document_back_path = db.Column(db.String(255), nullable=False)
    address_proof_path = db.Column(db.String(255), nullable=False)
    
    # Metadados
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='En attente')  # En attente, Accepté, Refusé
    
    def __repr__(self):
        return f'<Application {self.first_name} {self.last_name} - Job {self.job_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'citizenship': self.citizenship,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'document_front_path': self.document_front_path,
            'document_back_path': self.document_back_path,
            'address_proof_path': self.address_proof_path,
            'job_id': self.job_id,
            'job_title': self.job.title if self.job else None,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'status': self.status
        }

