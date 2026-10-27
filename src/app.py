from fastapi import FastAPI, HTTPException

import joblib
import tensorflow as tf
import json
import os

model = tf.keras.models.load_model("model/model.keras")
vectorizer = joblib.load("model/vectoriseur.joblib")
with open("model/metrics.json", "r", encoding="utf-8") as f:
    metrics = json.load(f)

app = FastAPI()

COMMIT_HASH = os.getenv("COMMIT_HASH", "inconnu")

# Fonction pour health
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_version": metrics.get("version", "1.0"),
        "commit": COMMIT_HASH
    }


# Fonction pour predict
@app.get("/predict")
def predict_movie(text):
    if not text or len(text.strip()) <10:
        raise HTTPException(status_code=400, detail="Le texte est trop court ou vide.")
    X_vec = vectorizer.transform([text]).toarray()
    proba = float(model.predict(X_vec).item())
    if proba > 0.5:
        classe = 1
    else: 
        classe = 0

    return {
        "classe": classe,
        "probabilité": proba,
        "model_version" : metrics.get("version", "1.0")
    }

# Lancer avec uvicorn src.app:app --reload

# Fonction pour test hello
@app.get("/hello")
def say_hello():
    return {"message": "Hello depuis le conteneur Azure !"}