import sqlite3
import os

def inicializar_banco():
    # Define os caminhos corretos baseados na nova estrutura de pastas
    pasta_instance = 'instance'
    caminho_banco = os.path.join(pasta_instance, 'caderneta.db')
    caminho_sql = os.path.join('app', 'schema.sql')

    # Garante que a pasta instance existe antes de criar o banco
    os.makedirs(pasta_instance, exist_ok=True)

    conexao = sqlite3.connect(caminho_banco)
    
    with open(caminho_sql, 'r', encoding='utf-8') as f:
        conexao.executescript(f.read())
        
    conexao.commit()
    conexao.close()
    print("Banco de dados 'caderneta.db' inicializado com sucesso na pasta instance!")

if __name__ == '__main__':
    inicializar_banco()