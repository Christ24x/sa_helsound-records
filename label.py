import json
chemin = "C:/Users/HP/OneDrive/Documents/Tp_Python/catalogue.json"
def charger_catalogue(chemin):
    """
    Charge le fichier JSON et retourne le catalogue.

    Args:
        chemin (str): Le chemin vers le fichier JSON à charger.

    Returns:
        list: Le catalogue sous forme de liste de dictionnaires.
    """
    try:
        with open(chemin ,'r', encoding='utf-8',) as f:
            return json.load(f) 
    except (FileNotFoundError, json.JSONDecodeError):
        return [] # Retourne une liste vide si le fichier n'existe pas 


def sauvegarder_catalogue(data,chemin):
    """
    Sauvegarde les données du catalogue dans un fichier JSON.

    Args:
        data (list): Les données du catalogue sous forme de liste de dictionnaires à sauvegarder.
        chemin (str): Le chemin vers le fichier JSON où sauvegarder.

    Returns:
        None
    """
    try:
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4) 
        return True #sauvegarde réussie
    except Exception:
        return False #sauvegarde échouée

def lister_artistes(catalogue):
    """
    Retourne une liste d'informations résumées des artistes.

    Args:
        catalogue (list): Le catalogue des artistes.

    Returns:
        list: Liste résumée des artistes avec nom, genre, pays et nombre d'albums.
    """
    artistes = []
    for artiste in catalogue:
        artistes.append({
            "nom": artiste["nom"],
            "genre": artiste["genre"],
            "pays": artiste["pays"],
            "nbre_albums": len(artiste["albums"]) # Compte le nombre d'albums pour chaque artiste
        })
    return artistes


def rechercher_artiste(catalogue, critere, valeur):
    """
    Recherche un artiste par nom ou genre.

    Args:
        catalogue (list): Le catalogue des artistes.
        critere (str): Le critère de recherche ("nom" ou "genre").
        valeur (str): La valeur à rechercher.

    Returns:
        - Si critere = "nom": retourne l'artiste trouvé (dict) ou None
        - Si critere = "genre": retourne la liste des artistes (list)
    """
    if critere not in ["nom", "genre"]:
        return None  # Critère invalide
    if critere == "nom":
        for artiste in catalogue:
            if artiste["nom"].lower() == valeur.lower():
                return artiste
        return None
    elif critere == "genre":
        artistes = []
        for artiste in catalogue:
            if artiste["genre"].lower() == valeur.lower():
                artistes.append(artiste)
        return artistes
    else:
        return None
    

def ajouter_artiste(catalogue, artiste):
    """
    Ajoute un nouvel artiste au catalogue après validation des données et sauvegarde le catalogue.

    Args:
        catalogue (list): Le catalogue des artistes.
        artiste (dict): Le dictionnaire de l'artiste à ajouter.

    Returns:
        dict or None: Le nouvel artiste ajouté, ou None si l'ID existe déjà.
    """
    
   # Vérifier que l'ID n'existe pas déjà
    for artiste_existant in catalogue:
        if artiste_existant["id"] == artiste["id"]:
            return None  # ID déjà utilisé
    
    # Ajouter l'artiste
    catalogue.append(artiste)
    return catalogue


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
    for artiste in catalogue:
        if artiste["id"] == id_artiste:
            artiste["albums"].append(album)
            return catalogue #Album ajouté avec succès
    return None  # Artiste non trouvé
        
