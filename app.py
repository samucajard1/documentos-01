import os
import sqlite3
from datetime import datetime
from flask import Flask, send_from_directory, jsonify, request, session
from flask_cors import CORS

# Criar aplicação Flask
app = Flask(__name__, static_folder='src/static')
app.config['SECRET_KEY'] = 'airbus-secret-key-2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configurar CORS
CORS(app, origins="*")

# Configurar banco de dados
DATABASE_PATH = os.path.join('src', 'database', 'applications.db')

def init_database():
    """Inicializar banco de dados SQLite"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Criar tabela de candidaturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            birth_date TEXT,
            citizenship TEXT,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            job_title TEXT,
            created_at TEXT NOT NULL,
            status TEXT DEFAULT 'Nova',
            document_front TEXT,
            document_back TEXT,
            address_proof TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Obter conexão com banco de dados"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Dados das vagas
MOCK_JOBS = [
    {
        "id": 1,
        "title": "Ingénieur Aérodynamique Senior",
        "location": "Toulouse",
        "department": "Ingénierie",
        "type": "CDI",
        "description": "Rejoignez notre équipe d'ingénierie aérodynamique pour développer les technologies de demain dans l'aviation commerciale.",
        "requirements": "Master en ingénierie aéronautique ou équivalent, minimum 5 ans d'expérience en aérodynamique.",
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
        "description": "Assurez la qualité de nos hélicoptères civils et militaires.",
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
        "description": "Effectuez la maintenance préventive et corrective sur notre flotte d'avions.",
        "requirements": "Licence de mécanicien aéronautique (Part-66), expérience sur avions commerciaux.",
        "salary": "38,000 - 48,000 €"
    }
]

# Lista de candidaturas - REMOVIDA (agora usa banco de dados)

# Inicializar banco de dados na inicialização
init_database()

@app.route('/')
def index():
    return send_from_directory('src/static', 'index.html')

@app.route('/api/jobs')
def get_jobs():
    return jsonify(MOCK_JOBS)

@app.route('/api/applications', methods=['POST'])
def submit_application():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if request.content_type and 'multipart/form-data' in request.content_type:
            data = request.form.to_dict()
            files = request.files
            
            # Validar campos obrigatórios - aceitar ambos os formatos
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
            
            upload_dir = os.path.join('src', 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            file_paths = {}
            file_fields = ['document_front', 'document_back', 'address_proof']
            
            for field in file_fields:
                if field in files and files[field].filename:
                    file = files[field]
                    # Gerar nome único baseado em timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{timestamp}_{field}_{file.filename}"
                    file_path = os.path.join(upload_dir, filename)
                    file.save(file_path)
                    file_paths[field] = filename
            
            # Inserir no banco de dados
            cursor.execute('''
                INSERT INTO applications (
                    first_name, last_name, birth_date, citizenship, email, 
                    document_front, document_back, address_proof
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('firstName') or data.get('first_name'),
                data.get('lastName') or data.get('last_name'),
                data.get('birth_date', 'N/A'),
                data.get('citizenship', 'undefined'),
                data.get('email'),
                data.get('phone'),
                data.get('address', 'undefined'),
                data.get('job_title', 'undefined'),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Nova',
                file_paths.get('document_front'),
                file_paths.get('document_back'),
                file_paths.get('address_proof')
            ))
            
            application_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return jsonify({
                "success": True,
                "message": "Candidatura enviada com sucesso!",
                "id": application_id
            }), 201
            
        else:
            data = request.get_json()
            
            required_fields = [
                ('firstName', 'first_name', 'Prénom'),
                ('lastName', 'last_name', 'Nom'),
                ('email', 'email', 'Email'),
                ('phone', 'phone', 'Téléphone')
            ]
            
            for field1, field2, label in required_fields:
                value = data.get(field1) or data.get(field2)
                if not value:
                    return jsonify({"error": f"Le champ {label} est requis"}), 400
            
            # Inserir no banco de dados
            cursor.execute('''
                INSERT INTO applications (
                    first_name, last_name, birth_date, citizenship, email, 
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('firstName') or data.get('first_name'),
                data.get('lastName') or data.get('last_name'),
                data.get('birth_date', 'N/A'),
                data.get('citizenship', 'undefined'),
                data.get('email'),
                data.get('phone'),
                data.get('address', 'undefined'),
                data.get('job_title', 'undefined'),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Nova'
            ))
            
            application_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return jsonify({
                "success": True,
                "message": "Candidatura enviada com sucesso!",
                "id": application_id
            }), 201
            
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username == 'admin' and password == 'admin123':
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, first_name, last_name, birth_date, citizenship, email, 
                   document_front, document_back, address_proof
            FROM applications 
            ORDER BY created_at DESC
        ''')
        
        applications = []
        for row in cursor.fetchall():
            app_data = {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'birth_date': row['birth_date'],
                'citizenship': row['citizenship'],
                'email': row['email'],
                'phone': row['phone'],
                'address': row['address'],
                'job_title': row['job_title'],
                'created_at': row['created_at'],
                'status': row['status'],
                'files': {
                    'document_front': row['document_front'],
                    'document_back': row['document_back'],
                    'address_proof': row['address_proof']
                }
            }
            applications.append(app_data)
        
        conn.close()
        return jsonify(applications)
        
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/api/applications/<int:application_id>')
def get_application(application_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, first_name, last_name, birth_date, citizenship, email, 
                   document_front, document_back, address_proof
            FROM applications 
            WHERE id = ?
        ''', (application_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            application = {
                'id': row['id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'birth_date': row['birth_date'],
                'citizenship': row['citizenship'],
                'email': row['email'],
                'phone': row['phone'],
                'address': row['address'],
                'job_title': row['job_title'],
                'created_at': row['created_at'],
                'status': row['status'],
                'files': {
                    'document_front': row['document_front'],
                    'document_back': row['document_back'],
                    'address_proof': row['address_proof']
                }
            }
            
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
        if 'conn' in locals():
            conn.close()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/api/admin/stats')
def get_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total de candidaturas
        cursor.execute('SELECT COUNT(*) as total FROM applications')
        total_applications = cursor.fetchone()['total']
        
        # Candidaturas de hoje
        today = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('SELECT COUNT(*) as today FROM applications WHERE DATE(created_at) = ?', (today,))
        applications_today = cursor.fetchone()['today']
        
        conn.close()
        
        return jsonify({
            "total_jobs": len(MOCK_JOBS),
            "total_applications": total_applications,
            "applications_today": applications_today,
            "departments": ["Ingénierie", "Production", "Support", "IT", "Finance"]
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<int:application_id>/<file_type>')
def download_file(application_id, file_type):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT document_front, document_back, address_proof
            FROM applications 
            WHERE id = ?
        ''', (application_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({"error": "Candidatura não encontrada"}), 404
        
        file_mapping = {
            'document_front': row['document_front'],
            'document_back': row['document_back'],
            'address_proof': row['address_proof']
        }
        
        if file_type not in file_mapping:
            return jsonify({"error": "Tipo de arquivo inválido"}), 400
        
        filename = file_mapping[file_type]
        if not filename:
            return jsonify({"error": "Arquivo não encontrado"}), 404
        
        upload_dir = os.path.join('src', 'static', 'uploads')
        file_path = os.path.join(upload_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({"error": "Arquivo físico não encontrado"}), 404
        
        return send_from_directory(upload_dir, filename, as_attachment=True)
        
    except Exception as e:
        if 'conn' in locals():
            conn.close()
        return jsonify({"error": str(e)}), 500

@app.route('/admin-rh-airbus')
def admin_page():
    return send_from_directory('src/static', 'admin.html')

@app.route('/api/admin/check-auth')
def check_auth():
    return jsonify({"authenticated": session.get('admin_logged_in', False)})

@app.route('/api/admin/dashboard')
def admin_dashboard():
    return jsonify({"message": "Dashboard carregado"})

# Servir arquivos estáticos
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('src/static', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

