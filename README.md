# 🎬 API de Classification de Films (Horreur / Comédie)

API de classification automatique de synopsis de films basée sur un modèle Deep Learning (Keras/TensorFlow) et TF-IDF. L'application est conteneurisée avec Docker, validée via une pipeline CI/CD (GitHub Actions) intégrant une barrière de qualité, et déployée sur Azure Container Apps.

---

## 📂 Structure du Projet

- `notebook.ipynb` : Notebook d'entraînement structuré en 8 parties (de la collecte/préparation jusqu'à l'évaluation et l'export).
- `model/` : Artefacts du modèle (`model.keras`, `vectoriseur.joblib`, `metrics.json` et dataset de référence).
- `src/` : Code source de l'API FastAPI (`app.py`) et script de barrière de qualité (`quality_gate.py`).
- `tests/` : Suite de tests unitaires et d'intégration (`pytest`).
- `.github/workflows/` : Pipeline de CI/CD automatisée.
- `dockerfile` & `.dockerignore` : Configuration du conteneur Docker.
- `config.yaml` : Configuration des seuils de métriques.
- `requirements.txt` : Dépendances Python.

---

## 🚀 Utilisation en Local

### 1. Installation des dépendances
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Exécution des tests et de la barrière de qualité
```bash
PYTHONPATH=. pytest
```

### 3. Lancement de l'API FastAPI
```bash
uvicorn src.app:app --reload --port 8000
```
- Documentation interactive (Swagger UI) : `http://localhost:8000/docs`
- Endpoint d'état de santé : `http://localhost:8000/health`

---

## 🐳 Déploiement Local avec Docker

### 1. Construction de l'image
```bash
docker build -t film-classifier-api .
```

### 2. Démarrage du conteneur
```bash
docker run -p 8000:8000 film-classifier-api
```

---

## 🔄 Pipeline CI/CD (GitHub Actions)

La pipeline automatise le contrôle qualité et la préparation de la livraison à chaque `push` :

1. **Test & Quality Gate** : Exécute les tests `pytest` et vérifie que la performance du modèle respecte le seuil défini dans `config.yaml`.
2. **Build & Validate** : Vérifie la construction et le bon fonctionnement du conteneur Docker.
3. **Publish** : Pousse l'image conteneurisée sur Azure Container Registry (ACR) étiquetée avec le SHA du commit Git (`COMMIT_HASH`).

---

## 📋 Procédure de Mise en Production & Journal des Versions

### Procédure de déploiement (Azure Container Apps)
1. Récupérer le tag correspondant au `COMMIT_HASH` validé par la pipeline CI/CD dans Azure Container Registry (ACR).
2. Déployer une nouvelle révision de l'application de conteneurs dans Azure Container Apps en ciblant cette image.
3. Vérifier le bon fonctionnement en interrogeant l'endpoint `/health` (qui renvoie le statut et le commit exact déployé).

### Journal des versions
- **v1.0.0** : Version initiale de l'API avec prédiction `/predict`, vérification `/health` (statut, version, commit SHA) et documentation `/docs`.