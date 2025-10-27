import os
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS

app = Flask(__name__, static_folder='src/static')

# Configuração para produção
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configurar CORS
CORS(app, origins="*")

# Dados mockados das vagas (sem banco de dados)
MOCK_JOBS = [
    {
        "id": 1,
        "title": "Ingénieur Aérodynamique Senior",
        "location": "Toulouse",
        "department": "Ingénierie",
        "type": "CDI",
        "description": "Rejoignez notre équipe d'ingénierie aérodynamique pour développer les technologies de demain dans l'aviation commerciale.",
        "requirements": "Master en ingénierie aéronautique ou équivalent, minimum 5 ans d'expérience en aérodynamique, maîtrise des outils CFD.",
        "salary": "55,000 - 75,000 €"
    },
    {
        "id": 2,
        "title": "Technicien de Production A350",
        "location": "Toulouse",
        "department": "Production",
        "type": "CDI",
        "description": "Participez à l'assemblage final de l'A350, l'avion le plus moderne de notre flotte.",
        "requirements": "Formation technique (BTS, DUT) en aéronautique ou mécanique, expérience en assemblage industriel souhaitée.",
        "salary": "35,000 - 45,000 €"
    },
    {
        "id": 3,
        "title": "Spécialiste Cybersécurité",
        "location": "Paris",
        "department": "IT",
        "type": "CDI",
        "description": "Protégez nos systèmes critiques et développez notre stratégie de cybersécurité.",
        "requirements": "Master en cybersécurité ou informatique, certifications CISSP/CISM/CEH, expérience en SOC.",
        "salary": "60,000 - 80,000 €"
    },
    {
        "id": 4,
        "title": "Ingénieur Systèmes Satellites",
        "location": "Toulouse",
        "department": "Defence & Space",
        "type": "CDI",
        "description": "Concevez et développez les systèmes satellitaires de nouvelle génération.",
        "requirements": "Diplôme d'ingénieur en systèmes spatiaux ou électronique, 3-5 ans d'expérience dans le spatial.",
        "salary": "50,000 - 65,000 €"
    },
    {
        "id": 5,
        "title": "Responsable Qualité Helicopters",
        "location": "Marignane",
        "department": "Qualité",
        "type": "CDI",
        "description": "Assurez la qualité de nos hélicoptères civils et militaires en supervisant les processus de contrôle qualité.",
        "requirements": "Ingénieur qualité avec spécialisation aéronautique, 5+ ans d'expérience en qualité industrielle.",
        "salary": "45,000 - 60,000 €"
    },
    {
        "id": 6,
        "title": "Analyste Financier",
        "location": "Paris",
        "department": "Finance",
        "type": "CDI",
        "description": "Analysez les performances financières et supportez les décisions stratégiques de l'entreprise.",
        "requirements": "Master en finance, comptabilité ou contrôle de gestion, première expérience en analyse financière.",
        "salary": "40,000 - 50,000 €"
    },
    {
        "id": 7,
        "title": "Chef de Projet Innovation",
        "location": "Toulouse",
        "department": "R&D",
        "type": "CDI",
        "description": "Pilotez les projets d'innovation technologique et coordonnez les équipes R&D.",
        "requirements": "Ingénieur avec expérience en gestion de projet, certification PMP souhaitée.",
        "salary": "65,000 - 85,000 €"
    },
    {
        "id": 8,
        "title": "Mécanicien Maintenance Avions",
        "location": "Toulouse",
        "department": "Maintenance",
        "type": "CDI",
        "description": "Effectuez la maintenance préventive et corrective sur notre flotte d'avions d'essai.",
        "requirements": "Licence de mécanicien aéronautique (Part-66), expérience sur avions commerciaux.",
        "salary": "38,000 - 48,000 €"
    }
]

# Lista para armazenar candidaturas (em memória)
APPLICATIONS = []

@app.route('/api/jobs')
def get_jobs():
    """Retorna todas as vagas"""
    return jsonify(MOCK_JOBS)

@app.route('/api/applications', methods=['POST'])
def submit_application():
    """Recebe candidatura"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        # Adicionar ID único
        application_id = len(APPLICATIONS) + 1
        data['id'] = application_id
        data['created_at'] = "2024-08-19"
        
        APPLICATIONS.append(data)
        
        return jsonify({
            "message": "Candidatura enviada com sucesso!",
            "id": application_id
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/applications')
def get_applications():
    """Retorna todas as candidaturas (para admin)"""
    return jsonify(APPLICATIONS)

@app.route('/api/admin/stats')
def get_stats():
    """Retorna estatísticas para o dashboard admin"""
    return jsonify({
        "total_jobs": len(MOCK_JOBS),
        "total_applications": len(APPLICATIONS),
        "applications_today": len([app for app in APPLICATIONS if app.get('created_at') == "2024-08-19"]),
        "departments": ["Ingénierie", "Production", "Support", "IT", "Finance"]
    })

@app.route('/admin-rh-airbus')
def admin_page():
    """Página do painel administrativo"""
    try:
        return send_from_directory('src/static', 'admin.html')
    except FileNotFoundError:
        return "admin.html not found", 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join('src/static', path)):
        return send_from_directory('src/static', path)
    else:
        try:
            return send_from_directory('src/static', 'index.html')
        except FileNotFoundError:
            return "index.html not found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

