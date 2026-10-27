# Utiliser une image Python officielle légère
FROM python:3.13-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Récupérer le hash du commit passé par le workflow GitHub Actions
ARG COMMIT_HASH="inconnu"
ENV COMMIT_HASH=$COMMIT_HASH

# Copier et installer les dépendances en premier (pour optimiser le cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source, le modèle et la config dans le conteneur
COPY src/ ./src/
COPY model/ ./model/
COPY config.yaml .

# Exposer le port sur lequel l'application tourne
EXPOSE 8000

# Commande pour lancer l'application avec Uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]