"""
PROGRAMME PRINCIPAL
Le CHEF du projet — lance le menu
"""

import os
import sys

import config
import utils
import traitement
import diagnostic
import affichage


def analyser_image(chemin_image, nom=None):
    """Analyse complete d'une seule image"""

    if nom is None:
        nom = os.path.basename(chemin_image)

    print(f"\n[INFO] Analyse de : {nom}")
    print("-" * 40)

    # 1. Charger
    image = utils.charger_image(chemin_image)
    if image is None:
        return None

    # 2. Traitement
    resultats = traitement.pipeline_complet(image)

    # 3. Diagnostic
    diag = diagnostic.diagnostic_complet(resultats['comptage'])

    # 4. Afficher dans le terminal
    diagnostic.afficher_diagnostic_console(diag)

    # 5. Afficher la figure
    affichage.afficher_analyse_complete(resultats, diag, nom)

    # 6. Sauvegarder
    utils.sauvegarder_resultats_json({
        'nom': nom,
        'bassin_etat': diag['bassin']['etat'],
        'sante_etat': diag['sante']['etat'],
        'couverture': diag['bassin']['couverture'],
        'ratio_malade': diag['sante']['ratio_malade'],
        'action_bassin': diag['bassin']['action'],
        'action_sante': diag['sante']['action'],
    })

    return diag


def analyser_dossier(chemin_dossier):
    """Analyse TOUTES les images d'un dossier"""

    extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    fichiers = [f for f in os.listdir(chemin_dossier)
                if f.lower().endswith(extensions)]

    if not fichiers:
        print(f"[ERREUR] Aucune image trouvee dans : {chemin_dossier}")
        return

    print(f"\n[INFO] {len(fichiers)} images trouvees dans {chemin_dossier}")

    tous_resultats = []
    tous_diagnostics = []
    tous_noms = []

    for fichier in fichiers:
        chemin = os.path.join(chemin_dossier, fichier)
        image = utils.charger_image(chemin)

        if image is not None:
            resultats = traitement.pipeline_complet(image)
            diag = diagnostic.diagnostic_complet(resultats['comptage'])

            diagnostic.afficher_diagnostic_console(diag)
            affichage.afficher_analyse_complete(resultats, diag, fichier)

            tous_resultats.append(resultats)
            tous_diagnostics.append(diag)
            tous_noms.append(fichier)

    # Comparaison si plusieurs images
    if len(tous_resultats) > 1:
        affichage.afficher_comparaison(tous_resultats, tous_diagnostics, tous_noms)


def menu_principal():
    """Le menu interactif"""

    utils.creer_dossiers()

    print()
    print("=" * 55)
    print("  SYSTEME DE TRAITEMENT D'IMAGE")
    print("  Detection de Maladie des Plantes")
    print("  PFE 2025-2026")
    print("=" * 55)

    while True:
        print("\n  OPTIONS :")
        print("  1 — Analyser une image")
        print("  2 — Analyser un dossier d'images")
        print("  3 — Lancer les tests (images simulees)")
        print("  4 — Afficher le pipeline (etapes)")
        print("  0 — Quitter")

        choix = input("\n  Votre choix : ").strip()

        if choix == '1':
            chemin = input("  Chemin de l'image : ").strip()
            analyser_image(chemin)

        elif choix == '2':
            dossier = input("  Chemin du dossier : ").strip()
            analyser_dossier(dossier)

        elif choix == '3':
            import test
            test.lancer_tests()

        elif choix == '4':
            import test
            image = test.creer_plante_malade()
            resultats = traitement.pipeline_complet(image)
            affichage.afficher_pipeline_etapes(resultats, "Exemple Pipeline")

        elif choix == '0':
            print("\n  Au revoir !")
            sys.exit(0)

        else:
            print("  [ERREUR] Choix invalide")


# ════════════════════════════════════
#  POINT D'ENTREE
# ════════════════════════════════════

if __name__ == "__main__":
    menu_principal()