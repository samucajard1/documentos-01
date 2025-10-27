import os
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder='src/static')

@app.route('/')
def home():
    try:
        return send_from_directory('src/static', 'index.html')
    except:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Airbus Careers - Site Funcionando!</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .success { color: green; font-size: 24px; }
                .info { color: #333; margin: 20px 0; }
            </style>
        </head>
        <body>
            <h1 class="success">✅ Site Airbus Careers Funcionando!</h1>
            <p class="info">O servidor está rodando corretamente no Railway.</p>
            <p class="info">Agora você pode adicionar os arquivos estáticos.</p>
            <a href="/admin-rh-airbus">Painel Admin</a>
        </body>
        </html>
        """

@app.route('/admin-rh-airbus')
def admin():
    try:
        return send_from_directory('src/static', 'admin.html')
    except:
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
            <p>Sistema funcionando corretamente!</p>
            <a href="/">Voltar ao Site</a>
        </body>
        </html>
        """

@app.route('/api/test')
def test():
    return jsonify({"status": "OK", "message": "API funcionando!"})

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory('src/static', path)
    except:
        return f"Arquivo {path} não encontrado", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Iniciando servidor na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

