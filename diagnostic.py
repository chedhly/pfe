"""
DIAGNOSTIC
Analyse les chiffres et donne un resultat
C'est le DOCTEUR du projet
"""

import config


def diagnostiquer_bassin(comptage):
    """
    Le bassin est plein ou vide ?
    Regarde le pourcentage de couverture vegetale
    """
    couverture = comptage['total_couverture']

    if couverture >= config.SEUIL_BASSIN_PLEIN:
        return {
            'etat': 'PLEIN',
            'couleur': 'green',
            'description': 'Bassin bien couvert, recolte possible',
            'couverture': couverture,
            'action': 'Planifier la recolte'
        }
    elif couverture >= config.SEUIL_BASSIN_MOYEN:
        return {
            'etat': 'MOYEN',
            'couleur': 'orange',
            'description': 'Azolla en croissance, attendre',
            'couverture': couverture,
            'action': 'Attendre la croissance'
        }
    elif couverture >= config.SEUIL_BASSIN_FAIBLE:
        return {
            'etat': 'FAIBLE',
            'couleur': 'orangered',
            'description': 'Peu d Azolla, verifier les conditions',
            'couverture': couverture,
            'action': 'Verifier nutriments et conditions'
        }
    else:
        return {
            'etat': 'VIDE',
            'couleur': 'red',
            'description': 'Bassin presque vide',
            'couverture': couverture,
            'action': 'Ajouter de l Azolla ou verifier le systeme'
        }


def diagnostiquer_sante(comptage):
    """
    La plante est saine ou malade ?
    Regarde le pourcentage de zones malades par rapport a la plante
    """
    ratio = comptage['ratio_malade']
    pct_chlorose = comptage.get('chlorose', {}).get('pourcentage', 0)
    pct_necrose = comptage.get('necrose', {}).get('pourcentage', 0)
    pct_rouge = comptage.get('rouge', {}).get('pourcentage', 0)

    # Liste des problemes detectes
    details = []
    if pct_chlorose > 2:
        details.append(f"Chlorose (jaunissement) : {pct_chlorose}%")
    if pct_necrose > 2:
        details.append(f"Necrose (zones marron) : {pct_necrose}%")
    if pct_rouge > 2:
        details.append(f"Taches rouges : {pct_rouge}%")

    if ratio < config.SEUIL_SANTE_SAINE:
        return {
            'etat': 'SAINE',
            'couleur': 'green',
            'description': 'Plante en bonne sante',
            'ratio_malade': ratio,
            'details': details,
            'action': 'Aucune action necessaire'
        }
    elif ratio < config.SEUIL_SANTE_DEBUT:
        return {
            'etat': 'DEBUT MALADIE',
            'couleur': 'orange',
            'description': 'Premiers signes de maladie detectes',
            'ratio_malade': ratio,
            'details': details,
            'action': 'Surveiller de pres, verifier pH et nutriments'
        }
    elif ratio < config.SEUIL_SANTE_MALADE:
        return {
            'etat': 'MALADE',
            'couleur': 'red',
            'description': 'Maladie confirmee, traitement necessaire',
            'ratio_malade': ratio,
            'details': details,
            'action': 'Ajuster nutriments, verifier temperature'
        }
    else:
        return {
            'etat': 'GRAVEMENT MALADE',
            'couleur': 'darkred',
            'description': 'Maladie grave, intervention urgente',
            'ratio_malade': ratio,
            'details': details,
            'action': 'Intervention urgente, isoler les zones malades'
        }


def diagnostic_complet(comptage):
    """
    Fait les 2 diagnostics en meme temps :
    bassin (plein/vide) + sante (saine/malade)
    """
    diag_bassin = diagnostiquer_bassin(comptage)
    diag_sante = diagnostiquer_sante(comptage)

    return {
        'bassin': diag_bassin,
        'sante': diag_sante,
        'resume': {
            'bassin_etat': diag_bassin['etat'],
            'sante_etat': diag_sante['etat'],
            'couverture': diag_bassin['couverture'],
            'ratio_malade': diag_sante['ratio_malade'],
        }
    }


def afficher_diagnostic_console(diagnostic):
    """Affiche le diagnostic dans le terminal"""

    bassin = diagnostic['bassin']
    sante = diagnostic['sante']

    print()
    print("=" * 55)
    print("  DIAGNOSTIC COMPLET")
    print("=" * 55)
    print()
    print("  BASSIN :")
    print(f"    Etat        : {bassin['etat']}")
    print(f"    Couverture  : {bassin['couverture']}%")
    print(f"    Description : {bassin['description']}")
    print(f"    Action      : {bassin['action']}")
    print()
    print("  SANTE :")
    print(f"    Etat        : {sante['etat']}")
    print(f"    Zone malade : {sante['ratio_malade']}%")
    print(f"    Description : {sante['description']}")
    print(f"    Action      : {sante['action']}")

    if sante['details']:
        print()
        print("  DETAILS MALADIE :")
        for detail in sante['details']:
            print(f"    - {detail}")

    print()
    print("=" * 55)