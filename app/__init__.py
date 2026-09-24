import os
from flask import Flask, render_template

def create_app():
    # Cria a instância do Flask
    app = Flask(__name__, instance_relative_config=True)

    # Configurações básicas de segurança e banco de dados
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'caderneta.db'),
    )

    # Garante que a pasta 'instance' exista
    os.makedirs(app.instance_path, exist_ok=True)

    # --- REGISTRO DOS MÓDULOS ---
    
    # Registra o banco de dados
    from . import db
    app.teardown_appcontext(db.close_db)

    # Registra o Blueprint de autenticação
    from . import auth
    app.register_blueprint(auth.bp)

    # --- ROTAS GERAIS ---
    
    @app.route('/')
    def index():
        return render_template('base.html')

    # Retorna o app para o Flask rodar
    return app