# Importations des modules nécessaires
from tkinter import *
from module.menu_horizontal import ResponsiveMenu  # Menu personnalisé
import module.sql as sql  # Module pour les opérations SQL
import module.info_client as info_client  # Module pour les fiches clients
from tkinter import messagebox
import re  # Pour les expressions régulières

# Définition des couleurs
background_color = '#3CB1E4'
background_color_menu = '#1767AA'

# Variable globale (à éviter normalement)
id_entreprise = 1

def page_client(root_frame, id_entreprise):
    """
    Crée la page principale de gestion des clients
    """
    # Création du frame principal
    client_frame = Frame(root_frame, bg='white')
    client_frame.pack(fill=BOTH, expand=True, side=TOP)

    # Frame pour le menu
    menu_frame = Frame(client_frame, bg=background_color_menu)
    menu_frame.pack(side=TOP, fill=X)

    # Frame pour le contenu
    content_frame = Frame(client_frame, bg=background_color)
    content_frame.pack(fill=BOTH, expand=True)

    # Création du menu horizontal
    menu = ResponsiveMenu(menu_frame, foreground_color='white', background_color=background_color_menu)
    menu.ajout_bouton("Liste Client", lambda: liste_client(content_frame, id_entreprise))
    menu.ajout_bouton("Ajouter Client", lambda: ajout_client(content_frame, id_entreprise))

    # Affichage par défaut de la liste des clients
    liste_client(content_frame, id_entreprise)

def liste_client(frame, id_entreprise):
    """
    Affiche la liste des clients
    """
    recup_client(frame, 'Liste', id_entreprise)

def ajout_client(frame, id_entreprise):
    """
    Affiche le formulaire d'ajout d'un client
    """
    # Nettoyage du frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Titre de la page
    Titre_ajout = Label(frame, text="Ajouter un Client", fg='#2C3E50', bg='#3CB1E4', font=('Bold', 18))
    Titre_ajout.pack(pady=20)

    # Configuration du système de défilement
    canvas_frame = Frame(frame, bg="#F0F0F0")
    canvas_frame.pack(pady=10, fill="both", expand=True)

    canvas = Canvas(canvas_frame, bg="#F0F0F0")
    scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#F0F0F0")

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

    # Champ Nom
    text_nom = Label(scrollable_frame, text="Nom :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    text_nom.pack(pady=10, padx=10, anchor="w")

    nom_entry = Entry(scrollable_frame, font=("Arial", 12), width=30)
    nom_entry.pack(pady=5, padx=10, fill='x')

    # Champ Prénom
    text_prenom = Label(scrollable_frame, text="Prénom :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    text_prenom.pack(pady=10, padx=10, anchor="w")

    prenom_entry = Entry(scrollable_frame, font=("Arial", 12), width=30)
    prenom_entry.pack(pady=5, padx=10, fill='x')

    # Champ Téléphone
    text_telephone = Label(scrollable_frame, text="Téléphone :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    text_telephone.pack(pady=10, padx=10, anchor="w")

    telephone_entry = Entry(scrollable_frame, font=("Arial", 12), width=30)
    telephone_entry.pack(pady=5, padx=10, fill='x')

    # Champ Adresse
    text_adresse = Label(scrollable_frame, text="Adresse :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    text_adresse.pack(pady=10, padx=10, anchor="w")

    frame_adresse = Frame(scrollable_frame, bg="#F0F0F0")
    frame_adresse.pack(pady=5, padx=10, anchor="w", fill="x")

    # Numéro de rue
    adresse_numero = Spinbox(frame_adresse, from_=1, to=9999, width=5, font=("Arial", 12))
    adresse_numero.pack(side="left", padx=10)

    # Nom de rue
    adresse_rue = Entry(frame_adresse, font=("Arial", 12), width=25)
    adresse_rue.pack(side="left", padx=10, fill="x", expand=True)

    # Champ Code postal et Ville
    text_cp_ville = Label(scrollable_frame, text="Code postal et Ville :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    text_cp_ville.pack(pady=10, padx=10, anchor="w")

    frame_CP_ville = Frame(scrollable_frame, bg="#F0F0F0")
    frame_CP_ville.pack(pady=5, padx=10, anchor="w", fill="x")

    # Code postal
    cp_spinbox = Spinbox(frame_CP_ville, from_=1000, to=99999, width=5, font=("Arial", 12))
    cp_spinbox.pack(side="left", padx=10)

    # Ville
    ville_entry = Entry(frame_CP_ville, font=("Arial", 12), width=25)
    ville_entry.pack(side="left", padx=10, fill="x", expand=True)

    # Bouton d'ajout
    ajouter_client_btn = Button(
        scrollable_frame,
        text="Ajouter Client",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12),
        command=lambda: ajout_client_action()
    )
    ajouter_client_btn.pack(pady=20, padx=10, fill="x")

    def ajout_client_action():
        """
        Valide et enregistre le nouveau client
        """
        # Récupération des valeurs
        nom = nom_entry.get()
        prenom = prenom_entry.get()
        telephone = telephone_entry.get()
        numero = adresse_numero.get()
        rue = adresse_rue.get()
        code_postal = cp_spinbox.get()
        ville = ville_entry.get()

        # Formatage de l'adresse
        num_rue = f"{numero} {rue}"

        # Formatage du code postal
        if len(code_postal) < 5:
            code_postal = "0" + code_postal

        # Validation des champs obligatoires
        if nom and prenom and telephone and num_rue and code_postal and ville:
            if est_numero_valide(telephone):
                # Enregistrement en base de données
                if sql.add_client(id_entreprise, nom, prenom, telephone, num_rue, code_postal, ville):
                    messagebox.showinfo("Succès", "✅ Le client a été ajouté avec succès.")
                    liste_client(frame, id_entreprise)
                else:
                    messagebox.showerror("Erreur", "❌ Échec de l'ajout du client. Veuillez réessayer.")
                    ajout_client(frame, id_entreprise)
            else:
                messagebox.showerror("Erreur", "❌ Échec de l'ajout du client. Numéro invalide.")
                ajout_client(frame, id_entreprise)
        else:
            messagebox.showerror("Erreur", "❌ Veuillez remplir tous les champs obligatoires.")
            ajout_client(frame, id_entreprise)

def suppr_client(frame, id_client, id_entreprise):
    """
    Supprime un client
    """
    if sql.delete_client(id_client, id_entreprise):
        messagebox.showinfo("Succès", "✅ Le client a été supprimé avec succès.")
        liste_client(frame, id_entreprise)
    else:
        messagebox.showerror("Erreur", "❌ Veuillez remplir tous les champs obligatoires.")
    
def est_numero_valide(numero):
    """
    Vérifie si un numéro de téléphone est valide
    Args:
        numero (str): Numéro à vérifier
    Returns:
        bool: True si valide, False sinon
    """
    return re.fullmatch(r"0[67][0-9]{8}", numero) is not None

def modify_client(frame, client):
    """
    Affiche le formulaire de modification d'un client
    """
    # Création de la fenêtre popup
    top = Toplevel(frame)
    top.title("Modifier le Client")
    top.geometry("600x450")
    top.minsize(600, 450)
    top.configure(bg="#3CB1E4")
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico") 

    # Titre de la fenêtre
    title_label = Label(top, text="Modification du Client", font=("Bold", 16), bg="#3CB1E4", fg="#2C3E50")
    title_label.pack(pady=20)

    # Configuration du système de défilement
    canvas_frame = Frame(top, bg="#B2CCE4")
    canvas_frame.pack(pady=10, fill="both", expand=True)

    canvas = Canvas(canvas_frame, bg="#B2CCE4")
    scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#B2CCE4")

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Gestion de la molette de la souris
    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # Frame pour le formulaire
    form_frame = Frame(scrollable_frame, bg="#B2CCE4")
    form_frame.pack(pady=10, padx=20, fill="x")

    # Champ Nom
    nom_label = Label(form_frame, text="Nom :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    nom_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    nom_entry = Entry(form_frame, font=("Arial", 12), width=30)
    nom_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    nom_entry.insert(0, client[2])  # Pré-remplissage avec la valeur existante

    # Champ Prénom
    prenom_label = Label(form_frame, text="Prénom :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    prenom_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    prenom_entry = Entry(form_frame, font=("Arial", 12), width=30)
    prenom_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    prenom_entry.insert(0, client[3])

    # Champ Téléphone
    telephone_label = Label(form_frame, text="Téléphone :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    telephone_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    telephone_entry = Entry(form_frame, font=("Arial", 12), width=30)
    telephone_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    telephone_entry.insert(0, client[4])

    # Champ Adresse
    adresse_label = Label(form_frame, text="Adresse :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    adresse_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    adresse_frame = Frame(form_frame, bg="#B2CCE4")
    adresse_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="w")

    # Numéro de rue
    adresse_numero = Spinbox(adresse_frame, from_=1, to=9999, width=5, font=("Arial", 12))
    adresse_numero.pack(side="left", padx=(0, 5))
    adresse_numero.delete(0, "end")
    adresse_numero.insert(0, client[5].split(" ", 1)[0])  # Extraction du numéro

    # Nom de rue
    adresse_rue = Entry(adresse_frame, font=("Arial", 12), width=24)
    adresse_rue.pack(side="left")
    adresse_rue.insert(0, client[5].split(" ", 1)[1])  # Extraction du nom de rue

    # Champ Code postal et Ville
    cp_ville_label = Label(form_frame, text="Code postal et Ville :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    cp_ville_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    cp_ville_frame = Frame(form_frame, bg="#B2CCE4")
    cp_ville_frame.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="w")

    # Code postal
    cp_spinbox = Spinbox(cp_ville_frame, from_=1000, to=99999, width=5, font=("Arial", 12))
    cp_spinbox.pack(side="left", padx=(0, 5))
    cp_spinbox.delete(0, "end")
    cp_spinbox.insert(0, client[6])

    # Ville
    ville_entry = Entry(cp_ville_frame, font=("Arial", 12), width=24)
    ville_entry.pack(side="left")
    ville_entry.insert(0, client[7])

    # Frame pour les boutons
    button_frame = Frame(top, bg="#3CB1E4")
    button_frame.pack(pady=20)

    # Bouton Enregistrer
    save_button = Button(button_frame, text="Enregistrer", font=("Arial", 12), bg="#4CAF50", fg="white", 
                        command=lambda: modify_client_action())
    save_button.pack(side="left", padx=10)

    # Bouton Annuler
    cancel_button = Button(button_frame, text="Annuler", font=("Arial", 12), bg="#FF4D4D", fg="white", 
                          command=top.destroy)
    cancel_button.pack(side="left", padx=10)

    def modify_client_action():
        """
        Valide et enregistre les modifications du client
        """
        # Récupération des valeurs
        id_client = client[0]
        entreprise_id = client[8]
        nom = nom_entry.get()
        prenom = prenom_entry.get()
        telephone = telephone_entry.get()
        numero = adresse_numero.get()
        rue = adresse_rue.get()
        code_postal = cp_spinbox.get()
        ville = ville_entry.get()

        # Formatage de l'adresse
        num_rue = f"{numero} {rue}"

        # Formatage du code postal
        if len(code_postal) < 5:
            code_postal = "0" + code_postal

        # Validation du numéro de téléphone
        if est_numero_valide(telephone):
            # Mise à jour en base de données
            if sql.update_client(id_client, nom, prenom, telephone, num_rue, code_postal, ville):
                messagebox.showinfo("Succès", "✅ Le client a été modifié avec succès.")
                top.destroy()
                liste_client(frame, entreprise_id)
            else:
                messagebox.showerror("Erreur", "❌ Échec de la modification du client. Veuillez réessayer.")
        else:
            messagebox.showerror("Erreur", "❌ Échec de la modification du client. Numéro invalide.")

def recup_client(frame, fonc, id_entreprise):
    """
    Affiche la liste des clients avec possibilité de recherche
    """
    # Nettoyage du frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Récupération de la liste des clients
    list_client = sql.get_all_client_with_id(id_entreprise)

    # Titre selon la fonctionnalité
    if fonc == 'Suppr':
        title_delete_client = Label(frame, text="Supprimer des Clients", fg='#2C3E50', bg=background_color, font=('Bold', 18))
        title_delete_client.pack(pady=20)
    elif fonc == 'Liste':
        title_list_client = Label(frame, text="Liste des Clients", fg='#2C3E50', bg=background_color, font=('Bold', 18))
        title_list_client.pack(pady=20)

    # Frame pour la recherche
    search_frame = Frame(frame, bg='white')
    search_frame.pack(pady=10)

    search_label = Label(search_frame, text="Recherchez par nom ou prénom : ", font=("Arial", 12), bg='white')
    search_label.pack(side="left", padx=5)

    search_entry = Entry(search_frame, font=("Arial", 12), width=30)
    search_entry.pack(side="left", padx=5)

    # Configuration du système de défilement
    canvas_frame = Frame(frame, bg="white")
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

        if list_client:
            # Filtrage des clients
            filtered_client = [
                client for client in list_client
                if search_text in client[2].lower() or search_text in client[3].lower()
            ]
            
            # Affichage des clients filtrés
            for client in filtered_client:
                client_text = (
                    f"ID: {client[0]}\n"
                    f"Nom: {client[2]}\n"
                    f"Prénom: {client[3]}\n"
                    f"Téléphone: {client[4]}\n"
                    f"Adresse: {client[5]} {client[6]} {client[7]}\n"
                )

                # Frame pour chaque client
                client_frame = Frame(scrollable_frame, bg="white", borderwidth=1, relief="solid")
                client_frame.pack(fill="x", padx=10, pady=5)

                # Affichage des infos du client
                client_label = Label(client_frame, text=client_text, font=("Arial", 12), bg="white", anchor="w", justify="left")
                client_label.pack(fill="x", padx=10, pady=5)

                # Frame pour les boutons d'action
                button_frame = Frame(client_frame, bg="white")
                button_frame.pack(pady=5)

                # Bouton Modifier
                modify_button = Button(button_frame, text="Modifier", bg="#5A9BD5", fg="white", 
                                     activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                     command=lambda client=client: modify_client(frame, client))
                modify_button.grid(row=0, column=0, padx=5)

                # Bouton Supprimer
                delete_button = Button(button_frame, text="Supprimer", bg="#5A9BD5", fg="white", 
                                     activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                     command=lambda frame=frame, id_client=client[0], id_entreprise=id_entreprise: 
                                     suppr_client(frame, id_client, id_entreprise))
                delete_button.grid(row=0, column=1, padx=5)

                # Bouton Fiche client
                fiche_button = Button(button_frame, text="Fiche client", bg="#5A9BD5", fg="white", 
                                    activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                    command=lambda frame=frame, id_client=client[0], id_entreprise=id_entreprise: 
                                    info_client.fiche_client(frame, id_client, id_entreprise))
                fiche_button.grid(row=0, column=2, padx=5)
        else:
            # Message si aucun résultat
            no_results_label = Label(scrollable_frame, text="Aucun résultat trouvé.", 
                                   font=("Arial", 12, "italic"), bg="white", fg="gray")
            no_results_label.pack(pady=10)

    # Liaison de la recherche à la mise à jour des résultats
    search_entry.bind("<KeyRelease>", lambda event: update_results())
    update_results()  # Affichage initial