import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

# Cria o Blueprint chamado 'auth'. Todas as rotas terão o prefixo '/auth'
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        db = get_db()
        erro = None

        if not email or not senha:
            erro = 'Email e senha são obrigatórios.'

        if erro is None:
            try:
                # generate_password_hash garante que a senha vire um texto embaralhado e seguro no banco
                db.execute(
                    "INSERT INTO tutor (nome, email, senha_hash) VALUES (?, ?, ?)",
                    (nome, email, generate_password_hash(senha))
                )
                db.commit()
                return redirect(url_for('auth.login'))
            except db.IntegrityError:
                erro = f"O email {email} já está cadastrado."

        flash(erro) # Mostra o erro na tela (precisaremos adicionar suporte a flash no base.html depois)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        db = get_db()
        erro = None

        tutor = db.execute('SELECT * FROM tutor WHERE email = ?', (email,)).fetchone()

        # check_password_hash compara a senha digitada com o hash salvo no banco
        if tutor is None or not check_password_hash(tutor['senha_hash'], senha):
            erro = 'Email ou senha incorretos.'

        if erro is None:
            # A 'session' é um cookie seguro guardado no navegador do usuário
            session.clear()
            session['tutor_id'] = tutor['id']
            return redirect(url_for('index')) # Por enquanto redireciona para a home

        flash(erro)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Este decorador será usado nas rotas que exigem que o usuário esteja logado (ex: Dashboard)
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.tutor is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# Carrega as informações do tutor logado antes de qualquer requisição
@bp.before_app_request
def load_logged_in_tutor():
    tutor_id = session.get('tutor_id')
    if tutor_id is None:
        g.tutor = None
    else:
        g.tutor = get_db().execute('SELECT * FROM tutor WHERE id = ?', (tutor_id,)).fetchone()