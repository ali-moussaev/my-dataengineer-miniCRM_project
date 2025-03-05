# Mini CRM Startup - Traitement et Validation de Données CSV

## 📋 Description
Ce projet est un Mini CRM conçu pour traiter et valider des fichiers CSV contenant des données utilisateurs. Il effectue plusieurs opérations de validation, de nettoyage et stocke les données dans une base de données SQLite, tout en assurant l'intégrité et la qualité des données.

## 🚀 Fonctionnalités
- Validation stricte des adresses email
- Vérification de l'âge (18-100 ans)
- Suppression des doublons
- Nettoyage des données manquantes
- Stockage dans une base de données SQLite
- Système de logging avec rotation des fichiers
- Gestion des erreurs avancée
- Validation des formats de données

## 📦 Prérequis
- Python 3.7+
- pip (gestionnaire de paquets Python)

## 🛠️ Installation

1. Clonez le repository :
```bash
git clone https://github.com/Shonan/myproject_miniCRM_startup.git
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
Le fichier CSV d'entrée **doit** contenir exactement les colonnes suivantes (les noms doivent être identiques) :
- `nom` (max 50 caractères)
- `prenom` (max 50 caractères)
- `email` (format valide)
- `age` (18-100)
- `pays` (max 30 caractères)

### Exemple de fichier CSV valide (dataset_startup.csv) :
```csv
nom,prenom,email,age,pays
Dupont,Jean,jean.dupont@example.com,25,France
Martin,Sophie,sophie.martin@email.com,30,Belgique
Garcia,Carlos,carlos.garcia@mail.com,45,Espagne
```

## 🔧 Utilisation
1. Placez votre fichier CSV nommé `dataset_startup.csv` dans le même répertoire que le script
2. Exécutez le script :
```bash
python script.py
```

## 📊 Résultats
Le script génère trois types de fichiers :

1. **Fichier CSV nettoyé** (`newdataset_startup.csv`) :
   - Contient uniquement les données valides
   - Suppression des doublons et des entrées invalides

2. **Base de données SQLite** (`utilisateurs.db`) :
   - Stockage permanent des données
   - Structure optimisée pour les requêtes

3. **Fichiers de log** (`data_processing.log`) :
   - Suivi détaillé des opérations
   - Rotation automatique des fichiers (max 5 fichiers de 1MB)

### Exemple de sortie de log :
```log
2024-03-06 10:00:00 - INFO - ===================================
2024-03-06 10:00:00 - INFO - Debut du traitement du fichier CSV
2024-03-06 10:00:01 - INFO - Chargement du fichier CSV...
2024-03-06 10:00:01 - INFO - Fichier CSV charge avec succes
2024-03-06 10:00:02 - INFO - Validation des adresses email...
2024-03-06 10:00:03 - WARNING - Email invalide trouve : test@invalid
2024-03-06 10:00:04 - INFO - Donnees inserees dans la base de donnees
```

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

### Extension du Projet
Le projet peut être étendu de plusieurs manières :
- Ajout de nouvelles validations de données
- Intégration d'une interface utilisateur
- Export vers d'autres formats de base de données
- Ajout de rapports statistiques

## 📝 Logs
Les logs sont générés dans `data_processing.log` avec rotation automatique des fichiers. Ils incluent :
- Horodatage précis
- Niveau de gravité (INFO, WARNING, ERROR)
- Description détaillée des opérations
- Traçage des erreurs avec stack trace

## ⚠️ Notes importantes
- Les données sensibles ne sont pas versionnées (fichiers .env, base de données)
- Les fichiers de log sont exclus du versionnement
- Vérifiez les permissions nécessaires pour l'écriture des fichiers
- Assurez-vous que les noms de colonnes dans votre CSV correspondent exactement à ceux attendus

## 🤝 Contribution
Les contributions sont les bienvenues ! Pour contribuer :
1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.