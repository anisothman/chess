import pygame
import sys
import copy

pygame.init()

LARGEUR = 640
HAUTEUR = 660
TAILLE_CASE = 80

BLANC  = (240, 217, 181)
MARRON = (181, 136, 99)
JAUNE  = (246, 246, 105)
BLEU   = (100, 149, 237)
ROUGE  = (220, 50, 50)

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Échecs ♟")

fonte = pygame.font.SysFont("segoeuisymbol", 58)
fonte_info = pygame.font.SysFont("arial", 22)

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

SYMBOLES = {
    "wK":"♔","wQ":"♕","wR":"♖","wB":"♗","wN":"♘","wP":"♙",
    "bK":"♚","bQ":"♛","bR":"♜","bB":"♝","bN":"♞","bP":"♟"
}

# =====================
# Logique des mouvements
# =====================

def mouvements_pion(board, lig, col):
    mouvements = []
    couleur = board[lig][col][0]
    direction = -1 if couleur == "w" else 1
    depart = 6 if couleur == "w" else 1

    nl = lig + direction
    if 0 <= nl < 8 and board[nl][col] == " ":
        mouvements.append((nl, col))
        if lig == depart:
            nl2 = lig + 2 * direction
            if board[nl2][col] == " ":
                mouvements.append((nl2, col))

    for dc in [-1, 1]:
        nc = col + dc
        nl = lig + direction
        if 0 <= nl < 8 and 0 <= nc < 8:
            cible = board[nl][nc]
            if cible != " " and cible[0] != couleur:
                mouvements.append((nl, nc))
    return mouvements

def mouvements_cavalier(board, lig, col):
    mouvements = []
    couleur = board[lig][col][0]
    for dl, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        nl, nc = lig+dl, col+dc
        if 0 <= nl < 8 and 0 <= nc < 8:
            if board[nl][nc] == " " or board[nl][nc][0] != couleur:
                mouvements.append((nl, nc))
    return mouvements

def mouvements_glissant(board, lig, col, directions):
    mouvements = []
    couleur = board[lig][col][0]
    for dl, dc in directions:
        nl, nc = lig+dl, col+dc
        while 0 <= nl < 8 and 0 <= nc < 8:
            if board[nl][nc] == " ":
                mouvements.append((nl, nc))
            elif board[nl][nc][0] != couleur:
                mouvements.append((nl, nc))
                break
            else:
                break
            nl += dl
            nc += dc
    return mouvements

def mouvements_roi(board, lig, col):
    mouvements = []
    couleur = board[lig][col][0]
    for dl, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        nl, nc = lig+dl, col+dc
        if 0 <= nl < 8 and 0 <= nc < 8:
            if board[nl][nc] == " " or board[nl][nc][0] != couleur:
                mouvements.append((nl, nc))
    return mouvements

def mouvements_valides(board, lig, col):
    piece = board[lig][col]
    if piece == " ": return []
    t = piece[1]
    if t == "P": return mouvements_pion(board, lig, col)
    elif t == "N": return mouvements_cavalier(board, lig, col)
    elif t == "B": return mouvements_glissant(board, lig, col, [(-1,-1),(-1,1),(1,-1),(1,1)])
    elif t == "R": return mouvements_glissant(board, lig, col, [(-1,0),(1,0),(0,-1),(0,1)])
    elif t == "Q": return mouvements_glissant(board, lig, col, [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)])
    elif t == "K": return mouvements_roi(board, lig, col)
    return []

def trouver_roi(board, couleur):
    for lig in range(8):
        for col in range(8):
            if board[lig][col] == couleur + "K":
                return (lig, col)
    return None

def est_en_echec(board, couleur):
    roi = trouver_roi(board, couleur)
    if not roi: return False
    lig_roi, col_roi = roi
    ennemi = "b" if couleur == "w" else "w"
    for lig in range(8):
        for col in range(8):
            if board[lig][col] != " " and board[lig][col][0] == ennemi:
                if (lig_roi, col_roi) in mouvements_valides(board, lig, col):
                    return True
    return False

def est_echec_et_mat(board, couleur):
    if not est_en_echec(board, couleur): return False
    for lig in range(8):
        for col in range(8):
            if board[lig][col] != " " and board[lig][col][0] == couleur:
                for (nl, nc) in mouvements_valides(board, lig, col):
                    nb = copy.deepcopy(board)
                    nb[nl][nc] = nb[lig][col]
                    nb[lig][col] = " "
                    if not est_en_echec(nb, couleur):
                        return False
    return True

# =====================
# IA Minimax
# =====================

VALEURS = {"P":1,"N":3,"B":3,"R":5,"Q":9,"K":0}

def evaluer(board):
    score = 0
    for lig in range(8):
        for col in range(8):
            p = board[lig][col]
            if p != " ":
                v = VALEURS[p[1]]
                score += v if p[0] == "w" else -v
    return score

def minimax(board, profondeur, maximise):
    if profondeur == 0:
        return evaluer(board), None
    couleur = "w" if maximise else "b"
    tous = []
    for lig in range(8):
        for col in range(8):
            if board[lig][col] != " " and board[lig][col][0] == couleur:
                for (nl, nc) in mouvements_valides(board, lig, col):
                    tous.append((lig, col, nl, nc))
    if not tous:
        return (-999 if maximise else 999), None
    meilleur = None
    if maximise:
        best = -999
        for (lig,col,nl,nc) in tous:
            nb = copy.deepcopy(board)
            nb[nl][nc] = nb[lig][col]; nb[lig][col] = " "
            v, _ = minimax(nb, profondeur-1, False)
            if v > best: best = v; meilleur = (lig,col,nl,nc)
        return best, meilleur
    else:
        best = 999
        for (lig,col,nl,nc) in tous:
            nb = copy.deepcopy(board)
            nb[nl][nc] = nb[lig][col]; nb[lig][col] = " "
            v, _ = minimax(nb, profondeur-1, True)
            if v < best: best = v; meilleur = (lig,col,nl,nc)
        return best, meilleur

# =====================
# État du jeu
# =====================

tour = "w"
selected = None
possibles = []
message = "Ton tour — clique une pièce"
game_over = False

# =====================
# Dessin
# =====================

def dessiner_rquette():
    for lig in range(8):
        for col in range(8):
            couleur = BLANC if (lig+col)%2==0 else MARRON
            pygame.draw.rect(ecran, couleur,
                (col*TAILLE_CASE, lig*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

def dessiner_surbrillance():
    if selected:
        lig, col = selected
        s = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
        s.fill((246, 246, 105, 160))
        ecran.blit(s, (col*TAILLE_CASE, lig*TAILLE_CASE))

    for (nl, nc) in possibles:
        s = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
        s.fill((100, 149, 237, 130))
        ecran.blit(s, (nc*TAILLE_CASE, nl*TAILLE_CASE))

def dessiner_pieces():
    for lig in range(8):
        for col in range(8):
            piece = board[lig][col]
            if piece != " ":
                symbole = SYMBOLES[piece]
                couleur_texte = (255,255,255) if piece[0]=="w" else (0,0,0)
                texte = fonte.render(symbole, True, couleur_texte)
                x = col*TAILLE_CASE + (TAILLE_CASE - texte.get_width())//2
                y = lig*TAILLE_CASE + (TAILLE_CASE - texte.get_height())//2
                ecran.blit(texte, (x, y))

def dessiner_message():
    couleur_msg = ROUGE if "mat" in message or "Échec" in message else (30,30,30)
    pygame.draw.rect(ecran, (220,220,220), (0, 640, 640, 20))
    texte = fonte_info.render(message, True, couleur_msg)
    ecran.blit(texte, (10, 642))

# =====================
# Boucle principale
# =====================

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and tour == "w":
            mx, my = pygame.mouse.get_pos()
            col_clic = mx // TAILLE_CASE
            lig_clic = my // TAILLE_CASE

            if lig_clic >= 8: continue

            if selected:
                if (lig_clic, col_clic) in possibles:
                    sauvegarde = board[lig_clic][col_clic]
                    board[lig_clic][col_clic] = board[selected[0]][selected[1]]
                    board[selected[0]][selected[1]] = " "

                    # Promotion pion blanc
                    if board[lig_clic][col_clic] == "wP" and lig_clic == 0:
                        board[lig_clic][col_clic] = "wQ"

                    if est_en_echec(board, "w"):
                        board[selected[0]][selected[1]] = board[lig_clic][col_clic]
                        board[lig_clic][col_clic] = sauvegarde
                        message = "Interdit — ton roi serait en échec !"
                    else:
                        selected = None
                        possibles = []
                        tour = "b"
                        message = "L'IA réfléchit..."

                        if est_en_echec(board, "b"):
                            message = "⚠ Échec au roi de l'IA !"

                else:
                    selected = None
                    possibles = []

            if tour == "w" and selected is None:
                piece = board[lig_clic][col_clic]
                if piece != " " and piece[0] == "w":
                    selected = (lig_clic, col_clic)
                    possibles = mouvements_valides(board, lig_clic, col_clic)

    # Tour IA
    if tour == "b" and not game_over:
        ecran.fill((200,200,200))
        dessiner_rquette()
        dessiner_surbrillance()
        dessiner_pieces()
        dessiner_message()
        pygame.display.flip()

        _, mouvement = minimax(board, 2, False)
        if mouvement:
            lig, col, nl, nc = mouvement
            board[nl][nc] = board[lig][col]
            board[lig][col] = " "
            if board[nl][nc] == "bP" and nl == 7:
                board[nl][nc] = "bQ"

        tour = "w"

        if est_echec_et_mat(board, "w"):
            message = "Échec et mat — l'IA gagne !"
            game_over = True
        elif est_echec_et_mat(board, "b"):
            message = "Échec et mat — tu gagnes !"
            game_over = True
        elif est_en_echec(board, "w"):
            message = "⚠ Échec à ton roi !"
        elif est_en_echec(board, "b"):
            message = "⚠ Échec au roi de l'IA !"
        else:
            message = "Ton tour — clique une pièce"

    ecran.fill((200,200,200))
    dessiner_rquette()
    dessiner_surbrillance()
    dessiner_pieces()
    dessiner_message()
    pygame.display.flip()
    clock.tick(60)