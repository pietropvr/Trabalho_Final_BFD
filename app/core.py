from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.db import get_db
from app.auth import login_required

# Cria o Blueprint para as rotas principais (sem prefixo de URL)
bp = Blueprint('core', __name__)

@bp.route('/')
@login_required # Garante que só quem está logado acesse esta página
def index():
    db = get_db()
    # Busca apenas os pets que pertencem ao tutor logado
    pets = db.execute(
        'SELECT * FROM pet WHERE tutor_id = ? ORDER BY nome ASC',
        (g.tutor['id'],)
    ).fetchall()
    
    return render_template('core/dashboard.html', pets=pets)

@bp.route('/pet/novo', methods=('GET', 'POST'))
@login_required
def novo_pet():
    if request.method == 'POST':
        nome = request.form['nome']
        especie = request.form['especie']
        raca = request.form['raca']
        data_nascimento = request.form['data_nascimento']
        peso = request.form['peso_atual_kg']
        microchip = request.form['numero_microchip']
        
        # Se os campos não obrigatórios estiverem vazios, transformamos em None (NULL no banco)
        peso = float(peso) if peso else None
        microchip = microchip if microchip else None
        
        db = get_db()
        erro = None

        if not nome or not especie:
            erro = 'Nome e espécie são obrigatórios.'

        if erro is None:
            try:
                db.execute(
                    '''INSERT INTO pet (tutor_id, nome, especie, raca, data_nascimento, peso_atual_kg, numero_microchip)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (g.tutor['id'], nome, especie, raca, data_nascimento, peso, microchip)
                )
                db.commit()
                flash('Pet cadastrado com sucesso!', 'success')
                return redirect(url_for('core.index'))
            except db.IntegrityError:
                erro = 'Este número de microchip já está cadastrado em outro pet.'

        if erro:
            flash(erro, 'error')

    return render_template('core/novo_pet.html')