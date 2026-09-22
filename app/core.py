import json
from io import StringIO
from flask import Response
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.db import get_db
from app.auth import login_required
from datetime import datetime, date
from app.utils import CalculadoraAlertas

# Cria o Blueprint para as rotas principais (sem prefixo de URL)
bp = Blueprint('core', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    
    # 1. Busca os pets do tutor
    pets = db.execute(
        'SELECT * FROM pet WHERE tutor_id = ?', (g.tutor['id'],)
    ).fetchall()

    # 2. Busca registros médicos com retorno agendado para os pets deste tutor
    registros_retorno = db.execute(
        '''SELECT r.tipo, r.descricao, r.data_retorno, p.nome as nome_pet, p.id as pet_id
           FROM registro_medico r 
           JOIN pet p ON r.pet_id = p.id 
           WHERE p.tutor_id = ? AND r.data_retorno IS NOT NULL AND r.data_retorno != ""
           ORDER BY r.data_retorno ASC''', 
        (g.tutor['id'],)
    ).fetchall()

    alertas = []
    hoje = date.today()

    # 3. Lógica de Negócio: Calcula os dias restantes
    for reg in registros_retorno:
        # Converte a string YYYY-MM-DD do banco para um objeto date do Python
        data_ret = datetime.strptime(reg['data_retorno'], '%Y-%m-%d').date()
        dias_restantes = (data_ret - hoje).days

        # Mostra qualquer registo atrasado no passado, e os que vencem nos próximos 30 dias
        if dias_restantes <= 30:
            status = 'vencido' if dias_restantes < 0 else 'proximo' if dias_restantes <= 15 else 'ok'
            
            alertas.append({
                'pet_id': reg['pet_id'],
                'nome_pet': reg['nome_pet'],
                'tipo': reg['tipo'],
                'descricao': reg['descricao'],
                'data_formatada': reg['data_retorno'].split('-')[::-1], # Para DD/MM/AAAA
                'dias_restantes': abs(dias_restantes),
                'status': status,
                'venceu': dias_restantes < 0
            })

    return render_template('core/dashboard.html', pets=pets, alertas=alertas)

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

@bp.route('/pet/<int:id>/editar', methods=('GET', 'POST'))
@login_required
def editar_pet(id):
    db = get_db()
    # Busca o pet garantindo que ele pertence ao tutor logado
    pet = db.execute(
        'SELECT * FROM pet WHERE id = ? AND tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()

    if pet is None:
        flash('Pet não encontrado ou você não tem permissão para editá-lo.')
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        nome = request.form['nome']
        especie = request.form['especie']
        raca = request.form['raca']
        data_nascimento = request.form['data_nascimento']
        peso = request.form['peso']
        numero_microchip = request.form.get('numero_microchip', '')

        db.execute(
            'UPDATE pet SET nome = ?, especie = ?, raca = ?, data_nascimento = ?, peso = ?, numero_microchip = ? '
            'WHERE id = ? AND tutor_id = ?',
            (nome, especie, raca, data_nascimento, peso, numero_microchip, id, g.tutor['id'])
        )
        db.commit()
        flash('Dados do pet atualizados com sucesso!')
        return redirect(url_for('core.index'))

    return render_template('core/editar_pet.html', pet=pet)

@bp.route('/pet/<int:id>/excluir', methods=('POST',))
@login_required
def excluir_pet(id):
    db = get_db()
    db.execute('DELETE FROM pet WHERE id = ? AND tutor_id = ?', (id, g.tutor['id']))
    db.commit()
    flash('Pet removido com sucesso.')
    return redirect(url_for('core.index'))

@bp.route('/pet/<int:id>/prontuario', methods=('GET', 'POST'))
@login_required
def prontuario(id):
    db = get_db()
    
    pet = db.execute(
        'SELECT * FROM pet WHERE id = ? AND tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()

    if pet is None:
        flash('Pet não encontrado ou acesso negado.')
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        data_registro = request.form['data_registro']
        data_retorno = request.form.get('data_retorno', None)

        db.execute(
            'INSERT INTO registro_medico (pet_id, tipo, descricao, data_registro, data_retorno) '
            'VALUES (?, ?, ?, ?, ?)',
            (id, tipo, descricao, data_registro, data_retorno)
        )
        db.commit()
        flash('Registo médico adicionado com sucesso!')
        return redirect(url_for('core.prontuario', id=id))

    registos_db = db.execute(
        'SELECT * FROM registro_medico WHERE pet_id = ? ORDER BY data_registro DESC', (id,)
    ).fetchall()

    # --- APLICAÇÃO DA CLASSE POO ---
    calculadora = CalculadoraAlertas(dias_aviso=30)
    registos_processados = []
    
    for reg in registos_db:
        reg_dict = dict(reg) # Converte a linha da base de dados para um dicionário editável
        # Usa a classe para calcular o status e guarda o resultado na chave 'status_alerta'
        reg_dict['status_alerta'] = calculadora.analisar_vencimento(reg_dict['data_retorno'])
        registos_processados.append(reg_dict)

    return render_template('core/prontuario.html', pet=pet, registos=registos_processados)

@bp.route('/registro/<int:id>/editar', methods=('GET', 'POST'))
@login_required
def editar_registro(id):
    db = get_db()
    # Confirma se o registo existe e pertence a um pet do tutor logado
    registro = db.execute(
        'SELECT r.*, p.nome FROM registro_medico r JOIN pet p ON r.pet_id = p.id '
        'WHERE r.id = ? AND p.tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()

    if registro is None:
        flash('Registo não encontrado ou acesso negado.')
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        data_registro = request.form['data_registro']
        data_retorno = request.form.get('data_retorno', None)

        db.execute(
            'UPDATE registro_medico SET tipo = ?, descricao = ?, data_registro = ?, data_retorno = ? '
            'WHERE id = ?', (tipo, descricao, data_registro, data_retorno, id)
        )
        db.commit()
        flash('Registo médico atualizado com sucesso!')
        # Redireciona de volta para o prontuário daquele pet específico
        return redirect(url_for('core.prontuario', id=registro['pet_id']))

    return render_template('core/editar_registro.html', registro=registro)

@bp.route('/registro/<int:id>/excluir', methods=('POST',))
@login_required
def excluir_registro(id):
    db = get_db()
    registro = db.execute(
        'SELECT r.pet_id FROM registro_medico r JOIN pet p ON r.pet_id = p.id '
        'WHERE r.id = ? AND p.tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()
    
    if registro:
        db.execute('DELETE FROM registro_medico WHERE id = ?', (id,))
        db.commit()
        flash('Registo eliminado com sucesso.')
        return redirect(url_for('core.prontuario', id=registro['pet_id']))
        
    return redirect(url_for('core.index'))

@bp.route('/pet/<int:id>/exportar')
@login_required
def exportar_prontuario(id):
    from flask import make_response
    
    db = get_db()
    pet = db.execute(
        'SELECT * FROM pet WHERE id = ? AND tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()

    if pet is None:
        flash('Pet não encontrado.')
        return redirect(url_for('core.index'))

    registros = db.execute(
        'SELECT * FROM registro_medico WHERE pet_id = ? ORDER BY data_registro DESC', (id,)
    ).fetchall()

    # Converte as linhas do banco de dados (sqlite3.Row) para dicionários comuns do Python
    pet_dict = dict(pet)
    registros_dict = [dict(reg) for reg in registros]

    # Renderiza um template HTML passando os dados em formato JSON (texto)
    html_content = render_template(
        'core/exportacao_offline.html',
        pet_json=json.dumps(pet_dict),
        registros_json=json.dumps(registros_dict)
    )

    # Cria a resposta forçando o download de um arquivo .html
    output = make_response(html_content)
    nome_seguro = pet['nome'].replace(' ', '_')
    output.headers["Content-Disposition"] = f"attachment; filename=relatorio_{nome_seguro}.html"
    output.headers["Content-type"] = "text/html; charset=utf-8"
    
    return output

@bp.route('/api/racas/<especie>')
@login_required
def api_racas(especie):
    import urllib.request
    import json
    from flask import jsonify

    if especie == 'Cachorro':
        url = 'https://api.thedogapi.com/v1/breeds'
        api_key = 'live_kR0OpYbrakeLp7BHt5WSfrAfaSV8EGsph5cOmmGKBo7mzbAE0vmWkLMl7EDK0DrI'
        try:
            req = urllib.request.Request(url, headers={'x-api-key': api_key})
            with urllib.request.urlopen(req) as resposta:
                dados = json.loads(resposta.read().decode('utf-8'))
                return jsonify(dados)
        except Exception as e:
            print(f"Erro na API externa (Cão): {e}")
            return jsonify({'erro': 'Falha na comunicação com a API externa'}), 500

    elif especie == 'Gato':
        # Retorna uma lista estática instantânea, sem depender de chaves externas
        racas_gatos = [
            {"name": "Persa"},
            {"name": "Siamês"},
            {"name": "Maine Coon"},
            {"name": "Angorá"},
            {"name": "Sphynx"},
            {"name": "Ragdoll"},
            {"name": "British Shorthair"},
            {"name": "Bengal"}
        ]
        return jsonify(racas_gatos)

    else:
        return jsonify({'erro': 'Espécie inválida'}), 400