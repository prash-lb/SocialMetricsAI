#!/bin/bash

# Script pour automatiser le réentraînement du modèle SocialMetricsAI

echo "--- Début du réentraînement automatisé : $(date) ---"

docker exec socialmetrics_api python src/model.py

echo "--- Fin du réentraînement automatisé ---"