miniCRM Project
Ce projet est une application de mini-CRM destinée à démontrer une approche professionnelle de la manipulation et du nettoyage de données, ainsi que leur stockage dans une base de données SQLite.

Description
Ce projet lit un fichier CSV contenant des informations d'utilisateurs, effectue un nettoyage et une validation des données (suppression des doublons, gestion des valeurs manquantes, validation des emails et vérification de l'âge) puis enregistre les données validées dans :

Un nouveau fichier CSV.
Une base de données SQLite, en utilisant une logique de mise à jour en cas de conflit sur l'email.
Le projet utilise également un système de logging avancé avec rotation des fichiers pour faciliter le suivi et le débogage.

Fonctionnalités
Lecture du fichier CSV : Importation des données utilisateur à partir d'un CSV.
Nettoyage des données : Suppression des doublons et des lignes contenant des valeurs manquantes.
Validation des emails : Vérification du format des adresses email avec une expression régulière optimisée.
Filtrage des âges : Conversion de la colonne age en entier et filtrage pour ne garder que des âges réalistes (entre 18 et 100 ans).
Vérification de la longueur des champs : Limitation de la taille des champs nom, prenom et pays pour éviter des valeurs aberrantes.
Stockage des données :
Enregistrement des données nettoyées dans un nouveau fichier CSV.
Insertion sécurisée dans une base de données SQLite avec gestion des conflits via ON CONFLICT(email) DO UPDATE.
Gestion des logs : Enregistrement détaillé des opérations dans un fichier de log avec rotation pour éviter la saturation.
Technologies utilisées
Python 3
Pandas pour la manipulation des données
SQLite3 pour la gestion de la base de données
Logging (avec RotatingFileHandler) pour le suivi des opérations
Regex pour la validation des adresses email
Prérequis
Python 3 installé sur votre machine.

Installation des bibliothèques Python nécessaires. Vous pouvez installer pandas via pip :

bash
Copier
Modifier
pip install pandas
(Les modules sqlite3, logging et re font partie de la bibliothèque standard de Python.)

Structure du projet
graphql
Copier
Modifier
.
├── dataset_startup.csv       # Fichier CSV d'entrée contenant les données utilisateur.
├── newdataset_startup.csv    # Fichier CSV généré après le nettoyage et la validation des données.
├── data_processing.log       # Fichier de log généré par le script.
├── utilisateurs.db           # Base de données SQLite contenant les données validées.
└── main.py                   # Script principal du projet.
Utilisation
Préparez le fichier CSV
Placez votre fichier dataset_startup.csv dans le répertoire du projet.

Exécutez le script
Dans un terminal, lancez la commande suivante :

bash
Copier
Modifier
python main.py
Résultats

Un nouveau fichier CSV (newdataset_startup.csv) sera généré avec les données nettoyées et validées.
Les données seront insérées dans la base de données SQLite utilisateurs.db.
Les opérations et éventuelles erreurs seront consignées dans data_processing.log.
Améliorations futures
Tests unitaires : Ajouter des tests pour les fonctions clés (par exemple, est_email_valide) afin d'assurer la robustesse du code.
Interface utilisateur : Développer une interface graphique ou une API pour interagir avec les données.
Extensions fonctionnelles : Ajouter des fonctionnalités pour mettre à jour, supprimer ou rechercher des enregistrements dans le CRM.
Sécurité : Renforcer la sécurité lors du traitement et du stockage des données sensibles.
Auteur
Ali Moussaev
Projet réalisé dans le cadre d'une recherche d'alternance.
Licence
Ce projet est sous licence MIT. Vous pouvez consulter le fichier LICENSE pour plus de détails.