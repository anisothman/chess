# ♟ Jeu d'Échecs en Python

Un jeu d'échecs complet avec interface graphique et intelligence artificielle, développé en Python avec pygame.

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Aperçu

- Joue contre une IA basée sur l'algorithme **Minimax**
- Interface graphique avec **pygame**
- Détection de l'**échec** et de l'**échec et mat**
- Surbrillance des mouvements possibles
- Promotion automatique des pions en dame

## Fichiers

```
chess/
├── chess.py        # Version terminal (2 joueurs)
├── chess_gui.py    # Version graphique (joueur vs IA)
└── README.md
```


**2. Installer pygame**
```bash
py -3.13 -m pip install pygame
```

## Lancer le jeu

**Version graphique (recommandée)**
```bash
py -3.13 chess_gui.py
```

**Version terminal**
```bash
py -3.13 chess.py
```

## Comment jouer

- Clique sur une pièce blanche pour la sélectionner
- Les cases bleues montrent les mouvements possibles
- Clique sur une case bleue pour déplacer
- L'IA joue automatiquement après ton coup

## Fonctionnalités

| Fonctionnalité | Terminal | Graphique |
|---|---|---|
| Toutes les pièces | ✅ | ✅ |
| Règles complètes | ✅ | ✅ |
| Détection échec | ✅ | ✅ |
| Échec et mat | ✅ | ✅ |
| IA Minimax | ✅ | ✅ |
| Interface graphique | ❌ | ✅ |
| Surbrillance mouvements | ❌ | ✅ |

## Comment fonctionne l'IA

L'IA utilise l'algorithme **Minimax** avec une profondeur de 2 coups :

1. Elle simule tous les mouvements possibles
2. Pour chaque mouvement, elle simule la réponse du joueur
3. Elle évalue chaque position selon la valeur des pièces
4. Elle choisit le mouvement qui lui donne le meilleur avantage

| Pièce | Valeur |
|---|---|
| Pion | 1 |
| Cavalier | 3 |
| Fou | 3 |
| Tour | 5 |
| Dame | 9 |

## Prérequis

- Python 3.13
- pygame 2.6.1

## Auteur

Développé étape par étape en apprenant Python et l'IA.
