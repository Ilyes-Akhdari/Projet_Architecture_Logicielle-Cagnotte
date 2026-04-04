import logging
from flask import Flask, flash, redirect, url_for, request, jsonify

def create_app():
    app = Flask(__name__)
    app.secret_key = "cle_secrete_pour_le_projet_archilog"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("archilog.log"),
            logging.StreamHandler()
        ]
    )
    
    # --- GESTIONNAIRE D'ERREURS DYNAMIQUE ---
    @app.errorhandler(500)
    def handle_internal_error(error):
        logging.exception(error)
        # Si c'est une requête API, on renvoie une erreur JSON
        if request.path.startswith('/api'):
            return jsonify({"error": "Erreur interne du serveur"}), 500
        # Sinon, c'est le site web normal, on redirige avec un message Flash
        flash("Erreur interne du serveur", "error")
        return redirect(url_for("web_ui.home"))

    from archilog.auth import auth
    @app.context_processor
    def inject_user():
        return dict(
            current_user=auth.current_user(),
            is_admin=(auth.current_user() == 'admin') if auth.current_user() else False
        )

    # --- ENREGISTREMENT DES BLUEPRINTS ---
    from archilog.views import web_ui, init_db_command
    from archilog.api import api, api_spec # Import du nouveau module API

    app.register_blueprint(web_ui, url_prefix="/")
    app.register_blueprint(api, url_prefix="/api")
    
    # Indispensable pour générer la page Swagger
    api_spec.register(app)
    
    app.cli.add_command(init_db_command)
    
    return app