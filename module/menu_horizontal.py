# Importation du module Tkinter pour l'interface graphique
from tkinter import *

# Classe pour créer un menu responsive qui s'adapte à la taille de la fenêtre
class ResponsiveMenu:
    def __init__(self, root, foreground_color='white', background_color='black'):
        # Initialisation avec la fenêtre principale et les couleurs
        self.root = root  # Fenêtre parente
        self.foreground_color = foreground_color  # Couleur du texte
        self.background_color = background_color  # Couleur de fond

        # Création du cadre horizontal pour le menu
        self.menu_horizontal = Frame(self.root, bg=self.background_color)
        self.menu_horizontal.pack(pady=5, fill=X)  # Placement avec remplissage horizontal
        self.menu_horizontal.pack_propagate(False)  # Empêche le redimensionnement automatique
        self.menu_horizontal.config(height=40)  # Hauteur fixe du menu

        # Listes pour stocker les boutons et leurs indicateurs
        self.boutons = []
        self.indicateurs_liste = []

        # Liaison de l'événement de redimensionnement de la fenêtre
        self.root.bind('<Configure>', lambda event: self.update_menu())

    def ajout_bouton(self, label, command):
        """
        Ajoute un bouton au menu avec un indicateur visuel
        label: texte du bouton
        command: fonction à exécuter lors du clic
        """
        # Couleur de l'indicateur (blanc pour le premier bouton, noir pour les autres)
        couleur_indicateur = self.foreground_color if not self.boutons else self.background_color
       
        # Création de l'indicateur (petite barre sous le bouton)
        indicateur = Label(self.menu_horizontal, bg=couleur_indicateur)

        # Création du bouton avec ses propriétés
        btn = Button(
            self.menu_horizontal,
            text=label,
            font=('Arial', 13),  # Police et taille
            bd=0,  # Pas de bordure
            bg=self.background_color,  # Couleur de fond
            activebackground=self.background_color,  # Couleur quand cliqué
            fg=self.foreground_color,  # Couleur du texte
            activeforeground=self.foreground_color,  # Couleur du texte quand cliqué
            command=lambda: self.switch_indicateur(indicateur, command))  # Action au clic

        # Ajout aux listes
        self.boutons.append(btn)
        self.indicateurs_liste.append(indicateur)
       
        # Mise à jour de l'affichage
        self.update_menu()

    def switch_indicateur(self, indicateur_actif, page_command):
        """
        Change l'indicateur visuel et exécute la commande associée
        indicateur_actif: l'indicateur à mettre en avant
        page_command: fonction à exécuter
        """
        # Réinitialise tous les indicateurs
        for indicateur in self.indicateurs_liste:
            indicateur.config(bg=self.background_color)
       
        # Met en avant l'indicateur actif
        indicateur_actif.config(bg=self.foreground_color)
       
        # Exécute la fonction associée au bouton
        page_command()

    def update_menu(self):
        """
        Met à jour la disposition des boutons en fonction de la taille de la fenêtre
        """
        if not self.boutons:  # Si aucun bouton, on ne fait rien
            return

        # Calcul des dimensions
        total_buttons = len(self.boutons)  # Nombre total de boutons
        width = self.root.winfo_width()  # Largeur actuelle de la fenêtre
        bouton_width = width // total_buttons  # Largeur de chaque bouton

        # Placement de chaque bouton et indicateur
        for i, (btn, indicator) in enumerate(zip(self.boutons, self.indicateurs_liste)):
            x_position = i * bouton_width  # Position horizontale
           
            # Configuration du bouton
            btn.place(x=x_position, y=0, width=bouton_width, height=35)
           
            # Configuration de l'indicateur (légèrement plus petit que le bouton)
            indicator.place(x=x_position + 10, y=35, width=bouton_width - 20, height=3)