import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from database import get_db_connection

# Définition du dossier de sauvegarde des modèles
MODEL_DIR = os.path.join(os.path.dirname(__file__), '../models')
os.makedirs(MODEL_DIR, exist_ok=True)

VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')
MODEL_POS_PATH = os.path.join(MODEL_DIR, 'model_positive.pkl')
MODEL_NEG_PATH = os.path.join(MODEL_DIR, 'model_negative.pkl')

def load_data_from_db():
    """Récupère les tweets et les annotations depuis MySQL."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    # Utilisation de pandas pour lire la table SQL directement dans un DataFrame
    query = "SELECT text, positive, negative FROM tweets"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def train_model():
    """Entraîne le vectoriseur et les modèles de Régression Logistique."""
    df = load_data_from_db()
    
    if df is None or df.empty:
        print("⚠️ La base de données est vide. Insérez des données avant d'entraîner le modèle.")
        return False
    
    print(f"📊 Données chargées : {len(df)} tweets trouvés pour l'entraînement.")
    
    # 1. Vectorisation du texte (TF-IDF)
    # Convertit les phrases en matrices numériques en éliminant les mots vides anglais (the, is, etc.)
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X = vectorizer.fit_transform(df['text'])
    
    # 2. Définition des étiquettes (labels)
    y_positive = df['positive']
    y_negative = df['negative']
    
    # 3. Entraînement du modèle de positivité
    print("🧠 Entraînement du modèle de détection positive...")
    model_positive = LogisticRegression()
    model_positive.fit(X, y_positive)
    
    # 4. Entraînement du modèle de négativité
    print("🧠 Entraînement du modèle de détection négative...")
    model_negative = LogisticRegression()
    model_negative.fit(X, y_negative)
    
    # 5. Sauvegarde des modèles et du vectoriseur
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(model_positive, MODEL_POS_PATH)
    joblib.dump(model_negative, MODEL_NEG_PATH)
    
    print("🚀 Étape 2 validée : Les modèles ont été entraînés et sauvegardés avec succès dans /models/ !")
    return True

if __name__ == "__main__":
    train_model()