import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for 
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Função auxiliar para conectar ao banco de dados
def get_db_connection():
    caminho_banco = os.path.join('database', 'caderneta.db')
    conn = sqlite3.connect(caminho_banco)
    conn.row_factory = sqlite3.Row # Permite acessar as colunas pelo nome (ex: row['nome'])
    return conn


@app.route('/')

def index():
    # Rota principal que renderiza o template base.html
    return render_template('base.html')

# Nova Rota: Cadastro de Tutor
@app.route('/cadastro', methods=['GET', 'POST'])

def cadastro_tutor():
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário HTML
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

	# Gera o hash criptografado da senha
        senha_hash = generate_password_hash(senha)
        
        # Conecta ao banco e insere o novo tutor

        conn = get_db_connection();
        try:
            conn.execute('INSERT INTO TUTOR (nome, email, senha_hash) VALUES (?, ?, ?)', (nome, email, senha_hash))
            conn.commit()

        except sqlite3.IntegrityError:
        
        # Captura o erro caso o e-mail (que marcamos como UNIQUE no schema) já exista
            conn.close()
            
        return "Erro: Este e-mail já está cadastrado."
    conn.close()
        
        # Após cadastrar com sucesso, redireciona o usuário para a página inicial (por enquanto)
    return redirect(url_for('index'))

    # Se o método for GET, apenas renderiza a página do formulário
    return render_template('cadastro.html')

if __name__ == '__main__':
    # debug=True reinicia o servidor automaticamente ao salvar o código
    app.run(debug=True)