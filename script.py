import os  # Importation de la bibliothèque os pour la gestion des chemins de fichiers
import pandas as pd  # Importation de la bibliothèque pandas pour la manipulation de données
import re  # Importation de la bibliothèque re pour les expressions régulières
import sqlite3  # Importation de la bibliothèque sqlite3 pour la gestion de la base de données SQLite
import logging  # Importation de la bibliothèque logging pour la gestion des logs
from logging.handlers import RotatingFileHandler  # Importation du gestionnaire de fichiers rotatifs

# Configuration avancée du logging avec rotation
log_handler = RotatingFileHandler('data_processing.log', maxBytes=1000000, backupCount=5)
logging.basicConfig(
    handlers=[log_handler],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_db_connection():
    """Crée et retourne une connexion SQLite."""
    return sqlite3.connect('utilisateurs.db')

def est_email_valide(email):
    """
    Vérifie si l'email a un format valide.
    """
    if pd.isna(email):  # Vérifie si l'email est NaN
        return False
    # Expression régulière optimisée pour valider les adresses email
    motif = r"^(?!.*\.\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(motif, email))  # Retourne True si l'email correspond au motif, sinon False

def create_database():
    """Cree une base de données SQLite et une table utilisateurs."""
    conn = get_db_connection()  # Obtenir la connexion à la base de données
    cursor = conn.cursor()  # Crée un curseur pour exécuter des commandes SQL

    # Supprimer la table existante si elle existe
    cursor.execute('DROP TABLE IF EXISTS utilisateurs')

    # Création de la table utilisateurs avec une contrainte d'unicité sur l'email
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            pays TEXT NOT NULL
        )
    ''')
    conn.commit()  # Valide les changements
    conn.close()  # Ferme la connexion

def main():
    # Chemins de fichiers dynamiques
    base_path = os.path.dirname(os.path.abspath(__file__))  # Chemin du script
    input_file = os.path.join(base_path, 'dataset_startup.csv')  # Chemin d'accès au fichier d'entrée
    output_file = os.path.join(base_path, 'newdataset_startup.csv')  # Chemin d'accès au fichier de sortie

    try:
        logging.info("===================================")
        logging.info("Debut du traitement du fichier CSV")
        logging.info("===================================")

        logging.info("Chargement du fichier CSV...")
        try:
            df = pd.read_csv(
                input_file,  # Utilisation du chemin dynamique
                sep=',',  # Spécifie le séparateur utilisé dans le fichier CSV (ici, une virgule)
                skipinitialspace=True,  # Ignore les espaces après le séparateur
                na_values=["NA", "n/a"]  # Liste des valeurs considérées comme manquantes dans le DataFrame
            )
            logging.info("Fichier CSV charge avec succes.")
        except FileNotFoundError:
            logging.error(f"Le fichier {input_file} est introuvable.")
            return  # Arrêter le script
        except pd.errors.ParserError:
            logging.error(f"Erreur lors de la lecture du fichier {input_file}.")
            return  # Arrêter le script

        # Vérification des colonnes obligatoires
        colonnes_obligatoires = {'nom', 'prenom', 'email', 'age', 'pays'}
        if not colonnes_obligatoires.issubset(df.columns):
            logging.error(f"Colonnes manquantes dans le fichier CSV : {colonnes_obligatoires - set(df.columns)}")
            return  # Arrêter le script

        # Vérification des valeurs manquantes avant suppression
        logging.info(f"Valeurs manquantes avant suppression :\n{df.isna().sum()}")

        logging.info("Suppression des doublons...")
        df.drop_duplicates(inplace=True)  # Supprime les doublons dans le DataFrame

        logging.info("Suppression des lignes avec des valeurs manquantes...")
        df.dropna(inplace=True)  # Supprime les lignes contenant des valeurs manquantes

        # Vérification de la présence de la colonne 'email'
        if 'email' in df.columns:
            logging.info("Validation des adresses email...")
            df['email_valide'] = df['email'].apply(est_email_valide)  # Applique la fonction de validation à chaque adresse email
        else:
            logging.error("La colonne 'email' est absente du fichier CSV.")
            return  # Arrêter le script

        logging.info("Filtrage des lignes avec des emails valides...")
        df = df[df['email_valide']]  # Garde uniquement les lignes avec des adresses email valides

        logging.info("Verification et conversion de l'age...")
        df = df[df['age'].apply(lambda x: str(x).isdigit())]  # Filtrer les valeurs non numériques
        df['age'] = df['age'].astype(int)  # Convertit la colonne âge en entier
        df = df[df['age'].between(18, 100)]  # Garde uniquement les âges réalistes

        # Vérification de la longueur des champs
        df = df[df['nom'].str.len() <= 50]  # Limite la longueur du nom à 50 caractères
        df = df[df['prenom'].str.len() <= 50]  # Limite la longueur du prénom à 50 caractères
        df = df[df['pays'].str.len() <= 30]  # Limite la longueur du pays à 30 caractères

        logging.info("Enregistrement du DataFrame dans un nouveau fichier CSV...")
        df[['nom', 'prenom', 'email', 'age', 'pays']].to_csv(output_file, index=False, float_format='%.0f')  # Enregistre le DataFrame avec la colonne prénom
        logging.info(f"Les donnees ont ete enregistrees dans '{output_file}'.")  # Confirmation de l'enregistrement

        # Créer la base de données et la table utilisateurs
        create_database()

        # Insérer les données dans la table utilisateurs
        conn = get_db_connection()  # Obtenir la connexion à la base de données
        cursor = conn.cursor()  # Crée un curseur pour exécuter des commandes SQL

        # Démarrer une transaction
        try:
            cursor.executemany('''
                INSERT INTO utilisateurs (nom, prenom, email, age, pays)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET age = excluded.age, pays = excluded.pays;
            ''', df[['nom', 'prenom', 'email', 'age', 'pays']].values.tolist())  # Utilisez 'prenom' ici
            conn.commit()  # Valide les changements
            logging.info("Les donnees ont ete inserees dans la base de donnees utilisateurs.db.")
        except sqlite3.IntegrityError as e:  # Gestion des erreurs d'intégrité (par exemple, doublons d'email)
            logging.error(f"Erreur d'integrité : {e}")  # Enregistre un message d'erreur si une contrainte est violée
            conn.rollback()  # Annule les changements en cas d'erreur
        finally:
            conn.close()  # Ferme la connexion

        logging.info("===================================")
        logging.info("Traitement du fichier CSV termine")
        logging.info("===================================")

    except Exception as e:  # Gestion des exceptions
        logging.exception("Une erreur inattendue s'est produite")  # Enregistre un message d'erreur si une exception est levée

if __name__ == "__main__":  # Vérifie si le script est exécuté directement
    main()  # Appelle la fonction main pour exécuter le code
