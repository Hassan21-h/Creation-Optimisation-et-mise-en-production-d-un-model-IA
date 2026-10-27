import pytest
from fastapi.testclient import TestClient
import json
import os

# On importe l'application depuis le dossier src
from src.app import app

client = TestClient(app)

def test_health_check():
    """Vérifie que l'API répond et que le statut est ok"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_predict_valid():
    """Vérifie qu'un texte valide renvoie bien une prédiction correcte"""
    response = client.get("/predict?text=This+movie+was+absolutely+fantastic+and+wonderful!")
    assert response.status_code == 200
    data = response.json()
    assert "classe" in data
    assert "probabilité" in data
    assert data["classe"] in [0, 1]

def test_predict_too_short():
    """Vérifie qu'un texte trop court (cas limite) est refusé"""
    response = client.get("/predict?text=Hi")
    assert response.status_code == 400

def test_predict_empty():
    """Vérifie qu'un texte vide (invalide) est refusé"""
    response = client.get("/predict?text=")
    assert response.status_code == 400

def test_model_metrics_threshold():
    """Vérifie que le modèle atteint un score minimum (ex: F1 > 0.5)"""
    metrics_path = "model/metrics.json"
    assert os.path.exists(metrics_path), "Le fichier metrics.json est introuvable."
    
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    
    # On récupère directement la clé test_f1_score
    f1_score = metrics.get("test_f1_score", 0.0)    
    
    # Seuil minimal exigé
    assert f1_score >= 0.5, f"Le score F1 ({f1_score}) est inférieur au seuil minimal de 0.5"