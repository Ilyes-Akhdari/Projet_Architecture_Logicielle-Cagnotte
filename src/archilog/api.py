from flask import Blueprint, jsonify
from spectree import SpecTree, SecurityScheme
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from archilog.auth import token_auth
from archilog.data import get_all_money_pots, create_expense, delete_money_pot, delete_expense
from archilog.domain import get_money_pot_details

api = Blueprint("api", __name__)

# --- Configuration Spectree (Validation + Swagger) ---
api_spec = SpecTree(
    "flask",
    app=api,
    security_schemes=[
        SecurityScheme(
            name="bearer_token",
            data={"type": "http", "scheme": "bearer"}
        )
    ],
    security=[{"bearer_token": []}]
)

# --- Modèles de Données (Pydantic) ---
class ExpenseData(BaseModel):
    paid_by: str = Field(min_length=1, max_length=50)
    amount: float = Field(gt=0)

class CreatePotData(BaseModel):
    pot_name: str = Field(min_length=1, max_length=50)
    paid_by: str = Field(min_length=1, max_length=50)
    amount: float = Field(gt=0)

# --- ROUTES CAGNOTTES ---

@api.get("/pots")
@api_spec.validate(tags=["Cagnottes"])
@token_auth.login_required
def get_pots():
    """Récupère la liste de toutes les cagnottes (Lecture)."""
    pots = get_all_money_pots()
    return jsonify([{"name": p.name} for p in pots])

@api.post("/pots")
@api_spec.validate(tags=["Cagnottes"])
@token_auth.login_required(role="admin")
def create_pot(json: CreatePotData):
    """Crée une nouvelle cagnotte et sa première dépense (Création - Admin uniquement)."""
    try:
        create_expense(json.pot_name, json.paid_by, json.amount)
        return jsonify({"message": f"Cagnotte '{json.pot_name}' créée avec succès."}), 201
    except IntegrityError:
        return jsonify({"error": "Une erreur d'intégrité est survenue (doublon possible)."}), 400

@api.get("/pots/<name>")
@api_spec.validate(tags=["Cagnottes"])
@token_auth.login_required
def get_pot_details(name: str):
    """Récupère les détails, dépenses et l'équilibre financier d'une cagnotte (Lecture)."""
    try:
        mp, transactions = get_money_pot_details(name)
        return jsonify({
            "name": mp.name,
            "expenses": [{"paid_by": e.paid_by, "amount": e.amount} for e in mp.expenses],
            "transactions": [{"sender": t.sender, "receiver": t.receiver, "amount": t.amount} for t in transactions]
        })
    except Exception:
        return jsonify({"error": f"Cagnotte '{name}' introuvable."}), 404

@api.delete("/pots/<name>")
@api_spec.validate(tags=["Cagnottes"])
@token_auth.login_required(role="admin")
def delete_pot(name: str):
    """Supprime définitivement une cagnotte (Suppression - Admin uniquement)."""
    delete_money_pot(name)
    return jsonify({"message": f"Cagnotte '{name}' supprimée avec succès."}), 200

# --- ROUTES DEPENSES ---

@api.post("/pots/<name>/expenses")
@api_spec.validate(tags=["Dépenses"])
@token_auth.login_required
def api_add_expense(name: str, json: ExpenseData):
    """Ajoute une dépense à une cagnotte existante."""
    try:
        create_expense(name, json.paid_by, json.amount)
        return jsonify({"message": f"Dépense de {json.amount}€ ajoutée pour {json.paid_by}."}), 201
    except IntegrityError:
        return jsonify({"error": "Impossible : Cette personne a déjà payé dans cette cagnotte."}), 400

@api.delete("/pots/<name>/expenses/<paid_by>")
@api_spec.validate(tags=["Dépenses"])
@token_auth.login_required
def api_delete_expense(name: str, paid_by: str):
    """Supprime une dépense spécifique d'une cagnotte."""
    delete_expense(name, paid_by)
    return jsonify({"message": f"Dépense de {paid_by} supprimée."}), 200