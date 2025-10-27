from src.models.user import db
from datetime import datetime

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contract_type = db.Column(db.String(50), nullable=False)  # CDI, CDD, Stage, etc.
    experience_level = db.Column(db.String(50), nullable=False)  # Junior, Senior, etc.
    requirements = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text)
    salary_range = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relacionamento com candidaturas
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Job {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'department': self.department,
            'contract_type': self.contract_type,
            'experience_level': self.experience_level,
            'requirements': self.requirements,
            'benefits': self.benefits,
            'salary_range': self.salary_range,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'applications_count': len(self.applications)
        }

