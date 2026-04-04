# 💰 Archilog - Projet Cagnotte (Rendu Final)

Application de gestion de cagnottes permettant le partage de dépenses et le calcul automatique de l'équilibre financier ("qui doit à qui"). 

Ce projet a été réalisé dans le cadre du module d'Architecture Logicielle (BUT2 INFO S4). Il met en œuvre une architecture **N-Tier** stricte, comprenant une interface Web native et une API HTTP complète, prêtes pour l'industrialisation.

---

## ✨ Fonctionnalités Principales

* **Équilibre financier automatique :** Calcul intelligent des transactions nécessaires pour rembourser les participants de manière optimale.
* **Interface Web Native :** Navigation fluide propulsée par des templates Jinja2 (HTML/CSS, sans JavaScript).
* **API HTTP (REST) :** Interface machine-to-machine avec documentation interactive (Swagger) couvrant 100% des opérations (CRUD).
* **Sécurité & Rôles :** Distinction des privilèges (Admin/User). L'Admin a un accès total, l'User a un accès restreint (lecture et ajout de dépenses uniquement).

---

## 🏗️ Architecture et Choix Techniques

Le projet respecte les standards professionnels de développement web :

1. **Architecture N-Tier & Blueprints :** Séparation stricte entre la Vue (Web/API/CLI), le Domaine (logique pure) et la Data. L'application utilise une `Application Factory` et des routeurs indépendants.
2. **Configuration Centralisée :** Les variables d'environnement (`dev.env`) pilotent la configuration de l'application via `config.py`.
3. **Persistance (SQLAlchemy Core) :** Utilisation exclusive de SQLAlchemy Core sans ORM. Contraintes d'intégrité métier assurées par clé primaire composite (une seule dépense par participant pour une même cagnotte).
4. **Sécurité Web (WTForms) :** Sécurisation des formulaires Web avec validation syntaxique, sémantique et protection CSRF.
5. **Sécurité API (Pydantic & SpecTree) :** Validation stricte des flux JSON entrants et génération automatique de la documentation OpenAPI. 
6. **Authentification Hybride :** Utilisation de `flask-httpauth`. Le site Web utilise une authentification `BasicAuth` (Identifiant/Mot de passe), tandis que l'API est sécurisée par un `TokenAuth` (Bearer Token).
7. **Traçabilité :** Fichier de logs (`archilog.log`) et `errorhandler(500)` intelligent (renvoie du JSON pour l'API, ou une redirection avec message Flash pour le Web).

---

## 🔌 Documentation de l'API HTTP

L'API suit les standards REST. Les créations (POST) utilisent le corps de la requête (JSON), tandis que les lectures/suppressions (GET/DELETE) ciblent directement l'URI. 

Voici un aperçu des routes disponibles (nécessitent un Bearer Token) :

* `GET /api/pots` : Liste toutes les cagnottes.
* `GET /api/pots/{name}` : Affiche les détails, les dépenses et le calcul de l'équilibre financier d'une cagnotte.
* `POST /api/pots` : Crée une nouvelle cagnotte.
* `POST /api/pots/{name}/expenses` : Ajoute une dépense.
  * *Exemple de Request Body (JSON) attendu :*
    ```json
    {
      "paid_by": "Ilyes",
      "amount": 50.50
    }
    ```
* `DELETE /api/pots/{name}` : Supprime une cagnotte (Admin uniquement).
* `DELETE /api/pots/{name}/expenses/{paid_by}` : Supprime la dépense d'un participant.

*(Note : Une documentation Swagger interactive et complète est générée automatiquement à l'adresse `/api/apidoc/swagger` une fois le serveur lancé).*

---

## 🔐 Identifiants de test

L'application intègre des identifiants en mémoire pour tester les rôles.

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

### 2. Commandes d'exécution (Bash / PowerShell)
```bash
# 1. Télécharger et synchroniser les dépendances
uv sync

# 2. Initialiser la base de données
uv run --env-file dev.env flask --app archilog init-db

# 3. Lancer le serveur Web et l'API
uv run --env-file dev.env flask --app archilog --debug run

# 4. Lancer les tests unitaires de la logique métier
uv run pytest
```