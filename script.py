import pandas as pd  # Importation de la bibliothèque pandas pour la manipulation de données
import re  # Importation de la bibliothèque re pour les expressions régulières
import sqlite3  # Importation de la bibliothèque sqlite3 pour la gestion de la base de données SQLite

def est_email_valide(email):
    """
    Vérifie si l'email a un format valide.
    """
    if pd.isna(email):  # Vérifie si l'email est NaN
        return False
    motif = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # Motif regex pour valider les adresses email
    return bool(re.match(motif, email))  # Retourne True si l'email correspond au motif, sinon False

def create_database():
    """Crée une base de données SQLite et une table utilisateurs."""
    conn = sqlite3.connect('utilisateurs.db')  # Crée une connexion à la base de données (ou la crée si elle n'existe pas)
    cursor = conn.cursor()  # Crée un curseur pour exécuter des commandes SQL

    # Création de la table utilisateurs avec une contrainte d'unicité sur l'email
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,  -- Contrainte d'unicité sur l'email
            âge INTEGER NOT NULL,
            pays TEXT NOT NULL
        )
    ''')
    conn.commit()  # Valide les changements
    conn.close()  # Ferme la connexion

def main():
    try:
        print("Chargement du fichier CSV...")
        df = pd.read_csv(
            'C:/Users/Shonan/Desktop/MyDataEngineerProject/myproject_miniCRM_startup/dataset_startup.csv',  # Chemin d'accès au fichier CSV
            sep=',',  # Spécifie le séparateur utilisé dans le fichier CSV (ici, une virgule)
            skipinitialspace=True,  # Ignore les espaces après le séparateur
            na_values=["NA", "n/a"]  # Liste des valeurs considérées comme manquantes dans le DataFrame
        )
        print("Fichier CSV chargé avec succès.")

        print("Affichage du DataFrame...")
        print(df)  # Affiche le DataFrame chargé dans la console

        print("Suppression des doublons...")
        df.drop_duplicates(inplace=True)  # Supprime les doublons dans le DataFrame

        print("Suppression des lignes avec des valeurs manquantes...")
        df.dropna(inplace=True)  # Supprime les lignes contenant des valeurs manquantes

        print("Validation des adresses email...")
        df['email_valide'] = df['email'].apply(est_email_valide)  # Applique la fonction de validation à chaque adresse email

        print("Filtrage des lignes avec des emails valides...")
        df = df[df['email_valide']]  # Garde uniquement les lignes avec des adresses email valides

        print("Vérification et conversion de l'âge...")
        df['âge'] = pd.to_numeric(df['âge'], errors='coerce')  # Convertit la colonne âge en numérique, les erreurs deviennent NaN
        df.dropna(subset=['âge'], inplace=True)  # Supprime les lignes où l'âge est NaN
        df = df[(df['âge'] >= 18) & (df['âge'] <= 100)]  # Garde uniquement les âges réalistes

        print("Enregistrement du DataFrame dans un nouveau fichier CSV...")
        output_file = 'C:/Users/Shonan/Desktop/MyDataEngineerProject/myproject_miniCRM_startup/newdataset_startup.csv'  # Chemin d'accès pour le nouveau fichier
        df.to_csv(output_file, index=False)  # Enregistre le DataFrame dans le fichier CSV sans l'index
        print(f"Les données ont été enregistrées dans '{output_file}'.")  # Confirmation de l'enregistrement

        # Créer la base de données et la table utilisateurs
        create_database()

        # Insérer les données dans la table utilisateurs
        conn = sqlite3.connect('utilisateurs.db')  # Connexion à la base de données
        cursor = conn.cursor()  # Crée un curseur pour exécuter des commandes SQL

        # Démarrer une transaction
        try:
            for index, row in df.iterrows():  # Itère sur chaque ligne du DataFrame
                cursor.execute('''
                    INSERT INTO utilisateurs (nom, email, âge, pays) VALUES (?, ?, ?, ?)
                ''', (row['nom'], row['email'], row['âge'], row['pays']))  # Insère les données dans la table
            conn.commit()  # Valide les changements
            print("Les données ont été insérées dans la base de données utilisateurs.db.")
        except sqlite3.IntegrityError as e:  # Gestion des erreurs d'intégrité (par exemple, doublons d'email)
            print(f"Erreur d'intégrité : {e}")  # Affiche un message d'erreur si une contrainte est violée
            conn.rollback()  # Annule les changements en cas d'erreur
        finally:
            conn.close()  # Ferme la connexion

    except Exception as e:  # Gestion des exceptions
        print(f"Une erreur s'est produite : {e}")  # Affiche un message d'erreur si une exception est levée

if __name__ == "__main__":  # Vérifie si le script est exécuté directement
    main()  # Appelle la fonction main pour exécuter le code
