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

    @app.errorhandler(500)
    def handle_internal_error(error):
        logging.exception(error)
        if request.path.startswith('/api'):
            return jsonify({"error": "Erreur interne du serveur"}), 500
        flash("Erreur interne du serveur", "error")
        return redirect(url_for("web_ui.home"))

    from archilog.auth import auth

    @app.context_processor
    def inject_user():
        return dict(
            current_user=auth.current_user(),
            is_admin=(auth.current_user() == 'admin') if auth.current_user() else False
        )

    # --- IMPORTS DEPUIS LE SOUS-DOSSIER VIEWS ---
    from archilog.views.web import web_ui
    from archilog.views.api import api, api_spec
    from archilog.views.cli import cli as click_cli

    app.register_blueprint(web_ui, url_prefix="/")
    app.register_blueprint(api, url_prefix="/api")

    api_spec.register(app)

    # Enregistrement des commandes CLI
    for name, cmd in click_cli.commands.items():
        app.cli.add_command(cmd, name=name)

    return app