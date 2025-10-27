# 🛩️ Airbus Carrières - Site de Vagas de Emprego

Site completo de vagas de emprego da Airbus França com sistema de candidaturas e painel administrativo.

## 🌟 **Características**

### **Site Principal**
- 🎨 Design moderno e responsivo
- 🇫🇷 Interface 100% em francês
- 📱 Otimizado para mobile
- 🎠 Carrossel de vagas interativo
- 🔍 Filtros por categoria
- 📋 Formulário de candidatura completo
- 📎 Upload de documentos
- ✨ Animações elegantes

### **Painel Administrativo**
- 🔐 Acesso seguro via `/admin-rh-airbus`
- 📊 Dashboard com estatísticas
- 👥 Gestão de candidaturas
- 📄 Visualização de documentos
- ⬇️ Download de arquivos
- 💼 Gestão de vagas

## 🚀 **Deploy Rápido**

### **Railway (Recomendado)**
1. Faça fork deste repositório
2. Conecte ao [Railway](https://railway.app/)
3. Configure as variáveis de ambiente
4. Deploy automático!

📖 **Guia completo**: [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)

### **Desenvolvimento Local**
```bash
# Clonar repositório
git clone https://github.com/seu-usuario/airbus-careers.git
cd airbus-careers

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
cd src
python main.py
```

## 🔗 **URLs do Sistema**

- **Site Principal**: `/`
- **Painel Admin**: `/admin-rh-airbus`

## 🔐 **Credenciais Padrão**

- **Usuário**: `admin`
- **Senha**: `admin123`

## 🛠️ **Tecnologias**

- **Backend**: Flask + SQLAlchemy
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Banco**: SQLite (padrão) / PostgreSQL
- **Deploy**: Railway / Heroku / Docker

## 📁 **Estrutura**

```
src/
├── static/              # Frontend
│   ├── index.html      # Página principal
│   ├── admin.html      # Painel admin
│   ├── styles.css      # Estilos principais
│   ├── script.js       # JavaScript principal
│   └── images/         # Imagens
├── models/             # Modelos do banco
├── routes/             # Rotas da API
└── main.py            # Aplicação principal
```

## 🎯 **Funcionalidades**

### **Para Candidatos**
- ✅ Visualizar vagas disponíveis
- ✅ Filtrar por categoria
- ✅ Candidatar-se online
- ✅ Upload de documentos
- ✅ Confirmação de envio

### **Para RH**
- ✅ Visualizar todas as candidaturas
- ✅ Filtrar e buscar candidatos
- ✅ Baixar documentos
- ✅ Gerenciar vagas
- ✅ Dashboard com métricas

## 🔧 **Configuração**

### **Variáveis de Ambiente**
```env
SECRET_KEY=sua-chave-secreta
FLASK_ENV=production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
DATABASE_URL=sqlite:///database.db
```

### **Personalização**
- Editar vagas em `populate_db.py`
- Personalizar estilos em `styles.css`
- Modificar textos em `index.html`

## 📱 **Responsividade**

- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (320px - 767px)

## 🌐 **Idiomas**

- 🇫🇷 Francês (principal)
- 🔄 Fácil tradução para outros idiomas

## 📞 **Suporte**

Para dúvidas ou problemas:
1. Verificar [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)
2. Verificar logs da aplicação
3. Abrir issue no GitHub

## 📄 **Licença**

Este projeto é open source e está disponível sob a licença MIT.

---

**Desenvolvido para a Airbus França** ✈️

