# 1. Utiliser une image Python officielle et légère
FROM python:3.10-slim

# 2. Définir le dossier de travail dans le conteneur
WORKDIR /app

# 3. Copier le fichier des dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier tout le reste du code du projet dans le conteneur
COPY . .

# 5. Informer Docker que l'API écoute sur le port 5000
EXPOSE 5000

# 6. Commande par défaut pour lancer l'API
CMD ["python", "src/app.py"]