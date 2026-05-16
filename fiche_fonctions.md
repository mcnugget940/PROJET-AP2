 Fiche de révision — Saute Mouton

---

## Constantes globales

| Nom | Valeur | Rôle |
|-----|--------|------|
| `LARGEUR`, `HAUTEUR` | 20, 20 | Taille en pixels du personnage (hitbox) |
| `VMAX` | 15.0 | Vitesse max qu'un clic peut donner |
| `GRAVITE` | (0, 0.5) | Accélération vers le bas (y augmente vers le bas) |
| `PAS` | 0.5 | Durée d'un sous-pas de simulation |
| `LARGEUR_FENETRE`, `HAUTEUR_FENETRE` | 340, 400 | Dimensions de la fenêtre |
| `MAX_PAS_SIMULATION` | 2000 | Limite avant de déclarer une boucle infinie |
| `A_APPROX` | 10 | Taille d'une cellule pour comparer deux positions |
| `B_APPROX` | 5 | Pas du quadrillage de vitesses pour le solveur |
| `PROFONDEUR_MAX_SOLVEUR` | 8 | Nombre max de sauts testés par le solveur |
| `ECHELLE_FLECHE` | 5 | Facteur visuel pour rendre la flèche lisible |
| `COULEURS_BLOCS` | dict | Couleur de chaque type de surface |

---

## Tâche 1 — Représentation

### `charger_niveau(nom_fichier)`
**Ce qu'elle fait :** lit un fichier `.txt` ligne par ligne et construit les trois structures du jeu.

**Ligne 1** → position initiale du personnage → dict `{"position": (x,y), "vitesse": (0,0)}`  
**Ligne 2** → coin haut-gauche et bas-droit de la zone objectif → tuple `((x1,y1),(x2,y2))`  
**Lignes 3+** → chaque bloc = `((x1,y1),(x2,y2))` ou `((x1,y1),(x2,y2), "type")` si 5 valeurs

**Retourne :** `(personnage, objectif, lst_blocs)`

**Point clé :** si la 5e colonne est absente, le bloc n'a que 2 éléments et `get_type_bloc` lui donnera "herbe" par défaut.

---

### `get_type_bloc(bloc)`
**Ce qu'elle fait :** accède au type de surface d'un bloc.

**Point clé :** un bloc peut avoir 2 ou 3 éléments. `len(bloc) > 2` vérifie si le type est présent sinon renvoie `"herbe"`.

---

### `clic_vers_vitesse(personnage, clic)`
**Ce qu'elle fait :** transforme un clic souris en vecteur vitesse pour le personnage.

**Formule :** `vx = clic_x - perso_x`, `vy = clic_y - perso_y`  
**Plafonnement :** si la norme dépasse `VMAX`, on divise par la norme puis multiplie par `VMAX` (même direction, norme = VMAX).  
**Cas spécial :** si le clic est exactement sur le personnage, vitesse = (0,0).

---

### `collision(personnage, lst_blocs)`
**Ce qu'elle fait :** détecte si le personnage chevauche un bloc.

**Méthode AABB :** deux rectangles se chevauchent si et seulement si :
- `px < bx2` ET `px+LARGEUR > bx1` (axe horizontal)
- `py < by2` ET `py+HAUTEUR > by1` (axe vertical)

**Retourne :** le premier bloc en collision, ou `None`.

---

### `victoire(personnage, objectif)`
**Ce qu'elle fait :** vérifie si le personnage atteint la zone objectif.

**Même test AABB** que `collision` mais appliqué à l'objectif.  
**Retourne :** `True` ou `False`.

---

## Tâche 2 — Moteur physique

### `appliquer_choc(personnage, cote, type_surface)`
**Ce qu'elle fait :** modifie la vitesse selon le type de surface et le côté touché.

| Surface | Effet |
|---------|-------|
| herbe | vitesse → (0,0), arrêt si côté = dessus |
| glace | composante perpendiculaire annulée, l'autre conservée |
| boue | composante perpendiculaire annulée, l'autre × 0.85 |
| caoutchouc | composante perpendiculaire inversée (rebond élastique) |
| ballon | rebond amorti × 0.7 |
| colle | vitesse → (0,0), arrêt immédiat |

**Retourne :** `True` si la simulation doit s'arrêter, `False` sinon.

**Point clé :** "dessus" = le personnage tombe sur la face supérieure du bloc → on annule `vy`. "gauche" = le personnage frappe la face gauche du bloc → on annule `vx`.

---

### `choc(personnage, lst_blocs)`
**Ce qu'elle fait :** résout une collision : replace le personnage contre le bon bord et applique l'effet de surface.

**Algorithme :**
1. Appelle `collision()` — si aucune, retourne False.
2. Calcule le **recouvrement** sur chaque face (distance à repousser).
3. Garde seulement les faces **cohérentes avec la vitesse** (ex : si `vy > 0`, on ne considère que le dessus du bloc).
4. Choisit la face avec le **plus petit recouvrement** → c'est le côté frappé.
5. Replace le personnage exactement contre ce bord.
6. Appelle `appliquer_choc`.

**Cas de repli :** si vitesse nulle (sommet de trajectoire), on teste toutes les faces avec recouvrement positif.

---

### `pas(personnage, lst_blocs)`
**Ce qu'elle fait :** avance la simulation d'un sous-pas.

**Ordre :**
1. `position += vitesse × PAS` (déplacement)
2. `vitesse += GRAVITE × PAS` (accélération gravitationnelle)
3. `choc(...)` (collision éventuelle)

**Retourne :** `True` si le personnage est au repos.

---

### `simuler(personnage, lst_blocs)`
**Ce qu'elle fait :** répète `pas()` jusqu'à l'arrêt ou la limite `MAX_PAS_SIMULATION`.

**Retourne :** `True` si arrêt normal, `False` si boucle infinie détectée.

---

## Tâche 3 — Interface graphique

### `dessiner_bloc(bloc)`
Dessine un rectangle coloré selon le type de surface + contour noir.

### `dessiner_objectif(objectif)`
Dessine le carré rouge avec deux diagonales (croix) pour le repérer facilement.

### `dessiner_personnage(personnage)`
Affiche le sprite `mouton.png` centré sur la position du personnage.  
**Point clé :** `fltk.image` attend le **centre** de l'image, pas le coin haut-gauche.

### `dessiner_fleche(personnage, souris)`
**Ce qu'elle fait :** trace une flèche rouge de la direction du prochain saut.

**Calcul :**
- Vecteur `(dx, dy)` du personnage vers la souris, plafonné à VMAX.
- Pointe = centre personnage + vecteur × `ECHELLE_FLECHE`.
- Deux ailerons par rotation de ±36° autour de l'axe du vecteur.

### `dessiner_trajectoire(trajectoire)`
Dessine une série de petits cercles bleus à chaque position enregistrée lors du saut.

### `dessiner_jeu(personnage, lst_blocs, objectif, souris, nb_sauts, trajectoire=None)`
**Ce qu'elle fait :** efface l'écran et redessine tout dans l'ordre :
1. Image de fond
2. Blocs
3. Objectif
4. Trajectoire (si fournie)
5. Personnage
6. Flèche
7. HUD (compteur de sauts + aide en bas)

**Point clé :** l'ordre est important — ce qui est dessiné en dernier apparaît par-dessus.

---

### `simuler_et_afficher(personnage, lst_blocs, objectif, nb_sauts)`
**Ce qu'elle fait :** joue le saut en temps réel avec animation.

**Fonctionnement :**
- Sauvegarde position et vitesse initiales.
- À chaque pas, ajoute la position dans `trajectoire` et rafraîchit l'écran tous les 2 pas (animation progressive).
- Si arrêt normal → retourne `(True, trajectoire)`.
- Si boucle infinie → restaure l'état initial et retourne `(False, [])`.

---

### `afficher_message_popup(titre, corps, couleur_titre)`
Affiche un encadré centré par-dessus la scène et attend un clic ou une touche pour continuer.

---

### `lister_niveaux()`
Retourne la liste codée en dur des fichiers de niveau : `["niveau1.txt", "niveau2.txt"]`.

---

### `menu()`
**Ce qu'elle fait :** affiche les boutons de sélection de niveau et attend un clic.

**Fonctionnement :**
- Boucle infinie qui redessine le menu à chaque tour.
- Calcule les zones cliquables de chaque bouton.
- Sur `ClicGauche`, vérifie si le clic est dans une zone → retourne le nom du fichier.
- Sur `Quitte` → retourne `None`.

---

### `boucle_jeu(nom_fichier)`
**Ce qu'elle fait :** gère la partie complète sur un niveau.

**Variables importantes :**
- `historique` : pile (liste) des positions avant chaque saut → permet l'annulation.
- `trajectoire` : liste des positions du dernier saut → affichée en permanence.
- `souris` : position du dernier clic gauche → pour dessiner la flèche.
- `nb_sauts` : compteur affiché dans le HUD.

**Événements gérés :**

| Événement | Action |
|-----------|--------|
| `ClicGauche` | Met à jour la visée (flèche) |
| `ClicDroit` | Lance le saut, anime, vérifie la victoire |
| `BackSpace` | Annule le dernier saut (dépile `historique`) |
| `s` | Lance le solveur DFS |
| `Escape` | Retourne au menu |
| `Quitte` | Ferme le jeu |

---

## Tâche 4 — Solveur DFS

### `generer_vitesses()`
**Ce qu'elle fait :** construit la liste des vitesses à tester pour le solveur.

**Méthode :** quadrillage `{-15,-10,-5,0,5,10,15}²` avec pas `B_APPROX`, filtré pour ne garder que les vecteurs de norme dans `]0, VMAX]`.  
**Résultat :** 28 vitesses différentes.

---

### `position_discrete(pos)`
**Ce qu'elle fait :** convertit une position flottante en case discrète.

**Formule :** `(int(x) // A_APPROX, int(y) // A_APPROX)`

**Pourquoi :** deux positions très proches (< A_APPROX pixels d'écart) sont traitées comme identiques → évite de revisiter inutilement des positions quasi-identiques.

---

### `solveur_dfs(personnage, lst_blocs, objectif, visite, chemin, positions_explorees, profondeur_max, ctx_visu)`
**Ce qu'elle fait :** cherche un chemin vers l'objectif par backtracking récursif.

**Algorithme :**
1. Si victoire → retourne `True`.
2. Si profondeur = 0 → retourne `False`.
3. Si position déjà visitée → retourne `False`.
4. Marque la position comme visitée.
5. Pour chaque vitesse de `generer_vitesses()` :
   - Simule le saut.
   - Si la simulation se termine normalement (pas de boucle infinie) :
     - Ajoute la position finale dans `chemin`.
     - Appelle récursivement `solveur_dfs`.
     - Si trouvé → propage `True`.
     - Sinon → retire du chemin (**backtrack**) et restaure l'état.
6. Retourne `False` si aucune vitesse ne mène à l'objectif.

**Visualisation :** toutes les 40 positions explorées, l'écran est mis à jour avec des points bleus.

---

### `lancer_solveur(personnage_initial, lst_blocs, objectif, nb_sauts)`
**Ce qu'elle fait :** prépare et lance `solveur_dfs`, puis affiche le résultat.

**Affichage du résultat :**
- Points bleus = toutes les positions explorées.
- Lignes et points verts = chemin gagnant (s'il existe).
- Message en haut = nombre de sauts trouvés ou "aucune solution".

---

### `main()`
Point d'entrée : crée la fenêtre, boucle sur `menu()` → `boucle_jeu()` jusqu'à ce que le joueur ferme la fenêtre.
