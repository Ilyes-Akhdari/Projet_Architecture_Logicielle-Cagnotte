from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer') # NOUVEAU : Pour l'API

users = {
    "admin": generate_password_hash("admin123"),
    "user": generate_password_hash("user123")
}

roles = {
    "admin": "admin",
    "user": "user"
}

# NOUVEAU : Base de données de tokens temporaire
tokens = {
    "token-secret-admin": "admin",
    "token-secret-user": "user"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

@auth.get_user_roles
def get_user_roles(username):
    return roles.get(username)

# NOUVEAU : Vérification du token pour l'API
@token_auth.verify_token
def verify_token(token):
    return tokens.get(token)

@token_auth.get_user_roles
def get_token_roles(username):
    return roles.get(username)