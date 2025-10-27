#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db, User
from src.models.job import Job
from src.models.application import Application
from src.main import app
from werkzeug.security import generate_password_hash

def populate_database():
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Criar usuário admin se não existir
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@airbus.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            print("Usuário admin criado (username: admin, password: admin123)")
        
        # Criar vagas de exemplo
        sample_jobs = [
            {
                'title': 'Ingénieur Aérodynamique Senior',
                'description': 'Rejoignez notre équipe d\'ingénierie aérodynamique pour développer les technologies de demain dans l\'aviation commerciale. Vous travaillerez sur des projets innovants incluant la conception d\'ailes, l\'optimisation des performances et la réduction de la consommation de carburant.',
                'location': 'Toulouse',
                'department': 'Ingénierie',
                'contract_type': 'CDI',
                'experience_level': 'Senior',
                'requirements': 'Master en ingénierie aéronautique ou équivalent, minimum 5 ans d\'expérience en aérodynamique, maîtrise des outils CFD (ANSYS Fluent, OpenFOAM), connaissance des normes aéronautiques.',
                'benefits': 'Salaire compétitif, participation aux bénéfices, formation continue, télétravail partiel, restaurant d\'entreprise, mutuelle premium.',
                'salary_range': '55,000 - 75,000 €'
            },
            {
                'title': 'Technicien de Production A350',
                'description': 'Participez à l\'assemblage final de l\'A350, l\'avion le plus moderne de notre flotte. Vous serez responsable du montage des systèmes, du câblage et des tests de fonctionnement dans un environnement de haute technologie.',
                'location': 'Toulouse',
                'department': 'Production',
                'contract_type': 'CDI',
                'experience_level': 'Intermédiaire',
                'requirements': 'Formation technique (BTS, DUT) en aéronautique ou mécanique, expérience en assemblage industriel souhaitée, capacité à travailler en équipe, rigueur et précision.',
                'benefits': 'Prime de production, horaires flexibles, formation interne, évolution de carrière, comité d\'entreprise actif.',
                'salary_range': '35,000 - 45,000 €'
            },
            {
                'title': 'Spécialiste Cybersécurité',
                'description': 'Protégez nos systèmes critiques et développez notre stratégie de cybersécurité. Vous serez en charge de l\'analyse des menaces, de la mise en place de solutions de sécurité et de la sensibilisation des équipes.',
                'location': 'Paris',
                'department': 'IT',
                'contract_type': 'CDI',
                'experience_level': 'Senior',
                'requirements': 'Master en cybersécurité ou informatique, certifications CISSP/CISM/CEH, expérience en SOC, connaissance des frameworks de sécurité (ISO 27001, NIST).',
                'benefits': 'Package salarial attractif, télétravail jusqu\'à 3 jours/semaine, formations certifiantes, participation aux conférences internationales.',
                'salary_range': '60,000 - 80,000 €'
            },
            {
                'title': 'Ingénieur Systèmes Satellites',
                'description': 'Concevez et développez les systèmes satellitaires de nouvelle génération pour les missions d\'observation de la Terre et de télécommunications. Vous travaillerez sur des projets spatiaux d\'envergure internationale.',
                'location': 'Toulouse',
                'department': 'Defence & Space',
                'contract_type': 'CDI',
                'experience_level': 'Intermédiaire',
                'requirements': 'Diplôme d\'ingénieur en systèmes spatiaux ou électronique, 3-5 ans d\'expérience dans le spatial, maîtrise des standards spatiaux (ECSS), anglais technique courant.',
                'benefits': 'Projets internationaux, mobilité géographique possible, formation continue, participation aux lancements, environnement high-tech.',
                'salary_range': '50,000 - 65,000 €'
            },
            {
                'title': 'Responsable Qualité Helicopters',
                'description': 'Assurez la qualité de nos hélicoptères civils et militaires en supervisant les processus de contrôle qualité, les audits et la certification. Vous garantirez la conformité aux standards aéronautiques les plus stricts.',
                'location': 'Marignane',
                'department': 'Qualité',
                'contract_type': 'CDI',
                'experience_level': 'Senior',
                'requirements': 'Ingénieur qualité avec spécialisation aéronautique, 5+ ans d\'expérience en qualité industrielle, connaissance des normes AS9100/EN9100, leadership d\'équipe.',
                'benefits': 'Management d\'équipe, responsabilités étendues, formation leadership, participation aux certifications internationales.',
                'salary_range': '45,000 - 60,000 €'
            },
            {
                'title': 'Analyste Financier',
                'description': 'Analysez les performances financières et supportez les décisions stratégiques de l\'entreprise. Vous préparerez les reportings, analyserez les coûts et participerez aux budgets prévisionnels.',
                'location': 'Paris',
                'department': 'Finance',
                'contract_type': 'CDI',
                'experience_level': 'Junior',
                'requirements': 'Master en finance, comptabilité ou contrôle de gestion, première expérience en analyse financière, maîtrise d\'Excel et des outils BI, anglais des affaires.',
                'benefits': 'Évolution rapide, formation continue, environnement international, participation aux résultats, mutuelle famille.',
                'salary_range': '40,000 - 50,000 €'
            },
            {
                'title': 'Chef de Projet Innovation',
                'description': 'Pilotez les projets d\'innovation technologique et coordonnez les équipes R&D pour développer les solutions aéronautiques du futur. Vous gérerez des projets transversaux à fort impact.',
                'location': 'Toulouse',
                'department': 'R&D',
                'contract_type': 'CDI',
                'experience_level': 'Senior',
                'requirements': 'Ingénieur avec expérience en gestion de projet, certification PMP souhaitée, expérience en innovation technologique, leadership et communication.',
                'benefits': 'Projets d\'avant-garde, équipes internationales, budget conséquent, visibilité direction, formation management.',
                'salary_range': '65,000 - 85,000 €'
            },
            {
                'title': 'Mécanicien Maintenance Avions',
                'description': 'Effectuez la maintenance préventive et corrective sur notre flotte d\'avions d\'essai et de démonstration. Vous assurerez la navigabilité et la sécurité de nos aéronefs.',
                'location': 'Toulouse',
                'department': 'Maintenance',
                'contract_type': 'CDI',
                'experience_level': 'Intermédiaire',
                'requirements': 'Licence de mécanicien aéronautique (Part-66), expérience sur avions commerciaux, habilitations électriques, travail en équipe.',
                'benefits': 'Primes de maintenance, horaires variables, formation continue, évolution vers inspecteur, environnement technique.',
                'salary_range': '38,000 - 48,000 €'
            }
        ]
        
        # Ajouter les vagas se elas não existirem
        for job_data in sample_jobs:
            existing_job = Job.query.filter_by(title=job_data['title']).first()
            if not existing_job:
                job = Job(**job_data)
                db.session.add(job)
                print(f"Vaga criada: {job_data['title']}")
        
        # Commit das mudanças
        db.session.commit()
        print("Banco de dados populado com sucesso!")
        
        # Mostrar estatísticas
        total_jobs = Job.query.count()
        total_users = User.query.count()
        print(f"Total de vagas: {total_jobs}")
        print(f"Total de usuários: {total_users}")

if __name__ == '__main__':
    populate_database()

