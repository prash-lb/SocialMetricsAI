import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from database import get_db_connection

def evaluate_model_performance():
    conn = get_db_connection()
    if conn is None:
        print("Impossible de se connecter à la base de données.")
        return
    
    df = pd.read_sql("SELECT text, positive, negative FROM tweets", conn)
    conn.close()
    
    if len(df) < 10:
        print(" Pas assez de données pour faire une validation croisée.")
        return

    print(" --- DÉBUT DE L'ÉVALUATION DU MODÈLE --- \n")

    X_train, X_val, y_train, y_val = train_test_split(
        df['text'], 
        df[['positive', 'negative']], 
        test_size=0.20, 
        random_state=42
    )

    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_val_tfidf = vectorizer.transform(X_val)


    print("=== 1. PERFORMANCES DU MODÈLE POSITIF ===")
    model_pos = LogisticRegression()
    model_pos.fit(X_train_tfidf, y_train['positive'])
    preds_pos = model_pos.predict(X_val_tfidf)
    
    print("\n📜 Rapport de Classification (Positif) :")
    print(classification_report(y_val['positive'], preds_pos, zero_division=0))
    
    print(" Matrice de Confusion (Positif) :")
    cm_pos = confusion_matrix(y_val['positive'], preds_pos)
    print(cm_pos)

    print("\n=== 2. PERFORMANCES DU MODÈLE NÉGATIF ===")
    model_neg = LogisticRegression()
    model_neg.fit(X_train_tfidf, y_train['negative'])
    preds_neg = model_neg.predict(X_val_tfidf)
    
    print("\n📜 Rapport de Classification (Négatif) :")
    print(classification_report(y_val['negative'], preds_neg, zero_division=0))
    
    print(" Matrice de Confusion (Négatif) :")
    cm_neg = confusion_matrix(y_val['negative'], preds_neg)
    print(cm_neg)

if __name__ == "__main__":
    evaluate_model_performance()