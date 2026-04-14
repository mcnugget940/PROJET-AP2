from fltk import *
import math

# ============================================================
#  CONSTANTES
# ============================================================

LARGEUR  = 20          # largeur du personnage en pixels
HAUTEUR  = 20          # hauteur du personnage en pixels
VMAX     = 15          # vitesse maximale autorisée
GRAVITE  = (0, 0.5)    # gravité (axe y vers le bas avec fltk)
PAS      = 0.5         # pas de la simulation (finesse)

# Dimensions de la fenêtre de jeu
FENETRE_LARGEUR  = 800
FENETRE_HAUTEUR  = 600

# ============================================================
#  CHARGEMENT DU NIVEAU
# ============================================================

def charger_niveau(nom_fichier):
    """
    Lit un fichier texte décrivant un niveau et renvoie :
      - le dictionnaire personnage
      - le tuple objectif  ((x1,y1),(x2,y2))
      - la liste lst_blocs [ ((x1,y1),(x2,y2)), ... ]

    Format du fichier :
      ligne 1 : x,y                   -> position du personnage
      ligne 2 : x1,y1,x2,y2           -> objectif
      lignes suivantes : x1,y1,x2,y2  -> un bloc par ligne
    Les commentaires (# ...) sont ignorés.
    """
    personnage = None
    objectif   = None
    lst_blocs  = []

    with open(nom_fichier, "r") as f:
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
