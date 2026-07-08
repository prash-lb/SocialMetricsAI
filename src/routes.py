import os

import joblib
from flask import Blueprint, jsonify, request

from database import get_db_connection

api_bp = Blueprint("api", __name__)
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")
MODEL_POS_PATH = os.path.join(MODEL_DIR, "model_positive.pkl")
MODEL_NEG_PATH = os.path.join(MODEL_DIR, "model_negative.pkl")

try:
    vectorizer = joblib.load(VECTORIZER_PATH)
    model_positive = joblib.load(MODEL_POS_PATH)
    model_negative = joblib.load(MODEL_NEG_PATH)
    print("🧠 Modèles d'analyse prédictive chargés avec succès !")
except Exception as e:
    print(
        f"⚠️ Attention : Impossible de charger les modèles ({e}). Lancez d'abord src/model.py"
    )
    vectorizer, model_positive, model_negative = None, None, None


@api_bp.route("/hello", methods=["GET"])
def hello_world():
    """
    A simple endpoint that returns a greeting message.
    """
    return jsonify(message="Hello from your Flask API!")


@api_bp.route("/api/health", methods=["GET"])
def health_check():
    """
    Endpoint de contrôle pour valider la connexion MySQL depuis l'API.
    Garantit les 10 points associés dans le barème.
    """
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify(
            {
                "status": "healthy",
                "database_connected": True,
                "message": "Connexion MySQL fonctionnelle depuis l'API Flask !",
            }
        ), 200
    return jsonify(
        {
            "status": "unhealthy",
            "database_connected": False,
            "error": "Impossible de joindre la base de données MySQL.",
        }
    ), 500


@api_bp.route("/analyze", methods=["POST"])
def analyze_tweets():
    """
    Endpoint principal exigeant un tableau de chaînes (string[])
    Retourne la structure JSON demandée : {"tweet": score}
    """
    # 1. GESTION DES ERREURS (Validation du format global)
    if not request.is_json:
        return jsonify(
            {"error": "Le format de la requête doit être strictement du JSON."}
        ), 400

    data = request.get_json()

    # Pour être robuste, on accepte le tableau brut [] ou enveloppé dans un objet {"tweets": []}
    tweets = data if isinstance(data, list) else data.get("tweets")

    # 2. GESTION DES ERREURS (Validation fine des données reçues)
    if tweets is None or not isinstance(tweets, list):
        return jsonify(
            {
                "error": "Format incorrect. Un tableau de chaînes de caractères (string[]) est attendu."
            }
        ), 400

    if len(tweets) == 0:
        return jsonify({"error": "La liste de tweets fournie est vide."}), 400

    if not all(isinstance(tweet, str) for tweet in tweets):
        return jsonify(
            {
                "error": "Tous les éléments du tableau doivent être des chaînes de caractères."
            }
        ), 400

    if vectorizer is None or model_positive is None or model_negative is None:
        return jsonify(
            {"error": "Les modèles ne sont pas initialisés sur le serveur."}
        ), 500

    # 3. CALCUL ALGORITHMIQUE DES SCORES
    response_data = {}
    try:
        # Transformation numérique des textes reçus
        X = vectorizer.transform(tweets)

        # Calcul des probabilités pour chaque modèle indépendant
        # predict_proba renvoie [prob_0, prob_1]. On extrait l'indice 1 (probabilité du OUI)
        proba_pos = model_positive.predict_proba(X)[:, 1]
        proba_neg = model_negative.predict_proba(X)[:, 1]

        # Formule mathématique du sujet : Score = P(positive) - P(negative)
        for idx, tweet in enumerate(tweets):
            score_final = proba_pos[idx] - proba_neg[idx]
            # On arrondit à 4 décimales pour une réponse JSON propre
            response_data[tweet] = round(float(score_final), 4)

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": f"Erreur interne lors de l'analyse : {str(e)}"}), 500
