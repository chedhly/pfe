"""
BOITE A OUTILS
Fonctions utilitaires : charger, sauvegarder, creer dossiers
"""

import os
import json
from datetime import datetime
import cv2
import config


def creer_dossiers():
    """Cree les dossiers images/, resultats/, modeles/"""
    dossiers = [config.DOSSIER_IMAGES,
                config.DOSSIER_RESULTATS,
                config.DOSSIER_MODELES]

    for dossier in dossiers:
        os.makedirs(dossier, exist_ok=True)

    print("[OK] Dossiers crees")


def horodatage():
    """Retourne la date et heure actuelle"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def charger_image(chemin):
    """
    Ouvre une image depuis un fichier

    Parametre : chemin du fichier (ex: 'images/photo.jpg')
    Retourne  : image (tableau numpy) ou None si erreur
    """
    image = cv2.imread(chemin)

    if image is None:
        print(f"[ERREUR] Image non trouvee : {chemin}")
        return None

    print(f"[OK] Image chargee : {chemin}")
    print(f"     Taille : {image.shape[1]}x{image.shape[0]} pixels")

    return image


def sauvegarder_image(image, nom_fichier):
    """Sauvegarde une image dans le dossier resultats/"""
    chemin = os.path.join(config.DOSSIER_RESULTATS, nom_fichier)
    cv2.imwrite(chemin, image)
    print(f"[OK] Image sauvegardee : {chemin}")


def sauvegarder_resultats_json(resultats, nom_fichier=None):
    """Sauvegarde les resultats en fichier JSON"""
    if nom_fichier is None:
        nom_fichier = f"analyse_{horodatage()}.json"

    chemin = os.path.join(config.DOSSIER_RESULTATS, nom_fichier)

    # Filtrer les tableaux numpy (pas serialisables en JSON)
    donnees = {}
    for cle, valeur in resultats.items():
        if not hasattr(valeur, 'shape'):
            donnees[cle] = valeur

    with open(chemin, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=2, ensure_ascii=False)

    print(f"[OK] Resultats sauvegardes : {chemin}")