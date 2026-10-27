import yaml
import json
import os
import sys

def check_quality_gate():
    # 1. Charger la configuration
    config_path = "config.yaml"
    if not os.path.exists(config_path):
        print(f"❌ Erreur : Le fichier de configuration {config_path} est introuvable.")
        sys.exit(1)
        
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    min_f1 = config.get("min_f1_score", 0.70)
    min_size = config.get("min_test_size", 100)
    
    # 2. Charger les métriques du modèle
    metrics_path = "model/metrics.json"
    if not os.path.exists(metrics_path):
        print(f"❌ Erreur : Le fichier {metrics_path} est introuvable.")
        sys.exit(1)
        
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)
        
    # Récupération des valeurs
    f1_score = metrics.get("test_f1_score", 0.0)
    test_size = metrics.get("test_size", 0)
    
    print(f"--- 🔍 Vérification de la Barrière Qualité ---")
    print(f"Score F1 mesuré : {f1_score:.4f} (Seuil requis : >= {min_f1})")
    print(f"Taille du test : {test_size} (Seuil requis : >= {min_size})")
    
    # 3. Validation des seuils
    if f1_score < min_f1 or test_size < min_size:
        print("❌ ÉCHEC : Le modèle ne respecte pas les critères de qualité et est REJETÉ.")
        sys.exit(1)  # Fait échouer le script (très utile pour les pipelines CI/CD)
    else:
        print("✅ SUCCÈS : Le modèle respecte tous les critères et est ACCEPTÉ !")
        sys.exit(0)

if __name__ == "__main__":
    check_quality_gate()