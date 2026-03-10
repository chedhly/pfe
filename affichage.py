"""
AFFICHAGE
Dessine les graphiques et les figures
C'est le DESSINATEUR du projet
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import config


def afficher_analyse_complete(resultats, diagnostic, nom="Analyse", sauvegarder=True):
    """
    Affiche 1 figure avec 4 images :
    - Image originale
    - Carte de diagnostic
    - Superposition
    - Barres de pourcentages
    """

    comptage = resultats['comptage']
    bassin = diagnostic['bassin']
    sante = diagnostic['sante']

    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.suptitle(f"Analyse : {nom}", fontsize=16, fontweight='bold', y=1.02)

    # Image 1 : Originale
    axes[0].imshow(resultats['image_rgb'])
    axes[0].set_title("Image Originale", fontsize=12, fontweight='bold')
    axes[0].axis('off')

    # Image 2 : Carte de diagnostic
    axes[1].imshow(resultats['carte'])
    axes[1].set_title("Carte de Diagnostic", fontsize=12, fontweight='bold')
    axes[1].axis('off')
    axes[1].text(0.5, -0.06,
                 "VERT=Sain  JAUNE=Chlorose  MARRON=Necrose  BLEU=Eau",
                 transform=axes[1].transAxes, fontsize=8,
                 ha='center', style='italic', color='gray')

    # Image 3 : Superposition
    axes[2].imshow(resultats['superposition'])
    axes[2].set_title("Superposition", fontsize=12, fontweight='bold')
    axes[2].axis('off')

    # Image 4 : Barres de pourcentages
    categories = ['Sain', 'Chlorose', 'Necrose', 'Eau']
    valeurs = [
        comptage.get('sain', {}).get('pourcentage', 0),
        comptage.get('chlorose', {}).get('pourcentage', 0),
        comptage.get('necrose', {}).get('pourcentage', 0),
        comptage.get('eau', {}).get('pourcentage', 0),
    ]
    couleurs_barres = ['#2d6a4f', '#f4d03f', '#a0522d', '#5dade2']

    bars = axes[3].barh(categories, valeurs, color=couleurs_barres, height=0.6)
    axes[3].set_xlim(0, 100)
    axes[3].set_xlabel('Pourcentage (%)', fontsize=10)
    axes[3].set_title("Repartition", fontsize=12, fontweight='bold')

    for bar, val in zip(bars, valeurs):
        if val > 1:
            axes[3].text(bar.get_width() + 1.5, bar.get_y() + bar.get_height()/2,
                        f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')

    # Diagnostic en bas de la figure
    fig.text(0.5, -0.06,
             f"BASSIN: {bassin['etat']}  |  "
             f"SANTE: {sante['etat']}  |  "
             f"Couverture: {bassin['couverture']}%  |  "
             f"Malade: {sante['ratio_malade']}%",
             ha='center', fontsize=13, fontweight='bold',
             color=sante['couleur'],
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='gray'))

    plt.tight_layout()

    if sauvegarder:
        chemin = os.path.join(config.DOSSIER_RESULTATS,
                              f"analyse_{nom.lower().replace(' ', '_')}.png")
        plt.savefig(chemin, dpi=150, bbox_inches='tight')
        print(f"[OK] Figure sauvegardee : {chemin}")

    plt.show()


def afficher_pipeline_etapes(resultats, nom="Pipeline"):
    """
    Affiche les 8 etapes du pipeline dans 1 figure
    Pour voir comment l'image est transformee a chaque etape
    """

    masques = resultats['masques']

    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle(f"Pipeline : {nom}", fontsize=16, fontweight='bold')

    axes[0][0].imshow(resultats['image_rgb'])
    axes[0][0].set_title("1. Image Originale\n(224x224)")
    axes[0][0].axis('off')

    axes[0][1].imshow(resultats['image_hsv'][:,:,0], cmap='hsv')
    axes[0][1].set_title("2. Canal H (HSV)\nTeinte des couleurs")
    axes[0][1].axis('off')

    axes[0][2].imshow(masques.get('sain', np.zeros((224,224))), cmap='Greens')
    axes[0][2].set_title("3. Masque VERT\n(zones saines)")
    axes[0][2].axis('off')

    axes[0][3].imshow(masques.get('chlorose', np.zeros((224,224))), cmap='YlOrBr')
    axes[0][3].set_title("4. Masque JAUNE\n(chlorose)")
    axes[0][3].axis('off')

    axes[1][0].imshow(masques.get('necrose', np.zeros((224,224))), cmap='Oranges')
    axes[1][0].set_title("5. Masque MARRON\n(necrose)")
    axes[1][0].axis('off')

    axes[1][1].imshow(masques.get('eau', np.zeros((224,224))), cmap='Blues')
    axes[1][1].set_title("6. Masque BLEU\n(eau)")
    axes[1][1].axis('off')

    axes[1][2].imshow(resultats['carte'])
    axes[1][2].set_title("7. Carte Diagnostic\n(toutes les zones)")
    axes[1][2].axis('off')

    axes[1][3].imshow(resultats['superposition'])
    axes[1][3].set_title("8. Superposition\n(resultat final)")
    axes[1][3].axis('off')

    plt.tight_layout()

    chemin = os.path.join(config.DOSSIER_RESULTATS,
                          f"pipeline_{nom.lower().replace(' ', '_')}.png")
    plt.savefig(chemin, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"[OK] Pipeline sauvegarde : {chemin}")


def afficher_comparaison(liste_resultats, liste_diagnostics, liste_noms):
    """
    Compare plusieurs analyses cote a cote
    Utile pour comparer les 4 tests
    """
    n = len(liste_resultats)

    fig, axes = plt.subplots(n, 3, figsize=(16, 5 * n))
    fig.suptitle("Comparaison des Analyses", fontsize=16, fontweight='bold')

    for i in range(n):
        r = liste_resultats[i]
        d = liste_diagnostics[i]
        nom = liste_noms[i]
        comptage = r['comptage']

        # Image originale
        axes[i][0].imshow(r['image_rgb'])
        axes[i][0].set_title(f"{nom}\n(Originale)", fontsize=11, fontweight='bold')
        axes[i][0].axis('off')

        # Superposition
        axes[i][1].imshow(r['superposition'])
        axes[i][1].set_title(f"Diagnostic\nBassin: {d['bassin']['etat']} | Sante: {d['sante']['etat']}",
                             fontsize=10, fontweight='bold')
        axes[i][1].axis('off')

        # Barres
        cats = ['Sain', 'Chlorose', 'Necrose', 'Eau']
        vals = [
            comptage.get('sain', {}).get('pourcentage', 0),
            comptage.get('chlorose', {}).get('pourcentage', 0),
            comptage.get('necrose', {}).get('pourcentage', 0),
            comptage.get('eau', {}).get('pourcentage', 0),
        ]
        couleurs = ['#2d6a4f', '#f4d03f', '#a0522d', '#5dade2']

        bars = axes[i][2].barh(cats, vals, color=couleurs, height=0.6)
        axes[i][2].set_xlim(0, 100)
        axes[i][2].set_title("Repartition (%)", fontsize=11, fontweight='bold')

        for bar, val in zip(bars, vals):
            if val > 1:
                axes[i][2].text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                              f'{val:.1f}%', va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    chemin = os.path.join(config.DOSSIER_RESULTATS, "comparaison.png")
    plt.savefig(chemin, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"[OK] Comparaison sauvegardee : {chemin}")