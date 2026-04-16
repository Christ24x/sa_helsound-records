import json

def charger_catalogue(chemin):
    """
    Charge le fichier JSON et retourne le catalogue.
    Args:
        chemin (str): Le chemin vers le fichier JSON à charger.
    Returns:
        list: Le catalogue sous forme de liste de dictionnaires.
    """
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def sauvegarder_catalogue(data, chemin):
    """
    Sauvegarde les données du catalogue dans un fichier JSON.
    Args:
        data (list): Les données du catalogue.
        chemin (str): Le chemin vers le fichier JSON.
    Returns:
        bool: True si succès, False sinon.
    """
    try:
        with open(chemin, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False

def lister_artistes(catalogue):
    """
    Retourne une liste d'informations résumées des artistes.
    Args:
        catalogue (list): Le catalogue des artistes.
    Returns:
        list: Liste résumée avec nom, genre, pays et nb_albums.
    """
    artistes = []
    for artiste in catalogue:
        artistes.append({
            "nom": artiste["nom"],
            "genre": artiste["genre"],
            "pays": artiste["pays"],
            "nb_albums": len(artiste["albums"])  # clé harmonisée avec main.py
        })
    return artistes

def rechercher_artiste(catalogue, critere, valeur):
    """
    Recherche un artiste par nom, genre ou id.
    Args:
        catalogue (list): Le catalogue des artistes.
        critere (str): "nom", "genre" ou "id".
        valeur (str): La valeur à rechercher.
    Returns:
        list: Liste des artistes correspondants (vide si aucun résultat).
    """
    resultats = []
    for artiste in catalogue:
        if critere == "id":
            if artiste["id"].lower() == valeur.lower():
                resultats.append(artiste)
        elif critere == "nom":
            if valeur.lower() in artiste["nom"].lower():
                resultats.append(artiste)
        elif critere == "genre":
            if valeur.lower() in artiste["genre"].lower():
                resultats.append(artiste)
    return resultats

def ajouter_artiste(catalogue, artiste):
    """
    Ajoute un nouvel artiste au catalogue après validation.
    Args:
        catalogue (list): Le catalogue des artistes.
        artiste (dict): L'artiste à ajouter.
    Returns:
        list: Le catalogue mis à jour.
    Raises:
        ValueError: Si l'ID existe déjà.
    """
    for artiste_existant in catalogue:
        if artiste_existant["id"] == artiste["id"]:
            raise ValueError(f"L'identifiant '{artiste['id']}' existe déjà.")
    catalogue.append(artiste)
    return catalogue

def ajouter_album(catalogue, id_artiste, album):
    """
    Ajoute un album à un artiste existant.
    Args:
        catalogue (list): Le catalogue des artistes.
        id_artiste (str): L'identifiant de l'artiste.
        album (dict): L'album à ajouter (titre, annee, streams).
    Returns:
        list: Le catalogue mis à jour.
    Raises:
        ValueError: Si l'artiste est introuvable.
    """
    for artiste in catalogue:
        if artiste["id"] == id_artiste:
            artiste["albums"].append(album)
            return catalogue
    raise ValueError(f"Artiste '{id_artiste}' introuvable.")
