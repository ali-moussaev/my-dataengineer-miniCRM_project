import os  # Importation de la bibliothèque os pour la gestion des chemins de fichiers
import pandas as pd  # Importation de la bibliothèque pandas pour la manipulation de données
import re  # Importation de la bibliothèque re pour les expressions régulières
import sqlite3  # Importation de la bibliothèque sqlite3 pour la gestion de la base de données SQLite
import logging  # Importation de la bibliothèque logging pour la gestion des logs

# Configuration du logging
logging.basicConfig(
    filename='data_processing.log',  # Nom du fichier de log
    level=logging.INFO,  # Niveau de logging
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format des messages de log
)

def est_email_valide(email):
    """
    Verifie si l'email a un format valide.
    """
    if pd.isna(email):  # Vérifie si l'email est NaN
        return False
    motif = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # Motif regex pour valider les adresses email
    return bool(re.match(motif, email))  # Retourne True si l'email correspond au motif, sinon False

def create_database():
    """Cree une base de données SQLite et une table utilisateurs."""
    conn = sqlite3.connect('utilisateurs.db')  # Crée une connexion à la base de données (ou la crée si elle n'existe pas)
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
            logging.info("Fichier CSV charge avec succès.")
        except FileNotFoundError:
            logging.error(f"Le fichier {input_file} est introuvable.")
            return  # Arrêter le script
        except pd.errors.ParserError:
            logging.error(f"Erreur lors de la lecture du fichier {input_file}.")
            return  # Arrêter le script

        # Vérification des valeurs manquantes avant suppression
        logging.info(f"Valeurs manquantes avant suppression :\n{df.isna().sum()}")

        logging.info("Suppression des doublons...")
        df.drop_duplicates(inplace=True)  # Supprime les doublons dans le DataFrame

        logging.info("Suppression des lignes avec des valeurs manquantes...")
        df.dropna(inplace=True)  # Supprime les lignes contenant des valeurs manquantes

        logging.info("Validation des adresses email...")
        df['email_valide'] = df['email'].apply(est_email_valide)  # Applique la fonction de validation à chaque adresse email

        logging.info("Filtrage des lignes avec des emails valides...")
        df = df[df['email_valide']]  # Garde uniquement les lignes avec des adresses email valides

        logging.info("Verification et conversion de l'age...")
        df['age'] = pd.to_numeric(df['age'], errors='coerce')  # Convertit la colonne âge en numérique, les erreurs deviennent NaN
        df.dropna(subset=['age'], inplace=True)  # Supprime les lignes où l'âge est NaN
        df = df[(df['age'] >= 18) & (df['age'] <= 100)]  # Garde uniquement les âges réalistes

        logging.info("Enregistrement du DataFrame dans un nouveau fichier CSV...")
        df[['nom', 'prenom', 'email', 'age', 'pays']].to_csv(output_file, index=False, float_format='%.0f')  # Enregistre le DataFrame avec la colonne prénom
        logging.info(f"Les donnees ont ete enregistrees dans '{output_file}'.")  # Confirmation de l'enregistrement

        # Créer la base de données et la table utilisateurs
        create_database()

        # Insérer les données dans la table utilisateurs
        conn = sqlite3.connect('utilisateurs.db')  # Connexion à la base de données
        cursor = conn.cursor()  # Crée un curseur pour exécuter des commandes SQL

        # Démarrer une transaction
        try:
            cursor.executemany('''
                REPLACE INTO utilisateurs (nom, prenom, email, age, pays) VALUES (?, ?, ?, ?, ?)
            ''', df[['nom', 'prenom', 'email', 'age', 'pays']].values.tolist())  # Utilisez 'prenom' ici
            conn.commit()  # Valide les changements
            logging.info("Les donnees ont ete inserees dans la base de donnees utilisateurs.db.")
        except sqlite3.IntegrityError as e:  # Gestion des erreurs d'intégrité (par exemple, doublons d'email)
            logging.error(f"Erreur d'intégrité : {e}")  # Enregistre un message d'erreur si une contrainte est violée
            conn.rollback()  # Annule les changements en cas d'erreur
        finally:
            conn.close()  # Ferme la connexion

        logging.info("===================================")
        logging.info("Traitement du fichier CSV terminé")
        logging.info("===================================")

    except Exception as e:  # Gestion des exceptions
        logging.error(f"Une erreur s'est produite : {e}")  # Enregistre un message d'erreur si une exception est levée

if __name__ == "__main__":  # Vérifie si le script est exécuté directement
    main()  # Appelle la fonction main pour exécuter le code
