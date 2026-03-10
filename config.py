"""
CONFIGURATION GENERALE
Tous les parametres du traitement d'image
"""

import numpy as np

# Taille de l'image
IMG_WIDTH = 224
IMG_HEIGHT = 224
IMG_SIZE = (IMG_WIDTH, IMG_HEIGHT)

# VERT = Plante saine
VERT_MIN = np.array([35, 40, 40])
VERT_MAX = np.array([85, 255, 255])

# JAUNE = Chlorose (debut de maladie)
JAUNE_MIN = np.array([20, 40, 40])
JAUNE_MAX = np.array([35, 255, 255])

# MARRON = Necrose (maladie avancee)
MARRON_MIN = np.array([5, 40, 20])
MARRON_MAX = np.array([20, 255, 200])

# ROUGE = Maladie grave
ROUGE_MIN_1 = np.array([0, 50, 50])
ROUGE_MAX_1 = np.array([5, 255, 255])
ROUGE_MIN_2 = np.array([170, 50, 50])
ROUGE_MAX_2 = np.array([180, 255, 255])

# NOIR = Zones mortes
NOIR_MIN = np.array([0, 0, 0])
NOIR_MAX = np.array([180, 255, 40])

# BLEU = Eau visible
BLEU_MIN = np.array([90, 30, 30])
BLEU_MAX = np.array([130, 255, 255])

# BLANC = Reflet eau
BLANC_MIN = np.array([0, 0, 180])
BLANC_MAX = np.array([180, 40, 255])

# Seuils bassin (pourcentage couverture)
SEUIL_BASSIN_PLEIN = 70
SEUIL_BASSIN_MOYEN = 40
SEUIL_BASSIN_FAIBLE = 15

# Seuils sante (pourcentage malade)
SEUIL_SANTE_SAINE = 5
SEUIL_SANTE_DEBUT = 15
SEUIL_SANTE_MALADE = 30

# Couleurs affichage (RGB)
COULEUR_SAIN = [0, 200, 0]
COULEUR_CHLOROSE = [255, 255, 0]
COULEUR_NECROSE = [180, 60, 20]
COULEUR_ROUGE = [255, 0, 0]
COULEUR_MORT = [50, 50, 50]
COULEUR_EAU = [50, 150, 255]
COULEUR_BLANC = [220, 220, 220]

# Parametres filtrage
TAILLE_FILTRE_GAUSSIEN = (5, 5)
TAILLE_NOYAU_MORPHO = (5, 5)

# Dossiers
DOSSIER_IMAGES = 'images'
DOSSIER_RESULTATS = 'resultats'
DOSSIER_MODELES = 'modeles'