<<<<<<< HEAD
import os
import json
import base64 # <-- IMPORTAÇÃO NOVA
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, make_response, current_app
=======
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, make_response
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
from app.db import get_db
from app.auth import login_required
from datetime import datetime, date
from app.utils import CalculadoraAlertas
<<<<<<< HEAD
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
=======
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

# Cria o Blueprint para as rotas principais
bp = Blueprint('core', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    
<<<<<<< HEAD
    # Busca registros médicos com retorno agendado para os pets deste tutor, ignorando os concluídos (concluido = 1)
    registros_retorno = db.execute(
        '''SELECT r.id as reg_id, r.tipo, r.descricao, r.data_retorno, p.nome as nome_pet, p.id as pet_id, r.concluido
           FROM registro_medico r 
           JOIN pet p ON r.pet_id = p.id 
           WHERE p.tutor_id = ? AND r.data_retorno IS NOT NULL AND r.data_retorno != "" AND (r.concluido = 0 OR r.concluido IS NULL)
=======
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
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
           ORDER BY r.data_retorno ASC''', 
        (g.tutor['id'],)
    ).fetchall()

    alertas = []
    hoje = date.today()

<<<<<<< HEAD
    # Lógica de Negócio: Calcula os dias restantes para os alertas do Dashboard
=======
    # 3. Lógica de Negócio: Calcula os dias restantes
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
    for reg in registros_retorno:
        data_ret = datetime.strptime(reg['data_retorno'], '%Y-%m-%d').date()
        dias_restantes = (data_ret - hoje).days

        if dias_restantes <= 30:
<<<<<<< HEAD
            if dias_restantes < 0:
                status = 'vencido'
            elif dias_restantes == 0:
                status = 'hoje'
            elif dias_restantes <= 15:
                status = 'proximo'
            else:
                status = 'ok'

=======
            status = 'vencido' if dias_restantes < 0 else 'proximo' if dias_restantes <= 15 else 'ok'
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
            alertas.append({
                'pet_id': reg['pet_id'],
                'nome_pet': reg['nome_pet'],
                'tipo': reg['tipo'],
                'descricao': reg['descricao'],
                'data_formatada': reg['data_retorno'].split('-')[::-1],
                'dias_restantes': abs(dias_restantes),
                'status': status,
                'venceu': dias_restantes < 0
            })

<<<<<<< HEAD
    return render_template('core/dashboard.html', alertas=alertas)

# Nova rota exclusiva para visualizar os pets cadastrados
@bp.route('/meus_pets')
@login_required
def meus_pets():
    db = get_db()
    pets = db.execute(
        'SELECT * FROM pet WHERE tutor_id = ?', (g.tutor['id'],)
    ).fetchall()
    return render_template('core/meus_pets.html', pets=pets)
=======
    return render_template('core/dashboard.html', pets=pets, alertas=alertas)
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

@bp.route('/pet/novo', methods=('GET', 'POST'))
@login_required
def novo_pet():
    if request.method == 'POST':
        nome = request.form['nome']
        especie = request.form['especie']
        raca = request.form['raca']
        data_nascimento = request.form['data_nascimento']
        
<<<<<<< HEAD
        peso_form = request.form.get('peso_atual_kg', '')
        microchip_form = request.form.get('numero_microchip', '')
        
        peso = float(peso_form) if peso_form else None
        microchip = microchip_form if microchip_form else None
        
        # Lógica de Upload de Imagem
        foto = request.files.get('foto')
        nome_foto = 'default.png'
        
        if foto and foto.filename != '':
            nome_foto = secure_filename(foto.filename)
            pasta_uploads = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(pasta_uploads, exist_ok=True)
            foto.save(os.path.join(pasta_uploads, nome_foto))
        
=======
        # Recebe os dados do form mantendo a compatibilidade com o HTML
        peso_form = request.form.get('peso_atual_kg', '')
        microchip_form = request.form.get('numero_microchip', '')
        
        # Converte para NULL (None) se estiverem vazios
        peso = float(peso_form) if peso_form else None
        microchip = microchip_form if microchip_form else None
        
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
        db = get_db()
        erro = None

        if not nome or not especie:
            erro = 'Nome e espécie são obrigatórios.'

        if erro is None:
            try:
                db.execute(
<<<<<<< HEAD
                    '''INSERT INTO pet (tutor_id, nome, especie, raca, data_nascimento, peso, microchip, foto)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (g.tutor['id'], nome, especie, raca, data_nascimento, peso, microchip, nome_foto)
                )
                db.commit()
                flash('Pet cadastrado com sucesso!', 'success')
                return redirect(url_for('core.meus_pets')) # Alterado para voltar a Meus Pets
=======
                    '''INSERT INTO pet (tutor_id, nome, especie, raca, data_nascimento, peso, microchip)
                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (g.tutor['id'], nome, especie, raca, data_nascimento, peso, microchip)
                )
                db.commit()
                flash('Pet cadastrado com sucesso!', 'success')
                return redirect(url_for('core.index'))
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
            except db.IntegrityError:
                erro = 'Este número de microchip já está cadastrado em outro pet.'

        if erro:
            flash(erro, 'error')

    return render_template('core/novo_pet.html')

@bp.route('/pet/<int:id>/editar', methods=('GET', 'POST'))
@login_required
def editar_pet(id):
    db = get_db()
    pet = db.execute(
        'SELECT * FROM pet WHERE id = ? AND tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()

    if pet is None:
        flash('Pet não encontrado ou você não tem permissão para editá-lo.')
<<<<<<< HEAD
        return redirect(url_for('core.meus_pets'))
=======
        return redirect(url_for('core.index'))
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

    if request.method == 'POST':
        nome = request.form['nome']
        especie = request.form['especie']
        raca = request.form['raca']
        data_nascimento = request.form['data_nascimento']
        
<<<<<<< HEAD
=======
        # Lida com variações dos nomes dos inputs HTML
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
        peso_form = request.form.get('peso_atual_kg', request.form.get('peso', ''))
        microchip_form = request.form.get('numero_microchip', request.form.get('microchip', ''))

        peso = float(peso_form) if peso_form else None
        microchip = microchip_form if microchip_form else None

<<<<<<< HEAD
        # Verifica se o utilizador enviou uma nova foto
        foto = request.files.get('foto')
        nome_foto = pet['foto'] # Mantém a antiga por predefinição
        
        if foto and foto.filename != '':
            nome_foto = secure_filename(foto.filename)
            pasta_uploads = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(pasta_uploads, exist_ok=True)
            foto.save(os.path.join(pasta_uploads, nome_foto))

        db.execute(
            'UPDATE pet SET nome = ?, especie = ?, raca = ?, data_nascimento = ?, peso = ?, microchip = ?, foto = ? '
            'WHERE id = ? AND tutor_id = ?',
            (nome, especie, raca, data_nascimento, peso, microchip, nome_foto, id, g.tutor['id'])
        )
        db.commit()
        flash('Dados do pet atualizados com sucesso!', 'success')
        return redirect(url_for('core.meus_pets')) # Alterado para voltar a Meus Pets
=======
        db.execute(
            'UPDATE pet SET nome = ?, especie = ?, raca = ?, data_nascimento = ?, peso = ?, microchip = ? '
            'WHERE id = ? AND tutor_id = ?',
            (nome, especie, raca, data_nascimento, peso, microchip, id, g.tutor['id'])
        )
        db.commit()
        flash('Dados do pet atualizados com sucesso!', 'success')
        return redirect(url_for('core.index'))
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

    return render_template('core/editar_pet.html', pet=pet)

@bp.route('/pet/<int:id>/excluir', methods=('POST',))
@login_required
def excluir_pet(id):
    db = get_db()
    db.execute('DELETE FROM pet WHERE id = ? AND tutor_id = ?', (id, g.tutor['id']))
    db.commit()
    flash('Pet removido com sucesso.', 'success')
<<<<<<< HEAD
    return redirect(url_for('core.meus_pets')) # Alterado para voltar a Meus Pets
=======
    return redirect(url_for('core.index'))
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

@bp.route('/pet/<int:id>/prontuario', methods=('GET', 'POST'))
@login_required
def prontuario(id):
    db = get_db()
    
    pet = db.execute(
        'SELECT * FROM pet WHERE id = ? AND tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()

    if pet is None:
        flash('Pet não encontrado ou acesso negado.')
<<<<<<< HEAD
        return redirect(url_for('core.meus_pets'))
=======
        return redirect(url_for('core.index'))
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

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
<<<<<<< HEAD
        flash('Registro médico adicionado com sucesso!', 'success')
        return redirect(url_for('core.prontuario', id=id))

    registros_db = db.execute(
=======
        flash('Registo médico adicionado com sucesso!', 'success')
        return redirect(url_for('core.prontuario', id=id))

    registos_db = db.execute(
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
        'SELECT * FROM registro_medico WHERE pet_id = ? ORDER BY data_registro DESC', (id,)
    ).fetchall()

    calculadora = CalculadoraAlertas(dias_aviso=30)
<<<<<<< HEAD
    registros_processados = []
    
    for reg in registros_db:
        reg_dict = dict(reg)
        reg_dict['status_alerta'] = calculadora.analisar_vencimento(reg_dict['data_retorno'])
        registros_processados.append(reg_dict)

    return render_template('core/prontuario.html', pet=pet, registros=registros_processados)

# Rota para marcar/desmarcar procedimento concluído
@bp.route('/registro/<int:id>/concluir', methods=['POST'])
@login_required
def concluir_registro(id):
    db = get_db()
    registro = db.execute(
        'SELECT r.pet_id, r.concluido FROM registro_medico r JOIN pet p ON r.pet_id = p.id '
        'WHERE r.id = ? AND p.tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()

    if registro:
        # Inverte o valor (se era 0 vira 1, se era 1 vira 0)
        novo_status = 0 if registro['concluido'] else 1
        db.execute('UPDATE registro_medico SET concluido = ? WHERE id = ?', (novo_status, id))
        db.commit()
        flash('Status do procedimento atualizado!', 'success')
        return redirect(url_for('core.prontuario', id=registro['pet_id']))
        
    flash('Registro não encontrado ou acesso negado.', 'error')
    return redirect(url_for('core.meus_pets'))
=======
    registos_processados = []
    
    for reg in registos_db:
        reg_dict = dict(reg)
        reg_dict['status_alerta'] = calculadora.analisar_vencimento(reg_dict['data_retorno'])
        registos_processados.append(reg_dict)

    return render_template('core/prontuario.html', pet=pet, registos=registos_processados)
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

@bp.route('/registro/<int:id>/editar', methods=('GET', 'POST'))
@login_required
def editar_registro(id):
    db = get_db()
    registro = db.execute(
        'SELECT r.*, p.nome FROM registro_medico r JOIN pet p ON r.pet_id = p.id '
        'WHERE r.id = ? AND p.tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()

    if registro is None:
<<<<<<< HEAD
        flash('Registro não encontrado ou acesso negado.')
        return redirect(url_for('core.meus_pets'))
=======
        flash('Registo não encontrado ou acesso negado.')
        return redirect(url_for('core.index'))
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

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
<<<<<<< HEAD
        flash('Registro médico atualizado com sucesso!', 'success')
=======
        flash('Registo médico atualizado com sucesso!', 'success')
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
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
<<<<<<< HEAD
        flash('Registro eliminado com sucesso.', 'success')
        return redirect(url_for('core.prontuario', id=registro['pet_id']))
        
    return redirect(url_for('core.meus_pets'))
=======
        flash('Registo eliminado com sucesso.', 'success')
        return redirect(url_for('core.prontuario', id=registro['pet_id']))
        
    return redirect(url_for('core.index'))
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

@bp.route('/pet/<int:id>/exportar')
@login_required
def exportar_prontuario(id):
    db = get_db()
<<<<<<< HEAD
    pet = db.execute('SELECT * FROM pet WHERE id = ? AND tutor_id = ?', (id, g.tutor['id'])).fetchone()

    if pet is None:
        flash('Pet não encontrado.')
        return redirect(url_for('core.meus_pets'))

    registros = db.execute('SELECT * FROM registro_medico WHERE pet_id = ? ORDER BY data_registro DESC', (id,)).fetchall()
=======
    pet = db.execute(
        'SELECT * FROM pet WHERE id = ? AND tutor_id = ?', (id, g.tutor['id'])
    ).fetchone()

    if pet is None:
        flash('Pet não encontrado.')
        return redirect(url_for('core.index'))

    registros = db.execute(
        'SELECT * FROM registro_medico WHERE pet_id = ? ORDER BY data_registro DESC', (id,)
    ).fetchall()
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

    pet_dict = dict(pet)
    registros_dict = [dict(reg) for reg in registros]

<<<<<<< HEAD
    # MAGIA DO OFFLINE: Converte a foto física num código de texto Base64
    foto_b64 = ""
    nome_foto = pet_dict.get('foto')
    if not nome_foto or nome_foto == '':
        nome_foto = 'default.png'
        
    caminho_foto = os.path.join(current_app.root_path, 'static', 'uploads', nome_foto)
    if not os.path.exists(caminho_foto):
        caminho_foto = os.path.join(current_app.root_path, 'static', 'default.png')
        
    try:
        if os.path.exists(caminho_foto):
            with open(caminho_foto, "rb") as img_file:
                # O formato b64encode transforma a imagem em caracteres para funcionar sem ficheiros soltos
                foto_b64 = base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Erro ao converter imagem: {e}")

    html_content = render_template(
        'core/exportacao_offline.html',
        pet_json=json.dumps(pet_dict),
        registros_json=json.dumps(registros_dict),
        foto_b64=foto_b64  # Passamos a imagem embutida para o template
=======
    html_content = render_template(
        'core/exportacao_offline.html',
        pet_json=json.dumps(pet_dict),
        registros_json=json.dumps(registros_dict)
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
    )

    output = make_response(html_content)
    nome_seguro = pet['nome'].replace(' ', '_')
    output.headers["Content-Disposition"] = f"attachment; filename=relatorio_{nome_seguro}.html"
    output.headers["Content-type"] = "text/html; charset=utf-8"
    
    return output

@bp.route('/api/racas/<especie>')
@login_required
def api_racas(especie):
    import urllib.request
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
        racas_gatos = [
            {"name": "Persa"}, {"name": "Siamês"}, {"name": "Maine Coon"},
            {"name": "Angorá"}, {"name": "Sphynx"}, {"name": "Ragdoll"},
            {"name": "British Shorthair"}, {"name": "Bengal"}
        ]
        return jsonify(racas_gatos)

    else:
        return jsonify({'erro': 'Espécie inválida'}), 400

<<<<<<< HEAD
@bp.route('/perfil', methods=('GET', 'POST'))
@login_required
def perfil():
    if request.method == 'POST':
        senha_atual = request.form['senha_atual']
        nova_senha = request.form['nova_senha']
        confirmar_senha = request.form['confirmar_senha']
        
        db = get_db()
        tutor = db.execute('SELECT * FROM tutor WHERE id = ?', (g.tutor['id'],)).fetchone()
        erro = None
        
        # Validação cruzada (aceita os nossos tutores com HASH e o avaliador com texto limpo)
        senha_valida = False
        if tutor['senha_hash']:
            if check_password_hash(tutor['senha_hash'], senha_atual):
                senha_valida = True
        else:
            if tutor['senha'] == senha_atual:
                senha_valida = True
                
        if not senha_valida:
            erro = 'A senha atual está incorreta.'
        elif nova_senha != confirmar_senha:
            erro = 'A nova senha e a confirmação não coincidem.'
        elif len(nova_senha) < 6:
            erro = 'A nova senha deve ter pelo menos 6 caracteres.'
            
        if erro is None:
            # Atualiza o hash seguro e limpa o texto base (caso seja o avaliador a mudar a password)
            db.execute(
                'UPDATE tutor SET senha_hash = ?, senha = NULL WHERE id = ?',
                (generate_password_hash(nova_senha), g.tutor['id'])
            )
            db.commit()
            flash('Senha atualizada com sucesso!', 'success')
            return redirect(url_for('core.perfil'))
        else:
            flash(erro, 'error')
            
=======
@bp.route('/perfil')
@login_required
def perfil():
    # Os dados do tutor já estão carregados globalmente na variável 'g.tutor'
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
    return render_template('core/perfil.html')