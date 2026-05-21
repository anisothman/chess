board = [
    ["bR","bN","bB","bQ","bK","bB","bN","bR"],
    ["bP","bP","bP","bP","bP","bP","bP","bP"],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    ["wP","wP","wP","wP","wP","wP","wP","wP"],
    ["wR","wN","wB","wQ","wK","wB","wN","wR"],
]

def afficher_board(board):
    print("  a b c d e f g h")
    for i, ligne in enumerate(board):
        print(8 - i, end=" ")
        for case in ligne:
            print(case[1] if case != " " else ".", end=" ")
        print(8 - i)
    print("  a b c d e f g h")
def deplacer(board, depuis, vers):
    # Convertir "e2" -> (ligne, colonne)
    colonnes = "abcdefgh"
    
    col_depuis = colonnes.index(depuis[0])
    lig_depuis = 8 - int(depuis[1])
    
    col_vers = colonnes.index(vers[0])
    lig_vers = 8 - int(vers[1])
    
    # Déplacer la pièce
    piece = board[lig_depuis][col_depuis]
    board[lig_vers][col_vers] = piece
    board[lig_depuis][col_depuis] = " "

def mouvements_pion(board, lig, col):
    mouvements = []
    piece = board[lig][col]
    couleur = piece[0]

    if couleur == "w":
        direction = -1   # les blancs montent
        depart = 6       # ligne de départ des blancs
    else:
        direction = 1    # les noirs descendent
        depart = 1       # ligne de départ des noirs

    # Avancer d'une case
    nouvelle_lig = lig + direction
    if 0 <= nouvelle_lig < 8:
        if board[nouvelle_lig][col] == " ":
            mouvements.append((nouvelle_lig, col))

            # Avancer de deux cases depuis la ligne de départ
            if lig == depart:
                nouvelle_lig2 = lig + 2 * direction
                if board[nouvelle_lig2][col] == " ":
                    mouvements.append((nouvelle_lig2, col))

    # Manger en diagonale
    for dc in [-1, 1]:
        nouvelle_col = col + dc
        nouvelle_lig = lig + direction
        if 0 <= nouvelle_lig < 8 and 0 <= nouvelle_col < 8:
            cible = board[nouvelle_lig][nouvelle_col]
            if cible != " " and cible[0] != couleur:
                mouvements.append((nouvelle_lig, nouvelle_col))

    return mouvements
def mouvements_cavalier(board, lig, col):
    mouvements = []
    couleur = board[lig][col][0]
    
    sauts = [
        (-2,-1),(-2,1),
        (-1,-2),(-1,2),
        ( 1,-2),( 1,2),
        ( 2,-1),( 2,1)
    ]
    
    for dl, dc in sauts:
        nl, nc = lig + dl, col + dc
        if 0 <= nl < 8 and 0 <= nc < 8:
            cible = board[nl][nc]
            if cible == " " or cible[0] != couleur:
                mouvements.append((nl, nc))
    
    return mouvements


def mouvements_glissant(board, lig, col, directions):
    mouvements = []
    couleur = board[lig][col][0]
    
    for dl, dc in directions:
        nl, nc = lig + dl, col + dc
        while 0 <= nl < 8 and 0 <= nc < 8:
            cible = board[nl][nc]
            if cible == " ":
                mouvements.append((nl, nc))
            elif cible[0] != couleur:
                mouvements.append((nl, nc))
                break  # on mange et on s'arrête
            else:
                break  # bloqué par sa propre pièce
            nl += dl
            nc += dc
    
    return mouvements


def mouvements_roi(board, lig, col):
    mouvements = []
    couleur = board[lig][col][0]
    
    directions = [
        (-1,-1),(-1,0),(-1,1),
        ( 0,-1),        (0,1),
        ( 1,-1),( 1,0),( 1,1)
    ]
    
    for dl, dc in directions:
        nl, nc = lig + dl, col + dc
        if 0 <= nl < 8 and 0 <= nc < 8:
            cible = board[nl][nc]
            if cible == " " or cible[0] != couleur:
                mouvements.append((nl, nc))
    
    return mouvements
def mouvements_valides(board, lig, col):
    piece = board[lig][col]
    if piece == " ":
        return []
    
    type_piece = piece[1]
    
    if type_piece == "P":
        return mouvements_pion(board, lig, col)
    
    elif type_piece == "N":  # cavalier
        return mouvements_cavalier(board, lig, col)
    
    elif type_piece == "B":  # fou
        return mouvements_glissant(board, lig, col,
               [(-1,-1),(-1,1),(1,-1),(1,1)])
    
    elif type_piece == "R":  # tour
        return mouvements_glissant(board, lig, col,
               [(-1,0),(1,0),(0,-1),(0,1)])
    
    elif type_piece == "Q":  # dame
        return mouvements_glissant(board, lig, col,
               [(-1,-1),(-1,1),(1,-1),(1,1),
                (-1,0),(1,0),(0,-1),(0,1)])
    
    elif type_piece == "K":  # roi
        return mouvements_roi(board, lig, col)
    
    return []
def trouver_roi(board, couleur):
    for lig in range(8):
        for col in range(8):
            if board[lig][col] == couleur + "K":
                return (lig, col)
    return None


def est_en_echec(board, couleur):
    lig_roi, col_roi = trouver_roi(board, couleur)
    ennemi = "b" if couleur == "w" else "w"
    
    # Parcourir toutes les pièces ennemies
    for lig in range(8):
        for col in range(8):
            piece = board[lig][col]
            if piece != " " and piece[0] == ennemi:
                mouvements = mouvements_valides(board, lig, col)
                if (lig_roi, col_roi) in mouvements:
                    return True
    return False


def est_echec_et_mat(board, couleur):
    if not est_en_echec(board, couleur):
        return False
    
    # Essayer tous les mouvements possibles
    for lig in range(8):
        for col in range(8):
            piece = board[lig][col]
            if piece != " " and piece[0] == couleur:
                for (nl, nc) in mouvements_valides(board, lig, col):
                    
                    # Simuler le mouvement
                    sauvegarde = board[nl][nc]
                    board[nl][nc] = board[lig][col]
                    board[lig][col] = " "
                    
                    # Après ce mouvement, est-on encore en échec ?
                    encore_echec = est_en_echec(board, couleur)
                    
                    # Annuler le mouvement
                    board[lig][col] = board[nl][nc]
                    board[nl][nc] = sauvegarde
                    
                    if not encore_echec:
                        return False  # il existe un mouvement qui sauve le roi
    
    return True  # aucun mouvement possible -> échec et mat
VALEURS = {
    "P": 1,
    "N": 3,
    "B": 3,
    "R": 5,
    "Q": 9,
    "K": 0
}

def evaluer(board):
    score = 0
    for lig in range(8):
        for col in range(8):
            piece = board[lig][col]
            if piece != " ":
                valeur = VALEURS[piece[1]]
                if piece[0] == "w":
                    score += valeur
                else:
                    score -= valeur
    return score
import copy

def minimax(board, profondeur, maximise):
    # Cas de base — on arrête de chercher
    if profondeur == 0:
        return evaluer(board), None

    couleur = "w" if maximise else "b"
    tous_mouvements = []

    # Collecter tous les mouvements possibles
    for lig in range(8):
        for col in range(8):
            piece = board[lig][col]
            if piece != " " and piece[0] == couleur:
                for (nl, nc) in mouvements_valides(board, lig, col):
                    tous_mouvements.append((lig, col, nl, nc))

    if not tous_mouvements:
        if est_en_echec(board, couleur):
            return (-999 if maximise else 999), None
        return 0, None  # pat

    meilleur_mouvement = None

    if maximise:
        meilleur_score = -999
        for (lig, col, nl, nc) in tous_mouvements:

            # Simuler le mouvement
            nouveau_board = copy.deepcopy(board)
            nouveau_board[nl][nc] = nouveau_board[lig][col]
            nouveau_board[lig][col] = " "

            score, _ = minimax(nouveau_board, profondeur - 1, False)

            if score > meilleur_score:
                meilleur_score = score
                meilleur_mouvement = (lig, col, nl, nc)

        return meilleur_score, meilleur_mouvement

    else:
        meilleur_score = 999
        for (lig, col, nl, nc) in tous_mouvements:

            nouveau_board = copy.deepcopy(board)
            nouveau_board[nl][nc] = nouveau_board[lig][col]
            nouveau_board[lig][col] = " "

            score, _ = minimax(nouveau_board, profondeur - 1, True)

            if score < meilleur_score:
                meilleur_score = score
                meilleur_mouvement = (lig, col, nl, nc)

        return meilleur_score, meilleur_mouvement
def jouer():
    tour = "w"
    colonnes = "abcdefgh"

    while True:
        afficher_board(board)

        if est_echec_et_mat(board, tour):
            gagnant = "Noirs" if tour == "w" else "Blancs"
            print(f"\n♔ Échec et mat ! Les {gagnant} gagnent !")
            break

        if est_en_echec(board, tour):
            print("⚠ Échec au roi !")

        # Tour du joueur (blancs)
        if tour == "w":
            print("\nTon tour (Blancs)")
            depuis = input("Depuis (ex: e2) : ")
            vers   = input("Vers   (ex: e4) : ")

            col_depuis = colonnes.index(depuis[0])
            lig_depuis = 8 - int(depuis[1])
            col_vers   = colonnes.index(vers[0])
            lig_vers   = 8 - int(vers[1])

            piece = board[lig_depuis][col_depuis]

            if piece == " ":
                print("Case vide !")
                continue
            if piece[0] != "w":
                print("Ce n'est pas ta pièce !")
                continue

            valides = mouvements_valides(board, lig_depuis, col_depuis)
            if (lig_vers, col_vers) not in valides:
                print("Mouvement invalide !")
                continue

            sauvegarde = board[lig_vers][col_vers]
            board[lig_vers][col_vers] = board[lig_depuis][col_depuis]
            board[lig_depuis][col_depuis] = " "

            if est_en_echec(board, "w"):
                board[lig_depuis][col_depuis] = board[lig_vers][col_vers]
                board[lig_vers][col_vers] = sauvegarde
                print("Ton roi serait en échec !")
                continue

        # Tour de l'IA (noirs)
        else:
            print("\nL'IA réfléchit...")
            _, mouvement = minimax(board, 2, False)  # profondeur 2

            if mouvement:
                lig, col, nl, nc = mouvement
                board[nl][nc] = board[lig][col]
                board[lig][col] = " "

                # Afficher le mouvement de l'IA
                depuis_ia = colonnes[col] + str(8 - lig)
                vers_ia   = colonnes[nc]  + str(8 - nl)
                print(f"L'IA joue : {depuis_ia} -> {vers_ia}")

        tour = "b" if tour == "w" else "w"


# Test

afficher_board(board)
jouer()
