# Importations des modules nécessaires
from tkinter import *
from tkinter import messagebox, ttk, filedialog  # Composants Tkinter supplémentaires
import shutil  # Pour les opérations sur les fichiers
from datetime import datetime  # Pour la gestion des dates
import module.sql as sql  # Module pour les opérations SQL
from module.info_client import fiche_client  # Module pour les fiches clients
import os  # Pour les opérations système

# Définition des couleurs
background_color = '#3CB1E4'  # Couleur de fond
button_bg_color = '#007BFF'  # Couleur de fond des boutons
button_fg_color = 'white'  # Couleur du texte des boutons

def ouvrir_toplevel_marque(accueil_frame):
    """
    Ouvre une fenêtre pour ajouter une nouvelle marque
    """
    # Création de la fenêtre popup
    top_marque = Toplevel(accueil_frame)
    top_marque.title("Ajouter une Marque")
    top_marque.geometry("300x200")
    top_marque.minsize(300, 200)
    top_marque.iconbitmap("IMG/ICONE/logo_sans_fond.ico")  

    # Label pour le nom de la marque
    label_nom = Label(top_marque, text="Nom de la Marque:")
    label_nom.pack(pady=10)

    # Champ de saisie pour le nom de la marque
    entry_nom_marque = Entry(top_marque, width=30)
    entry_nom_marque.pack(pady=5)

    def ajouter_marque():
        """
        Valide et enregistre la nouvelle marque
        """
        nom_marque = entry_nom_marque.get()
        list_marque = sql.get_all_marque()
        
        # Création d'une liste des marques en majuscules pour la comparaison
        list_marque_upper = []
        for marque in list_marque:
            list_marque_upper.append(marque[1].upper())
            
        # Validation des données
        if nom_marque:
            if nom_marque.upper() not in list_marque_upper:
                # Enregistrement en base de données
                if sql.add_marque(nom_marque.upper()):
                    messagebox.showinfo("Succès", "✅ La marque a été ajouté avec succès.")
                    top_marque.destroy()
                else:
                    messagebox.showerror("Erreur", "❌ Échec de la requete sql. Veuillez réessayer.")
            else:
                messagebox.showerror("Erreur", "❌ Marque déjà présent.")
        else:
            messagebox.showerror("Erreur", "❌ Veuillez remplir tout les champs.")  

    # Bouton de validation
    bouton_ajouter = Button(top_marque, text="Ajouter", command=ajouter_marque)
    bouton_ajouter.pack(pady=20)

def ouvrir_toplevel_modele(accueil_frame):
    """
    Ouvre une fenêtre pour ajouter un nouveau modèle
    """
    # Création de la fenêtre popup
    top_modele = Toplevel(accueil_frame)
    top_modele.title("Ajouter un Modèle")
    top_modele.geometry("300x600")
    top_modele.minsize(300, 600)
    top_modele.iconbitmap("IMG/ICONE/logo_sans_fond.ico")  

    # Sélection de la marque
    label_marque = Label(top_modele, text="La marque :")
    label_marque.pack(pady=10)

    # Récupération des marques existantes
    choices_marque = []
    list_marque = sql.get_all_marque()
    for id_marque, marque in list_marque:
        choices_marque.append(f'{id_marque} - {marque}') 

    # Combobox pour choisir la marque
    marque_combobox = ttk.Combobox(top_modele, values=choices_marque, state="readonly", font=("Arial", 12))
    marque_combobox.current(0)  # Sélection par défaut
    marque_combobox.pack(pady=10, padx=10, fill='x')

    # Champ pour le nom du modèle
    label_nom = Label(top_modele, text="Nom du modèle :")
    label_nom.pack(pady=10)

    entry_nom_modele = Entry(top_modele, width=30)
    entry_nom_modele.pack(pady=5)

    # Champ pour la longueur du véhicule
    label_longueur = Label(top_modele, text="Longueur du véhicule :")
    label_longueur.pack(pady=10)

    spinbox_longueur = Spinbox(top_modele, from_=0.0, to=5.0, increment=0.01, width=5, font=("Arial", 12))
    spinbox_longueur.pack(pady=5)

    # Champ pour la largeur du véhicule
    label_largeur = Label(top_modele, text="Largeur du véhicule :")
    label_largeur.pack(pady=10)

    spinbox_largeur = Spinbox(top_modele, from_=0.0, to=5.0, increment=0.01, width=5, font=("Arial", 12))
    spinbox_largeur.pack(pady=5)

    # Champ pour la hauteur du véhicule
    label_hauteur = Label(top_modele, text="Hauteur du véhicule :")
    label_hauteur.pack(pady=10)

    spinbox_hauteur = Spinbox(top_modele, from_=0.0, to=5.0, increment=0.01, width=5, font=("Arial", 12))
    spinbox_hauteur.pack(pady=5)

    def ajouter_marque():
        """
        Valide et enregistre le nouveau modèle
        """
        # Récupération des valeurs
        nom_modele = entry_nom_modele.get()
        longueur = spinbox_longueur.get()
        largeur = spinbox_largeur.get()
        hauteur = spinbox_hauteur.get()
        id_marque = marque_combobox.get().split(" - ")[0]  # Extraction de l'ID
        
        # Vérification de l'unicité du modèle
        list_modele = sql.get_all_modele_by_marque(id_marque)
        list_modele_lower = []
        for modele in list_modele:
            list_modele_lower.append(modele[1].lower())
            
        # Validation des données
        if nom_modele and longueur and largeur and hauteur:
            if nom_modele.lower() not in list_modele_lower:
                # Enregistrement en base de données
                if sql.add_modele(nom_modele.capitalize(), id_marque, longueur, largeur, hauteur):
                    messagebox.showinfo("Succès", "✅ Le modèle a été ajouté avec succès.")
                    top_modele.destroy()
                else:
                    messagebox.showerror("Erreur", "❌ Échec de la requete sql. Veuillez réessayer.")
            else:
                messagebox.showerror("Erreur", "❌ Modèle déjà présent.")
        else:
            messagebox.showerror("Erreur", "❌ Veuillez remplir tout les champs.") 

    # Bouton de validation
    bouton_ajouter = Button(top_modele, text="Ajouter", command=ajouter_marque)
    bouton_ajouter.pack(pady=20)

def ouvrir_toplevel_photos(frame, id_entreprise):
    """
    Ouvre une fenêtre pour ajouter des photos aux rendez-vous
    Args:
        frame (Frame): Le frame parent
        id_entreprise (int): ID de l'entreprise
    """
    # Création de la fenêtre popup
    top_photos = Toplevel(frame)
    top_photos.title("Ajouter des Photos")
    top_photos.geometry("800x600")
    top_photos.iconbitmap("IMG/ICONE/logo_sans_fond.ico")  

    # Récupération des rendez-vous de l'entreprise
    list_rdv = sql.get_rdv_ie(id_entreprise)
    # Tri des rendez-vous par date (du plus récent)
    list_rdv.sort(key=lambda x: x[3], reverse=True)

    # Frame pour la recherche
    search_frame = Frame(top_photos, bg='white')
    search_frame.pack(pady=10)  

    # Label et champ de recherche
    search_label = Label(search_frame, text="Recherchez par véhicule ou par date : ", 
                        font=("Arial", 12), bg='white')
    search_label.pack(side="left", padx=5) 

    search_entry = Entry(search_frame, font=("Arial", 12), width=30)  
    search_entry.pack(side="left", padx=5)  

    # Configuration du système de défilement
    canvas_frame = Frame(top_photos, bg="white")
    canvas_frame.pack(pady=10, fill="both", expand=True) 

    canvas = Canvas(canvas_frame, bg="#B2CCE4") 
    scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview) 
    scrollable_frame = Frame(canvas, bg="#B2CCE4") 

    canvas.configure(yscrollcommand=scrollbar.set)  
    scrollbar.pack(side="right", fill="y")  
    canvas.pack(side="left", fill="both", expand=True) 
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  

    # Gestion du redimensionnement
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  
    canvas.bind("<Configure>", lambda e: canvas.itemconfig("all", width=canvas.winfo_width())) 

    # Gestion de la molette de la souris
    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")  
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel)) 
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>")) 

    def update_results():
        """
        Met à jour les résultats affichés en fonction de la recherche
        """
        # Nettoyage des anciens résultats
        for widget in scrollable_frame.winfo_children():
            widget.destroy()  

        search_text = search_entry.get().lower()  
        
        if list_rdv: 
            # Filtrage des rendez-vous
            filtered_rdv = [
                rdv for rdv in list_rdv
                if (search_text in rdv[3].lower() or  # Date
                    search_text in rdv[9].lower() or  # Marque du véhicule
                    search_text in rdv[10].lower())   # Modèle du véhicule
            ] 
            
            # Affichage des rendez-vous filtrés
            for rdv in filtered_rdv:
                # Formatage des informations du rendez-vous
                rdv_text = (
                    f"ID: {rdv[0]}\n"
                    f"Client ID: {rdv[1]}\n"
                    f"Entreprise ID: {rdv[2]}\n"
                    f"Date: {rdv[3]} à {rdv[4]}\n"
                    f"Statut: {rdv[5]}\n"
                    f"Adresse: {rdv[6]} {rdv[7]} {rdv[8]}\n"
                    f"Véhicule: {rdv[9]} {rdv[10]} {rdv[11]}. Places\n"
                    f"Forfait: {rdv[12]}\n"
                    f"Prix: {rdv[13]} €\n"
                    f"Remarque: {rdv[14]}"
                )  

                # Création d'un frame pour chaque rendez-vous
                rdv_frame = Frame(scrollable_frame, bg="white", borderwidth=1, relief="solid")  
                rdv_frame.pack(fill="x", padx=10, pady=5) 

                # Affichage des infos du rendez-vous
                rdv_label = Label(rdv_frame, text=rdv_text, font=("Arial", 12), 
                                bg="white", anchor="w", justify="left")  
                rdv_label.pack(fill="x", padx=10, pady=5) 

                # Frame pour les boutons d'action
                button_frame = Frame(rdv_frame, bg="white") 
                button_frame.pack(pady=5)  

                # Bouton Fiche client
                client_button = Button(button_frame, text="Fiche client", bg="#5A9BD5", fg="white", 
                                     activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                     command=lambda frame=frame, id_client=rdv[1], id_entreprise=id_entreprise:
                                     fiche_client(frame, id_client, id_entreprise))  
                client_button.grid(row=0, column=0, padx=5)

                # Bouton Ajouter photo
                photo_button = Button(button_frame, text="Ajouter une image", bg="#5A9BD5", fg="white", 
                                    activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                    command=lambda date=rdv[3], id_rdv=rdv[0]: ajout_photo(date, id_rdv))  
                photo_button.grid(row=0, column=0, padx=5) 

        else: 
            # Message si aucun résultat
            no_results_label = Label(scrollable_frame, text="Aucun résultat trouvé.", 
                                   font=("Arial", 12, "italic"), bg="white", fg="gray")  
            no_results_label.pack(pady=10)  

    # Liaison de la recherche à la mise à jour des résultats
    search_entry.bind("<KeyRelease>", lambda event: update_results())  
    update_results()  # Affichage initial

def ajout_photo(date, id_rdv):
    """
    Ajoute des photos à un rendez-vous spécifique
    Args:
        date (str): Date du rendez-vous
        id_rdv (int): ID du rendez-vous
    """
    # Création du chemin pour stocker les photos
    chemin_photo = f'IMG_RDV/{date}_{id_rdv}'
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    chemin = os.path.join(chemin_actuel, chemin_photo)

    # Création du dossier s'il n'existe pas
    if not os.path.exists(chemin):
        os.makedirs(chemin)

    # Sélection des images
    chemins_images = filedialog.askopenfilenames(
        title="Sélectionner des images",
        filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )

    if chemins_images:
        erreurs = []
        # Copie des images sélectionnées
        for idx, chemin_image in enumerate(chemins_images):
            try:
                extension = os.path.splitext(chemin_image)[1]
                # Nom du fichier avec format: date_idrdv_numeroX.extension
                nom_fichier_renomme = f"{date}_{id_rdv}_numero {idx+1}{extension}"
                chemin_destination = os.path.join(chemin, nom_fichier_renomme)

                # Copie du fichier
                shutil.copy(chemin_image, chemin_destination)

                # Vérification de la copie
                if not os.path.exists(chemin_destination) or not os.path.isfile(chemin_destination):
                    erreurs.append(nom_fichier_renomme)
            except Exception as e:
                erreurs.append(f"{nom_fichier_renomme} (erreur : {str(e)})")

        # Affichage des erreurs éventuelles
        if erreurs:
            messagebox.showerror("Erreur de copie", 
                               "Les fichiers suivants n'ont pas pu être copiés :\n" + "\n".join(erreurs))
        else:
            messagebox.showinfo("Succès", "Toutes les images ont été copiées avec succès.")
    else:
        messagebox.showerror("Aucune sélection", "Vous n'avez sélectionné aucune image.")

def ouvrir_toplevel_factures(parent):
    """
    Ouvre une fenêtre pour gérer les factures (version simplifiée)
    Args:
        parent (Widget): Le widget parent
    """
    top_factures = Toplevel(parent)
    top_factures.title("Ajouter une Facture")
    top_factures.geometry("300x200")
    top_factures.iconbitmap("IMG/ICONE/logo_sans_fond.ico") 
    label_facture = Label(top_factures, text="Interface pour ajouter une facture à venir")
    label_facture.pack(pady=50)

def style_button(button):
    """
    Applique un style uniforme aux boutons
    Args:
        button (Button): Le bouton à styliser
    """
    button.config(
        bg=button_bg_color,
        fg=button_fg_color,
        font=('Arial', 12, 'bold'),
        relief='flat',
        width=20,
        height=2
    )

def page_accueil(frame, id_entreprise):
    """
    Affiche la page d'accueil principale
    Args:
        frame (Frame): Le frame parent
        id_entreprise (int): ID de l'entreprise
    """
    # Configuration du frame principal
    accueil_frame = Frame(frame)
    accueil_frame.config(bg=background_color)

    # Configuration de la grille
    accueil_frame.columnconfigure(0, weight=1)
    accueil_frame.columnconfigure(1, weight=1) 

    # Récupération des informations de l'entreprise
    denomination = sql.get_denomination(id_entreprise)
    denomination_separer = denomination.split("|")
    dirigeant = denomination_separer[0]
    nom_entreprise = denomination_separer[1]

    # Message de bienvenue
    message_bienvenue = f"Bonjour {dirigeant}bienvenue sur la gestion de{nom_entreprise} !"
    bienvenue_label = Label(accueil_frame, text=message_bienvenue, 
                          font=('Bold', 20), bg=background_color)
    bienvenue_label.grid(column=0, row=1, columnspan=2, pady=10)  

    # Affichage de la date actuelle
    date_actuelle = datetime.today().date()
    message_date = f"Nous sommes le {date_actuelle}."
    date_label = Label(accueil_frame, text=message_date, 
                      font=('Bold', 18), bg=background_color)
    date_label.grid(column=0, row=2, columnspan=2, pady=10)

    # Bouton Ajouter Marque
    bouton_ajouter_marque = Button(accueil_frame, text="Ajouter Marque", 
                                  command=lambda: ouvrir_toplevel_marque(accueil_frame))
    style_button(bouton_ajouter_marque)
    bouton_ajouter_marque.grid(column=0, row=3, pady=20)

    # Bouton Ajouter Modèle
    bouton_ajouter_modele = Button(accueil_frame, text="Ajouter Modèle", 
                                  command=lambda: ouvrir_toplevel_modele(accueil_frame))
    style_button(bouton_ajouter_modele)
    bouton_ajouter_modele.grid(column=1, row=3, pady=20)

    # Bouton Ajouter Photos
    bouton_ajouter_photos = Button(accueil_frame, text="Ajouter Photos", 
                                  command=lambda: ouvrir_toplevel_photos(accueil_frame, id_entreprise))
    style_button(bouton_ajouter_photos)
    bouton_ajouter_photos.grid(column=0, row=4, pady=20)

    # Bouton Ajouter Facture (version simplifiée)
    bouton_ajouter_factures = Button(accueil_frame, text="Ajouter Facture", 
                                    command=lambda: ouvrir_toplevel_factures(accueil_frame))
    style_button(bouton_ajouter_factures)
    bouton_ajouter_factures.grid(column=1, row=4, pady=20)

    # Placement final du frame
    accueil_frame.grid(sticky="nsew")  
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)