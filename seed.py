import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_db():
    # Caminho para o banco de dados na pasta instance
    db_path = os.path.join('instance', 'caderneta.db')
    
    # Garante que a pasta instance existe
    if not os.path.exists('instance'):
        os.makedirs('instance')

    # Conecta ao SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Executa o schema.sql para limpar e recriar as tabelas
    schema_path = os.path.join('app', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        print("1. Tabelas recriadas com sucesso.")
    else:
        print("Erro: Arquivo app/schema.sql não encontrado.")
        return

    # 2. Inserir Tutor de Teste
    senha_hash = generate_password_hash('123456') # Requisito: senha em hash
    cursor.execute("INSERT INTO tutor (nome, email, senha) VALUES (?, ?, ?)",
                   ('Avaliador (Professor)', 'avaliador@teste.com', senha_hash))
    tutor_id = cursor.lastrowid
    print("2. Tutor 'Avaliador' inserido.")

    # 3. Inserir Pet de Teste
    cursor.execute("""INSERT INTO pet (tutor_id, nome, especie, raca, data_nascimento, peso, microchip)
                      VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   (tutor_id, 'Rex', 'Cachorro', 'Pug', '2020-05-10', 8.5, '982000000000001'))
    pet_id = cursor.lastrowid
    print("3. Pet 'Rex' inserido.")

    # 4. Inserir Registros Médicos (Lógica de Alertas)
    hoje = datetime.now()
    data_atrasada = (hoje - timedelta(days=5)).strftime('%Y-%m-%d')
    data_proxima = (hoje + timedelta(days=10)).strftime('%Y-%m-%d')

    cursor.execute("""INSERT INTO registro_medico (pet_id, tipo, descricao, data_registro, data_retorno)
                      VALUES (?, ?, ?, ?, ?)""",
                   (pet_id, 'Vacina', 'Vacina Antirrábica (Atrasada)', '2025-05-10', data_atrasada))

    cursor.execute("""INSERT INTO registro_medico (pet_id, tipo, descricao, data_registro, data_retorno)
                      VALUES (?, ?, ?, ?, ?)""",
                   (pet_id, 'Vermífugo', 'Drontal Plus (Próximo)', '2026-08-10', data_proxima))
    print("4. Registros médicos e alertas gerados.")

    conn.commit()
    conn.close()
    
    print("\n" + "="*50)
    print("BANCO DE DADOS POPULADO COM SUCESSO!")
    print("Credenciais de acesso para o avaliador:")
    print("E-mail: avaliador@teste.com")
    print("Senha:  123456")
    print("="*50 + "\n")

if __name__ == '__main__':
    seed_db()