######################################################################
#                  AP1 - 2025 - Projet 1 - PICK TOK                  #
######################################################################

import fltk
import random
import json
# --------------------------------------------------------------------
# CONSTANTES POUR LA PAGE D'ACCUEIL
# --------------------------------------------------------------------

LARGEUR_FENETRE = 900
HAUTEUR_FENETRE = 620
# ---------------------------------
# Sauvegarder pour le mode solo
# ---------------------------------
def sauvegarder_partie_solo():
    ''' On va créer un dictionnaire qui contiendra toute les informations à sauvegarder'''
    donnees = {
        "plateau_solo": plateau_solo,                  # Sauvegarde l'état du plateau de jeu solo
        "jetons_ratelier_solo": jetons_ratelier_solo,  # Sauvegarde les jetons présents dans le ratelier
        "score_solo": score_solo,                      # Sauvegarde le score du joueur
        "partie_terminee_solo": partie_terminee_solo,  # Sauvegarde si la partie est terminée ou non (BOOL)
        "premier_clic_solo": premier_clic_solo         # Sauvegarde du premier clic
    }

    with open("sauvegarde_solo.json", "w") as f:       # On ouvre le fichier en mode écriture (write -> w)
        json.dump(donnees, f)                          # On écrit le dictionnaire au format JSON


def charger_partie_solo():
    '''Dans cet fonction suivante on va recharger la partie solo'''
    global plateau_solo, jetons_ratelier_solo, score_solo   # On récupère les variables qui nous sont utiles et on les modifie par leur valeur sauvegarder 
    global partie_terminee_solo, premier_clic_solo          # -----

    with open("sauvegarde_solo.json", "r") as f:            # Ouvre le fichier en mode lecture
        donnees = json.load(f)                              # Lit le fichier JSON et puis le transforme en dico Python

    plateau_solo = donnees["plateau_solo"]                  # On recharge les données stockés
    jetons_ratelier_solo = donnees["jetons_ratelier_solo"]  # ----
    score_solo = donnees["score_solo"]                      # -----
    partie_terminee_solo = donnees["partie_terminee_solo"]  # -----
    premier_clic_solo = donnees["premier_clic_solo"]        # -----

# -------------------------------------------
# Sauvegarde pour le mode multijoueur
# -------------------------------------------

def sauvegarder_partie_multi():
    '''On crée un dictionnaire qui va contenir tout l’état du jeu (comme le mode solo)'''
    donnees = {
        "plateau_multi": plateau_multi,                 # sauvegarde l'état du plateau multijoueur 
        "jetons_ratelier_multi": jetons_ratelier_multi, # etc 
        "score_j1_multi": score_j1_multi,
        "score_j2_multi": score_j2_multi,
        "tour_joueur_1_multi": tour_joueur_1_multi,
        "partie_terminee_multi": partie_terminee_multi,
        "premier_clic_multi": premier_clic_multi
    }

    with open("sauvegarde_multi.json", "w") as f:       # Ouvre le fichier de sauvegarde multijoueur en écriture.
        json.dump(donnees, f)                           # Convertit le dico Python en JSON et l'écrit dans le fichier

def charger_partie_multi():
    '''Dans cet fonction suivante on va recharger la partie multijoueur'''
    global plateau_multi, jetons_ratelier_multi         # On récupère les varibales qui nous concernent pour les modifié dans le but de reprendre leur valeur sauvegarder
    global score_j1_multi, score_j2_multi               # ----
    global tour_joueur_1_multi, partie_terminee_multi, premier_clic_multi # ---

    with open("sauvegarde_multi.json", "r") as f:       # On ouvre le fichier sauvegarder en lecture (read)
        donnees = json.load(f)                          # Transforme le dico json en python
    '''Rechargement de l'état (ils reprennent leur valeurs respectifs lors de la sauvegarde)'''
    plateau_multi = donnees["plateau_multi"]
    jetons_ratelier_multi = donnees["jetons_ratelier_multi"]
    score_j1_multi = donnees["score_j1_multi"]
    score_j2_multi = donnees["score_j2_multi"]
    tour_joueur_1_multi = donnees["tour_joueur_1_multi"]
    partie_terminee_multi = donnees["partie_terminee_multi"]
    premier_clic_multi = donnees["premier_clic_multi"]

# -------------------------------------
def afficher_page_accueil():
    """Affiche la page d'accueil et retourne le mode sélectionné"""
    fltk.cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)   # Crée la fenetre graphique avec les dimensions définies par les constantes
    fltk.efface_tout() # Efface tout ce qui pourrait éventuellement déjà etre affiché
    fltk.rectangle(0, 0, LARGEUR_FENETRE, HAUTEUR_FENETRE, remplissage="black", couleur="") # Dessine un fond noir qui recouvre toute la fenetre

    fltk.texte(LARGEUR_FENETRE//2, 150, "Bienvenue sur PICK TOK !", couleur="white", taille=40, ancrage="center")   # Affiche le titre principale au centre
    fltk.texte(LARGEUR_FENETRE//2, 250, "Projet AP1 - 2025", couleur="white", taille=25, ancrage="center")          # Affiche le sous titre du projet
    fltk.texte(LARGEUR_FENETRE//2, 350, "Choisissez un mode", couleur="white", taille=20, ancrage="center")         # Invitation à choisir un mode de jeu

    def cadre_texte(texte, x, y, couleur_texte="white"):
        '''Cet fonction a pour but de dessiner 
            un bouton avec un texte entourée de cadre rouge et à retouner ses coordonnées '''
        taille_police = 40
        largeur, hauteur = fltk.taille_texte(texte, "Courier", taille_police)   #Calcule la taille réelle du texte à l'écran (EN PIXELS !)
        marge = 10  # Il s'agit de l'espace autour du texte
        fltk.rectangle(x - largeur//2 - marge, y - hauteur//2 - marge,
                       x + largeur//2 + marge, y + hauteur//2 + marge,
                       remplissage="", couleur="red")   # dessine le cadre rouge autour du texte
        fltk.texte(x, y, texte, taille=taille_police, couleur=couleur_texte, ancrage="center")  # Affiche le texte centré dans le cadre via les coordonnées
        return (x - largeur//2 - marge, y - hauteur//2 - marge,
                x + largeur//2 + marge, y + hauteur//2 + marge) # Ici on retourne les coordonnées du rectangle cliquable (elles vont servir à detecter les clics)

    x_solo, y_solo, x2_solo, y2_solo = cadre_texte("Solo", LARGEUR_FENETRE//4, HAUTEUR_FENETRE - 100)   # Creation du bouton solo a gauche
    x_multi, y_multi, x2_multi, y2_multi = cadre_texte("Multijoueur", 3*LARGEUR_FENETRE//4, HAUTEUR_FENETRE - 100)  #Creation du bouton multijoueur a droite

    fltk.mise_a_jour()  # Met à jour la fenêtre. Les dessins ne sont affichés qu’après l’appel à cette fonction.

    while True:     # Sa fait une boucle infini tant que l'utilisateur ne clique pas (pas d'action = pas de changement)
        ev = fltk.attend_ev()   # J'attend qu'un évènement se produise dans la fenetre -> et je le stocke dans la variable ev
        if fltk.type_ev(ev) == "Quitte":    # Si le l'utilsateur ferme sa fenetre
            fltk.ferme_fenetre()        # Alors, on ferme le jeu
            exit()                  # Termine le programme immédiatement           
        
        if fltk.type_ev(ev) == "ClicGauche":        # si l'utlisateur clique a gauche
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev) # on recupère ici les coordonées du clic 
            if x_solo <= x <= x2_solo and y_solo <= y <= y2_solo:   # Si il est compris dans le bouton Solo
                fltk.ferme_fenetre()    # ferme la fenetre
                return "solo"           # et on retourne solo
            elif x_multi <= x <= x2_multi and y_multi <= y <= y2_multi: # meme logique pour le mode multijoueur
                fltk.ferme_fenetre()
                return "multi"


#             --------------------------SOLO------------------------------
# CONSTANTES
'''Dimensions de la fenetre pour le modo solo'''
LARGEUR_FENETRE_SOLO = 800
HAUTEUR_FENETRE_SOLO = 600

NB_COLONNES_SOLO = 8
NB_LIGNES_SOLO = 10

TAILLE_CELLULE_SOLO = 55    # chaque cellule = 55 pixels
DECALAGE_X_SOLO = 100       # décalage (marge d'écart) pour ne pas coller la fenetre
DECALAGE_Y_SOLO = 20        # ------

COULEURS_FOND_SOLO = ["light pink", "light blue", "light green"]    # Il s'agit là des coueleurs qu'on a choisi pour le fond du jeu
COULEURS_JETONS_SOLO = ["yellow", "red", "green", "orange", "blue"] # Ce sont les couleurs des jetons

RATELIER_X_SOLO = 600
RATELIER_Y_SOLO = 20
CAPACITE_RATELIER_SOLO = 5  # 5 jetons max dans le ratelier 

# --------------------------------------------------------------------
# VARIABLES GLOBALES
# --------------------------------------------------------------------

plateau_solo = [[None for _ in range(NB_COLONNES_SOLO)] for _ in range(NB_LIGNES_SOLO)]     # Création du plateau vide, matrice 10×8 remplie de None.
''' Variables qui vont permettre de gérer tout ce qui est : 
    les jetons du joueur, le score, les clics, etc ... '''
jetons_ratelier_solo = []  
score_solo = 0
partie_terminee_solo = False
ecran_fin_affiche_solo = False
premier_clic_solo = False

# --------------------------------------------------------------------
# AFFICHAGE
# --------------------------------------------------------------------

def afficher_page_accueil_solo():
    pass  # Inutile, on utilise la page d'accueil commune du début

def coordonnees_cellule_solo(colonne, ligne):
    """Convertit une cellule (colonne, ligne) en coordonnées pixels"""
    x = DECALAGE_X_SOLO + colonne * TAILLE_CELLULE_SOLO
    y = DECALAGE_Y_SOLO + ligne * TAILLE_CELLULE_SOLO
    return x, y

def afficher_grille_solo():
    '''Trace les lignes verticales de la grille'''
    for col in range(NB_COLONNES_SOLO + 1):
        x = DECALAGE_X_SOLO + col * TAILLE_CELLULE_SOLO
        fltk.ligne(x, DECALAGE_Y_SOLO,
                   x, DECALAGE_Y_SOLO + NB_LIGNES_SOLO * TAILLE_CELLULE_SOLO)
    '''Trace les lignes horizontale, complétant ainsi la grille'''
    for lig in range(NB_LIGNES_SOLO + 1):
        y = DECALAGE_Y_SOLO + lig * TAILLE_CELLULE_SOLO
        fltk.ligne(DECALAGE_X_SOLO, y,
                   DECALAGE_X_SOLO + NB_COLONNES_SOLO * TAILLE_CELLULE_SOLO, y)

def afficher_zone_score_solo():
    ''' Dessine yn rectangle noir pour encadrer le score'''
    fltk.texte(LARGEUR_FENETRE_SOLO - 150, 410, "Score", taille=20)
    fltk.rectangle(LARGEUR_FENETRE_SOLO - 210, 410,
                   LARGEUR_FENETRE_SOLO - 20, 520)

def afficher_ratelier_solo():
    '''Dessine le ratelier vertical'''
    ''' Trace les lignes horizontales du ratelier (commes cases empilés verticalement)'''
    for i in range(CAPACITE_RATELIER_SOLO + 1):
        y = RATELIER_Y_SOLO + i * TAILLE_CELLULE_SOLO
        fltk.ligne(RATELIER_X_SOLO, y,
                   RATELIER_X_SOLO + TAILLE_CELLULE_SOLO, y)
    # -- Trace les bordure verticales du ratelier pour fermer les cases
    fltk.ligne(RATELIER_X_SOLO, RATELIER_Y_SOLO,
               RATELIER_X_SOLO, RATELIER_Y_SOLO + CAPACITE_RATELIER_SOLO * TAILLE_CELLULE_SOLO)

    fltk.ligne(RATELIER_X_SOLO + TAILLE_CELLULE_SOLO, RATELIER_Y_SOLO,
               RATELIER_X_SOLO + TAILLE_CELLULE_SOLO, RATELIER_Y_SOLO + CAPACITE_RATELIER_SOLO * TAILLE_CELLULE_SOLO)
    # On ajoute le texte Ratelier a coter du plateau pour indiquer son emplacement
    fltk.texte(RATELIER_X_SOLO + 70, RATELIER_Y_SOLO + 10, "Ratelier", taille=20)

def afficher_score_solo():
    """Met à jour l'affichage du score (uniquement après le premier clic : fond gris et valeur) """
    global premier_clic_solo # Nous allons prendre et modifier la variable globale premier_clic_solo
    if premier_clic_solo:
        '''Dessine un rectangle gris claie pour effacer l'ancien score et créer un fond visible'''
        fltk.rectangle(LARGEUR_FENETRE_SOLO - 200, 440,
                       LARGEUR_FENETRE_SOLO - 30, 500,
                       remplissage="light grey", couleur="light grey")
        '''Nous allons afficher le score actuel (score_solo) en rouge au centre de ce rectangle'''
        fltk.texte(LARGEUR_FENETRE_SOLO - 115, 470,
                   str(score_solo), taille=30,
                   couleur="red", ancrage="center")
        '''Dessine un rectangle noir autour du gris, histoire que cela soit propre'''
        fltk.rectangle(LARGEUR_FENETRE_SOLO - 200, 440,
                       LARGEUR_FENETRE_SOLO - 30, 500,
                       couleur="black")

# --------------------------------------------------------------------
# JETONS
# --------------------------------------------------------------------

def dessiner_jeton_plateau_solo(jeton, centre_x, centre_y):
    """Dessine un jeton sur le plateau"""
    if jeton["type"] == "simple":
        if "affichage" in jeton:
            couleur = jeton["affichage"]
        else : couleur = jeton["couleur"]
        fltk.cercle(centre_x, centre_y, 22, remplissage=couleur, couleur="")
    else:
        fltk.cercle(centre_x, centre_y, 22, remplissage="white", couleur="black")
        fltk.cercle(centre_x, centre_y, 12, remplissage=jeton["couleur"], couleur="black")

def dessiner_jeton_ratelier_solo(jeton, index):
    """Dessine un jeton dans le ratelier"""
    centre_x = RATELIER_X_SOLO + TAILLE_CELLULE_SOLO // 2
    centre_y = RATELIER_Y_SOLO + index * TAILLE_CELLULE_SOLO + TAILLE_CELLULE_SOLO // 2
    fltk.cercle(centre_x, centre_y, 22, remplissage=jeton["couleur"], couleur="")  # Dessine un cercle plein

# --------------------------------------------------------------------
# CASES NOIRES
# --------------------------------------------------------------------

def colorier_cellule_solo(colonne, ligne, couleur):
    """Colorie une cellule du plateau"""
    x1, y1 = coordonnees_cellule_solo(colonne, ligne)
    x2 = x1 + TAILLE_CELLULE_SOLO   # calcule le coin bas-droit de la cellule
    y2 = y1 + TAILLE_CELLULE_SOLO
    fltk.rectangle(x1 + 2, y1 + 2, x2 - 1, y2 - 1, remplissage=couleur, couleur="") # dessin du rectangle

def generer_cases_noires_solo():
    '''Génère aléatoirement des cases noires sur 
    le plateau et vérifie que la grille est jouable'''
    grille_valide = False
    while not grille_valide:    # Tant que la grille n'est pas jouable, on recommence tout 
        N = 10
        cases_noires = []   # cet listes va stocker les positions des cases noires
        while len(cases_noires) < N: # tant qu'on a pas 10 cases noires on continue de boucler
            col = random.randint(0, NB_COLONNES_SOLO-1) # on choisit au hasard uen colonne valide
            lig = random.randint(0, NB_LIGNES_SOLO-1)   # -- ligne valide
            if (col, lig) not in cases_noires: # Point important : on verifie que cet case n'a pas déjà été choisie
                cases_noires.append((col, lig)) # si la case est nouvelle on l'ajoute alors et le compteur augmente de meme

        # Réinitialiser le plateau avant de placer les cases noires (plateau avec des jetons partout)
        initialiser_plateau_solo()  

        for col, lig in cases_noires:   # cases_noires c'est une liste de tuples (ex :[(2, 4),..] )
            colorier_cellule_solo(col, lig, "black") # a partir de la fonction crée ci dessus, elle va calculer les coordonées pixel de la cellule et dessiner un rectangle noir 
            plateau_solo[lig][col] = {"type": "scelle"} # IMPORTANT ICI ! elle modifie le modèle de données du jeu (important pour la sauvegarde aussi)

        # Vérifier si la grille est jouable
        grille_valide = grille_est_jouable_solo() # si jouable alors True sinon False (fonction ci-dessous nous dir 1 clique = true)

# --------------------------------------------------------------------
# INITIALISATION
# --------------------------------------------------------------------

def initialiser_plateau_solo():
    """Place automatiquement les jetons sur le plateau"""
    for lig in range(NB_LIGNES_SOLO):   # On parcourt toute les cases du plateau, ligne par ligne
        for col in range(NB_COLONNES_SOLO): # -- colonne par colonne
            '''Calcul du centre de la cellule'''
            centre_x = DECALAGE_X_SOLO + col * TAILLE_CELLULE_SOLO + TAILLE_CELLULE_SOLO // 2   # A noter que le '+ TAILLE_CELLULE_SOLO // 2 permet de centrer le jeton dans la case
            centre_y = DECALAGE_Y_SOLO + lig * TAILLE_CELLULE_SOLO + TAILLE_CELLULE_SOLO // 2

            if lig == 0:    # première ligne du plateau (logique)
                jeton = {
                    "type": "simple",
                    "couleur": random.choice(COULEURS_JETONS_SOLO),
                    "capturable": True
                }
            else:
                jeton = {
                    "type": "double",
                    "couleur": random.choice(COULEURS_JETONS_SOLO),
                    "capturable": False
                }

            plateau_solo[lig][col] = jeton  # On met le jeton dans la matrice du plateau
            dessiner_jeton_plateau_solo(jeton, centre_x, centre_y)  # On dessine le jeton à l'écran 


def plateau_est_vide_solo():
    """Vérifie si le plateau ne contient plus de jetons jouables (ignore les cases scellées) -> plus aucun jeton jouable sur le plateau"""
    for ligne in plateau_solo:    # parcourt chaque ligne de la liste plateau_solo
        for jeton in ligne:       # parcourt chaque jeton de chaque liste ligne (attention dans ce cas la on est dans une liste de liste)
            if jeton is not None:   
                if jeton["type"] != "scelle":
                    return False  # Alors le plateau n'est pas vide -> on continue alors
    return True




def jeton_est_accessible_solo(ligne, colonne):
    """Vérifie si un jeton est accessible (pas entouré de cases noires)"""
    voisins = [(ligne - 1, colonne), (ligne + 1, colonne),
               (ligne, colonne - 1), (ligne, colonne + 1)] # il s'agit là des cases tout autour pas les diagonales

    for lig_v, col_v in voisins:
        if 0 <= lig_v < NB_LIGNES_SOLO and 0 <= col_v < NB_COLONNES_SOLO: # on s'assure que on est tjr dans le plateau
            voisin = plateau_solo[lig_v][col_v]
            if voisin is None:
                return True
            if voisin is not None and voisin["type"] != "scelle": # None signifie que la case est vide et donc accessible
                return True
    return False

def grille_est_jouable_solo():
    """Vérifie si la grille est jouable (au moins un jeton capturable et accessible)"""
    for ligne in range(NB_LIGNES_SOLO): # on parcourt toutes les cases du plateau (indices) -> lignes
        for colonne in range(NB_COLONNES_SOLO): # ---> colonnes
            jeton = plateau_solo[ligne][colonne] # -- > recuperation du jeton (peut etre None, simple, double, scelle)
            if jeton is not None:   # on s'assure que la case contient un jeton
                if jeton["type"] == "simple" and jeton["capturable"] == True:
                    if jeton_est_accessible_solo(ligne, colonne):
                        return True
    return False

def contient_triplette_solo(ratelier):
    """Vérifie si le râtelier contient 3 jetons de la même couleur"""
    couleurs = [jeton["couleur"] for jeton in ratelier] # on récupère la couleur de CHAQUE jeton du ratelier
    for couleur in set(couleurs): # On va boucler sur chaque couleur différente sur le ratelier
        if couleurs.count(couleur) == 3: #ici le couleurs.count(couleur) va comptez combien de fois cet couleurs apparait si 3 fois alors == triplette
            return True
    return False # aucune triplette détecté


# --------------------------------------------------------------------
# INTERACTIONS
# --------------------------------------------------------------------

def cellule_depuis_clic_solo(x, y):
    '''Cet fonction fait le lien entre le clic de la souris et le plateau de jeu'''
    if x < DECALAGE_X_SOLO or y < DECALAGE_Y_SOLO: # c'est a dire or de la grille
        return None

    colonne = (x - DECALAGE_X_SOLO) // TAILLE_CELLULE_SOLO # donne l'indice de la cellule. (x - DECALAGE_X_SOLO) donne la position relative à la grille
    ligne = (y - DECALAGE_Y_SOLO) // TAILLE_CELLULE_SOLO

    if 0 <= colonne < NB_COLONNES_SOLO and 0 <= ligne < NB_LIGNES_SOLO: # on verifie que la ligne existe
        return colonne, ligne   # on retourne un tuple

    return None     # le clic n'est pas sur une cellule du plateau

def gerer_clic_souris_solo(x, y):
    global score_solo, partie_terminee_solo, premier_clic_solo  # on prend ces variables définie pour ce

    if partie_terminee_solo:
        return  # partie terminee -> alors le joueur ne peut plus jouer

    cellule = cellule_depuis_clic_solo(x, y)    #si le clic est hors du plateau on sort immédiatement
    if cellule is None:
        return

    '''on récupère le jeton cliqué '''
    colonne, ligne = cellule
    jeton_clique = plateau_solo[ligne][colonne]

    if jeton_clique is None: # ici on vérifie, c'est a dire si ce n'est pas un vrai jeton (cases vides, scelle)
        return # pas vrai jeton alors on ignore, renvoie rien

    if jeton_clique["type"] == "simple" and jeton_clique["capturable"]: # on verifie si le jeton est cliquable et simple
        if not premier_clic_solo:
            premier_clic_solo = True # affiche le score uniqument après la première action

        plateau_solo[ligne][colonne] = None  # Retirer le jeton du plateau (après clique)
         # Redessiner la cellule vide
        x1, y1 = coordonnees_cellule_solo(colonne, ligne)
        x2 = x1 + TAILLE_CELLULE_SOLO
        y2 = y1 + TAILLE_CELLULE_SOLO
        fltk.rectangle(x1 + 2, y1 + 2, x2 - 1, y2 - 1, remplissage="light grey", couleur="light grey")

        voisins = [(ligne - 1, colonne), (ligne + 1, colonne),
                   (ligne, colonne - 1), (ligne, colonne + 1)]

        '''Pour chaque voisin, s'il existe et s'il est double - > il devient simple et capturable'''
        for lig_v, col_v in voisins:
            if 0 <= lig_v < NB_LIGNES_SOLO and 0 <= col_v < NB_COLONNES_SOLO:
                voisin = plateau_solo[lig_v][col_v]
                if voisin is not None and voisin["type"] == "double":
                    voisin["type"] = "simple"
                    voisin["capturable"] = True

                    cx_v = DECALAGE_X_SOLO + col_v * TAILLE_CELLULE_SOLO + TAILLE_CELLULE_SOLO // 2
                    cy_v = DECALAGE_Y_SOLO + lig_v * TAILLE_CELLULE_SOLO + TAILLE_CELLULE_SOLO // 2
                    dessiner_jeton_plateau_solo(voisin, cx_v, cy_v)     # On le dessine sur le plateau

        if len(jetons_ratelier_solo) < CAPACITE_RATELIER_SOLO:
            jetons_ratelier_solo.append({"couleur": jeton_clique["couleur"]})   #On stocke la couleur du jeton capturé

        '''On nettoie visuellement le ratelier afin d'éviter des superpositions'''
        fltk.rectangle(RATELIER_X_SOLO, RATELIER_Y_SOLO,
                       RATELIER_X_SOLO + TAILLE_CELLULE_SOLO,
                       RATELIER_Y_SOLO + CAPACITE_RATELIER_SOLO * TAILLE_CELLULE_SOLO,
                       remplissage="light grey", couleur="black")

        afficher_ratelier_solo()    # on redessine la structure du ratelier

        for index, jeton in enumerate(jetons_ratelier_solo):
            dessiner_jeton_ratelier_solo(jeton, index)  # redessiner le jeton (index -> positions, jetons -> couleurs)

        couleur_cible = jeton_clique["couleur"] # connaitre la coueleurs du jeton capturé
        
        '''transforme la liste de dictionnaire en liste de couleurs ( ex : jetons_ratelier_solo = 
        [{"couleur": "red"}, {"couleur": "blue"}, {"couleur": "red"}] -> ["red", "blue", "red"] ),
          ensuite elle comptent cmb de fois elle appaait avec .count()'''
        compteur_cible = [j["couleur"] for j in jetons_ratelier_solo].count(couleur_cible)

        if compteur_cible >= 3: # si y'a au moins 3 jetons de meme couelurs
            ratelier_etait_plein = len(jetons_ratelier_solo) == CAPACITE_RATELIER_SOLO # dans le cas ou le ratelier était plein on mémorise avant de modifier le ratelier

            nouveau_ratelier = []
            compteur_supprimes = 0
            for jeton in jetons_ratelier_solo: # on regarde chaque jeton un par un
                if jeton["couleur"] == couleur_cible and compteur_supprimes < 3: # si il s'agit d'un jeton de meme couelurs et que l'on n'a pas encore supprimébses 3 là 
                    compteur_supprimes += 1 # ces jetons sont supprimées 
                else:
                    nouveau_ratelier.append(jeton) # tout les jetons d'autres couleurs sont conservées
            jetons_ratelier_solo[:] = nouveau_ratelier #on remplace donc ce ratelier (on modifie la liste existante sans en crée une nouvelle ref)

            fltk.rectangle(
                RATELIER_X_SOLO, RATELIER_Y_SOLO,
                RATELIER_X_SOLO + TAILLE_CELLULE_SOLO,
                RATELIER_Y_SOLO + CAPACITE_RATELIER_SOLO * TAILLE_CELLULE_SOLO,
                remplissage="light grey", couleur="black"
            )

            afficher_ratelier_solo()
            
            for index, jeton in enumerate(jetons_ratelier_solo):
                dessiner_jeton_ratelier_solo(jeton, index)

            if ratelier_etait_plein:
                score_solo += 2 # quand ratelier était plein alors on ajoute 2 points au score
            else:
                score_solo += 1 # sinon 1 points

            afficher_score_solo() # score redessiné sur l'instant

        afficher_score_solo() # on le met encore à jour

        if plateau_est_vide_solo(): # si cet fonction est TRUE
            '''On afficge un message de récompense'''
            fltk.rectangle(LARGEUR_FENETRE_SOLO - 210, 310, LARGEUR_FENETRE_SOLO - 20, 400, remplissage="white", couleur="black")
            fltk.texte(LARGEUR_FENETRE_SOLO - 115, 330, "Bonus !!! :", couleur="red", ancrage="center", taille=23)
            fltk.texte(LARGEUR_FENETRE_SOLO - 115, 380, "+ 20 points", couleur="red", ancrage="center", taille=23)

            fltk.mise_a_jour()
            fltk.attente(2)  # Attendre 2 secondes pour laisser le temps de lire le message

            # Augmenter le score de 20 points
            score_solo += 20
            afficher_score_solo()
            partie_terminee_solo = True

        if len(jetons_ratelier_solo) >= CAPACITE_RATELIER_SOLO: # cas inverse ratelier plein et sans solution alors -> DEFAITE
            if not contient_triplette_solo(jetons_ratelier_solo) and not plateau_est_vide_solo(): # les deux conditions sont : PAS de triplette et plateau pas vide
                partie_terminee_solo = True
                '''On affiche le message de foin de partie'''
                fltk.rectangle(LARGEUR_FENETRE_SOLO - 210, 360, LARGEUR_FENETRE_SOLO - 20, 400, remplissage="white", couleur="black")
                fltk.texte(LARGEUR_FENETRE_SOLO - 115, 380, "Partie perdu !", couleur="red", ancrage="center", taille=23)

        fltk.mise_a_jour()  # dernière mis a jour de la game
        sauvegarder_partie_solo() # sauvegarde finale

def afficher_resultat_solo():
    """Affiche l'écran de fin avec le score du joueur"""
    fltk.efface_tout()
    fltk.rectangle(0, 0, LARGEUR_FENETRE_SOLO, HAUTEUR_FENETRE_SOLO, remplissage="black")

    fltk.texte(LARGEUR_FENETRE_SOLO // 2, HAUTEUR_FENETRE_SOLO // 2 - 150, "Fin de la partie !", taille=40, ancrage="center", couleur="white")

    # Ajout du score du joueur
    fltk.texte(LARGEUR_FENETRE_SOLO // 2, HAUTEUR_FENETRE_SOLO // 2 - 50, f"Votre score est de : {score_solo} points", taille=30, ancrage="center", couleur="white")

    fltk.mise_a_jour()

def afficher_ecran_fin_solo():
    """Affiche l'écran noir de fin"""
    fltk.efface_tout()
    fltk.rectangle(0, 0,
                   LARGEUR_FENETRE_SOLO, HAUTEUR_FENETRE_SOLO,
                   remplissage="black")

    fltk.texte(LARGEUR_FENETRE_SOLO // 2, HAUTEUR_FENETRE_SOLO // 2 - 100,
               "Merci d'avoir joué !",
               taille=40, ancrage="center", couleur="white")

    fltk.texte(LARGEUR_FENETRE_SOLO // 2, HAUTEUR_FENETRE_SOLO // 2 + 20,
               "À bientôt sur PICK TOK ",
               taille=25, ancrage="center", couleur="red")

    fltk.texte(LARGEUR_FENETRE_SOLO // 2, HAUTEUR_FENETRE_SOLO - 50,
               "(Cliquez sur la croix pour fermer)",
               taille=18, ancrage="center", couleur="grey")

    fltk.mise_a_jour()

def lancer_mode_solo():     # le chef d'orchestre, le maestro du mode solo
    """Lance le mode solo"""
    global plateau_solo, jetons_ratelier_solo, score_solo, partie_terminee_solo, ecran_fin_affiche_solo, premier_clic_solo
    plateau_solo = [[None for _ in range(NB_COLONNES_SOLO)] for _ in range(NB_LIGNES_SOLO)]
    jetons_ratelier_solo = []
    score_solo = 0
    partie_terminee_solo = False
    ecran_fin_affiche_solo = False
    premier_clic_solo = False

    fltk.cree_fenetre(LARGEUR_FENETRE_SOLO, HAUTEUR_FENETRE_SOLO)
    fltk.rectangle(0, 0, LARGEUR_FENETRE_SOLO, HAUTEUR_FENETRE_SOLO, remplissage=random.choice(COULEURS_FOND_SOLO))
    afficher_grille_solo()
    afficher_zone_score_solo()
    afficher_ratelier_solo()
    initialiser_plateau_solo()
    generer_cases_noires_solo()
    fltk.mise_a_jour()

    while True: # le jeu tourne tant que la fenetre est ouverte
        evenement = fltk.attend_ev() # le programme attend le clique comme citée précdemment

        if evenement:
            if fltk.type_ev(evenement) == "Quitte":
                fltk.ferme_fenetre()
                exit()

        if fltk.type_ev(evenement) == "ClicGauche" and not partie_terminee_solo:
            gerer_clic_souris_solo(fltk.abscisse(evenement),
                                  fltk.ordonnee(evenement))

        if partie_terminee_solo and not ecran_fin_affiche_solo:
            fltk.attente(1.5) # temps d'attente pour que la page finale s'affiche 1s
            afficher_resultat_solo()
            fltk.attente(3)
            afficher_ecran_fin_solo()
            ecran_fin_affiche_solo = True

        fltk.mise_a_jour()


######################################################################
#                  AP1 - 2025 - Projet 1 - PICK TOK (Multijoueur)     #
######################################################################

# --------------------------------------------------------------------
# CONSTANTES
# --------------------------------------------------------------------

LARG_MULTI = 900
HAUT_MULTI = 620

NB_COLS_MULTI = 8
NB_LIGS_MULTI = 10

TAILLE_CEL_MULTI = 55
X_OFFSET_MULTI = 100
Y_OFFSET_MULTI = 20

COULEURS_FOND_MULTI = ["Light Blue", "Light Green", "Light Pink"]
COULEURS_JETONS_MULTI = ["red", "blue", "orange", "green", "yellow"]

RATELIER_X_MULTI = 600
RATELIER_Y1_MULTI = 20   # Y de départ du râtelier Joueur 1
RATELIER_Y2_MULTI = 315  # Y de départ du râtelier Joueur 2 (décalé en bas)
RATELIER_CASES_MULTI = 5

# --------------------------------------------------------------------
# VARIABLES GLOBALES
# --------------------------------------------------------------------

plateau_multi = [[None for _ in range(NB_COLS_MULTI)] for _ in range(NB_LIGS_MULTI)]
jetons_ratelier_multi = []
score_j1_multi = 0
score_j2_multi = 0
tour_joueur_1_multi = True
partie_terminee_multi = False
ecran_fin_affiche_multi = False
premier_clic_multi = False
N_CASES_NOIRES_MULTI = 10

# --------------------------------------------------------------------
# AFFICHAGE
# --------------------------------------------------------------------

def afficher_page_accueil_multi():
    pass  # Inutile, on utilise la page d'accueil commune

def coord_case_multi(col, lig):
    """Convertit des indices de grille en coordonnées pixel."""
    x = X_OFFSET_MULTI + col * TAILLE_CEL_MULTI
    y = Y_OFFSET_MULTI + lig * TAILLE_CEL_MULTI
    return x, y

def afficher_grille_multi():
    """Dessine la grille du plateau"""
    for col in range(NB_COLS_MULTI + 1):
        x = X_OFFSET_MULTI + col * TAILLE_CEL_MULTI
        fltk.ligne(x, Y_OFFSET_MULTI, x, Y_OFFSET_MULTI + NB_LIGS_MULTI * TAILLE_CEL_MULTI, couleur="black")

    for lig in range(NB_LIGS_MULTI + 1):
        y = Y_OFFSET_MULTI + lig * TAILLE_CEL_MULTI
        fltk.ligne(X_OFFSET_MULTI, y, X_OFFSET_MULTI + NB_COLS_MULTI * TAILLE_CEL_MULTI, y, couleur="black")

def afficher_zone_score_j1_multi():
    """Affiche la zone du score du joueur 1"""
    fltk.texte(LARG_MULTI-265, 360, "Score J1", taille=20, ancrage="center")
    fltk.rectangle(LARG_MULTI-350, 345, LARG_MULTI-180, 445, couleur="black")

def afficher_zone_score_j2_multi():
    """Affiche la zone du score du joueur 2"""
    fltk.texte(LARG_MULTI-265, 485, "Score J2", taille=20, ancrage="center")
    fltk.rectangle(LARG_MULTI-350, 470, LARG_MULTI-180, 570, couleur="black")

def afficher_ratelier_multi():
    """Dessine le ratelier vertical commun"""
    if premier_clic_multi:
        fltk.rectangle(RATELIER_X_MULTI, RATELIER_Y1_MULTI, RATELIER_X_MULTI + TAILLE_CEL_MULTI, RATELIER_Y1_MULTI + RATELIER_CASES_MULTI * TAILLE_CEL_MULTI, remplissage="light grey", couleur="black")
    else:
        fltk.rectangle(RATELIER_X_MULTI, RATELIER_Y1_MULTI, RATELIER_X_MULTI + TAILLE_CEL_MULTI, RATELIER_Y1_MULTI + RATELIER_CASES_MULTI * TAILLE_CEL_MULTI, remplissage="", couleur="black")
    for i in range(RATELIER_CASES_MULTI + 1):
        y = RATELIER_Y1_MULTI + i * TAILLE_CEL_MULTI
        fltk.ligne(RATELIER_X_MULTI, y, RATELIER_X_MULTI + TAILLE_CEL_MULTI, y)
    fltk.ligne(RATELIER_X_MULTI, RATELIER_Y1_MULTI, RATELIER_X_MULTI, RATELIER_Y1_MULTI + RATELIER_CASES_MULTI * TAILLE_CEL_MULTI)
    fltk.ligne(RATELIER_X_MULTI + TAILLE_CEL_MULTI, RATELIER_Y1_MULTI, RATELIER_X_MULTI + TAILLE_CEL_MULTI, RATELIER_Y1_MULTI + RATELIER_CASES_MULTI * TAILLE_CEL_MULTI)
    fltk.texte(RATELIER_X_MULTI + 70, RATELIER_Y1_MULTI + 10, "Ratelier", taille=20)

def afficher_score_j1_multi():
    """Met à jour l'affichage du score du joueur 1"""
    if premier_clic_multi:
        fltk.rectangle(LARG_MULTI-340, 375, LARG_MULTI-190, 435, remplissage="light grey", couleur="light grey")
    fltk.texte(LARG_MULTI-265, 405, str(score_j1_multi), taille=30, couleur="red", ancrage="center")
    fltk.rectangle(LARG_MULTI-340, 375, LARG_MULTI-190, 435, couleur="black")

def afficher_score_j2_multi():
    """Met à jour l'affichage du score du joueur 2"""
    if premier_clic_multi:
        fltk.rectangle(LARG_MULTI-340, 500, LARG_MULTI-190, 560, remplissage="light grey", couleur="light grey")
    fltk.texte(LARG_MULTI-265, 530, str(score_j2_multi), taille=30, couleur="red", ancrage="center")
    fltk.rectangle(LARG_MULTI-340, 500, LARG_MULTI-190, 560, couleur="black")

# --------------------------------------------------------------------
# JETONS
# --------------------------------------------------------------------

def dessiner_jeton_plateau_multi(jeton, centre_x, centre_y):
    """Dessine un jeton sur le plateau"""
    if jeton["type"] == "simple":
        if "affichage" in jeton:
            couleur = jeton["affichage"]
        else : couleur = jeton ["couleur"]
        
        fltk.cercle(centre_x, centre_y, 22, remplissage=couleur, couleur="black")
    else:
        fltk.cercle(centre_x, centre_y, 22, remplissage="white", couleur="black")
        fltk.cercle(centre_x, centre_y, 12, remplissage=jeton["couleur"], couleur="black")

def dessiner_jeton_ratelier_multi(jeton, index):
    """Dessine un jeton dans le ratelier commun"""
    centre_x = RATELIER_X_MULTI + TAILLE_CEL_MULTI // 2
    centre_y = RATELIER_Y1_MULTI + index * TAILLE_CEL_MULTI + TAILLE_CEL_MULTI // 2
    fltk.cercle(centre_x, centre_y, 22, remplissage=jeton["couleur"], couleur="black")

# --------------------------------------------------------------------
# CASES NOIRES
# --------------------------------------------------------------------

def colorier_case_multi(col, lig, couleur):
    """Colorie en `couleur` la case (col, lig) du plateau."""
    x1, y1 = coord_case_multi(col, lig)
    fltk.rectangle(x1+2, y1+2, x1+TAILLE_CEL_MULTI-1, y1+TAILLE_CEL_MULTI-1, remplissage=couleur, couleur="")

def generer_cases_noires_multi():
    """Génère des cases noires aléatoires uniques sur le plateau."""
    cases_noires = set()
    while len(cases_noires) < N_CASES_NOIRES_MULTI:
        col = random.randint(0, NB_COLS_MULTI - 1)
        lig = random.randint(0, NB_LIGS_MULTI - 1)
        cases_noires.add((col, lig))
    for col, lig in cases_noires:
        colorier_case_multi(col, lig, "black")
        plateau_multi[lig][col] = {"type": "scelle"}

# --------------------------------------------------------------------
# INITIALISATION
# --------------------------------------------------------------------

def initialiser_plateau_multi():
    """Place automatiquement les jetons sur le plateau"""
    for lig in range(NB_LIGS_MULTI):
        for col in range(NB_COLS_MULTI):
            centre_x = X_OFFSET_MULTI + col * TAILLE_CEL_MULTI + TAILLE_CEL_MULTI // 2
            centre_y = Y_OFFSET_MULTI + lig * TAILLE_CEL_MULTI + TAILLE_CEL_MULTI // 2

            if lig == 0:
                jeton = {"type": "simple", "couleur": random.choice(COULEURS_JETONS_MULTI), "capturable": True}
            else:
                jeton = {"type": "double", "couleur": random.choice(COULEURS_JETONS_MULTI), "capturable": False}

            plateau_multi[lig][col] = jeton
            dessiner_jeton_plateau_multi(jeton, centre_x, centre_y)

def plateau_est_vide_multi():
    """Vérifie si le plateau est vide"""
    for ligne in plateau_multi:
        for jeton in ligne:
            if jeton is not None:
                if jeton["type"] != "scelle":
                    return False
    return True

def contient_triplette_multi(ratelier):
    """Vérifie si le râtelier contient 3 jetons de la même couleur"""
    couleurs = [jeton["couleur"] for jeton in ratelier]
    for couleur in set(couleurs):
        if couleurs.count(couleur) >= 3:
            return True
    return False

def afficher_tour_actuel_multi():
    """Affiche quel joueur doit jouer"""
    if tour_joueur_1_multi:
        fltk.rectangle(LARG_MULTI - 235, 270, LARG_MULTI - 5, 310, remplissage="white", couleur="black")
        fltk.texte(LARG_MULTI - 125, 290, "Tour du Joueur 1", couleur="red", ancrage="center", taille=20)
    else:
        fltk.rectangle(LARG_MULTI - 235, 270, LARG_MULTI - 5, 310, remplissage="white", couleur="black")
        fltk.texte(LARG_MULTI - 125, 290, "Tour du Joueur 2", couleur="blue", ancrage="center", taille=20)
    fltk.mise_a_jour()

# --------------------------------------------------------------------
# INTERACTIONS
# --------------------------------------------------------------------

def cellule_depuis_clic_multi(x, y):
    """Retourne la cellule cliquée ou None"""
    if x < X_OFFSET_MULTI or y < Y_OFFSET_MULTI:
        return None

    col = (x - X_OFFSET_MULTI) // TAILLE_CEL_MULTI
    lig = (y - Y_OFFSET_MULTI) // TAILLE_CEL_MULTI

    if 0 <= col < NB_COLS_MULTI and 0 <= lig < NB_LIGS_MULTI:
        return col, lig

    return None

def gerer_clic_souris_multi(x, y):
    """Gère les clics en mode multijoueur"""
    global score_j1_multi, score_j2_multi, partie_terminee_multi, premier_clic_multi, tour_joueur_1_multi, jetons_ratelier_multi

    if partie_terminee_multi:
        return

    cellule = cellule_depuis_clic_multi(x, y)
    if cellule is None:
        return

    col, lig = cellule
    jeton_clique = plateau_multi[lig][col]

    if jeton_clique is None:
        return

    if jeton_clique["type"] == "simple" and jeton_clique["capturable"]:
        # ---- PREMIER CLIC ----
        if not premier_clic_multi:
            premier_clic_multi = True
            afficher_ratelier_multi()
            afficher_score_j1_multi()
            afficher_score_j2_multi()
            afficher_tour_actuel_multi()
            fltk.mise_a_jour()

        # ---- RETIRER DU PLATEAU ----
        plateau_multi[lig][col] = None
        x1, y1 = coord_case_multi(col, lig)
        fltk.rectangle(x1 +2, y1 +2, x1+ TAILLE_CEL_MULTI -1, y1+ TAILLE_CEL_MULTI -1, remplissage="light grey", couleur="light grey")

        # ---- RENDRE LES VOISINS SIMPLES ----
        voisins = [(lig - 1, col), (lig + 1, col), (lig, col - 1), (lig, col + 1)]
        for lv, cv in voisins:
            if 0 <= lv < NB_LIGS_MULTI and 0 <= cv < NB_COLS_MULTI:
                voisin = plateau_multi[lv][cv]
                if voisin is not None and type(voisin) is dict and voisin["type"] == "double":
                    voisin["type"] = "simple"
                    voisin["capturable"] = True
                    cx_v = X_OFFSET_MULTI + cv * TAILLE_CEL_MULTI + TAILLE_CEL_MULTI // 2
                    cy_v = Y_OFFSET_MULTI + lv * TAILLE_CEL_MULTI + TAILLE_CEL_MULTI // 2
                    dessiner_jeton_plateau_multi(voisin, cx_v, cy_v)
                    
        # ---- AJOUT AU RATELIER ----
        if len(jetons_ratelier_multi) < RATELIER_CASES_MULTI:
            jetons_ratelier_multi.append({"couleur": jeton_clique["couleur"], "joueur": 1 if tour_joueur_1_multi else 2})

            # ---- DÉTECTION TRIPLETTE ----
    couleur_cible = jeton_clique["couleur"]
    compteur = 0
    for j in jetons_ratelier_multi:
        if j["couleur"] == couleur_cible:
            compteur += 1
            
    # ---- SUPPRESSION TRIPLETTE + SCORE ----
    if compteur >= 3:
            
        ratelier_etait_plein = len(jetons_ratelier_multi) == RATELIER_CASES_MULTI
            
        nouveau_ratelier = []
        supprimes = 0
        for jeton in jetons_ratelier_multi:
            if jeton["couleur"] == couleur_cible and supprimes < 3:
                supprimes += 1
            else:
                nouveau_ratelier.append(jeton)

        jetons_ratelier_multi[:] = nouveau_ratelier
            
        if ratelier_etait_plein:
            if tour_joueur_1_multi:
                score_j1_multi += 2
            else:
                score_j2_multi += 2
        else:
            if tour_joueur_1_multi:
                score_j1_multi += 1
            else:
                score_j2_multi += 1
                    
        afficher_score_j1_multi()
        afficher_score_j2_multi()
                        
    # ---- RAFRAÎCHISSEMENT RATELIER ----
    fltk.rectangle(
        RATELIER_X_MULTI, RATELIER_Y1_MULTI,
        RATELIER_X_MULTI + TAILLE_CEL_MULTI,
        RATELIER_Y1_MULTI + RATELIER_CASES_MULTI * TAILLE_CEL_MULTI,
        remplissage="light grey", couleur="black")

    afficher_ratelier_multi()

    for index, jeton in enumerate(jetons_ratelier_multi):
        dessiner_jeton_ratelier_multi(jeton, index)


    # ---- FIN DE PARTIE ----
    if plateau_est_vide_multi():
        partie_terminee_multi = True

    if len(jetons_ratelier_multi) >= RATELIER_CASES_MULTI:
        if not contient_triplette_multi(jetons_ratelier_multi):
            partie_terminee_multi = True
    
    if len(jetons_ratelier_multi) >= RATELIER_CASES_MULTI:
        if not contient_triplette_multi(jetons_ratelier_multi):
            # le joueur perd donc score remis à 0
            if tour_joueur_1_multi:
                score_j1_multi = 0
            else:
                score_j2_multi = 0

            afficher_score_j1_multi()
            afficher_score_j2_multi()
            fltk.attente(1)
            partie_terminee_multi = True        

    # ---- CHANGEMENT DE JOUEUR ----
    tour_joueur_1_multi = not tour_joueur_1_multi
    afficher_tour_actuel_multi()

    if partie_terminee_multi:
        fltk.rectangle(LARG_MULTI - 235, 270, LARG_MULTI - 5, 310, remplissage="white", couleur="black")
        fltk.texte(LARG_MULTI - 125, 290, "Partie terminée !", couleur="red", ancrage="center", taille=20)

    fltk.mise_a_jour()
    sauvegarder_partie_multi()
    

def afficher_resultat_multi():
    """Affiche l'écran de fin avec les scores des deux joueurs"""
    fltk.efface_tout()
    fltk.rectangle(0, 0, LARG_MULTI, HAUT_MULTI, remplissage="black")

    fltk.texte(LARG_MULTI // 2, HAUT_MULTI // 2 - 150, "Fin de la partie !", taille=40, ancrage="center", couleur="white")

    fltk.texte(LARG_MULTI // 2, HAUT_MULTI // 2 - 50, f"Score J1 : {score_j1_multi}", taille=30, ancrage="center", couleur="light blue")

    fltk.texte(LARG_MULTI // 2, HAUT_MULTI // 2 + 50, f"Score J2 : {score_j2_multi}", taille=30, ancrage="center", couleur="light green")

    if score_j1_multi > score_j2_multi:
        fltk.texte(LARG_MULTI // 2, HAUT_MULTI // 2 + 150, "Joueur 1 gagne ! 🎉", taille=30, ancrage="center", couleur="yellow")
    elif score_j2_multi > score_j1_multi:
        fltk.texte(LARG_MULTI // 2, HAUT_MULTI // 2 + 150, "Joueur 2 gagne ! 🎉", taille=30, ancrage="center", couleur="yellow")
    else:
        fltk.texte(LARG_MULTI // 2, HAUT_MULTI // 2 + 150, "Égalité ! 🤝", taille=30, ancrage="center", couleur="yellow")

    fltk.texte(LARG_MULTI // 2, HAUT_MULTI - 50, "(Cliquez sur la croix pour fermer)", taille=18, ancrage="center", couleur="grey")

    fltk.mise_a_jour()

def afficher_ecran_fin_multi():
    """Affiche l'écran noir de fin"""
    fltk.efface_tout()
    fltk.rectangle(0, 0,
                   LARG_MULTI, HAUT_MULTI,
                   remplissage="black")

    fltk.texte(LARG_MULTI// 2, HAUT_MULTI// 2 - 100,
               "Merci d'avoir joué !",
               taille=40, ancrage="center", couleur="white")

    fltk.texte(LARG_MULTI // 2, HAUT_MULTI // 2 + 20,
               "À bientôt sur PICK TOK 🕹",
               taille=25, ancrage="center", couleur="red")

    fltk.texte(LARG_MULTI // 2, HAUT_MULTI - 50,
               "(Cliquez sur la croix pour fermer)",
               taille=18, ancrage="center", couleur="grey")

    fltk.mise_a_jour()

def lancer_mode_multi():
    """Lance le mode multijoueur"""
    global plateau_multi, jetons_ratelier_multi, score_j1_multi, score_j2_multi, partie_terminee_multi, ecran_fin_affiche_multi, premier_clic_multi, tour_joueur_1_multi
    plateau_multi = [[None for _ in range(NB_COLS_MULTI)] for _ in range(NB_LIGS_MULTI)]
    jetons_ratelier_multi = []
    score_j1_multi = 0
    score_j2_multi = 0
    partie_terminee_multi = False
    ecran_fin_affiche_multi = False
    premier_clic_multi = False
    tour_joueur_1_multi = True

    fltk.cree_fenetre(LARG_MULTI, HAUT_MULTI)
    fltk.rectangle(0, 0, LARG_MULTI, HAUT_MULTI, remplissage=random.choice(COULEURS_FOND_MULTI))
    afficher_grille_multi()
    afficher_zone_score_j1_multi()
    afficher_zone_score_j2_multi()
    afficher_ratelier_multi()
    initialiser_plateau_multi()
    generer_cases_noires_multi()
    afficher_tour_actuel_multi()
    fltk.mise_a_jour()

    while True:
        ev = fltk.attend_ev()

        if ev:
            if fltk.type_ev(ev) == "Quitte":
                fltk.ferme_fenetre()
                exit()

        if fltk.type_ev(ev) == "ClicGauche" and not partie_terminee_multi:
            gerer_clic_souris_multi(fltk.abscisse(ev), fltk.ordonnee(ev))

        if partie_terminee_multi and not ecran_fin_affiche_multi:
            fltk.attente(3)
            afficher_resultat_multi()
            fltk.attente(3.5)
            afficher_ecran_fin_multi()
            ecran_fin_affiche_multi = True

        fltk.mise_a_jour()

# --------------------------------------------------------------------
# PROGRAMME PRINCIPAL
# --------------------------------------------------------------------
try:
    charger_partie_solo()
except:
    pass

try:
    charger_partie_multi()
except:
    pass

mode = afficher_page_accueil()
if mode == "solo":
    lancer_mode_solo()
elif mode == "multi":
    lancer_mode_multi()

