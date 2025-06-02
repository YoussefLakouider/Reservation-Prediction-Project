# -*- coding: utf-8 -*-
import pandas as pd
import datetime 
import unittest
from sqlalchemy import create_engine, text
import pandas as pd
import os

#fonction pour se connecter à Snowflake

def connect_to_snowflake(user, password, account, warehouse, database, schema, role):
    try:

        snowflake_url = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}"

        engine = create_engine(snowflake_url)

        with engine.connect() as conn:
            print("Connexion réussie à Snowflake")
            return engine
        
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return  None
    
# Fonction pour extraire les données de Snowflake

def load_data(query, engine):
    try:
        df = pd.read_sql_query(query, engine)
        print("Données extraites avec succès.")
        return df
    except Exception as e:
        print(f"Erreur d'extraction des données : {e}")
        return None

# Fonction pour transformer les données
def transform_data(df_ventes, df_promotions):
    df_ventes = df_ventes[df_ventes["nb_produits"].astype(str).str.replace('.', '', 1).str.isnumeric()].copy()
    df_ventes["nb_produits"] = df_ventes["nb_produits"].astype(float)
    df_ventes = df_ventes.dropna(subset=["pu_produit_ht", "nb_produits"])
    df_ventes["date_achat"] = pd.to_datetime(df_ventes["date_achat"])
    df_promotions["date_debut_promo"] = pd.to_datetime(df_promotions["date_debut_promo"])
    df_promotions["date_fin_promo"] = pd.to_datetime(df_promotions["date_fin_promo"])
    return df_ventes, df_promotions

# Fonction pour calculer le chiffre d'affaires hors promotions

def calcul_chiffre_affaires_hors_promotions(df_ventes, df_promotions):
    df_ventes, df_promotions = transform_data(df_ventes, df_promotions)
    
    df_ventes["mois"] = df_ventes["date_achat"].dt.to_period("M")

    df_ventes["in_promo"] = False
    for _, promo in df_promotions.iterrows():
        mask = (
            (df_ventes["nom_produit"] == promo["libelle_produit"]) &
            (df_ventes["date_achat"] >= promo["date_debut_promo"]) &
            (df_ventes["date_achat"] <= promo["date_fin_promo"])
        )
        df_ventes.loc[mask, "in_promo"] = True

    df_hors_promo = df_ventes[~df_ventes["in_promo"]].copy()
    df_hors_promo["CA_HT"] = df_hors_promo["pu_produit_ht"] * df_hors_promo["nb_produits"]
    df_ca = df_hors_promo.groupby(["mois", "nom_agence"])["CA_HT"].sum().reset_index()
    return df_ca



def calcul_total_paye_par_client(df_ventes, df_promotions):
    df_ventes["prix_total_paye"] = df_ventes["nb_produits"] * df_ventes["pu_produit_ht"] 
    for _, promo in df_promotions.iterrows():
        mask = (
            (df_ventes["nom_produit"] == promo["libelle_produit"]) & 
            (df_ventes["date_achat"] >= promo["date_debut_promo"]) &
            (df_ventes["date_achat"] <= promo["date_fin_promo"])
        )
        df_ventes.loc[mask, "prix_total_paye"] *= (1 - promo["taux_reduction"] / 100)
        
    df_total_clients = df_ventes.groupby("nom_prenom", as_index=False)["prix_total_paye"].sum()
    return df_total_clients

# Fonction pour calculer le prix total (pour le test unitaire) 
def calcul_prix_total(nb_produits, pu_produit_ht, taux_reduction):
    return nb_produits * pu_produit_ht * (1 - taux_reduction)

class TestCalculPrixTotal(unittest.TestCase):
    def test_calcul(self):
        self.assertEqual(calcul_prix_total(5, 100, 0.2), 400)
        self.assertEqual(calcul_prix_total(3, 200, 0.1), 540)
        self.assertEqual(calcul_prix_total(1, 150, 0), 150)
        self.assertEqual(calcul_prix_total(0, 100, 0.5), 0)


def create_table(engine):
    create_sql = """
    CREATE OR REPLACE TABLE PRIX_PROMO (
        NOM_PRENOM STRING,
        PU_PRODUIT_HT FLOAT,
        NB_PRODUITS INT,
        TAUX_REDUCTION FLOAT,
        PRIX_TOTAL_PAYE FLOAT
    );
    """

    with engine.connect() as conn:
        conn.execute(text(create_sql))
        print("Table PRIX_PROMO créée avec succès.")



if __name__ == "__main__":
    # Connexion à Snowflake
    password = os.getenv('PASSWORD_SNOWFLAKE')
    user = os.getenv('USER_SNOWFLAKE')
    account = os.getenv('ACCOUNT_SNOWFLAKE')
    warehouse = "COMPUTE_WH"
    database = "RESERVATIONS"
    schema = "PUBLIC"
    role = "SYSADMIN"
    engine = connect_to_snowflake(user, password, account, warehouse, database, schema, role)
    if engine:
        # Chargement des données
        query_ventes = "SELECT * FROM VENTES"
        query_promotions = "SELECT * FROM PROMO"
        df_ventes = load_data(query_ventes, engine)
        df_promotions = load_data(query_promotions, engine)
      
        # Transformation des données
        df_ventes, df_promotions = transform_data(df_ventes, df_promotions)
        print("Données transformées avec succès.")
        
        
        # Calcul du chiffre d'affaires hors promotions
        df_ca_hors_promo = calcul_chiffre_affaires_hors_promotions(df_ventes, df_promotions)
        print(df_ca_hors_promo)

        # Calcul du total payé par client
        df_total_clients = calcul_total_paye_par_client(df_ventes, df_promotions)
        print(df_total_clients)
        # Test unitaire
        unittest.main(argv=[''], exit=False)
        
        # Création de la table PRIX_PROMO
        create_table(engine)
        
        # Insertion des données dans la table PRIX_PROMO
        data = [
                ("Nom1 Prenom1", 100.0, 5, 0.20, calcul_prix_total(5, 100.0, 0.20)),
                ("Nom2 Prenom2", 200.0, 3, 0.10, calcul_prix_total(3, 200.0, 0.10)),
                ("Nom3 Prenom3", 300.0, 7, 0.30, calcul_prix_total(7, 300.0, 0.30))
            ]


        df = pd.DataFrame(data, columns=[
            "NOM_PRENOM", "PU_PRODUIT_HT", "NB_PRODUITS", "TAUX_REDUCTION", "PRIX_TOTAL_PAYE"
        ])
        df.to_sql("PRIX_PROMO", engine, if_exists="append", index=False)
        print("Données insérées avec succès dans la table PRIX_PROMO.")
        
        # Vérification de l'insertion
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM PRIX_PROMO"))
            for row in result:
                print(row)
