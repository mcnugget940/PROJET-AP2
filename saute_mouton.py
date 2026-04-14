import fltk
import random
import json

# constantes 
LARGEUR  = 20          # largeur du personnage en pixels
HAUTEUR  = 20          # hauteur du personnage en pixels
VMAX     = 15          # vitesse maximale autorisée (la limite de vitesse que le joueur peut donner au perso)
GRAVITE  = (0, 9,8)    # gravité qui tire le mouton
PAS      = 0.5         # pas de la simulation 

# Dimensions de la fenêtre de jeu
FENETRE_LARGEUR  = 800
FENETRE_HAUTEUR  = 600

# ============================================================
#  CHARGEMENT DU NIVEAU
# ============================================================

def charger_niveau(nom_fichier):
    
    personnage = None
    objectif   = None
    lst_blocs  = []

    with open(nom_fichier, "r") as f:  # on ouvre le fichier sous format lecture
        lignes = f.readlines()

    for i, ligne in enumerate(lignes):
        # Supprime les commentaires et les espaces inutiles
        ligne = ligne.split("#")[0].strip()
        if not ligne:          # ligne vide ou que commentaire
            continue

        valeurs = [int(v) for v in ligne.split(",")]

        if personnage is None:
            # Première ligne utile : position du personnage
            x, y = valeurs
            personnage = {
                "position": (x, y),
                "vitesse":  (0, 0)
            }
        elif objectif is None:
            # Deuxième ligne utile : objectif
            x1, y1, x2, y2 = valeurs
            objectif = ((x1, y1), (x2, y2))
        else:
            # Lignes suivantes : blocs
            x1, y1, x2, y2 = valeurs
            lst_blocs.append(((x1, y1), (x2, y2)))

    return personnage, objectif, lst_blocs

