# Importando as bibliotecas necessárias
from flask import Flask, render_template, request, redirect, url_for, session, flash  # Importa funções do Flask para criar o app, renderizar templates, manipular requisições, redirecionar, gerenciar sessão e exibir mensagens.
from flask_sqlalchemy import SQLAlchemy  # Importa o SQLAlchemy para interagir com o banco de dados.
from werkzeug.security import generate_password_hash, check_password_hash  # Funções para gerar e verificar senhas de forma segura.

# Criando a instância do Flask
app = Flask(__name__)  # Cria o app Flask.
app.config['SECRET_KEY'] = 'segredo'  # Define uma chave secreta para sessões seguras.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///frotas.db'  # Define o URI para o banco de dados (um arquivo SQLite chamado frotas.db).
db = SQLAlchemy(app)  # Cria a instância do SQLAlchemy com a configuração do app.

# Modelo de usuário
class Usuario(db.Model):  # Define a tabela de usuários no banco de dados.
    id = db.Column(db.Integer, primary_key=True)  # Define a coluna id como chave primária.
    username = db.Column(db.String(50), unique=True, nullable=False)  # Define o nome de usuário, único e não nulo.
    password = db.Column(db.String(200), nullable=False)  # Define a senha do usuário, não nula.

# Modelo de veículo
class Veiculo(db.Model):  # Define a tabela de veículos no banco de dados.
    id = db.Column(db.Integer, primary_key=True)  # Define a coluna id como chave primária.
    placa = db.Column(db.String(10), unique=True, nullable=False)  # Define a coluna de placa, única e não nula.
    modelo = db.Column(db.String(100), nullable=False)  # Define a coluna de modelo do veículo, não nula.
    ano = db.Column(db.Integer, nullable=False)  # Define a coluna do ano, não nula.

# Rota para a página inicial
@app.route('/')  # Define a rota para o caminho raiz ("/").
def index():
    return redirect(url_for('login'))  # Redireciona para a página de login.

# Rota de login
@app.route('/login', methods=['GET', 'POST'])  # Define a rota para login, aceita GET e POST.
def login():
    if request.method == 'POST':  # Se for uma requisição POST (enviado pelo formulário).
        username = request.form['username']  # Obtém o nome de usuário enviado.
        password = request.form['password']  # Obtém a senha enviada.
        user = Usuario.query.filter_by(username=username).first()  # Procura o usuário no banco de dados.
        if user and check_password_hash(user.password, password):  # Se o usuário existir e a senha estiver correta.
            session['user_id'] = user.id  # Armazena o ID do usuário na sessão.
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard.
        flash('Usuário ou senha inválidos!')  # Se as credenciais estiverem erradas, exibe uma mensagem de erro.
    return render_template('login.html')  # Exibe o template de login.

# Rota de cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])  # Define a rota para cadastro de usuário, aceita GET e POST.
def cadastro():
    if request.method == 'POST':  # Se for uma requisição POST (formulário enviado).
        username = request.form['username']  # Obtém o nome de usuário enviado.
        password = request.form['password']  # Obtém a senha enviada.
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Gera o hash da senha para segurança.
        novo_usuario = Usuario(username=username, password=hashed_password)  # Cria um novo usuário com os dados.
        db.session.add(novo_usuario)  # Adiciona o novo usuário à sessão do banco de dados.
        db.session.commit()  # Commit (salva) as mudanças no banco de dados.
        flash('Usuário cadastrado com sucesso!')  # Exibe mensagem de sucesso.
        return redirect(url_for('login'))  # Redireciona para a página de login.
    return render_template('cadastro.html')  # Exibe o template de cadastro.

# Rota de logout
@app.route('/logout')  # Define a rota para logout.
def logout():
    session.pop('user_id', None)  # Remove o ID do usuário da sessão (fazendo logout).
    return redirect(url_for('login'))  # Redireciona para a página de login.

# Rota do dashboard
@app.route('/dashboard')  # Define a rota para o dashboard.
def dashboard():
    if 'user_id' not in session:  # Se não houver um usuário na sessão (não logado).
        return redirect(url_for('login'))  # Redireciona para o login.
    veiculos = Veiculo.query.all()  # Obtém todos os veículos do banco de dados.
    return render_template('dashboard.html', veiculos=veiculos)  # Exibe o template do dashboard com a lista de veículos.

# Rota para adicionar veículo
@app.route('/adicionar', methods=['GET', 'POST'])  # Define a rota para adicionar veículo.
def adicionar():
    if 'user_id' not in session:  # Se não houver um usuário logado.
        return redirect(url_for('login'))  # Redireciona para o login.
    if request.method == 'POST':  # Se for uma requisição POST (formulário enviado).
        placa = request.form['placa']  # Obtém a placa do veículo.
        modelo = request.form['modelo']  # Obtém o modelo do veículo.
        ano = request.form['ano']  # Obtém o ano do veículo.
        novo_veiculo = Veiculo(placa=placa, modelo=modelo, ano=int(ano))  # Cria um novo objeto de veículo.
        db.session.add(novo_veiculo)  # Adiciona o novo veículo à sessão do banco de dados.
        db.session.commit()  # Commit (salva) as mudanças no banco de dados.
        return redirect(url_for('dashboard'))  # Redireciona para o dashboard.
    return render_template('adicionar.html')  # Exibe o template para adicionar veículo.

# Rota para editar veículo
@app.route('/editar/<int:id>', methods=['GET', 'POST'])  # Define a rota para editar um veículo, onde id é passado como parâmetro.
def editar(id):
    if 'user_id' not in session:  # Se não houver um usuário logado.
        return redirect(url_for('login'))  # Redireciona para o login.
    veiculo = Veiculo.query.get(id)  # Obtém o veículo pelo ID fornecido.
    if request.method == 'POST':  # Se for uma requisição POST (formulário enviado).
        veiculo.placa = request.form['placa']  # Atualiza a placa do veículo.
        veiculo.modelo = request.form['modelo']  # Atualiza o modelo do veículo.
        veiculo.ano = int(request.form['ano'])  # Atualiza o ano do veículo.
        db.session.commit()  # Commit (salva) as mudanças no banco de dados.
        return redirect(url_for('dashboard'))  # Redireciona para o dashboard.
    return render_template('editar.html', veiculo=veiculo)  # Exibe o template de edição do veículo.

# Rota para deletar veículo
@app.route('/deletar/<int:id>')  # Define a rota para deletar um veículo.
def deletar(id):
    if 'user_id' not in session:  # Se não houver um usuário logado.
        return redirect(url_for('login'))  # Redireciona para o login.
    veiculo = Veiculo.query.get(id)  # Obtém o veículo pelo ID fornecido.
    db.session.delete(veiculo)  # Deleta o veículo do banco de dados.
    db.session.commit()  # Commit (salva) as mudanças no banco de dados.
    return redirect(url_for('dashboard'))  # Redireciona para o dashboard.

# Execução do app
if __name__ == '__main__':  # Verifica se este script está sendo executado diretamente (não importado).
    with app.app_context():  # Cria um contexto de aplicativo.
        db.create_all()  # Cria todas as tabelas do banco de dados.
    app.run(debug=True)  # Inicia o servidor do Flask com modo de depuração ativado.
