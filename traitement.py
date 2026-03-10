"""
TRAITEMENT D'IMAGE — LE COEUR DU PROJET
Toutes les etapes du pipeline OpenCV
"""

import cv2
import numpy as np
import config


# ════════════════════════════════════
#  ETAPE 1 : REDIMENSIONNER
# ════════════════════════════════════

def redimensionner(image):
    """Reduit l'image a 224x224 pixels"""
    return cv2.resize(image, config.IMG_SIZE)


# ════════════════════════════════════
#  ETAPE 2 : CONVERTIR LES COULEURS
# ════════════════════════════════════

def convertir_rgb(image_bgr):
    """Convertit BGR (OpenCV) en RGB (affichage normal)"""
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)


def convertir_hsv(image_bgr):
    """Convertit BGR en HSV (pour detecter les couleurs facilement)"""
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)


# ════════════════════════════════════
#  ETAPE 3 : FILTRER LE BRUIT
# ════════════════════════════════════

def filtrer_bruit(image):
    """Applique un flou gaussien pour supprimer les petits points parasites"""
    return cv2.GaussianBlur(image, config.TAILLE_FILTRE_GAUSSIEN, 0)


# ════════════════════════════════════
#  ETAPE 4 : CREER LES MASQUES
# ════════════════════════════════════

def creer_masque(image_hsv, couleur_min, couleur_max):
    """
    Cree un masque noir et blanc pour une couleur
    Blanc = la couleur est detectee
    Noir  = la couleur n'est pas la
    """
    return cv2.inRange(image_hsv, couleur_min, couleur_max)


def creer_tous_les_masques(image_hsv):
    """Cree tous les masques de couleur necessaires"""
    masques = {}

    # Vert = sain
    masques['sain'] = creer_masque(image_hsv, config.VERT_MIN, config.VERT_MAX)

    # Jaune = chlorose
    masques['chlorose'] = creer_masque(image_hsv, config.JAUNE_MIN, config.JAUNE_MAX)

    # Marron = necrose
    masques['necrose'] = creer_masque(image_hsv, config.MARRON_MIN, config.MARRON_MAX)

    # Rouge = maladie grave (2 plages car le rouge est aux 2 bouts du cercle HSV)
    masque_rouge_1 = creer_masque(image_hsv, config.ROUGE_MIN_1, config.ROUGE_MAX_1)
    masque_rouge_2 = creer_masque(image_hsv, config.ROUGE_MIN_2, config.ROUGE_MAX_2)
    masques['rouge'] = cv2.bitwise_or(masque_rouge_1, masque_rouge_2)

    # Noir = zones mortes
    masques['mort'] = creer_masque(image_hsv, config.NOIR_MIN, config.NOIR_MAX)

    # Bleu = eau
    masques['eau'] = creer_masque(image_hsv, config.BLEU_MIN, config.BLEU_MAX)

    # Blanc = reflets
    masques['blanc'] = creer_masque(image_hsv, config.BLANC_MIN, config.BLANC_MAX)

    return masques


# ════════════════════════════════════
#  ETAPE 5 : NETTOYER LES MASQUES
# ════════════════════════════════════

def nettoyer_masque(masque):
    """
    Nettoie un masque :
    - Bouche les petits trous (MORPH_CLOSE)
    - Supprime les petits points isoles (MORPH_OPEN)
    """
    kernel = np.ones(config.TAILLE_NOYAU_MORPHO, np.uint8)
    masque = cv2.morphologyEx(masque, cv2.MORPH_CLOSE, kernel)
    masque = cv2.morphologyEx(masque, cv2.MORPH_OPEN, kernel)
    return masque


def nettoyer_tous_les_masques(masques):
    """Nettoie tous les masques"""
    masques_propres = {}
    for nom, masque in masques.items():
        masques_propres[nom] = nettoyer_masque(masque)
    return masques_propres


# ════════════════════════════════════
#  ETAPE 6 : COMPTER LES PIXELS
# ════════════════════════════════════

def compter_pixels(masques, taille_image):
    """
    Compte les pixels de chaque masque
    et calcule les pourcentages
    """
    total_pixels = taille_image[0] * taille_image[1]

    comptage = {}

    for nom, masque in masques.items():
        nb_pixels = cv2.countNonZero(masque)
        pourcentage = (nb_pixels / total_pixels) * 100
        comptage[nom] = {
            'pixels': nb_pixels,
            'pourcentage': round(pourcentage, 1)
        }

    # Calculer les totaux
    pct_sain = comptage.get('sain', {}).get('pourcentage', 0)
    pct_chlorose = comptage.get('chlorose', {}).get('pourcentage', 0)
    pct_necrose = comptage.get('necrose', {}).get('pourcentage', 0)
    pct_rouge = comptage.get('rouge', {}).get('pourcentage', 0)

    comptage['total_malade'] = round(pct_chlorose + pct_necrose + pct_rouge, 1)
    comptage['total_couverture'] = round(pct_sain + pct_chlorose + pct_necrose + pct_rouge, 1)

    # Ratio malade par rapport a la plante
    if comptage['total_couverture'] > 0:
        comptage['ratio_malade'] = round(
            (comptage['total_malade'] / comptage['total_couverture']) * 100, 1
        )
    else:
        comptage['ratio_malade'] = 0

    return comptage


# ════════════════════════════════════
#  ETAPE 7 : CARTE DE DIAGNOSTIC
# ════════════════════════════════════

def creer_carte_diagnostic(masques, taille):
    """Cree une image coloree montrant chaque zone"""
    carte = np.zeros(taille, dtype=np.uint8)

    if 'eau' in masques:
        carte[masques['eau'] > 0] = config.COULEUR_EAU
    if 'blanc' in masques:
        carte[masques['blanc'] > 0] = config.COULEUR_BLANC
    if 'sain' in masques:
        carte[masques['sain'] > 0] = config.COULEUR_SAIN
    if 'chlorose' in masques:
        carte[masques['chlorose'] > 0] = config.COULEUR_CHLOROSE
    if 'necrose' in masques:
        carte[masques['necrose'] > 0] = config.COULEUR_NECROSE
    if 'rouge' in masques:
        carte[masques['rouge'] > 0] = config.COULEUR_ROUGE
    if 'mort' in masques:
        carte[masques['mort'] > 0] = config.COULEUR_MORT

    return carte


def creer_superposition(image_rgb, carte, alpha=0.5):
    """Melange l'image originale avec la carte de diagnostic"""
    return cv2.addWeighted(image_rgb, alpha, carte, 1 - alpha, 0)


# ════════════════════════════════════
#  ETAPE 8 : PREPARER POUR L'IA
# ════════════════════════════════════

def preparer_pour_ia(image_rgb):
    """
    Prepare l'image pour le modele IA :
    - Convertir en float (nombres decimaux)
    - Diviser par 255 (normaliser entre 0 et 1)
    - Ajouter la dimension batch
    """
    image_float = np.array(image_rgb, dtype=np.float32) / 255.0
    image_batch = np.expand_dims(image_float, axis=0)
    return image_batch


# ════════════════════════════════════
#  PIPELINE COMPLET
# ════════════════════════════════════

def pipeline_complet(image_bgr):
    """
    Execute TOUTES les etapes dans l'ordre
    C'est LA fonction principale

    Entree : image BGR (n'importe quelle taille)
    Sortie : dictionnaire avec tous les resultats
    """

    # Etape 1
    image_224 = redimensionner(image_bgr)

    # Etape 2
    image_rgb = convertir_rgb(image_224)
    image_hsv = convertir_hsv(image_224)

    # Etape 3
    image_lissee = filtrer_bruit(image_224)
    hsv_lisse = convertir_hsv(image_lissee)

    # Etape 4
    masques = creer_tous_les_masques(hsv_lisse)

    # Etape 5
    masques = nettoyer_tous_les_masques(masques)

    # Etape 6
    comptage = compter_pixels(masques, (config.IMG_HEIGHT, config.IMG_WIDTH))

    # Etape 7
    carte = creer_carte_diagnostic(masques, image_rgb.shape)
    superposition = creer_superposition(image_rgb, carte)

    # Etape 8
    image_ia = preparer_pour_ia(image_rgb)

    # Tout rassembler
    resultats = {
        'image_rgb': image_rgb,
        'image_hsv': image_hsv,
        'masques': masques,
        'comptage': comptage,
        'carte': carte,
        'superposition': superposition,
        'image_ia': image_ia,
    }

    return resultats