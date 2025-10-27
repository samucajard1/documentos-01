import os
from datetime import datetime
from flask import Flask, send_from_directory, jsonify, request, session
from flask_cors import CORS

# Criar aplicação Flask
app = Flask(__name__, static_folder='src/static')

# Configuração para produção
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configurar CORS
CORS(app, origins="*")

# Dados mockados das vagas (em memória)
MOCK_JOBS = [
    {
        "id": 1,
        "title": "Ingénieur Aérodynamique Senior",
        "location": "Toulouse",
        "department": "Ingénierie",
        "type": "CDI",
        "description": "Rejoignez notre équipe d'ingénierie aérodynamique pour développer les technologies de demain dans l'aviation commerciale. Vous travaillerez sur des projets innovants incluant la conception d'ailes, l'optimisation des performances et la réduction de la consommation de carburant.",
        "requirements": "Master en ingénierie aéronautique ou équivalent, minimum 5 ans d'expérience en aérodynamique, maîtrise des outils CFD (ANSYS Fluent, OpenFOAM), connaissance des normes aéronautiques.",
        "salary": "55,000 - 75,000 €"
    },
    {
        "id": 2,
        "title": "Technicien de Production A350",
        "location": "Toulouse",
        "department": "Production",
        "type": "CDI",
        "description": "Participez à l'assemblage final de l'A350, l'avion le plus moderne de notre flotte. Vous serez responsable du montage des systèmes, du câblage et des tests de fonctionnement dans un environnement de haute technologie.",
        "requirements": "Formation technique (BTS, DUT) en aéronautique ou mécanique, expérience en assemblage industriel souhaitée, capacité à travailler en équipe, rigueur et précision.",
        "salary": "35,000 - 45,000 €"
    },
    {
        "id": 3,
        "title": "Spécialiste Cybersécurité",
        "location": "Paris",
        "department": "IT",
        "type": "CDI",
        "description": "Protégez nos systèmes critiques et développez notre stratégie de cybersécurité. Vous serez en charge de l'analyse des menaces, de la mise en place de solutions de sécurité et de la sensibilisation des équipes.",
        "requirements": "Master en cybersécurité ou informatique, certifications CISSP/CISM/CEH, expérience en SOC, connaissance des frameworks de sécurité (ISO 27001, NIST).",
        "salary": "60,000 - 80,000 €"
    },
    {
        "id": 4,
        "title": "Ingénieur Systèmes Satellites",
        "location": "Toulouse",
        "department": "Defence & Space",
        "type": "CDI",
        "description": "Concevez et développez les systèmes satellitaires de nouvelle génération pour les missions d'observation de la Terre et de télécommunications. Vous travaillerez sur des projets spatiaux d'envergure internationale.",
        "requirements": "Diplôme d'ingénieur en systèmes spatiaux ou électronique, 3-5 ans d'expérience dans le spatial, maîtrise des standards spatiaux (ECSS), anglais technique courant.",
        "salary": "50,000 - 65,000 €"
    },
    {
        "id": 5,
        "title": "Responsable Qualité Helicopters",
        "location": "Marignane",
        "department": "Qualité",
        "type": "CDI",
        "description": "Assurez la qualité de nos hélicoptères civils et militaires en supervisant les processus de contrôle qualité, les audits et la certification. Vous garantirez la conformité aux standards aéronautiques les plus stricts.",
        "requirements": "Ingénieur qualité avec spécialisation aéronautique, 5+ ans d'expérience en qualité industrielle, connaissance des normes AS9100/EN9100, leadership d'équipe.",
        "salary": "45,000 - 60,000 €"
    },
    {
        "id": 6,
        "title": "Analyste Financier",
        "location": "Paris",
        "department": "Finance",
        "type": "CDI",
        "description": "Analysez les performances financières et supportez les décisions stratégiques de l'entreprise. Vous préparerez les reportings, analyserez les coûts et participerez aux budgets prévisionnels.",
        "requirements": "Master en finance, comptabilité ou contrôle de gestion, première expérience en analyse financière, maîtrise d'Excel et des outils BI, anglais des affaires.",
        "salary": "40,000 - 50,000 €"
    },
    {
        "id": 7,
        "title": "Chef de Projet Innovation",
        "location": "Toulouse",
        "department": "R&D",
        "type": "CDI",
        "description": "Pilotez les projets d'innovation technologique et coordonnez les équipes R&D pour développer les solutions aéronautiques du futur. Vous gérerez des projets transversaux à fort impact.",
        "requirements": "Ingénieur avec expérience en gestion de projet, certification PMP souhaitée, expérience en innovation technologique, leadership et communication.",
        "salary": "65,000 - 85,000 €"
    },
    {
        "id": 8,
        "title": "Mécanicien Maintenance Avions",
        "location": "Toulouse",
        "department": "Maintenance",
        "type": "CDI",
        "description": "Effectuez la maintenance préventive et corrective sur notre flotte d'avions d'essai et de démonstration. Vous assurerez la navigabilité et la sécurité de nos aéronefs.",
        "requirements": "Licence de mécanicien aéronautique (Part-66), expérience sur avions commerciaux, habilitations électriques, travail en équipe.",
        "salary": "38,000 - 48,000 €"
    }
]

# Lista de candidaturas (em memória)
APPLICATIONS = []

# Credenciais do admin
ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123'
}

@app.route('/')
def index():
    """Página principal"""
    return send_from_directory('src/static', 'index.html')

@app.route('/api/jobs')
def get_jobs():
    """Retorna todas as vagas disponíveis"""
    return jsonify(MOCK_JOBS)

@app.route('/api/applications', methods=['POST'])
def submit_application():
    """Recebe candidatura com upload de arquivos"""
    try:
        # Verificar se é upload de arquivos ou JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Upload com arquivos
            data = request.form.to_dict()
            files = request.files
            
            # Validar campos obrigatórios
            required_fields = ['firstName', 'lastName', 'email', 'phone']
            for field in required_fields:
                if not data.get(field) or str(data.get(field)).strip() == '':
                    return jsonify({"error": f"Le champ {field} est requis"}), 400
            
            # Criar diretório de uploads se não existir
            upload_dir = os.path.join('src', 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Processar arquivos enviados
            file_paths = {}
            file_fields = ['document_front', 'document_back', 'address_proof']
            
            for field in file_fields:
                if field in files and files[field].filename:
                    file = files[field]
                    # Gerar nome único para o arquivo
                    filename = f"{len(APPLICATIONS) + 1}_{field}_{file.filename}"
                    file_path = os.path.join(upload_dir, filename)
                    file.save(file_path)
                    file_paths[field] = filename
            
            # Criar candidatura
            application_id = len(APPLICATIONS) + 1
            application_data = {
                'id': application_id,
                'first_name': data.get('firstName'),
                'last_name': data.get('lastName'),
                'birth_date': data.get('birth_date', 'N/A'),
                'citizenship': data.get('citizenship', 'undefined'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'address': data.get('address', 'undefined'),
                'job_title': data.get('job_title', 'undefined'),
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'Nova',
                'files': file_paths
            }
            
            APPLICATIONS.append(application_data)
            
            return jsonify({
                "success": True,
                "message": "Candidatura enviada com sucesso!",
                "id": application_id
            }), 201
            
        else:
            # JSON simples (para testes)
            data = request.get_json()
            
            # Validar campos obrigatórios
            required_fields = [
                ('firstName', 'first_name', 'Prénom'),
                ('lastName', 'last_name', 'Nom'),
                ('email', 'email', 'Email'),
                ('phone', 'phone', 'Téléphone')
            ]
            
            for field1, field2, label in required_fields:
                value = data.get(field1) or data.get(field2)
                if not value or str(value).strip() == '':
                    return jsonify({"error": f"Le champ {label} est requis"}), 400
            
            # Normalizar nomes dos campos
            normalized_data = {}
            for key, value in data.items():
                if key == 'firstName':
                    normalized_data['first_name'] = value
                elif key == 'lastName':
                    normalized_data['last_name'] = value
                else:
                    normalized_data[key] = value
            
            # Adicionar ID único e timestamp
            application_id = len(APPLICATIONS) + 1
            normalized_data['id'] = application_id
            normalized_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            normalized_data['status'] = "Nova"
            normalized_data['files'] = {}
            
            APPLICATIONS.append(normalized_data)
            
            return jsonify({
                "success": True,
                "message": "Candidatura enviada com sucesso!",
                "id": application_id
            }), 201
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Login do admin"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
            session['admin_logged_in'] = True
            return jsonify({
                "success": True,
                "message": "Login realizado com sucesso!"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Credenciais inválidas"
            }), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/applications')
def get_applications():
    """Retorna todas as candidaturas (para admin)"""
    return jsonify(APPLICATIONS)

@app.route('/api/applications/<int:application_id>')
def get_application(application_id):
    """Retorna uma candidatura específica pelo ID"""
    try:
        # Buscar candidatura pelo ID
        application = None
        for app in APPLICATIONS:
            if app.get('id') == application_id:
                application = app
                break
        
        if application:
            return jsonify({
                "success": True,
                "application": application
            })
        else:
            return jsonify({
                "success": False,
                "message": "Candidatura não encontrada"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/api/admin/stats')
def get_stats():
    """Retorna estatísticas para o dashboard admin"""
    today = datetime.now().strftime("%Y-%m-%d")
    applications_today = len([app for app in APPLICATIONS if today in app.get('created_at', '')])
    
    return jsonify({
        "total_jobs": len(MOCK_JOBS),
        "total_applications": len(APPLICATIONS),
        "applications_today": applications_today,
        "departments": ["Ingénierie", "Production", "Support", "IT", "Finance"]
    })

@app.route('/api/download/<int:application_id>/<file_type>')
def download_file(application_id, file_type):
    """Download de arquivos das candidaturas"""
    try:
        # Buscar candidatura
        application = None
        for app in APPLICATIONS:
            if app.get('id') == application_id:
                application = app
                break
        
        if not application:
            return jsonify({"error": "Candidatura não encontrada"}), 404
        
        # Verificar se o arquivo existe
        files = application.get('files', {})
        if file_type not in files:
            return jsonify({"error": "Arquivo não encontrado"}), 404
        
        filename = files[file_type]
        upload_dir = os.path.join('src', 'static', 'uploads')
        
        return send_from_directory(upload_dir, filename, as_attachment=True)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin-rh-airbus')
def admin_page():
    """Página do painel administrativo"""
    try:
        return send_from_directory('src/static', 'admin.html')
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin - Airbus Careers</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .admin { color: blue; font-size: 24px; }
            </style>
        </head>
        <body>
            <h1 class="admin">🔐 Painel Admin Airbus</h1>
            <p>Login: admin / admin123</p>
            <a href="/">Voltar ao Site</a>
        </body>
        </html>
        """

# Para Railway - usar variável de ambiente PORT com fallback robusto
if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 8080))
    except (ValueError, TypeError):
        port = 8080
    
    print("🚀 Iniciando Airbus Careers")
    print(f"📊 {len(MOCK_JOBS)} vagas carregadas")
    print("🔐 Admin: admin / admin123")
    print(f"🌐 Porta: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

