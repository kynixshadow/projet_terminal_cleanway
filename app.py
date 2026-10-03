# Importation des modules nécessaires
from tkinter import *
import accueil  # Module pour la page d'accueil
import client  # Module pour la gestion des clients
import compta  # Module pour la comptabilité
import para  # Module pour les paramètres
import rdv  # Module pour les rendez-vous

def main(id):
    """
    Fonction principale qui crée la fenêtre principale de l'application
    """
    # Création de la fenêtre principale
    root = Tk()
    root.title("CleanWay")  
    root.geometry("1150x650") 
    root.minsize(1150, 650)  
    root.iconbitmap("IMG/ICONE/logo_sans_fond.ico")  

    # Couleur de la barre de menu
    menu_bar_color = '#2C3E50'  
    id_entreprise = id

    # Chargement des icônes
    icone_menu_1 = PhotoImage(file='IMG/ICONE/menu_btn_icone_1.png')  # Icône menu fermé
    icone_menu_2 = PhotoImage(file='IMG/ICONE/menu_btn_icone_2.png')  # Icône menu ouvert
    icone_accueil = PhotoImage(file='IMG/ICONE/accueil_icone.png')  # Icône accueil
    icone_client = PhotoImage(file='IMG/ICONE/client_icone.png')  # Icône client
    icone_compta = PhotoImage(file='IMG/ICONE/compta_icone.png')  # Icône comptabilité
    icone_rdv = PhotoImage(file='IMG/ICONE/rdv_icone.png')  # Icône rendez-vous
    icone_para = PhotoImage(file='IMG/ICONE/paramettre_icone.png')  # Icône paramètres

    def switch_indication(label_indicateur, page):
        """
        Change l'indicateur de page active et affiche la page correspondante
        """
        # Réinitialisation des couleurs des indicateurs
        bouton_accueil_indicateur.config(bg=menu_bar_color)
        bouton_client_indicateur.config(bg=menu_bar_color)
        bouton_compta_indicateur.config(bg=menu_bar_color)
        bouton_para_indicateur.config(bg=menu_bar_color)
        bouton_rdv_indicateur.config(bg=menu_bar_color)
        
        # Mise en surbrillance de l'indicateur actif
        label_indicateur.config(bg='white')  

        # Fermeture du menu si ouvert
        if menu_bar_frame.winfo_width() > 50:  
            menu_fermer()

        # Nettoyage de la frame de contenu
        for frame in page_frame.winfo_children():
            frame.destroy()

        # Affichage de la nouvelle page
        page() 

    def ouvrir_animation():
        """Animation d'ouverture du menu"""
        taille_actuelle = menu_bar_frame.winfo_width() 
        if not taille_actuelle > 190: 
            taille_actuelle += 10  
            menu_bar_frame.config(width=taille_actuelle)  
            root.after(ms=10, func=ouvrir_animation)  # Rappel récursif pour l'animation

    def fermer_animation():
        """Animation de fermeture du menu"""
        taille_actuelle = menu_bar_frame.winfo_width()  
        if not taille_actuelle <= 50: 
            taille_actuelle -= 10 
            menu_bar_frame.config(width=taille_actuelle) 
            root.after(ms=10, func=fermer_animation)  # Rappel récursif pour l'animation

    def menu_ouvrir():
        """Ouvre le menu avec animation"""
        ouvrir_animation() 
        bouton_menu.config(image=icone_menu_2, command=menu_fermer) 

    def menu_fermer():
        """Ferme le menu avec animation"""
        fermer_animation()  
        bouton_menu.config(image=icone_menu_1, command=menu_ouvrir)  

    # Frame pour le contenu principal
    page_frame = Frame(root, bg='black') 
    page_frame.place(relwidth=0.955, relheight=1.0, x=50)  

    # Frame pour la barre de menu
    menu_bar_frame = Frame(root, bg=menu_bar_color, pady=4, padx=3) 

    # Bouton pour ouvrir/fermer le menu
    bouton_menu = Button(menu_bar_frame, image=icone_menu_1, bg=menu_bar_color, 
                        bd=0, activebackground=menu_bar_color, command=menu_ouvrir)
    bouton_menu.place(x=4, y=10) 

    # Titre de l'application dans le menu
    menu_label = Label(menu_bar_frame, text="CleanWay", bg=menu_bar_color, 
                      fg='white', font=('Bold', 18), anchor=W)
    menu_label.place(x=50, y=8, width=120, height=40)  

    # Création des indicateurs de page active
    bouton_accueil_indicateur = Label(menu_bar_frame, bg=menu_bar_color)  
    bouton_client_indicateur = Label(menu_bar_frame, bg=menu_bar_color) 
    bouton_compta_indicateur = Label(menu_bar_frame, bg=menu_bar_color)
    bouton_rdv_indicateur = Label(menu_bar_frame, bg=menu_bar_color)
    bouton_para_indicateur = Label(menu_bar_frame, bg=menu_bar_color)

    # Bouton et label pour l'accueil
    bouton_accueil = Button(menu_bar_frame, image=icone_accueil, bg=menu_bar_color, 
                           bd=0, activebackground=menu_bar_color, 
                           command=lambda: switch_indication(
                               label_indicateur=bouton_accueil_indicateur, 
                               page=lambda: accueil.page_accueil(page_frame, id)))
    bouton_accueil.place(x=9, y=130, width=30, height=40)  
    bouton_accueil_indicateur.place(x=1, y=130, height=40, width=3)  

    accueil_label = Label(menu_bar_frame, text="Accueil", bg=menu_bar_color, 
                         fg='white', font=('Bold', 15), anchor=W)
    accueil_label.place(x=50, y=130, width=120, height=40)  
    accueil_label.bind('<Button-1>', 
                      lambda e: switch_indication(
                          label_indicateur=bouton_accueil_indicateur, 
                          page=lambda: accueil.page_accueil(page_frame, id))) 

    # Bouton et label pour les clients
    bouton_client = Button(menu_bar_frame, image=icone_client, bg=menu_bar_color, 
                          bd=0, activebackground=menu_bar_color, 
                          command=lambda: switch_indication(
                              label_indicateur=bouton_client_indicateur, 
                              page=lambda: client.page_client(page_frame, id)))
    bouton_client.place(x=9, y=190, width=30, height=40)  
    bouton_client_indicateur.place(x=1, y=190, height=40, width=3)  

    client_label = Label(menu_bar_frame, text="Client", bg=menu_bar_color, 
                        fg='white', font=('Bold', 15), anchor=W)
    client_label.place(x=50, y=190, width=120, height=40)  
    client_label.bind('<Button-1>', 
                     lambda e: switch_indication(
                         label_indicateur=bouton_client_indicateur, 
                         page=lambda: client.page_client(page_frame, id)))  

    # Bouton et label pour la comptabilité
    bouton_compta = Button(menu_bar_frame, image=icone_compta, bg=menu_bar_color, 
                          bd=0, activebackground=menu_bar_color, 
                          command=lambda: switch_indication(
                              label_indicateur=bouton_compta_indicateur, 
                              page=lambda: compta.page_compta(page_frame, id)))
    bouton_compta.place(x=9, y=250, width=30, height=40)  
    bouton_compta_indicateur.place(x=1, y=250, height=40, width=3) 

    compta_label = Label(menu_bar_frame, text="Comptabilité", bg=menu_bar_color, 
                        fg='white', font=('Bold', 15), anchor=W)
    compta_label.place(x=50, y=250, width=120, height=40)  
    compta_label.bind('<Button-1>', 
                     lambda e: switch_indication(
                         label_indicateur=bouton_compta_indicateur, 
                         page=lambda: compta.page_compta(page_frame, id)))  

    # Bouton et label pour les rendez-vous
    bouton_rdv = Button(menu_bar_frame, image=icone_rdv, bg=menu_bar_color, 
                       bd=0, activebackground=menu_bar_color, 
                       command=lambda: switch_indication(
                           label_indicateur=bouton_rdv_indicateur, 
                           page=lambda: rdv.page_rdv(page_frame, id)))
    bouton_rdv.place(x=9, y=310, width=30, height=40)  
    bouton_rdv_indicateur.place(x=1, y=310, height=40, width=3)  

    rdv_label = Label(menu_bar_frame, text="Rendez-vous", bg=menu_bar_color, 
                     fg='white', font=('Bold', 15), anchor=W)
    rdv_label.place(x=50, y=310, width=120, height=40)  
    rdv_label.bind('<Button-1>', 
                  lambda e: switch_indication(
                      label_indicateur=bouton_rdv_indicateur, 
                      page=lambda: rdv.page_rdv(page_frame, id)))  

    # Bouton et label pour les paramètres
    bouton_para = Button(menu_bar_frame, image=icone_para, bg=menu_bar_color, 
                        bd=0, activebackground=menu_bar_color, 
                        command=lambda: switch_indication(
                            label_indicateur=bouton_para_indicateur, 
                            page=lambda: para.page_para(page_frame, id)))
    bouton_para.place(x=9, y=370, width=30, height=40)  
    bouton_para_indicateur.place(x=1, y=370, height=40, width=3) 

    para_label = Label(menu_bar_frame, text="Paramètres", bg=menu_bar_color, 
                      fg='white', font=('Bold', 15), anchor=W)
    para_label.place(x=50, y=370, width=120, height=40)  
    para_label.bind('<Button-1>', 
                   lambda e: switch_indication(
                       label_indicateur=bouton_para_indicateur, 
                       page=lambda: para.page_para(page_frame, id)))  

    # Placement de la barre de menu
    menu_bar_frame.pack(side=LEFT, fill=Y)
    menu_bar_frame.pack_propagate(flag=False)  # Empêche le redimensionnement automatique

    # Affichage de la page d'accueil par défaut
    accueil.page_accueil(page_frame, id)
    bouton_accueil_indicateur.config(bg="white")


    # Initialisation du menu en position fermée
    menu_bar_frame.config(width=50)

    # Lancement de la boucle principale
    root.mainloop()