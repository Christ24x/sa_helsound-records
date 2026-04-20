import label
import analyse as any
import json
import pandas as pd
import os


def afficher_menu_principale():

    """Affiche le menu principal de l'application."""

    separateur = "-" * 50


    print("\n",separateur)
    print("   Bienvenue chez SAHELSOUND RECORDS 🎶")
    print("   Label Musical Indépendant Africain")
    print(separateur)

    print("\n",separateur)
    print("       🎵  SAHELSOUND RECORDS — MENU PRINCIPAL  🎵")
    print(separateur)
    print("  1. Consulter le catalogue")
    print("  2. Ajouter un artiste")
    print("  3. Ajouter un album à un artiste")
    print("  4. Statistiques et rapport")
    print("  5. Quitter")
    print(separateur)

# ──────────────────────────────────────────────
# SOUS-MENU 1 : Consulter le catalogue
# ──────────────────────────────────────────────

def consulter_catalogue(catalogue):
    """
    Sous-menu pour la consultation du catalogue.
 
    Args:
        catalogue (list): Liste des artistes chargés.
    """


    while True:
        
        print(f"\n{'─' * 50}")
        print("  CONSULTER LE CATALOGUE")
        print("─" * 50)
        print("  a. Afficher tous les artistes")
        print("  b. Rechercher un artiste par nom ou genre")
        print("  c. Afficher le détail d'un artiste")
        print("  r. Retour au menu principal")
        
        choix = input("\n  Votre choix : ").strip().lower()

        if choix == "a":
            """
                On affiche tout les artiste du catalogue
                ici artistes est une liste de plusieurs artiste(objets) que 
                je parcoure après pour avoir chaque informations.
            """
            artistes = label.lister_artistes2(catalogue)
            #print(artistes)
            if not artistes:
                print("  Aucun artiste dans le catalogue.")
            else:
                liste = pd.DataFrame(artistes)
                print("\n")
                #print(liste)

                for artiste in artistes:

                    print(f"\n  ┌─ {artiste['nom']} ({artiste['id']})")
                    print(f"  │  Genre : {artiste['genre']} | Pays : {artiste['pays']}")
                    print(f"  │  Albums ({len(artiste['albums'])}) :")
                    for alb in artiste["albums"]:
                        print(f"  │    • {alb['titre']} ({alb['annee']}) "
                            f"— {alb['streams']:,} streams")
                    print("  └─")
        
        elif choix == "b":
            """
                La logique est de vérifier à chaque fois les entrées dans 
                le cas ou il entre autre chose que le 'nom' ou le 'genre'
                avec une option 'q' pour quitter après un échec.
            """
            
            erreur = False

            while True:
                if not erreur:
                    critere = input("\n  Rechercher par (nom / genre) : ").strip().lower()
                else:
                    critere = input("\n  Rechercher par (nom / genre) (q pour quitter) : ").strip().lower()

                if critere == "q":
                    break

                if critere in ["nom", "genre"]:
                    break
                else:
                    print("\n  ❌  Critère invalide. Saisissez 'nom' ou 'genre'.")
                    erreur = True

            if critere == "q":
                continue


            erreur = False
                  
            while True:
            
                if not erreur:
                    valeur = input(f"\n Valeur Rechercher par {critere} : ").strip().lower()
                else:
                    valeur = input(f"\n Valeur Rechercher par {critere} (q pour quitter) : ").strip().lower()

                if valeur == "q":
                    break

                if valeur != "":
                    break
                else:
                    print("\n ❌ Veuillez entrer une valeur valide")
                    erreur = True
            
            if valeur == "q":
                continue

            """
            Resultat est une liste des artistes trouvées qu'on parcoure 
            """
            resultat = label.rechercher_artiste(catalogue,critere,valeur)
            # print(resultat)

            if not resultat:
                print(f"  Aucun résultat pour '{valeur}'.")
            else:
                # search = any.laoding_data(resultat)
                # print(search)
                for artiste in resultat:

                    print(f"\n  ┌─ {artiste['nom']} ({artiste['id']})")
                    print(f"  │  Genre : {artiste['genre']} | Pays : {artiste['pays']}")
                    print(f"  │  Albums ({len(artiste['albums'])}) :")
                    for alb in artiste["albums"]:
                        print(f"  │    • {alb['titre']} ({alb['annee']}) "
                            f"— {alb['streams']:,} streams")
                    print("  └─")

        elif choix == "c":
            """
            Ici il s'agie d'afficher le detail d'un artiste. 
            On demande l'id de l'artiste.
                 - On vérifie la validité du format (ART-XXX)
                 - L'existance de l'Id

            On retourne artiste. Mais comme on utilise l'id c'est que d'office 
            l'artiste est unique. 
            """
            
            erreur = False

            while True:
                if not erreur:
                    id_artiste = input("\n  Identifiant de l'artiste (ex: ART-001) : ").strip().lower()
                else:
                    id_artiste = input("\n  Identifiant de l'artiste (ex: ART-001)  (q pour quitter) : ").strip().lower()

                if id_artiste == "q":
                    break

                if id_artiste != "":
                    break
                else:
                    print("\n  ❌  Id_artiste invalide. Reesayer. ")
                    erreur = True

            if id_artiste == "q":
                continue

            artiste = label.show_detail(catalogue,id_artiste)

            if artiste is None:
                print(f"\n  ❌ Aucun artiste avec l'id '{id_artiste}'.")
            else:
                print(f"\n  ┌─ {artiste['nom']} ({artiste['id']})")
                # print(f"  │  Genre : {artiste['genre']} | Pays : {artiste['pays']}")
                print(f"  │  Albums ({len(artiste['albums'])}) :")
                for alb in artiste["albums"]:
                    print(f"  │    • {alb['titre']} ({alb['annee']}) "
                          f"— {alb['streams']:,} streams")
                print("  └─")  
        elif choix == "r":
            break
        else:
            print("  ❌ Option invalide.")

                    
def verification(type):
    """
        La fonction vérifie la validité de l'entré en parametre.
        Il est utilisé au niveau de ajouter artiste pour verifier 
        que les entrées ne soit pas null.

        Args:
           type(str): c'est l'entré demandé à l'utilisateur (nom/genre/...)
    """
    erreur = False
                    
    while True:
    
        if not erreur:
            variable = input(f"\n Entrer le {type} : ").strip()
        else:
            variable = input(f"\n  {type} (q pour quitter) : ").strip()

        if variable == "q":
            return None

        if variable != "":
            return variable
        else:
            print(f"\n ❌ Le {type} ne peut pas être vide.")
            erreur = True
    
def valider_id(valeur):
    """
    Vérifie si le format de l'id est valide.
    Utiliser dans ajouter artiste et ajout d'album

    Args:
      valeur(str): l'id entré
    """
    if not valeur.startswith("art-"):
        return False
    
    chiffres = valeur[4:]

    return chiffres.isdigit() and len(chiffres) == 3
    
# ──────────────────────────────────────────────
# SOUS-MENU 2 : Ajouter un artiste
# ──────────────────────────────────────────────

def add_artiste(catalogue,chemin):
    """
    Sous-menu pour ajouter un nouvel artiste au catalogue.
      - ajout avec id générer automatiquement
      - ajout manuel
 
    Args:
        catalogue (list): Liste des artistes (modifiée en place).
        chemin (str): le chemin du ficher
 
    Returns:
        list: Catalogue mis à jour.
    """

    while True:
        print(f"\n{'─' * 50}")
        print("  \t\tAJOUTER UN ARTISTE")
        print("─" * 50)
        print("  a. Id automatique")
        print("  b. Entrer l'id manuel")
        print("  c. Quitter")
        
        choix = input("\n  ------Votre choix : ").strip().lower()

        if choix == "c":
            break

        if choix not in ["a","b"]:
            print(" ❌ Veillez entrer un choix valide. ")


        if choix == "a":
            id_artiste = label.generate_id(catalogue)

        elif choix == "b":

            erreur = False
            while True:
                if not erreur:
                    id_artiste = input("\n  Identifiant de l'artiste (ex: ART-001) : ").strip().lower()
                else:
                    id_artiste = input("\n  Identifiant de l'artiste (ex: ART-001) (q pour quitter) : ").strip().lower()

                if id_artiste == "q":
                    break

                if valider_id(id_artiste):
                    break
                else:
                    print("\n ❌ Format invalide (ex: ART-001)")
                    erreur = True

            if id_artiste == "q":
                continue
            
                    
        nom = verification("Nom de scène ")
        if nom == None:
            continue
        
        genre = verification("Genre Musicale")
        if nom == None:
            continue

        pays = verification("Pays D'origine")
        if nom == None:
            continue
        
        nouvel_albums = []

        while True:
                
            albums = int(input("\n Combien d'album(s) voulez-vous entrer ? "))

            if albums <= 0 or albums == "":
                print("❌ Entrer un nombre positif")
            else:
                break  # ✅ valeur correcte → on sort de la boucle

        
        for loop in range(albums):
            
            titre = input("\n  Titre de l'album : ").strip()
            if not titre:
                print("\n  ❌ Le titre ne peut pas être vide.")
            
            while True:
                try:
                    annee = int(input("  Année de sortie : ").strip())
                    if annee < 0:
                        raise ValueError
                    break

                except ValueError:
                    print("\n  ❌ Année invalide — saisissez un nombre entier.")
                    continue
            
            while True:
                try:
                    streams = int(input("  Nombre de streams : ").strip())
                    if streams < 0:
                        raise ValueError
                    break
                except ValueError:
                    print("  ❌ Nombre de streams invalide — saisissez un entier positif.")
                    continue
        
            nouvel_album = {"titre": titre, "annee": annee, "streams": streams}
            nouvel_albums.append(nouvel_album)

    
        nouvel_artiste = {
            "id": id_artiste.upper(),
            "nom": nom,
            "genre": genre,
            "pays": pays,
            "albums": nouvel_albums,
        }
    
        try:
            try:
                catalogue = label.ajouter_artiste(catalogue, nouvel_artiste)
            except ValueError as e :
                print(e)
                continue
            
            label.sauvegarder_catalogue(catalogue, chemin)
            print(f"\n  ✅ Artiste '{nom}' ajouté avec succès et catalogue sauvegardé.")
        except ValueError as e:
            print(f"  ❌ {e}")

# ──────────────────────────────────────────────
# SOUS-MENU 3 : Ajouter un album
# ──────────────────────────────────────────────

def add_album(catalogue,chemin):
    """
    Ajouter un album à un artiste existant.
       - Demande l'id et vérifie le format. 
       si artiste trouvé le notifie sinon renvois une erreur.
 
    Args:
        catalogue (list): Liste des artistes (modifiée en place).
 
    Returns:
        list: Catalogue mis à jour.
    """

    while True: 
        print(f"\n{'─' * 55}")
        print("  AJOUTER UN ALBUM À UN ARTISTE")
        print("─" * 55)

        erreur = False
        while True:
            if not erreur:
                id_artiste = input("\n  Identifiant de l'artiste (ex: ART-001) : ").strip().lower()
            else:
                id_artiste = input("\n  Identifiant de l'artiste (ex: ART-001) (q pour quitter) : ").strip().lower()

            if id_artiste == "q":
                break

            if valider_id(id_artiste):
                break
            else:
                print("\n ❌ Format invalide (ex: ART-001)")
                erreur = True
                continue
        if id_artiste == "q":
            break

            
        try:
            artiste = label.get_artiste(catalogue,id_artiste)
            if artiste :
                print(" ✅ Artiste trouvé")
        except ValueError as e:
            print("\n",e)
            continue
        
        nouvel_albums = []

        while True:
                
            while True:
                albums = int(input("\n Combien d'album(s) voulez-vous entrer ? "))

                if albums <= 0 or albums == "":
                    print("❌ Entrer un nombre positif")
                    continue
                else:
                    break  

        
            for loop in range(albums):
                
                titre = input("\n  Titre de l'album : ").strip()
                if not titre:
                    print("\n  ❌ Le titre ne peut pas être vide.")
                
                while True:
                    try:
                        annee = int(input("  Année de sortie : ").strip())
                        if annee < 0:
                            raise ValueError
                        break

                    except ValueError:
                        print("\n  ❌ Année invalide — saisissez un nombre entier.")
                        continue
                
                while True:
                    try:
                        streams = int(input("  Nombre de streams : ").strip())
                        if streams < 0:
                            raise ValueError
                        break
                    except ValueError:
                        print("  ❌ Nombre de streams invalide — saisissez un entier positif.")
                        continue
            
                nouvel_album = {"titre": titre, "annee": annee, "streams": streams}
                nouvel_albums.append(nouvel_album)
             
                catalogue = label.ajouter_album(catalogue,id_artiste, nouvel_albums)            
                label.sauvegarder_catalogue(catalogue, chemin)
                for alb in nouvel_albums:
                    print(f"\n  ✅ L'album '{alb['titre']}' de l'Artiste '{artiste['nom']}' ajouté avec succès et catalogue sauvegardé.")
                    break
            break
        break
    
# ──────────────────────────────────────────────
# SOUS-MENU 4 : Statistiques et rapport
# ──────────────────────────────────────────────

def statistique_rapport():
    
    """Sous-menu pour les statistiques et l'export du rapport."""

    catalogue = any.charger_catalogue()
    liste = any.transformation(catalogue)
    datframe = any.creer_dataframe(liste)

    
    while True:
        print(f"\n{'─' * 50}")
        print("  STATISTIQUES ET RAPPORT")
        print("─" * 50)
        print("  a. Top 5 des artistes par streams")
        print("  b. Moyenne des streams par genre")
        print("  c. Nombre d'albums par année")
        print("  d. Exporter le rapport complet (rapport.csv)")
        print("  e. Générer un graphique des streams par genre.")
        print("  r. Retour au menu principal")
        
        choix = input("\n  Votre choix : ").strip().lower()

        if choix == "a":
            print("\n" + "=" * 50)
            print("   TOP 5 ARTISTES PAR NOMBRE TOTAL DE STREAMS")
            print("=" * 50)

            top_Five = any.top_five(datframe)
            print(top_Five)

        elif choix == "b":
            print("\n" + "=" * 50)
            print("   MOYENNE DES STREAMS PAR GENRE")
            print("=" * 50)

            moyenne = any.moy_par_genre(datframe)
            print(moyenne)

        elif choix =="c":
            print("\n" + "=" * 50)
            print("   NOMBRE D'ALBUMS PAR ANNÉE")
            print("=" * 50)

            """
            Ici deux possiblité soit avec l'année entrée -> filtrage avec masque booléen
                                           validation simple -> agregation 
            """

            while True: 

                print("  a. Entrer une année. ")
                print("  b. continer sans ")
                
                choix = input("\n  Votre choix : ").strip().lower()
                
                if choix == "a":
                    while True:
                        try:
                            annee = int(input("  Année : ").strip())
                            if annee < 0:
                                raise ValueError
                            break

                        except ValueError:
                            print("\n  ❌ Année invalide — saisissez un nombre entier.")
                            continue

                    album_years = any.filtrer_albums_par_an(datframe,annee)
                    print("\n",album_years)
                    break

                elif choix == "b":

                    album_years = any.albums_par_annee(datframe)
                    print(album_years)
                    break
                else:
                    print(" ❌ Option Invalide. Veillez réesayer. ")
                    continue

        elif choix == "d":
            """
            Exporte le rapport et l'ouvre automatiquement en fonction de l'os.
            """
            rapport = any.exporter_rapport(datframe,"rapport.csv")
            print("\n ✅ Rapport exporté avec succès")

            #os.startfile(rapport) #marche uniquement sur window
            any.ouvrir_fichier(rapport)

        elif choix == "e":
            any.graphique_moy_par_genre(datframe)
        elif choix == "r":
            break
        else:
            print(" ❌ Veillez entrer une option valide")
            continue


# ──────────────────────────────────────────────
# BOUCLE PRINCIPALE
# ──────────────────────────────────────────────

def main():
    
    
    chemin = "catalogue.json"

    try:
        catalogue = label.charger_catalogue(chemin)
        print(f"\n  ✅ Catalogue chargé — {len(catalogue)} artiste(s) trouvé(s).")
    except FileNotFoundError:
        print(f"  ⚠️  Fichier '{chemin}' introuvable. Catalogue vide créé.")
        catalogue = []
    except json.JSONDecodeError:
        print("  ❌ Format du Catalogue Invalide ")


    while True:
        afficher_menu_principale()
        
        try:
            choix = int(input("  -------Votre choix : ").strip())
        except ValueError:
            print(" ❌ Entrée invalide. Veuillez entrer un nombre entre 1 et 5.")
            continue  # revient au début de la boucle

        if int(choix) == 1:
            consulter_catalogue(catalogue)
        elif int(choix) == 2:
            add_artiste(catalogue,chemin)     
        elif int(choix) == 3: 
            add_album(catalogue,chemin)
        elif int(choix) == 4:
            statistique_rapport()
        elif int(choix) == 5: 
            print("\n  Merci 🎉 À bientôt sur SahelSound Records ! 🎵\n") 
            break
        else:
            print("  ❌ Option invalide. Choisissez entre 1 et 5.")
           


if __name__ == "__main__":
    main()