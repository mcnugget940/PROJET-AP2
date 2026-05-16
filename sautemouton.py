import math
import fltk

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

LARGEUR = 20        # largeur du personnage en pixels
HAUTEUR = 20        # hauteur du personnage en pixels

VMAX = 15.0         # vitesse maximale que le joueur peut donner au personnage
GRAVITE = (0, 0.5)  # vecteur gravité — vers le bas donc y > 0
PAS = 0.5           # pas de simulation (plus petit = plus précis mais plus lent)

LARGEUR_FENETRE = 340
HAUTEUR_FENETRE = 400

MAX_PAS_SIMULATION = 2000   # seuil de détection de boucle infinie

# Constantes du solveur
A_APPROX = 10  # finesse d'approximation des positions  : (x,y) → (x//a, y//a)
B_APPROX = 5   # finesse d'approximation des vitesses   : pas du quadrillage vx/vy
PROFONDEUR_MAX_SOLVEUR = 8  # profondeur maximale de la recherche (nb de sauts)
#
# Choix de a et b :
#   a=10 → ~34×40 = 1 360 cellules distinctes sur la fenêtre 340×400.
#           Deux positions distantes de moins de 10 px sont traitées comme identiques.
#   b=5  → quadrillage {-15,-10,-5,0,5,10,15}² filtré → 28 vitesses par position.
#   Ces valeurs offrent un bon compromis vitesse / qualité sur les niveaux simples.
#   Diminuer a ou b améliore la précision mais ralentit la recherche.

# Constantes d'affichage
ECHELLE_FLECHE = 5   # facteur d'échelle visuel de la flèche

COULEURS_BLOCS = {
    "herbe":      "#3a7d44",
    "glace":      "#a8d8ea",
    "boue":       "#8b5e3c",
    "caoutchouc": "#ff8c00",
    "ballon":     "#ff69b4",
    "colle":      "#ffd700",
}


# ---------------------------------------------------------------------------
# Tâche 1 — Représentation de l'état du jeu
# ---------------------------------------------------------------------------

def charger_niveau(nom_fichier):
    """
    Lit un fichier de niveau et renvoie le personnage, l'objectif et la liste
    des blocs.

    Format du fichier :
      - ligne 1 : x,y du personnage
      - ligne 2 : x1,y1,x2,y2 de l'objectif
      - lignes suivantes : x1,y1,x2,y2[,type] pour chaque bloc
        Le type est optionnel ; la valeur par défaut est 'herbe'.
    """
    with open(nom_fichier, 'r') as f:
        lignes = f.readlines()

    coords = lignes[0].strip().split(',')
    personnage = {
        "position": (int(coords[0]), int(coords[1])),
        "vitesse": (0, 0)
    }

    coords = lignes[1].strip().split(',')
    objectif = (
        (int(coords[0]), int(coords[1])),
        (int(coords[2]), int(coords[3]))
    )

    lst_blocs = []
    for ligne in lignes[2:]:
        ligne = ligne.strip()
        if ligne:
            parts = ligne.split(',')
            coins = (
                (int(parts[0]), int(parts[1])),
                (int(parts[2]), int(parts[3]))
            )
            if len(parts) == 5:
                lst_blocs.append((coins[0], coins[1], parts[4]))
            else:
                lst_blocs.append((coins[0], coins[1]))

    return personnage, objectif, lst_blocs


def get_type_bloc(bloc):
    """Renvoie le type de surface d'un bloc ('herbe' par défaut)."""
    return bloc[2] if len(bloc) > 2 else "herbe"


def clic_vers_vitesse(personnage, clic):
    """
    Calcule la vitesse à donner au personnage en fonction d'un clic.

    Le vecteur vitesse est le vecteur entre la position du personnage et le
    clic. Si sa norme dépasse VMAX, il est ramené à VMAX en conservant la
    direction.
    """
    px, py = personnage["position"]
    cx, cy = clic

    vx = cx - px
    vy = cy - py

    norme = math.sqrt(vx ** 2 + vy ** 2)

    if norme == 0:
        personnage["vitesse"] = (0, 0)
        return

    if norme > VMAX:
        vx = vx / norme * VMAX
        vy = vy / norme * VMAX

    personnage["vitesse"] = (vx, vy)


def collision(personnage, lst_blocs):
    """
    Renvoie le premier bloc avec lequel le personnage est en collision
    (partiellement à l'intérieur), ou None si aucune collision.
    """
    px, py = personnage["position"]
    px2 = px + LARGEUR
    py2 = py + HAUTEUR

    for bloc in lst_blocs:
        bx1, by1 = bloc[0]
        bx2, by2 = bloc[1]
        if px < bx2 and px2 > bx1 and py < by2 and py2 > by1:
            return bloc

    return None


def victoire(personnage, objectif):
    """Renvoie True si le personnage chevauche la zone de l'objectif."""
    px, py = personnage["position"]
    px2 = px + LARGEUR
    py2 = py + HAUTEUR

    (ox1, oy1), (ox2, oy2) = objectif

    return px < ox2 and px2 > ox1 and py < oy2 and py2 > oy1


# ---------------------------------------------------------------------------
# Tâche 2 — Moteur physique
# ---------------------------------------------------------------------------

def appliquer_choc(personnage, cote, type_surface):
    """
    Modifie la vitesse du personnage selon le type de surface et le côté touché.
    Renvoie True si la simulation doit s'arrêter.

    Types disponibles : herbe, glace, boue, caoutchouc, ballon, colle.
    """
    vx, vy = personnage["vitesse"]

    if type_surface == "glace":
        if cote in ('dessus', 'dessous'):
            personnage["vitesse"] = (vx, 0)
        else:
            personnage["vitesse"] = (0, vy)
        vx2, vy2 = personnage["vitesse"]
        return abs(vx2) < 0.01 and abs(vy2) < 0.01

    elif type_surface == "boue":
        FRICTION = 0.85
        if cote in ('dessus', 'dessous'):
            personnage["vitesse"] = (vx * FRICTION, 0)
        else:
            personnage["vitesse"] = (0, vy * FRICTION)
        vx2, vy2 = personnage["vitesse"]
        return abs(vx2) < 0.1 and abs(vy2) < 0.1

    elif type_surface == "caoutchouc":
        if cote in ('dessus', 'dessous'):
            personnage["vitesse"] = (vx, -vy)
        else:
            personnage["vitesse"] = (-vx, vy)
        return False

    elif type_surface == "ballon":
        FACTEUR = 0.7
        if cote in ('dessus', 'dessous'):
            personnage["vitesse"] = (vx, -vy * FACTEUR)
        else:
            personnage["vitesse"] = (-vx * FACTEUR, vy)
        vx2, vy2 = personnage["vitesse"]
        return abs(vx2) < 0.1 and abs(vy2) < 0.1

    elif type_surface == "colle":
        personnage["vitesse"] = (0, 0)
        return True

    else:
        # herbe ou type inconnu : choc mou
        personnage["vitesse"] = (0, 0)
        return cote == 'dessus'


def choc(personnage, lst_blocs):
    """
    Détecte et résout la collision entre le personnage et les blocs.

    Algorithme :
      1. Vérifie s'il y a collision.
      2. Détermine le côté touché : recouvrement minimal parmi les côtés
         cohérents avec le signe de la vitesse.
      3. Replace le personnage contre ce bord et applique l'effet de surface.

    Renvoie True si la simulation doit s'arrêter.
    """
    bloc = collision(personnage, lst_blocs)
    if bloc is None:
        return False

    bx1, by1 = bloc[0]
    bx2, by2 = bloc[1]
    px, py = personnage["position"]
    vx, vy = personnage["vitesse"]

    # Candidats : côtés cohérents avec la direction de déplacement
    candidats = []
    if vy > 0 and (py + HAUTEUR) > by1:
        candidats.append(('dessus', (py + HAUTEUR) - by1))
    if vy < 0 and by2 > py:
        candidats.append(('dessous', by2 - py))
    if vx > 0 and (px + LARGEUR) > bx1:
        candidats.append(('gauche', (px + LARGEUR) - bx1))
    if vx < 0 and bx2 > px:
        candidats.append(('droite', bx2 - px))

    # Repli si vitesse nulle ou apex de trajectoire
    if not candidats:
        tous = [
            ('dessus',  (py + HAUTEUR) - by1),
            ('dessous', by2 - py),
            ('gauche',  (px + LARGEUR) - bx1),
            ('droite',  bx2 - px),
        ]
        candidats = [(c, o) for c, o in tous if o > 0]

    if not candidats:
        return False

    cote, _ = min(candidats, key=lambda x: x[1])

    if cote == 'dessus':
        personnage["position"] = (px, by1 - HAUTEUR)
    elif cote == 'dessous':
        personnage["position"] = (px, by2)
    elif cote == 'gauche':
        personnage["position"] = (bx1 - LARGEUR, py)
    else:
        personnage["position"] = (bx2, py)

    return appliquer_choc(personnage, cote, get_type_bloc(bloc))


def pas(personnage, lst_blocs):
    """
    Réalise un pas élémentaire : déplacement, gravité, puis collision.
    Renvoie True si le personnage est au repos.
    """
    px, py = personnage["position"]
    vx, vy = personnage["vitesse"]

    personnage["position"] = (px + vx * PAS, py + vy * PAS)
    personnage["vitesse"] = (vx + GRAVITE[0] * PAS, vy + GRAVITE[1] * PAS)

    return choc(personnage, lst_blocs)


def simuler(personnage, lst_blocs):
    """
    Répète les pas jusqu'à l'arrêt ou jusqu'à la détection d'une boucle infinie.
    Renvoie True si terminé normalement, False sinon.
    """
    for _ in range(MAX_PAS_SIMULATION):
        if pas(personnage, lst_blocs):
            return True
    return False


# ---------------------------------------------------------------------------
# Tâche 3 — Affichage graphique et interface utilisateur
# ---------------------------------------------------------------------------

def dessiner_bloc(bloc):
    """Dessine un bloc rempli avec sa couleur de surface, encadré en noir."""
    x1, y1 = bloc[0]
    x2, y2 = bloc[1]
    couleur = COULEURS_BLOCS.get(get_type_bloc(bloc), "#3a7d44")
    fltk.rectangle(x1, y1, x2, y2, couleur=couleur, remplissage=couleur)
    fltk.rectangle(x1, y1, x2, y2, couleur='black', epaisseur=1)


def dessiner_objectif(objectif):
    """Dessine l'objectif : rectangle rouge avec une croix intérieure."""
    (x1, y1), (x2, y2) = objectif
    fltk.rectangle(x1, y1, x2, y2, couleur='red', remplissage='#ffcccc')
    fltk.ligne(x1, y1, x2, y2, couleur='red', epaisseur=2)
    fltk.ligne(x1, y2, x2, y1, couleur='red', epaisseur=2)
    fltk.rectangle(x1, y1, x2, y2, couleur='red', epaisseur=2)


def dessiner_personnage(personnage):
    """Dessine le personnage sous forme d'un sprite mouton."""
    px, py = personnage["position"]
    cx = px + LARGEUR // 2
    cy = py + HAUTEUR // 2
    fltk.image(cx, cy, "mouton.png", largeur=LARGEUR, hauteur=HAUTEUR)


def dessiner_fleche(personnage, souris):
    """
    Dessine la flèche rouge indiquant la direction et l'intensité du saut.
    La longueur visuelle est proportionnelle à la vitesse (plafonnée à VMAX).
    """
    if souris is None:
        return

    px, py = personnage["position"]
    # Point de départ : centre du personnage
    cx = px + LARGEUR // 2
    cy = py + HAUTEUR // 2

    # Vecteur vitesse (plafonné à VMAX)
    dx = souris[0] - px
    dy = souris[1] - py
    norme = math.sqrt(dx ** 2 + dy ** 2)
    if norme == 0:
        return
    if norme > VMAX:
        dx = dx / norme * VMAX
        dy = dy / norme * VMAX

    # Pointe de la flèche (mise à l'échelle pour la lisibilité)
    tx = cx + dx * ECHELLE_FLECHE
    ty = cy + dy * ECHELLE_FLECHE

    fltk.ligne(cx, cy, tx, ty, couleur='red', epaisseur=2)

    # Tête de flèche (deux ailerons)
    norme_v = math.sqrt(dx ** 2 + dy ** 2)
    if norme_v < 1:
        return
    ux = dx / norme_v
    uy = dy / norme_v
    taille = 8
    angle = math.pi / 5  # 36°

    ax1 = tx - taille * (ux * math.cos(angle) - uy * math.sin(angle))
    ay1 = ty - taille * (uy * math.cos(angle) + ux * math.sin(angle))
    ax2 = tx - taille * (ux * math.cos(angle) + uy * math.sin(angle))
    ay2 = ty - taille * (uy * math.cos(angle) - ux * math.sin(angle))

    fltk.ligne(tx, ty, ax1, ay1, couleur='red', epaisseur=2)
    fltk.ligne(tx, ty, ax2, ay2, couleur='red', epaisseur=2)


def dessiner_trajectoire(trajectoire):
    """Dessine la trace du dernier saut sous forme de petits cercles bleus."""
    for pos in trajectoire:
        cx = pos[0] + LARGEUR // 2
        cy = pos[1] + HAUTEUR // 2
        fltk.cercle(cx, cy, 2, couleur='#1565c0', remplissage='#90caf9')


def dessiner_jeu(personnage, lst_blocs, objectif, souris, nb_sauts, trajectoire=None):
    """Redessine l'intégralité de la scène de jeu."""
    fltk.efface_tout()

    # Fond : image de décor
    fltk.image(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2, "background.png",
               largeur=LARGEUR_FENETRE, hauteur=HAUTEUR_FENETRE)

    for bloc in lst_blocs:
        dessiner_bloc(bloc)

    dessiner_objectif(objectif)

    # Trace de la trajectoire (par-dessus les blocs, sous le personnage)
    if trajectoire:
        dessiner_trajectoire(trajectoire)

    dessiner_personnage(personnage)
    dessiner_fleche(personnage, souris)

    # Compteur de sauts
    fltk.texte(5, 5, f"Sauts : {nb_sauts}", couleur='#1a1a1a', taille=14)

    # Aide en bas
    aide = "G : viser   D : sauter   Ret.arr. : annuler   S : solveur   Echap : menu"
    fltk.texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE - 18,
               aide, couleur='#555555', ancrage='center', taille=9)

    fltk.mise_a_jour()


def simuler_et_afficher(personnage, lst_blocs, objectif, nb_sauts):
    """
    Simule le saut en animant le personnage à l'écran.
    Renvoie (True, trajectoire) si terminé normalement,
            (False, [])        si une boucle infinie est détectée.
    """
    pos_sauv = personnage["position"]
    vit_sauv = personnage["vitesse"]
    trajectoire = [personnage["position"]]

    for i in range(MAX_PAS_SIMULATION):
        arret = pas(personnage, lst_blocs)
        trajectoire.append(personnage["position"])

        # Mettre à jour l'affichage tous les 2 pas avec la trace en cours
        if i % 2 == 0:
            dessiner_jeu(personnage, lst_blocs, objectif, None, nb_sauts, trajectoire)

        if arret:
            dessiner_jeu(personnage, lst_blocs, objectif, None, nb_sauts, trajectoire)
            return True, trajectoire

    # Boucle infinie : restaurer l'état avant le saut
    personnage["position"] = pos_sauv
    personnage["vitesse"] = vit_sauv
    return False, []


def afficher_message_popup(titre, corps, couleur_titre='red'):
    """Affiche un message centré par-dessus la scène et attend un clic."""
    cx = LARGEUR_FENETRE // 2
    cy = HAUTEUR_FENETRE // 2

    fltk.rectangle(cx - 135, cy - 50, cx + 135, cy + 55,
                   couleur='white', remplissage='white')
    fltk.rectangle(cx - 135, cy - 50, cx + 135, cy + 55,
                   couleur=couleur_titre, epaisseur=3)
    fltk.texte(cx, cy - 25, titre,
               couleur=couleur_titre, ancrage='center', taille=20, police="Helvetica bold")
    fltk.texte(cx, cy + 5, corps,
               couleur='#333333', ancrage='center', taille=12)
    fltk.texte(cx, cy + 30, "— Cliquez pour continuer —",
               couleur='#888888', ancrage='center', taille=10)
    fltk.mise_a_jour()

    while True:
        ev = fltk.attend_ev()
        te = fltk.type_ev(ev)
        if te in ('ClicGauche', 'ClicDroit', 'Touche'):
            return
        if te == 'Quitte':
            return


def lister_niveaux():
    """Renvoie la liste des fichiers de niveau disponibles."""
    return ["niveau1.txt", "niveau2.txt"]


def menu():
    """
    Affiche le menu principal et renvoie le nom du niveau choisi.
    Renvoie None si le joueur ferme la fenêtre.
    """
    niveaux = lister_niveaux()

    while True:
        fltk.efface_tout()

        # Fond dégradé simulé par deux rectangles
        fltk.rectangle(0, 0, LARGEUR_FENETRE, HAUTEUR_FENETRE,
                       couleur='#c8e6c9', remplissage='#c8e6c9')
        fltk.rectangle(0, HAUTEUR_FENETRE // 2, LARGEUR_FENETRE, HAUTEUR_FENETRE,
                       couleur='#a5d6a7', remplissage='#a5d6a7')

        # Titre
        fltk.texte(LARGEUR_FENETRE // 2, 30, "SAUTE MOUTON",
                   couleur='#1b5e20', ancrage='center', taille=28, police="Helvetica bold")
        fltk.texte(LARGEUR_FENETRE // 2, 70, "Choisissez un niveau",
                   couleur='#2e7d32', ancrage='center', taille=14)

        # Boutons de niveaux
        zones_cliquables = []
        if niveaux:
            for i, nom in enumerate(niveaux):
                y_btn = 110 + i * 55
                x1 = LARGEUR_FENETRE // 2 - 110
                x2 = LARGEUR_FENETRE // 2 + 110
                # Ombre
                fltk.rectangle(x1 + 3, y_btn + 3, x2 + 3, y_btn + 40,
                               couleur='#1b5e20', remplissage='#1b5e20')
                # Bouton
                fltk.rectangle(x1, y_btn, x2, y_btn + 40,
                               couleur='#2e7d32', remplissage='#43a047')
                fltk.texte(LARGEUR_FENETRE // 2, y_btn + 20, nom,
                           couleur='white', ancrage='center', taille=14)
                zones_cliquables.append((x1, y_btn, x2, y_btn + 40, nom))
        else:
            fltk.texte(LARGEUR_FENETRE // 2, 160,
                       "Aucun fichier niveau*.txt trouvé.",
                       couleur='red', ancrage='center', taille=13)

        fltk.texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE - 25,
                   "Cliquez sur un niveau pour commencer",
                   couleur='#555555', ancrage='center', taille=10)

        fltk.mise_a_jour()

        ev = fltk.attend_ev()
        te = fltk.type_ev(ev)

        if te == 'Quitte':
            return None

        if te == 'ClicGauche':
            mx = fltk.abscisse(ev)
            my = fltk.ordonnee(ev)
            for x1, y1, x2, y2, nom in zones_cliquables:
                if x1 <= mx <= x2 and y1 <= my <= y2:
                    return nom


def boucle_jeu(nom_fichier):
    """
    Boucle principale d'une partie.
    Renvoie 'menu' pour revenir au menu, ou 'quitter' pour fermer le jeu.
    """
    personnage, objectif, lst_blocs = charger_niveau(nom_fichier)
    souris = None
    nb_sauts = 0
    historique = []      # pile des positions avant chaque saut (retour en arrière)
    trajectoire = []     # trace du dernier saut

    dessiner_jeu(personnage, lst_blocs, objectif, souris, nb_sauts, trajectoire)

    while True:
        ev = fltk.attend_ev()
        te = fltk.type_ev(ev)

        if te == 'Quitte':
            return 'quitter'

        elif te == 'Touche':
            if fltk.touche(ev) == 'Escape':
                return 'menu'

            elif fltk.touche(ev).lower() == 's':
                lancer_solveur(personnage, lst_blocs, objectif, nb_sauts)
                trajectoire = []
                dessiner_jeu(personnage, lst_blocs, objectif, None, nb_sauts, trajectoire)

            elif fltk.touche(ev) == 'BackSpace':
                if historique:
                    personnage["position"] = historique.pop()
                    personnage["vitesse"] = (0, 0)
                    nb_sauts -= 1
                    souris = None
                    trajectoire = []
                    dessiner_jeu(personnage, lst_blocs, objectif, None, nb_sauts, trajectoire)

        elif te == 'ClicGauche':
            # Mise à jour de la visée au clic
            souris = (fltk.abscisse(ev), fltk.ordonnee(ev))
            clic_vers_vitesse(personnage, souris)
            dessiner_jeu(personnage, lst_blocs, objectif, souris, nb_sauts, trajectoire)

        elif te == 'ClicDroit':
            vx, vy = personnage["vitesse"]
            if vx == 0.0 and vy == 0.0:
                continue  # aucune direction choisie, on ignore

            # Sauvegarder la position dans l'historique avant le saut
            historique.append(personnage["position"])
            nb_sauts += 1

            ok, trajectoire = simuler_et_afficher(personnage, lst_blocs, objectif, nb_sauts)

            if not ok:
                # Boucle infinie détectée : annuler le coup et restaurer
                personnage["position"] = historique.pop()
                personnage["vitesse"] = (0, 0)
                nb_sauts -= 1
                trajectoire = []
                dessiner_jeu(personnage, lst_blocs, objectif, None, nb_sauts, trajectoire)
                afficher_message_popup(
                    "Coup invalide !",
                    "Ce saut provoque une boucle infinie.\nLe coup a été annulé."
                )
                dessiner_jeu(personnage, lst_blocs, objectif, None, nb_sauts, trajectoire)
                souris = None
                continue

            souris = None

            # Vérifier la victoire
            if victoire(personnage, objectif):
                dessiner_jeu(personnage, lst_blocs, objectif, None, nb_sauts, trajectoire)
                afficher_message_popup(
                    "Victoire !",
                    f"Niveau terminé en {nb_sauts} saut(s) !",
                    couleur_titre='#2e7d32'
                )
                return 'menu'

            dessiner_jeu(personnage, lst_blocs, objectif, None, nb_sauts, trajectoire)


# ---------------------------------------------------------------------------
# Tâche 4 — Recherche automatique de solution (solveur DFS)
# ---------------------------------------------------------------------------

def generer_vitesses():
    """
    Renvoie la liste discrète des vitesses à essayer pour le solveur.

    On balaye un quadrillage (vx, vy) avec un pas B_APPROX en gardant
    uniquement les vecteurs de norme dans ]0, VMAX].
    Réduire B_APPROX augmente le nombre de vitesses testées (plus précis,
    plus lent) ; l'augmenter réduit le temps de recherche.
    """
    vitesses = []
    for vx in range(-int(VMAX), int(VMAX) + 1, B_APPROX):
        for vy in range(-int(VMAX), int(VMAX) + 1, B_APPROX):
            if 0 < math.sqrt(vx ** 2 + vy ** 2) <= VMAX:
                vitesses.append((float(vx), float(vy)))
    return vitesses


def position_discrete(pos):
    """
    Encode une position flottante en cellule discrète via division entière.

    Deux positions (x1,y1) et (x2,y2) sont considérées identiques si
    x1//A_APPROX == x2//A_APPROX  et  y1//A_APPROX == y2//A_APPROX,
    c'est-à-dire si elles tombent dans la même case d'un quadrillage A_APPROX×A_APPROX.
    Augmenter A_APPROX réduit le nombre de cellules → recherche plus rapide
    mais moins précise ; diminuer A_APPROX donne plus de précision.
    """
    px, py = pos
    return (int(px) // A_APPROX, int(py) // A_APPROX)


def solveur_dfs(personnage, lst_blocs, objectif, visite, chemin,
                positions_explorees, profondeur_max, ctx_visu=None):
    """
    Algorithme de recherche en profondeur (backtracking).

    Paramètres :
      personnage        — état courant du personnage (modifié en place)
      visite            — ensemble des positions déjà visitées (set)
      chemin            — liste des positions du parcours en cours
      positions_explorees — toutes les positions visitées (pour la visu)
      profondeur_max    — limite de profondeur restante
      ctx_visu          — dict optionnel pour la visualisation en cours de recherche

    Renvoie True si l'objectif est atteint, False sinon.
    Lorsque True est renvoyé, chemin contient la solution complète.
    """
    if victoire(personnage, objectif):
        return True

    if profondeur_max == 0:
        return False

    p = position_discrete(personnage["position"])
    if p in visite:
        return False
    visite.add(p)
    positions_explorees.append(personnage["position"])

    # Visualisation périodique : toutes les 40 positions explorées
    if ctx_visu and len(positions_explorees) % 40 == 0:
        dessiner_jeu(ctx_visu["perso_ref"], ctx_visu["lst_blocs"],
                     ctx_visu["objectif"], None, ctx_visu["nb_sauts"])
        for pos in positions_explorees:
            fltk.cercle(pos[0] + LARGEUR // 2, pos[1] + HAUTEUR // 2, 3,
                        couleur='#29b6f6', remplissage='#b3e5fc')
        fltk.texte(LARGEUR_FENETRE // 2, 5,
                   f"Exploration… {len(positions_explorees)} positions",
                   couleur='#0d47a1', ancrage='center', taille=11)
        fltk.mise_a_jour()

    pos_actuelle = personnage["position"]

    for vx, vy in generer_vitesses():
        personnage["position"] = pos_actuelle
        personnage["vitesse"] = (vx, vy)

        ok = simuler(personnage, lst_blocs)
        if not ok:
            personnage["position"] = pos_actuelle
            personnage["vitesse"] = (0, 0)
            continue

        chemin.append(personnage["position"])

        if solveur_dfs(personnage, lst_blocs, objectif, visite, chemin,
                       positions_explorees, profondeur_max - 1, ctx_visu):
            return True

        chemin.pop()
        personnage["position"] = pos_actuelle
        personnage["vitesse"] = (0, 0)

    return False


def lancer_solveur(personnage_initial, lst_blocs, objectif, nb_sauts):
    """
    Lance la recherche DFS depuis la position actuelle du personnage et
    visualise les résultats sur l'interface graphique.

    - Affiche les positions explorées en bleu clair.
    - Affiche le chemin gagnant en vert s'il est trouvé.
    - Attend un clic pour reprendre la partie.
    """
    perso_ref = {"position": personnage_initial["position"], "vitesse": (0, 0)}

    # Afficher le message de lancement
    dessiner_jeu(perso_ref, lst_blocs, objectif, None, nb_sauts)
    fltk.texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2,
               "Recherche en cours…",
               couleur='#0d47a1', ancrage='center', taille=16, police="Helvetica bold")
    fltk.mise_a_jour()

    # Préparer le solveur
    perso_solveur = {"position": personnage_initial["position"], "vitesse": (0, 0)}
    visite = set()
    chemin = [perso_solveur["position"]]
    positions_explorees = []

    ctx_visu = {
        "perso_ref": perso_ref,
        "lst_blocs": lst_blocs,
        "objectif": objectif,
        "nb_sauts": nb_sauts,
    }

    trouve = solveur_dfs(perso_solveur, lst_blocs, objectif, visite, chemin,
                         positions_explorees, PROFONDEUR_MAX_SOLVEUR, ctx_visu)

    # --- Affichage du résultat final ---
    dessiner_jeu(perso_ref, lst_blocs, objectif, None, nb_sauts)

    # Toutes les positions explorées (points bleus)
    for pos in positions_explorees:
        fltk.cercle(pos[0] + LARGEUR // 2, pos[1] + HAUTEUR // 2, 4,
                    couleur='#29b6f6', remplissage='#b3e5fc')

    if trouve:
        # Chemin gagnant : lignes vertes entre chaque étape
        for i in range(len(chemin) - 1):
            x1 = chemin[i][0] + LARGEUR // 2
            y1 = chemin[i][1] + HAUTEUR // 2
            x2 = chemin[i + 1][0] + LARGEUR // 2
            y2 = chemin[i + 1][1] + HAUTEUR // 2
            fltk.ligne(x1, y1, x2, y2, couleur='#00c853', epaisseur=3)

        # Points de passage (cercles verts)
        for pos in chemin:
            fltk.cercle(pos[0] + LARGEUR // 2, pos[1] + HAUTEUR // 2, 6,
                        couleur='#00c853', remplissage='#69f0ae')

        nb_coups = len(chemin) - 1
        msg = f"Solution : {nb_coups} saut(s) — {len(positions_explorees)} positions explorées"
        fltk.texte(LARGEUR_FENETRE // 2, 5, msg,
                   couleur='#1b5e20', ancrage='center', taille=11, police="Helvetica bold")
    else:
        msg = f"Aucune solution trouvée — {len(positions_explorees)} positions explorées"
        fltk.texte(LARGEUR_FENETRE // 2, 5, msg,
                   couleur='red', ancrage='center', taille=11, police="Helvetica bold")

    fltk.texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE - 18,
               "Cliquez pour reprendre", couleur='#555555', ancrage='center', taille=10)
    fltk.mise_a_jour()

    # Attendre un clic ou une touche pour reprendre
    while True:
        ev = fltk.attend_ev()
        te = fltk.type_ev(ev)
        if te in ('ClicGauche', 'ClicDroit', 'Touche', 'Quitte'):
            return trouve


def main():
    """Point d'entrée du jeu."""
    fltk.cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

    etat = 'menu'
    while etat == 'menu':
        nom_fichier = menu()
        if nom_fichier is None:
            break
        etat = boucle_jeu(nom_fichier)

    fltk.ferme_fenetre()


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
