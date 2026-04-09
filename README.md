# 💰 Archilog - Projet Cagnotte (Rendu Final)

Application de gestion de cagnottes permettant le partage de dépenses et le calcul automatique de l'équilibre financier ("qui doit à qui").

Ce projet a été réalisé dans le cadre du module d'Architecture Logicielle (BUT2 INFO S4). Il met en œuvre une architecture **N-Tier** stricte, comprenant une interface CLI, une interface Web native et une API HTTP complète.

---

## ✨ Fonctionnalités Principales

* **Interface CLI :** Gestion complète des cagnottes et dépenses en ligne de commande via Click.
* **Équilibre financier automatique :** Calcul intelligent des transactions pour rembourser les participants de manière optimale.
* **Interface Web Native :** Navigation fluide propulsée par des templates Jinja2 (HTML/CSS, sans JavaScript).
* **API HTTP (REST) :** Interface machine-to-machine avec documentation interactive (Swagger) couvrant 100% des opérations (CRUD).
* **Sécurité & Rôles :** Distinction des privilèges (Admin/User). L'Admin a un accès total, l'User peut uniquement consulter et ajouter des dépenses.

---

## 🏗️ Architecture et Choix Techniques

Le projet respecte les standards professionnels de développement web :

1. **Architecture N-Tier & Blueprints :** Séparation stricte entre la Vue (`web.py` / `api.py` / `cli.py`), le Domaine (`domain.py`) et la Data (`data.py`). L'application utilise une `Application Factory` et des routeurs indépendants.
2. **Configuration Centralisée :** Les variables d'environnement (`dev.env`) pilotent la configuration via `config.py`.
3. **Persistance (SQLAlchemy Core) :** Utilisation exclusive de SQLAlchemy Core sans ORM. Contraintes d'intégrité métier assurées par clé primaire composite (une seule dépense par participant pour une même cagnotte).
4. **Sécurité Web (WTForms) :** Sécurisation des formulaires Web avec validation syntaxique, sémantique et protection CSRF.
5. **Sécurité API (Pydantic & SpecTree) :** Validation stricte des flux JSON entrants et génération automatique de la documentation OpenAPI.
6. **Authentification Hybride :** Le site Web utilise `BasicAuth` (login/mot de passe), l'API est sécurisée par `TokenAuth` (Bearer Token).
7. **Traçabilité :** Fichier de logs (`archilog.log`) et `errorhandler(500)` intelligent (JSON pour l'API, redirection Flash pour le Web).

---

## 🖥️ Interface CLI

Toutes les commandes s'exécutent avec le préfixe `uv run --env-file dev.env archilog` :

| Commande | Description |
|---|---|
| `init-db` | Initialise la base de données |
| `create-pot <nom> <participant> <montant>` | Crée une cagnotte avec une première dépense |
| `add-expense <nom> <participant> <montant>` | Ajoute une dépense à une cagnotte |
| `delete-expense <nom> <participant>` | Supprime la dépense d'un participant |
| `delete-pot <nom>` | Supprime une cagnotte et toutes ses dépenses |
| `list-pots` | Liste toutes les cagnottes |
| `show-pot <nom>` | Affiche les dépenses et le bilan "qui doit à qui" |

Exemple :
```bash
uv run --env-file dev.env archilog create-pot "Vacances" "Alice" 50.0
uv run --env-file dev.env archilog add-expense "Vacances" "Bob" 30.0
uv run --env-file dev.env archilog show-pot "Vacances"
```

---

## 🔌 Documentation de l'API HTTP

L'API suit les standards REST. Les créations (POST) utilisent le corps de la requête (JSON), tandis que les lectures/suppressions (GET/DELETE) ciblent directement l'URI.

Voici un aperçu des routes disponibles (nécessitent un Bearer Token) :

* `GET /api/pots` : Liste toutes les cagnottes.
* `GET /api/pots/{name}` : Affiche les détails, les dépenses et le calcul de l'équilibre financier d'une cagnotte.
* `POST /api/pots` : Crée une nouvelle cagnotte *(Admin uniquement)*.
* `POST /api/pots/{name}/expenses` : Ajoute une dépense.
  * *Exemple de Request Body (JSON) :*
    ```json
    {
      "paid_by": "Ilyes",
      "amount": 50.50
    }
    ```
* `DELETE /api/pots/{name}` : Supprime une cagnotte *(Admin uniquement)*.
* `DELETE /api/pots/{name}/expenses/{paid_by}` : Supprime la dépense d'un participant.

*(Une documentation Swagger interactive est générée automatiquement à `/api/apidoc/swagger` une fois le serveur lancé).*

---

## 🔐 Identifiants de test

**Accès au Site Web (HTTP Basic Auth) :**
* Admin : `admin` / `admin123`
* User : `user` / `user123`

**Accès à l'API (HTTP Bearer Token) :**
* Admin Token : `token-secret-admin`
* User Token : `token-secret-user`

---

## 🚀 Lancement du projet

**Prérequis :** Python 3.11+ et le gestionnaire de paquets `uv` installés.

### 1. Configuration
Vérifiez que le fichier `dev.env` est bien présent à la racine du projet :
```env
ARCHILOG_DATABASE_URL=sqlite:///data.db
ARCHILOG_DEBUG=True
```

### 2. Commandes d'exécution
```bash
# 1. Synchroniser les dépendances
uv sync

# 2. Initialiser la base de données
uv run --env-file dev.env archilog init-db

# 3. Lancer le serveur Web et l'API
uv run --env-file dev.env flask --app archilog --debug run

# 4. Lancer les tests unitaires
uv run pytest
```
