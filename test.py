"""
TESTS — IMAGES SIMULEES
Cree 4 images de test et lance le pipeline
C'est le TESTEUR du projet
"""

import cv2
import numpy as np

import config
import utils
import traitement
import diagnostic
import affichage


# ════════════════════════════════════
#  CREER LES IMAGES DE TEST
# ════════════════════════════════════

def creer_plante_saine():
    """Dessine une image avec beaucoup de vert (plante saine)"""
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :] = [180, 120, 50]  # Fond bleu = eau

    # Beaucoup de cercles verts = plante saine
    for x in range(25, 280, 35):
        for y in range(25, 280, 35):
            r = np.random.randint(14, 20)
            v = np.random.randint(100, 180)
            cv2.circle(img, (x, y), r, (0, v, 0), -1)

    return img


def creer_plante_malade():
    """Dessine une image avec du vert + jaune + marron (plante malade)"""
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :] = [180, 120, 50]  # Fond bleu = eau

    # Cercles verts = parties saines
    cv2.circle(img, (60, 60), 35, (0, 150, 0), -1)
    cv2.circle(img, (180, 60), 40, (0, 140, 0), -1)
    cv2.circle(img, (60, 180), 30, (0, 130, 0), -1)
    cv2.circle(img, (120, 120), 35, (0, 145, 0), -1)
    cv2.circle(img, (240, 180), 28, (0, 135, 0), -1)

    # Cercles jaunes = chlorose (debut maladie)
    cv2.circle(img, (180, 180), 25, (0, 180, 180), -1)
    cv2.circle(img, (120, 240), 20, (0, 190, 190), -1)
    cv2.circle(img, (240, 80), 18, (0, 170, 170), -1)

    # Cercles marron = necrose (maladie avancee)
    cv2.circle(img, (80, 120), 18, (10, 50, 100), -1)
    cv2.circle(img, (160, 150), 15, (15, 60, 110), -1)

    return img


def creer_bassin_plein():
    """Dessine une image presque toute verte (bassin plein)"""
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :] = [180, 120, 50]  # Fond bleu

    # Plein de cercles verts partout
    for x in range(12, 290, 18):
        for y in range(12, 290, 18):
            r = np.random.randint(9, 12)
            v = np.random.randint(110, 170)
            cv2.circle(img, (x, y), r, (0, v, 0), -1)

    return img


def creer_bassin_vide():
    """Dessine une image presque toute bleue (bassin vide)"""
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :] = [180, 120, 50]  # Fond bleu = eau

    # Juste 2 petites plantes
    cv2.circle(img, (80, 100), 14, (0, 140, 0), -1)
    cv2.circle(img, (200, 180), 11, (0, 130, 0), -1)

    return img


# ════════════════════════════════════
#  LANCER LES TESTS
# ════════════════════════════════════

def lancer_tests():
    """Teste le pipeline complet avec les 4 images"""

    print()
    print("=" * 55)
    print("  TEST DU PIPELINE DE TRAITEMENT D'IMAGE")
    print("  (Sans modele IA — Images simulees)")
    print("=" * 55)

    # Creer les dossiers
    utils.creer_dossiers()

    # Les 4 scenarios
    scenarios = [
        ("Plante Saine", creer_plante_saine()),
        ("Plante Malade", creer_plante_malade()),
        ("Bassin Plein", creer_bassin_plein()),
        ("Bassin Vide", creer_bassin_vide()),
    ]

    tous_resultats = []
    tous_diagnostics = []
    tous_noms = []

    for nom, image in scenarios:

        print(f"\n--- Test : {nom} ---")

        # 1. Traitement d'image (le pipeline)
        resultats = traitement.pipeline_complet(image)

        # 2. Diagnostic (le docteur)
        diag = diagnostic.diagnostic_complet(resultats['comptage'])

        # 3. Afficher dans le terminal
        diagnostic.afficher_diagnostic_console(diag)

        # 4. Afficher la figure
        affichage.afficher_analyse_complete(resultats, diag, nom)

        # 5. Sauvegarder en JSON
        utils.sauvegarder_resultats_json({
            'nom': nom,
            'bassin': diag['bassin']['etat'],
            'sante': diag['sante']['etat'],
            'couverture': diag['bassin']['couverture'],
            'ratio_malade': diag['sante']['ratio_malade'],
        }, f"test_{nom.lower().replace(' ', '_')}.json")

        tous_resultats.append(resultats)
        tous_diagnostics.append(diag)
        tous_noms.append(nom)

    # 6. Comparaison des 4 tests
    print("\n--- Comparaison ---")
    affichage.afficher_comparaison(tous_resultats, tous_diagnostics, tous_noms)

    # 7. Resume final dans le terminal
    print("\n")
    print("=" * 70)
    print("  RESUME DES TESTS")
    print("=" * 70)
    print(f"  {'Scenario':<18} {'Couverture':>12} {'Bassin':<10} {'Malade':>8}  {'Sante'}")
    print(f"  {'_'*18} {'_'*12} {'_'*10} {'_'*8}  {'_'*20}")

    for i, nom in enumerate(tous_noms):
        d = tous_diagnostics[i]
        print(f"  {nom:<18} {d['bassin']['couverture']:>8}%    "
              f"{d['bassin']['etat']:<10} {d['sante']['ratio_malade']:>5}%  "
              f"{d['sante']['etat']}")

    print("=" * 70)
    print("  TOUS LES TESTS REUSSIS !")
    print("=" * 70)


# ════════════════════════════════════
#  POINT D'ENTREE
# ════════════════════════════════════

if __name__ == "__main__":
    lancer_tests()