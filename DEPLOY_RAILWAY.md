# 🚀 Deploy do Site Airbus Carrières no Railway

## 📋 **Pré-requisitos**

1. Conta no [Railway](https://railway.app/)
2. Conta no GitHub (para conectar o repositório)
3. Git instalado localmente

## 🔧 **Arquivos de Configuração Incluídos**

O projeto já está configurado com todos os arquivos necessários:

- ✅ `requirements.txt` - Dependências Python
- ✅ `Procfile` - Comando de inicialização
- ✅ `railway.json` - Configurações específicas do Railway
- ✅ `runtime.txt` - Versão do Python
- ✅ `.env.example` - Exemplo de variáveis de ambiente
- ✅ `.gitignore` - Arquivos a serem ignorados pelo Git

## 📁 **Estrutura do Projeto**

```
airbus-careers/
├── src/
│   ├── static/          # Frontend (HTML, CSS, JS, imagens)
│   ├── models/          # Modelos do banco de dados
│   ├── routes/          # Rotas da API
│   └── main.py          # Aplicação Flask principal
├── requirements.txt     # Dependências Python
├── Procfile            # Comando de inicialização
├── railway.json        # Configurações do Railway
├── runtime.txt         # Versão do Python
├── .env.example        # Exemplo de variáveis de ambiente
└── .gitignore          # Arquivos ignorados pelo Git
```

## 🚀 **Passos para Deploy**

### **1. Preparar Repositório Git**

```bash
# Navegar para o diretório do projeto
cd airbus-careers

# Inicializar repositório Git (se não existir)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit inicial
git commit -m "Initial commit - Airbus Careers Website"

# Conectar ao repositório GitHub (substitua pela sua URL)
git remote add origin https://github.com/seu-usuario/airbus-careers.git

# Enviar para GitHub
git push -u origin main
```

### **2. Configurar no Railway**

1. **Acessar Railway**: https://railway.app/
2. **Fazer login** com sua conta
3. **Criar novo projeto**: Clique em "New Project"
4. **Conectar GitHub**: Selecione "Deploy from GitHub repo"
5. **Selecionar repositório**: Escolha o repositório `airbus-careers`
6. **Aguardar deploy**: O Railway detectará automaticamente as configurações

### **3. Configurar Variáveis de Ambiente**

No painel do Railway, vá em **Variables** e adicione:

```
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=production
FLASK_DEBUG=False
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### **4. Configurar Domínio (Opcional)**

1. No painel do Railway, vá em **Settings**
2. Clique em **Domains**
3. Clique em **Generate Domain** para obter um domínio gratuito
4. Ou configure um domínio personalizado

## 🔗 **URLs do Sistema**

Após o deploy, o sistema estará disponível em:

- **Site Principal**: `https://seu-dominio.railway.app/`
- **Painel Admin**: `https://seu-dominio.railway.app/admin-rh-airbus`

## 🔐 **Credenciais de Acesso**

### **Painel Administrativo**
- **URL**: `/admin-rh-airbus`
- **Usuário**: `admin`
- **Senha**: `admin123`

## 📊 **Funcionalidades Incluídas**

### **Site Principal**
- ✅ Página inicial com informações da Airbus
- ✅ Carrossel de vagas de emprego
- ✅ Filtros por categoria (Ingénierie, Production, Support)
- ✅ Formulário de candidatura com upload de documentos
- ✅ Design responsivo para mobile
- ✅ Interface 100% em francês
- ✅ Animações de sucesso

### **Painel Administrativo**
- ✅ Dashboard com estatísticas
- ✅ Gestão de candidaturas
- ✅ Visualização de documentos
- ✅ Download de arquivos
- ✅ Gestão de vagas de emprego

## 🛠️ **Comandos Úteis**

### **Deploy Manual (se necessário)**
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
gunicorn --chdir src main:app --bind 0.0.0.0:$PORT
```

### **Desenvolvimento Local**
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar em modo desenvolvimento
cd src
python main.py
```

## 🔧 **Configurações Avançadas**

### **Banco de Dados**
- Por padrão usa SQLite
- Para PostgreSQL, configure `DATABASE_URL` nas variáveis de ambiente
- O banco é criado automaticamente na primeira execução

### **Upload de Arquivos**
- Limite: 16MB por arquivo
- Formatos aceitos: PDF, JPG, PNG
- Armazenamento local no diretório `uploads/`

### **CORS**
- Configurado para aceitar requisições de qualquer origem
- Adequado para desenvolvimento e produção

## 🐛 **Troubleshooting**

### **Erro de Build**
- Verificar se `requirements.txt` está correto
- Verificar se `runtime.txt` especifica Python 3.11

### **Erro de Inicialização**
- Verificar se `Procfile` está correto
- Verificar logs no painel do Railway

### **Erro de Banco de Dados**
- Verificar se diretório `database/` existe
- Verificar permissões de escrita

## 📞 **Suporte**

Para problemas técnicos:
1. Verificar logs no painel do Railway
2. Verificar configurações de variáveis de ambiente
3. Verificar se todos os arquivos foram enviados corretamente

## 🎯 **Próximos Passos**

Após o deploy bem-sucedido:
1. Testar todas as funcionalidades
2. Configurar domínio personalizado (se necessário)
3. Configurar backup do banco de dados
4. Monitorar logs e performance

---

**✅ O site está pronto para produção no Railway!**

