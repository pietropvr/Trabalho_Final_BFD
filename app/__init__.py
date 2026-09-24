import os
from flask import Flask, render_template

def create_app(test_config=None):
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

    # Registra o Blueprint principal (core - dashboard e pets)
    from . import core
    app.register_blueprint(core.bp)
    
    # Indica ao Flask que a rota 'index' (página inicial '/') pertence ao blueprint core
    app.add_url_rule('/', endpoint='index')

    # Tratamento de Erros HTTP ---
    @app.errorhandler(404)
    def pagina_nao_encontrada(e):
        # O número 404 no final é muito importante para o protocolo HTTP
        return render_template('erros/404.html'), 404

    @app.errorhandler(500)
    def erro_interno_servidor(e):
        return render_template('erros/500.html'), 500

    return app