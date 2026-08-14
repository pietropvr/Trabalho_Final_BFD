import sqlite3
import os

def inicializar_banco():
    caminho_banco = os.path.join('database', 'caderneta.db')
    caminho_sql = os.path.join('database', 'schema.sql')

    conexao = sqlite3.connect(caminho_banco)
    
    with open(caminho_sql, 'r', encoding='utf-8') as f:
        conexao.executescript(f.read())
        
    conexao.commit()
    conexao.close()
    print("Banco de dados 'caderneta.db' inicializado com sucesso!")

if __name__ == '__main__':
    inicializar_banco()