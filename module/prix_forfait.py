"""
Ce module effectue des calculs de prix pour différents forfaits de nettoyage de véhicules.
Il utilise une méthode d'arrondi spécifique pour correspondre au comportement de PHP dans le but d'avoir le même le resultat que sur un site web que j'ai développé.
"""

# Importation des modules nécessaires
from sqlite3 import *  
import math  

# Connexion à la base de données
conn = connect('DB/CleanWay.db')  # Ouvre la connexion à la DB
cur = conn.cursor()  # Crée un curseur pour exécuter des requêtes

def round_php(val, digits):
    """
    Imite le comportement de la fonction round() de PHP
    """
    factor = 10 ** abs(digits)  # Calcule le facteur de multiplication
    return math.floor(val / factor + 0.5) * factor  # Arrondi spécifique PHP

def calcul_prix(id_modele, nbre_siege, forfait):
    """
    Calcule le prix d'un forfait de nettoyage en fonction du modèle et du nombre de sièges
    """
   
    # Liste des forfaits disponibles
    liste_forfait = ["Forfait Complet", "Forfait Intérieur", "Forfait Extérieur"]
   
    # Vérification de la validité du forfait
    if forfait not in liste_forfait:
        raise ValueError(f"Le forfait '{forfait}' n'est pas valide. Valeurs autorisées : {liste_forfait}")

    try:
        # Récupération des dimensions du véhicule depuis la base de données
        cur.execute("SELECT Longueur, Largeur, Hauteur FROM Modele WHERE ID_Modele = ?", (id_modele,))
        taille = cur.fetchone()  # Récupère le premier résultat

        if taille:  # Si le modèle existe dans la DB
            longueur, largeur, hauteur = taille  # Dépaquete les dimensions

            # Calcul de base pour le forfait complet
            forfait_comp = 1.2 * longueur * largeur * hauteur * nbre_siege

            # Coefficients initiaux pour les sous-forfaits
            coef_interieur = 0.6  # 60% du prix complet
            coef_exterieur = 0.4  # 40% du prix complet
            seuil = 50  # Seuil pour ajustement des coefficients

            # Ajustement des coefficients si prix complet < seuil
            if forfait_comp < seuil:
                coef_interieur = 0.65  # Augmente la part intérieure
                coef_exterieur = 0.45  # Augmente la part extérieure

            # Calcul des sous-forfaits
            forfait_int = coef_interieur * forfait_comp  # Forfait intérieur
            forfait_ext = coef_exterieur * forfait_comp  # Forfait extérieur

            # Définition des seuils min/max en fonction du nombre de sièges
            if nbre_siege <= 7:  # Petits véhicules
                seuil_min_Complet, seuil_max_Complet = 50, 100
                seuil_min_Interieur, seuil_max_Interieur = 35, 70
                seuil_min_Exterieur, seuil_max_Exterieur = 20, 40
            elif 8 <= nbre_siege <= 10:  # Véhicules moyens
                seuil_min_Complet, seuil_max_Complet = 75, 150
                seuil_min_Interieur, seuil_max_Interieur = 50, 105
                seuil_min_Exterieur, seuil_max_Exterieur = 50, 70
            else:  # Gros véhicules
                seuil_min_Complet, seuil_max_Complet = 95, 195  
                seuil_min_Interieur, seuil_max_Interieur = 65, 130
                seuil_min_Exterieur, seuil_max_Exterieur = 60, 90

            # Application des seuils min/max
            forfait_comp = max(min(forfait_comp, seuil_max_Complet), seuil_min_Complet)
            forfait_int = max(min(forfait_int, seuil_max_Interieur), seuil_min_Interieur)
            forfait_ext = max(min(forfait_ext, seuil_max_Exterieur), seuil_min_Exterieur)

            # Arrondis spécifiques
            forfait_comp = math.floor(forfait_comp / 10) * 10  # Arrondi à la dizaine inférieure
            forfait_int = round_php(forfait_int, -1)  # Arrondi PHP à la dizaine
            forfait_ext = round_php(forfait_ext, -1)  # Arrondi PHP à la dizaine

            # Ajustement si la somme des sous-forfaits égale le forfait complet
            if forfait_comp == forfait_ext + forfait_int:
                forfait_int += 5  # Petite augmentation pour différencier
                forfait_ext += 5

            # Retourne le prix selon le forfait demandé
            if forfait == "Forfait Complet":
                return forfait_comp
            elif forfait == "Forfait Intérieur":
                return forfait_int
            elif forfait == "Forfait Extérieur":
                return forfait_ext

    except OperationalError as e:
        # Gestion des erreurs de base de données
        print(f'Erreur SQL calcul_prix : {e}')