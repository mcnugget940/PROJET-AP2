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
        lignes = f.readlines()		  # lit toutes les lignes du fichier d'un coup et met tout cela dans une liste python

    for i, ligne in enumerate(lignes):
        # Supprime les commentaires et les espaces inutiles
        ligne = ligne.split("#")[0].strip()
        if not ligne:          # ligne vide ou que commentaire
            continue

        valeurs = [int(v) for v in ligne.split(",")] # dans le cas suivant nous avons ligne.split() qui découpe les "," pour donner une liste de chaine. int() convertir chaque chaine en entier

        if personnage is None:	# on vérifie SI le personnage est crée
            
            x, y = valeurs 	# on récupère du coup la liste valeurs pour décompresser en deux variables séparées
            personnage = {
                "position": (x, y), # on récupère du coup la position avce les valeurs obtenue
                "vitesse":  (0, 0)	# vitesse nulle au départ 
            }
        elif objectif is None:	# on vérifie si on a crée l'objectif
            
            x1, y1, x2, y2 = valeurs
            objectif = ((x1, y1), (x2, y2)) #représentée par un tuple
        else:
            
            x1, y1, x2, y2 = valeurs
            lst_blocs.append(((x1, y1), (x2, y2)))

    return personnage, objectif, lst_blocs

# fonctions d'accès
def get_position(personnage):
    "elle renvoie la position du personnage"
    return personnage["position"]
def get_vitesser(personnage):
    "elle renvoie la vitesse du personnage"
    return personnage["vitesse"]
def set_position(personnage, pos):
    "elle modifie la position du personnage"
    personnage["position"] = pos
def set_vitesse(personnage, vit):
    perosnnage["vitesse"] = vit
    
def clic_vers_vitesse(personnage, clic) :
    
    px, py = get_position(personnage)
    cx, cy = clic
    
    #concernant la vitesse
    vx = cx - px
    vy = cy - py
    
    norme = sqrt(vx**2 + vy**2)
