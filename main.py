"""
main.py - Point d'entrée de l'application SahelSound Records
Auteur : [Ton nom]
Description : Menu principal et boucle de l'application console
"""

import sys
import label
import analyse

CHEMIN_CATALOGUE = "catalogue.json"


def afficher_banniere():
    """Affiche la bannière de bienvenue."""
    print("=" * 50)
    print("     SAHELSOUND RECORDS  ")
    print("   Label Musical Indépendant Africain")
    print("=" * 50)


def afficher_menu_principal():
    """Affiche le menu principal."""
    print("\n MENU PRINCIPAL")
    print("-" * 30)
    print("1. Consulter le catalogue")
    print("2. Ajouter un artiste")
    print("3. Ajouter un album à un artiste")
    print("4. Statistiques et rapport")
    print("5. Quitter")
    print("-" * 30)

# SOUS-MENU 1 : Consulter le catalogue#

def menu_consulter(catalogue):
    """Sous-menu pour consulter le catalogue."""
    while True:
        print("\n CONSULTER LE CATALOGUE")
        print("-" * 30)
        print("a. Afficher tous les artistes")
        print("b. Rechercher un artiste")
        print("c. Afficher le détail d'un artiste")
        print("r. Retour au menu principal")
        print("-" * 30)

        choix = input("Votre choix : ").strip().lower()

        if choix == "a":
            artistes = label.lister_artistes(catalogue)
            print(f"\n{'Nom':<20} {'Genre':<15} {'Pays':<10} {'Albums'}")
            print("-" * 55)
            for a in artistes:
                print(f"{a['nom']:<20} {a['genre']:<15} {a['pays']:<10} {a['nb_albums']}")

        elif choix == "b":
            print("\nRecherche par :")
            print("  1. Nom")
            print("  2. Genre")
            critere_choix = input("Votre choix (1/2) : ").strip()
            if critere_choix == "1":
                critere = "nom"
            elif critere_choix == "2":
                critere = "genre"
            else:
                print(" Choix invalide.")
                continue
            valeur = input(f"Entrez le {critere} : ").strip()
            resultats = label.rechercher_artiste(catalogue, critere, valeur)
            if not resultats:
                print(f"  Aucun artiste trouvé pour '{valeur}'.")
            else:
                print(f"\n{len(resultats)} résultat(s) :")
                for a in resultats:
                    print(f"  - [{a['id']}] {a['nom']} | {a['genre']} | {a['pays']}")

        elif choix == "c":
            id_artiste = input("Entrez l'identifiant de l'artiste (ex: ART-001) : ").strip()
            resultats = label.rechercher_artiste(catalogue, "id", id_artiste)
            if not resultats:
                print(f" Artiste '{id_artiste}' introuvable.")
            else:
                artiste = resultats[0]
                print(f"\n🎤 {artiste['nom']} ({artiste['pays']}) — {artiste['genre']}")
                print(f"   Albums ({len(artiste['albums'])}) :")
                for album in artiste["albums"]:
                    print(f"   • {album['titre']} ({album['annee']}) — {album['streams']:,} streams")

        elif choix == "r":
            break
        else:
            print(" Option invalide, réessayez.")


# SOUS-MENU 2 : Ajouter un artiste

def menu_ajouter_artiste(catalogue):
    """Sous-menu pour ajouter un nouvel artiste."""
    print("\n AJOUTER UN ARTISTE")
    print("-" * 30)

    try:
        id_artiste = input("Identifiant (ex: ART-013) : ").strip()
        nom       = input("Nom de scène : ").strip()
        genre     = input("Genre musical : ").strip()
        pays      = input("Pays d'origine : ").strip()

        if not id_artiste or not nom or not genre or not pays:
            print(" Tous les champs sont obligatoires.")
            return catalogue

        nouvel_artiste = {
            "id": id_artiste,
            "nom": nom,
            "genre": genre,
            "pays": pays,
            "albums": []
        }

        catalogue = label.ajouter_artiste(catalogue, nouvel_artiste)
        label.sauvegarder_catalogue(catalogue, CHEMIN_CATALOGUE)
        print(f" Artiste '{nom}' ajouté avec succès !")

    except ValueError as e:
        print(f" Erreur : {e}")

    return catalogue

# SOUS-MENU 3 : Ajouter un album

def menu_ajouter_album(catalogue):
    """Sous-menu pour ajouter un album à un artiste existant."""
    print("\n AJOUTER UN ALBUM")
    print("-" * 30)

    try:
        id_artiste = input("Identifiant de l'artiste : ").strip()
        resultats  = label.rechercher_artiste(catalogue, "id", id_artiste)

        if not resultats:
            print(f" Artiste '{id_artiste}' introuvable.")
            return catalogue

        print(f" Artiste trouvé : {resultats[0]['nom']}")

        titre   = input("Titre de l'album : ").strip()
        annee   = int(input("Année de sortie : ").strip())
        streams = int(input("Nombre de streams : ").strip())

        if not titre:
            print(" Le titre est obligatoire.")
            return catalogue

        nouvel_album = {
            "titre": titre,
            "annee": annee,
            "streams": streams
        }

        catalogue = label.ajouter_album(catalogue, id_artiste, nouvel_album)
        label.sauvegarder_catalogue(catalogue, CHEMIN_CATALOGUE)
        print(f" Album '{titre}' ajouté à {resultats[0]['nom']} !")

    except ValueError:
        print(" L'année et les streams doivent être des nombres entiers.")

    return catalogue


# SOUS-MENU 4 : Statistiques et rapport

def menu_statistiques():
    """Sous-menu pour afficher les statistiques et exporter le rapport."""
    while True:
        print("\n STATISTIQUES ET RAPPORT")
        print("-" * 30)
        print("a. Top 5 artistes par streams")
        print("b. Moyenne des streams par genre")
        print("c. Albums par année")
        print("d. Exporter le rapport complet (rapport.csv)")
        print("r. Retour au menu principal")
        print("-" * 30)

        choix = input("Votre choix : ").strip().lower()

        if choix == "a":
            top5 = analyse.top5_artistes(CHEMIN_CATALOGUE)
            print("\n Top 5 artistes par streams :")
            for i, (nom, streams) in enumerate(top5, 1):
                print(f"  {i}. {nom} — {streams:,} streams")

        elif choix == "b":
            moyennes = analyse.moyenne_streams_par_genre(CHEMIN_CATALOGUE)
            print("\n🎵 Moyenne des streams par genre :")
            for genre, moyenne in moyennes.items():
                print(f"  • {genre} : {moyenne:,.0f} streams")

        elif choix == "c":
            par_annee = analyse.albums_par_annee(CHEMIN_CATALOGUE)
            print("\n Albums sortis par année :")
            for annee, nb in par_annee.items():
                print(f"  • {annee} : {nb} album(s)")

        elif choix == "d":
            analyse.exporter_rapport(CHEMIN_CATALOGUE, "rapport.csv")
            print("Rapport exporté dans rapport.csv !")

        elif choix == "r":
            break
        else:
            print(" Option invalide, réessayez.")


# ──────────────────────────────────────────────
# BOUCLE PRINCIPALE
# ──────────────────────────────────────────────

def main():
    """Fonction principale — boucle du menu."""
    afficher_banniere()

    catalogue = label.charger_catalogue(CHEMIN_CATALOGUE)
    print(f"Catalogue chargé : {len(catalogue)} artiste(s) trouvé(s).")

    while True:
        afficher_menu_principal()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            menu_consulter(catalogue)
        elif choix == "2":
            catalogue = menu_ajouter_artiste(catalogue)
        elif choix == "3":
            catalogue = menu_ajouter_album(catalogue)
        elif choix == "4":
            menu_statistiques()
        elif choix == "5":
            print("\n À bientôt sur SahelSound Records !")
            sys.exit(0)
        else:
            print(" Option invalide, entrez un nombre entre 1 et 5.")


if __name__ == "__main__":
    main()
