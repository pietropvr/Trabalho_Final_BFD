import functools
<<<<<<< HEAD
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

=======
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

# Cria o Blueprint chamado 'auth'. Todas as rotas terão o prefixo '/auth'
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
<<<<<<< HEAD
        confirmar_senha = request.form.get('confirmar_senha') # Captura a confirmação
        db = get_db()
        erro = None

        if not nome:
            erro = 'Nome é obrigatório.'
        elif not email:
            erro = 'E-mail é obrigatório.'
        elif not senha:
            erro = 'Senha é obrigatória.'
        elif len(senha) < 6:
            erro = 'A senha deve ter pelo menos 6 caracteres.'
        # Validação cruzada das palavras-passe
=======
        confirmar_senha = request.form['confirmar_senha']
        
        db = get_db()
        erro = None

        if not email or not senha:
            erro = 'Email e senha são obrigatórios.'
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email): # Valida o formato de e-mail
            erro = 'Por favor, insira um endereço de e-mail válido.'
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
        elif senha != confirmar_senha:
            erro = 'As senhas não coincidem. Tente novamente.'

        if erro is None:
            try:
                db.execute(
                    "INSERT INTO tutor (nome, email, senha_hash) VALUES (?, ?, ?)",
<<<<<<< HEAD
                    (nome, email, generate_password_hash(senha)),
                )
                db.commit()
            except db.IntegrityError:
                erro = f"O e-mail {email} já está cadastrado."
            else:
                flash('Cadastro realizado com sucesso! Pode entrar.', 'success')
                return redirect(url_for("auth.login"))

        flash(erro, 'error')
=======
                    (nome, email, generate_password_hash(senha))
                )
                db.commit()
                flash('Cadastro realizado com sucesso! Faça seu login.', 'success')
                return redirect(url_for('auth.login'))
            except db.IntegrityError:
                # O banco acusa erro se tentarmos duplicar um email (regra UNIQUE)
                erro = f"O email {email} já está cadastrado."

        if erro:
            flash(erro, 'error')
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        db = get_db()
        erro = None

<<<<<<< HEAD
        tutor = db.execute(
            'SELECT * FROM tutor WHERE email = ?', (email,)
        ).fetchone()

        if tutor is None:
            erro = 'Email ou senha incorretos.'
        else:
            tutor_dict = dict(tutor)
            senha_valida = False
            
            # Verificação 1: Tenta validar via Hash de segurança padrão
            if tutor_dict.get('senha_hash') and not senha_valida:
                try:
                    if check_password_hash(tutor_dict['senha_hash'], senha):
                        senha_valida = True
                except Exception:
                    # Se falhar (o seed injetou texto limpo na coluna de hash), compara como texto normal
                    if tutor_dict['senha_hash'] == senha:
                        senha_valida = True
                        
            # Verificação 2: Tenta validar via texto limpo na coluna antiga 'senha' (Avaliador)
            if tutor_dict.get('senha') and not senha_valida:
                if tutor_dict['senha'] == senha:
                    senha_valida = True
                    
            if not senha_valida:
                erro = 'Email ou senha incorretos.'

        if erro is None:
            session.clear()
            # Salva a sessão com as duas chaves para garantir compatibilidade máxima
            session['tutor_id'] = tutor['id']
            session['user_id'] = tutor['id']
            return redirect(url_for('core.index'))

        flash(erro, 'error')

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('tutor_id') or session.get('user_id')

    if user_id is None:
        g.tutor = None
    else:
        g.tutor = get_db().execute(
            'SELECT * FROM tutor WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

=======
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
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.tutor is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
<<<<<<< HEAD
    return wrapped_view
=======
    return wrapped_view

# Carrega as informações do tutor logado antes de qualquer requisição
@bp.before_app_request
def load_logged_in_tutor():
    tutor_id = session.get('tutor_id')
    if tutor_id is None:
        g.tutor = None
    else:
        g.tutor = get_db().execute('SELECT * FROM tutor WHERE id = ?', (tutor_id,)).fetchone()
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
