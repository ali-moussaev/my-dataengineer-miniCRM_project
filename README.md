# Mini CRM Startup - Traitement de Données CSV

## 📋 Description
Ce projet est un script Python conçu pour traiter des fichiers CSV contenant des données utilisateurs. Il effectue plusieurs opérations de validation, de nettoyage et stocke les données dans une base de données SQLite.

## 🚀 Fonctionnalités
- Validation des adresses email
- Vérification de l'âge (18-100 ans)
- Suppression des doublons
- Nettoyage des données manquantes
- Stockage dans une base de données SQLite
- Système de logging avec rotation des fichiers
- Gestion des erreurs avancée

## 📦 Prérequis
- Python 3.x
- pip (gestionnaire de paquets Python)

## 🛠️ Installation

1. Clonez le repository :
```bash
git clone [votre-url-repository]
cd myproject_miniCRM_startup
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Pour Linux/Mac
# ou
venv\Scripts\activate  # Pour Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 📝 Format du fichier CSV attendu
Le fichier CSV d'entrée doit contenir les colonnes suivantes :
- nom (max 50 caractères)
- prenom (max 50 caractères)
- email (format valide)
- age (18-100)
- pays (max 30 caractères)

## 🔧 Utilisation
1. Placez votre fichier CSV nommé `dataset_startup.csv` dans le même répertoire que le script
2. Exécutez le script :
```bash
python script.py
```

## 📊 Résultats
Le script génère :
- Un nouveau fichier CSV nettoyé (`newdataset_startup.csv`)
- Une base de données SQLite (`utilisateurs.db`)
- Des fichiers de log (`data_processing.log`)

## 🔍 Structure du Projet
```
myproject_miniCRM_startup/
│
├── script.py              # Script principal
├── dataset_startup.csv    # Fichier d'entrée
├── requirements.txt       # Dépendances du projet
├── .gitignore            # Fichiers ignorés par Git
└── README.md             # Documentation
```

## 📝 Logs
Les logs sont générés dans `data_processing.log` avec rotation automatique des fichiers (max 5 fichiers de 1MB chacun).

## ⚠️ Notes importantes
- Les données sensibles ne sont pas versionnées (fichiers .env, base de données)
- Les fichiers de log sont exclus du versionnement
- Vérifiez les permissions nécessaires pour l'écriture des fichiers

## 🤝 Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une pull request.

## 📄 Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 