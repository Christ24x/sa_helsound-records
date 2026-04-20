import json
import pandas as pd  #importation de la biblio pandas
import logging
import matplotlib.pyplot as plt # a use apres pour le graphique
import os
import subprocess
import sys

def charger_catalogue():
    
    """
    Charge le catalogue depuis le fichier JSON "catalogue.json"

    Paramètres :
    chemin (str) : chemin vers le fichier JSON

    Retour :
    liste : données du catalogue (liste d'artistes)
    """ 

    try:
     with open("catalogue.json", "r", encoding="utf-8") as f: 
        sortie = json.load(f)
        logging.info("CE FICHIER JSON VIENT D'ETRE CHARGE CORRECTEMENT")
        print(" ✅ Catalogue chargé avec succès. ")
        return sortie
    except FileNotFoundError: 
       logging.error("FICHIER INTROUVABLE")
       return []
    except json.JSONDecodeError:
       logging.error("FORMAT JSON INCORRECT")
       return []
    

def transformation(catalogue):

    """
    Transforme un catalogue imbriqué en liste de dictionnaires aplatie

    Paramètres :
    catalogue (liste) : liste d'artistes contenant leurs albums

    Retour :
    liste : liste de dictionnaires avec artiste, genre,pays,titre, année et streams
    """
 
    try :
        data = [] 
        for artiste in catalogue : 
          for album in artiste["albums"]: 
            data.append({ 
                "artiste":artiste["nom"],
                "genre":artiste["genre"],
                "pays":artiste["pays"],
                "titre":album['titre'],
                "annee":album['annee'],
                "streams":album['streams']
            }) 
        reponse = data
        logging.info("LISTE DES ALMBUMS APLATIE AVEC SUCCES")
        return reponse

    except KeyError as g: 
        logging.error(f"Abscence de cette clé {g}") 
        return []

def creer_dataframe(data): 
        
        """
        Crée un DataFrame Pandas à partir des données aplaties

        Paramètres :
        data (liste) : liste de dictionnaires représentant les albums

        Retour :
        DataFrame : tableau de données exploitable (vide si erreur, c'est à dire si mal chargé)
        """

        if not data: 
            logging.warning("Aucune donnée disponible")
            return pd.DataFrame() 
        
        daframe = pd.DataFrame(data) 
        logging.info("LA DATAFRAME A ETE CREEE AVEC SUCCES")
        return daframe


# TOP 5 ARTISTES

def top_five (daframe) :

    """
    Retourne les 5 artistes ayant le plus de streams dans mon tableau de données

    Paramètres :
    daframe (DataFrame) : tableau contenant les données des albums

    Retour :
    Dataframe : liste des 5 artistes avec le total de leurs streams, triés du plus grand au plus petit
    """

    try :
        if daframe.empty:
            logging.warning("Le tableau est vide")
            return None
        
        reponse = daframe.groupby("artiste")["streams"] .sum()
        reponse = reponse.sort_values(ascending =False).head(5).reset_index()
    
        logging.info("TOP 5 artistes les plus streamés calculé avec succès")   
        return reponse
    except Exception as c :
        logging.error(f"Erreur :{c}")
        return None


# MOYENNE PAR GENRE "penser à gerer ces affichages là mais flemme pour l'instant"

def moy_par_genre(daframe):

    """
    Calcule la moyenne des streams pour chaque genre musical et génere un graphique matplotlib des streams par genre

    Paramètres :
    daframe (DataFrame) : tableau contenant les données des albums

    Retour :
    Series : moyenne des streams par genre
    """

    try:
        if daframe.empty:
            logging.warning("Le tableau est vide")
            return None
        
        reponse_a = daframe.groupby("genre")["streams"].mean()
        reponse_a = reponse_a.reset_index().round(0) #pour corriger l'annotation scientifique ,that's facultatif

        logging.info("MOYENNE DES STREAMS PAR GENRE CALCULEE AVEC SUCCES")
        return reponse_a
    
    except Exception as k :
        logging.error(f"Erreur concernant  la moyenne des streams par genre:{k}")
        return None
    

#GRAPHIQUE DES STREAMS PAR GENRE

def graphique_moy_par_genre(daframe):
    """
    Affiche un graphique basé sur la moy des streams par genre en utilisant la fonction moy_par_genre

    Paramètres :
    daframe (DataFrame) : tableau contenant les données des albums
    """

    try:
        dbz = moy_par_genre(daframe)

        dbz.plot(kind="bar",
                     x="genre",
                     y="streams",
                     legend=False
                     )
        plt.title("GRAPGHE MONTRANT L'EVOLUTION DES STREAMS PAR GENRE")
        plt.xlabel("Genre")
        plt.ylabel("Moyenne_Streams")
        plt.show()
        
    except Exception as o:
        logging.error(f"Erreur au niveau de la generation du graphique : {o}")
        


  # NOMBRE D'ALBUMS SORTIS PAR ANNEE

def albums_par_annee(daframe):

    """
    Calcule le nombre d'albums sortis par année

    Paramètres :
    daframe (DataFrame) : tableau contenant les données des albums

    Retour :
    pandas.DataFrame : tableau avec deux colonnes : 'annee' , 'nombre_albums'
    """

    try:
        if daframe.empty:
            return None

        resultat = daframe.groupby("annee").size().reset_index()
        resultat.columns=["annee","nombre_albums"]
        return resultat

    except Exception as e:
        logging.error(f"Erreur pour la sortie d'album par annee : {e}")
        return None
    
    
    #  NOMBRE D'ALBUMS SORTIS AVEC FILTRAGE PAR ANNEE

def filtrer_albums_par_an(daframe , annee):
  
    """
     Retourne les albums sortis pour une année donnée en utilisant un masque booléen
    
    Paramètres :
    daframe (DataFrame) : tableau contenant les données des albums
    annee(int): l'annee recherchée

    Retour :
    Pandas.DataFrame filtré: nombre d'albums filtré par année
    """

    try:

        masque_booleen = daframe["annee"] == annee
        resultat = daframe[masque_booleen].groupby("annee").size().reset_index()
        resultat.columns=["annee","nombre_albums"]

        logging.info("FILTRAGE PAR AN REUSSI")
        return resultat
     
    except Exception as i:
        logging.error(f"Erreur pour la sortie du nbre d'albums pour cette année:{i}")
        return None

def exporter_rapport(daframe, chemin_csv):
    """
    
    Exporte un rapport complet dans un fichier CSV (cré le ficher).
    on va l'ouvrir automatiquement avec Os mais ça marche que sur window donc 
    on verra une alternative si trouvé1
    Le rapport contient : top 5 streams, moyennes par genre,
    albums par année.
 
    Args:
        datframe (Dataframe): tableau contenant les données des albums
        chemin_csv (str): Chemin de destination du fichier rapport.csv.
 
    Returns:
        str: Chemin du fichier CSV généré avec ouverture automatique.
    """
    
    with open(chemin_csv, "w", encoding="utf-8-sig") as f:
        f.write("\n=== TOP 5 ARTISTES PAR STREAMS ===\n")
 
        top = top_five(daframe)
        top.to_csv(f, index=False,sep=";")
   
        f.write("\n=== MOYENNE STREAMS PAR GENRE ===\n")
 
        moyenne = moy_par_genre(daframe)
        moyenne.to_csv(f, index=False, sep=";")
    
    
        f.write("\n=== ALBUMS PAR ANNEE  ===\n")
 
        album = albums_par_annee(daframe)
        album.to_csv(f, index=False,sep=";")
    

    return chemin_csv



def ouvrir_fichier(chemin):
    """
    Permet d'ouvrir le ficher csv de façon automatique peut 
    importe l'os
    
    Parametre(str): le chemin du ficher

    return: ouvre le ficher dans un logiciel  
    
    """
    if sys.platform == "win32":
        os.startfile(chemin)
    elif sys.platform == "darwin":  # Mac
        subprocess.call(["open", chemin])
    else:  # Linux
        subprocess.call(["xdg-open", chemin])

