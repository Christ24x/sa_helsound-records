import json
import analyse as any


def charger_catalogue(chemin):
    """
    Charge le fichier JSON et retourne le catalogue.

    Args:
        chemin (str): Le chemin vers le fichier JSON à charger.

    Returns:
        list: Le catalogue sous forme de liste de dictionnaires.
    """
    with open(chemin, 'r',encoding="utf-8") as f:
        return json.load(f)


def sauvegarder_catalogue(data, chemin):
    """
    Sauvegarde les données du catalogue dans un fichier JSON.

    Args:
        data (list): Les données du catalogue sous forme de liste de dictionnaires à sauvegarder.
        chemin (str): Le chemin vers le fichier JSON où sauvegarder.

    Returns:
        Données sauvegardée dans le ficher 
    """

    with open(chemin , 'w', encoding="UTF-8") as f:
        return json.dump(data, f, ensure_ascii=False, indent=2)
    

def lister_artistes(catalogue):
    """
    Retourne une liste d'informations résumées des artistes.

    Args:
        catalogue (list): Le catalogue des artistes.

    Returns:
        list: Liste résumée des artistes avec nom, genre, pays et nombre d'albums.
    """
    
    artistes = []
    for art in catalogue:
        artiste = {
            "NOM": art["nom"],
            "GENRE": art["genre"],
            "PAYS": art["genre"],
            "Nombre_albums": len(art["albums"])
        }
        artistes.append(artiste)
    return artistes


def lister_artistes2(catalogue):
    
    """le code est bien mais le rendu pas acceptable. 
    test, meme chose que lister_artiste mais la liste 
    renvoyé est imbriquée ici. 
    """
    artistes = []
    for art in catalogue:

        artistes.append(art)
    return artistes


def rechercher_artiste(catalogue, critere, valeur):
    """
    Recherche un artiste par nom ou genre.

    Args:
        catalogue (list): Le catalogue des artistes.
        critere (str): Le critère de recherche ("nom" ou "genre").
        valeur (str): La valeur à rechercher.

    Returns:
        - Si critere = "nom": retourne la liste des artistes (en partant 
           du fait qu'on peut avoir des artistes avec le meme nom.)
        - Si critere = "genre": retourne la liste des artistes (list)
    """

    if critere.lower() == "nom":
        artistes = []
        for art in catalogue:
            if valeur.lower() in art["nom"].lower():
                artistes.append(art)
    elif critere.lower() == "genre":
        artistes = []
        for art in catalogue:
            if valeur.lower() in art["genre"].lower():
                artistes.append(art)
        
    return artistes


def ajouter_artiste(catalogue, artiste):
    """
    Ajoute un nouvel artiste au catalogue après validation des données et sauvegarde le catalogue.

    Args:
        catalogue (list): Le catalogue des artistes.
        artiste (dict): Le dictionnaire de l'artiste à ajouter.

    Returns:
        dict : Le nouvel artiste ajouté.
    """

    ids_existants = {a["id"] for a in catalogue}
    if artiste["id"] in ids_existants:
        raise ValueError(f"\n ❌ L'identifiant '{artiste['id']}' existe déjà. ❌")
    
    catalogue.append(artiste)

    return catalogue


def get_artiste(catalogue,id_artiste):
    """
    Retourne un artiste par son identifiant unique.
    C'est à utiliser dans ajouter album 
 
    Args:
        catalogue (list): Liste des artistes.
        id_artiste (str): Identifiant recherché.
 
    Returns:
        dict: L'artiste trouvé.
    """


    for art in catalogue:
        if id_artiste.upper() == art["id"]:
            artiste_existant = art
    if len(artiste_existant) :
        return artiste_existant        
    else:
        raise ValueError(f" ❌ Artiste avec l'id '{id_artiste}' introuvable.")


def ajouter_album(catalogue, id_artiste, album):
    """
    Ajoute un album à un artiste existant après validation des données et sauvegarde le catalogue.

    Args:
        catalogue (list): Le catalogue des artistes.
        id_artiste (str): L'identifiant de l'artiste auquel ajouter l'album.
        album (dict): L'album à ajouter (titre, annee, streams).

    Returns:
        dict: L'album ajouté avec les informations saisies.
    """
    
    for art in catalogue:
        if id_artiste.lower() == art["id"].lower():
            for alb in album:
                art["albums"].append(alb)

            return catalogue


def show_detail(catalogue,id_artiste):
    """
    Retourne un artiste par son identifiant unique.
 
    Args:
        catalogue (list): Liste des artistes.
        id_artiste (str): Identifiant recherché.
 
    Returns:
        dict or None: L'artiste trouvé, ou None si inexistant.
    """
    for artiste in catalogue:
        if artiste["id"].lower() == id_artiste:
            return artiste
    return None


def generate_id(catalogue):
    """
    Retourne un id d'artiste unique précisement ce qui suit 
      le tout dernier.
      utiliser dans ajouter artiste. On n'a crée une option 
      ou l'utilisateur n'a pas à entrer un id de façon manuel.
 
    Args:
        catalogue (list): Liste des artistes.
 
    Returns:
        str : id de l'artiste
    """

    id_existant = [a["id"] for a in catalogue]
    id = id_existant[-1]
    id = int(id[4:]) + 1

    return f"ART-{id:03d}"


