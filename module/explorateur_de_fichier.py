# Importation des modules nécessaires
from tkinter import *  
from tkinter import ttk, messagebox  
import os  # Module pour interagir avec le système d'exploitation

# Définition du dossier de base où seront stockées les factures
DOSSIER_BASE = os.getcwd()  # Obtient le dossier courant
DOSSIER_BASE = DOSSIER_BASE + "/factures"  # Ajoute un sous-dossier "factures"
dossier_actuel = DOSSIER_BASE  # Variable qui stocke le dossier actuellement affiché
arbre_fichiers = None  # Variable qui contiendra l'arbre d'affichage des fichiers

def configurer_interface(root):
    global arbre_fichiers  # On utilise la variable globale arbre_fichiers
   
    # Création d'un Treeview (arbre) avec 2 colonnes : Nom et Type
    arbre_fichiers = ttk.Treeview(root, columns=("Nom", "Type"), show="headings")
    arbre_fichiers.heading("Nom", text="Nom")  # En-tête de la colonne Nom
    arbre_fichiers.heading("Type", text="Type")  # En-tête de la colonne Type
    arbre_fichiers.pack(fill=BOTH, expand=True, padx=10, pady=5)  # Placement du widget
   
    # Création d'un bouton "Ouvrir" qui appelle la fonction gerer_ouverture
    bouton_ouvrir = Button(root, text="Ouvrir", command=gerer_ouverture)
    bouton_ouvrir.pack(pady=10)  # Placement du bouton
   
    # Liaison du double-clic sur l'arbre à la fonction gerer_ouverture
    arbre_fichiers.bind("<Double-1>", lambda e: gerer_ouverture())

def actualiser_affichage():
    global dossier_actuel, arbre_fichiers  # Variables globales utilisées
   
    # Efface tous les éléments actuels de l'arbre
    arbre_fichiers.delete(*arbre_fichiers.get_children())
   
    # Si on n'est pas à la racine, on ajoute un élément ".." pour remonter
    if dossier_actuel != DOSSIER_BASE:
        arbre_fichiers.insert("", "end", values=("..", "Dossier"))
   
    try:
        # Parcours de tous les éléments du dossier actuel
        for element in os.listdir(dossier_actuel):
            chemin = os.path.join(dossier_actuel, element)  # Crée le chemin complet
            if os.path.isdir(chemin):
                # Si c'est un dossier, on l'ajoute à l'arbre
                arbre_fichiers.insert("", "end", values=(element, "Dossier"))
            else:
                # Si c'est un fichier, on l'ajoute à l'arbre
                arbre_fichiers.insert("", "end", values=(element, "Fichier"))
    except Exception:
        # En cas d'erreur (dossier non accessible)
        messagebox.showerror("Erreur", "Accès refusé")

def gerer_ouverture():
    global dossier_actuel, arbre_fichiers  # Variables globales utilisées
   
    # Récupère la sélection actuelle dans l'arbre
    selection = arbre_fichiers.selection()
    if not selection:  # Si rien n'est sélectionné, on ne fait rien
        return
   
    # Récupère le nom et le type de l'élément sélectionné
    nom, typ = arbre_fichiers.item(selection, "values")
    chemin = os.path.join(dossier_actuel, nom)  # Crée le chemin complet
   
    if nom == "..":  # Si on a cliqué sur ".."
        dossier_actuel = os.path.dirname(dossier_actuel)  # Remonte d'un niveau
    elif typ == "Dossier":  # Si c'est un dossier
        dossier_actuel = chemin  # Change le dossier actuel
    else:  # Si c'est un fichier
        ouvrir_fichier(chemin)  # Ouvre le fichier
        return  # On ne rafraîchit pas l'affichage
   
    actualiser_affichage()  # Met à jour l'affichage après changement

def ouvrir_fichier(chemin):
    try:
        if os.name == 'nt':  # Si le système est Windows
            os.startfile(chemin)  # Ouvre le fichier avec l'application par défaut
        else:  # Pour Linux/Mac
            os.system(f'xdg-open "{chemin}"')  # Ouvre le fichier avec xdg-open
    except Exception:  # En cas d'erreur
        messagebox.showerror("Erreur", "Ouverture impossible")  # Affiche un message d'erreur

def demarrer_explorateur(root):
    # Fonction principale qui configure l'interface et affiche le contenu initial
    configurer_interface(root)
    actualiser_affichage()