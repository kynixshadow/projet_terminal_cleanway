from tkinter import *  
from tkinter import ttk  
from tkcalendar import Calendar  
from tkinter import messagebox  
from module.menu_horizontal import ResponsiveMenu 
import module.sql as sql  
import module.prix_forfait as prix_forfait
import photos as photo 
from datetime import datetime 
import os
from module.info_client import fiche_client

# Définition des couleurs de fond
background_color = '#3CB1E4'  
background_color_menu = '#1767AA'  

def page_rdv(root_frame, id_entreprise):
    """
    Fonction principale pour afficher la page des rendez-vous.
    Crée les frames principaux et initialise le menu.
    """
    # Frame principal pour les rendez-vous
    client_frame = Frame(root_frame, bg='white') 
    client_frame.pack(fill=BOTH, expand=True, side=TOP) 

    # Frame pour le menu
    menu_frame = Frame(client_frame, bg=background_color_menu) 
    menu_frame.pack(side=TOP, fill=X) 

    # Frame pour le contenu
    content_frame = Frame(client_frame, bg=background_color)  
    content_frame.pack(fill=BOTH, expand=True)  

    # Création du menu responsive
    menu = ResponsiveMenu(menu_frame, foreground_color='white', background_color=background_color_menu)
    menu.ajout_bouton("Liste Rendez-vous", lambda: liste_rdv(content_frame, id_entreprise))  
    menu.ajout_bouton("Ajouter Rendez-vous", lambda: ajout_rdv(content_frame, id_entreprise)) 
    menu.ajout_bouton("Supprimer Rendez-vous", lambda: suppr_rdv(content_frame, id_entreprise))  

    # Affichage par défaut de la liste des rendez-vous
    liste_rdv(content_frame, id_entreprise)

def open_date_picker(date_entry):
    """
    Ouvre un calendrier pour sélectionner une date et l'insère dans l'entrée spécifiée.
    """
    def get_date():
        # Récupère la date sélectionnée et l'insère dans l'entrée
        date = cal.get_date()  
        date_entry.delete(0, END)  
        date_entry.insert(0, date)  
        top.destroy()  # Ferme la fenêtre

    # Création de la fenêtre popup
    top = Toplevel()  
    top.title("Sélection date")  
    top.geometry("400x300")  
    top.minsize(400, 300)  
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico")  
    
    # Ajout du calendrier
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd') 
    cal.pack(pady=20) 
    
    # Bouton de validation
    button = Button(top, text="Sélectionner", command=get_date) 
    button.pack(pady=10)  

def open_time_picker(time_entry):
    """
    Ouvre un sélecteur d'heure et l'insère dans l'entrée spécifiée.
    """
    def get_time():
        # Récupère l'heure sélectionnée et l'insère dans l'entrée
        hour = hour_combobox.get()  
        minute = minute_combobox.get()  
        time_entry.delete(0, END) 
        time_entry.insert(0, f"{hour}:{minute}") 
        top.destroy()  # Ferme la fenêtre

    # Création de la fenêtre popup
    top = Toplevel() 
    top.title("Sélection heure")  
    top.geometry("300x150") 
    top.minsize(300, 150)  
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico") 
    
    # Frame pour les sélecteurs d'heure
    frame_time = Frame(top) 
    frame_time.pack(pady=10) 

    # Combobox pour les heures
    hour_combobox = ttk.Combobox(frame_time, values=[f"{i:02d}" for i in range(24)], width=3)  
    hour_combobox.set("00") 
    hour_combobox.pack(side="left", padx=5)  

    # Combobox pour les minutes
    minute_combobox = ttk.Combobox(frame_time, values=[f"{i:02d}" for i in range(0, 60, 5)], width=3)  
    minute_combobox.set("00")  
    minute_combobox.pack(side="left", padx=5) 

    # Bouton de validation
    button = Button(top, text="Sélectionner", command=get_time) 
    button.pack(pady=10)  

def liste_rdv(frame, id_entreprise):
    """
    Affiche la liste des rendez-vous.
    """
    recup_rdv(frame, 'Liste', id_entreprise)  

def ajout_rdv(frame, id_entreprise):
    """
    Affiche le formulaire pour ajouter un nouveau rendez-vous.
    """
    # Nettoyage du frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Titre de la section
    Titre_ajout = Label(frame, text="Ajouter un Rendez-vous", fg='#2C3E50', bg='#3CB1E4', font=('Bold', 18))
    Titre_ajout.pack(pady=20)  

    # Création d'un canvas avec scrollbar pour le formulaire
    canvas_frame = Frame(frame, bg="#F0F0F0")  
    canvas_frame.pack(pady=10, fill="both", expand=True)

    canvas = Canvas(canvas_frame, bg="#F0F0F0")
    scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)  
    scrollable_frame = Frame(canvas, bg="#F0F0F0")  

    # Configuration du scroll
    canvas.configure(yscrollcommand=scrollbar.set) 
    scrollbar.pack(side="right", fill="y") 
    canvas.pack(side="left", fill="both", expand=True) 
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) 
    canvas.bind("<Configure>", lambda e: canvas.itemconfig("all", width=canvas.winfo_width())) 

    # Gestion de la molette de la souris pour le scroll
    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units") 
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel)) 
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))  

    # Champ Client
    text_client = Label(scrollable_frame, text="Client :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    text_client.pack(pady=10, padx=10, anchor="w")

    # Récupération de la liste des clients
    choices_client = []
    list_clients = sql.get_all_id_name(id_entreprise)
    for id_client, nom, prenom in list_clients:
        choices_client.append(f'{id_client} - {nom} {prenom}') 

    # Combobox pour sélectionner un client
    client_combobox = ttk.Combobox(scrollable_frame, values=choices_client, state="readonly", font=("Arial", 12))
    client_combobox.current(0)  
    client_combobox.pack(pady=10, padx=10, fill='x')  

    # Champ Date
    text_date = Label(scrollable_frame, text="Date :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    text_date.pack(pady=10, padx=10, anchor="w")

    frame_date = Frame(scrollable_frame, bg="#F0F0F0") 
    frame_date.pack(pady=5, padx=10, anchor="w", fill="x")

    date_entry = Entry(frame_date, font=("Arial", 12), width=25)
    date_entry.pack(side="left", padx=10, fill="x", expand=True)
    date_button = Button(frame_date, text="Choisir Date", font=("Arial", 10), bg="#3CB1E4", fg="white", command=lambda: open_date_picker(date_entry))
    date_button.pack(side="right", padx=10)

    # Champ Heure
    texte_Heure = Label(scrollable_frame, text="Heure :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    texte_Heure.pack(pady=10, padx=10, anchor="w")

    frame_heure = Frame(scrollable_frame, bg="#F0F0F0")  
    frame_heure.pack(pady=5, padx=10, anchor="w", fill="x")

    heure_entry = Entry(frame_heure, font=("Arial", 12), width=10)
    heure_entry.pack(side="left", padx=10, fill="x", expand=True)
    heure_button = Button(frame_heure, text="Choisir Heure", font=("Arial", 10), bg="#3CB1E4", fg="white", command=lambda: open_time_picker(heure_entry))
    heure_button.pack(side="right", padx=10)

    # Champ Adresse
    text_adress = Label(scrollable_frame, text="Adresse :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    text_adress.pack(pady=10, padx=10, anchor="w")

    frame_adress = Frame(scrollable_frame, bg="#F0F0F0")  
    frame_adress.pack(pady=5, padx=10, anchor="w", fill="x")

    # Numéro de rue
    adresse_numero = Spinbox(frame_adress, from_=1, to=9999, width=5, font=("Arial", 12))
    adresse_numero.pack(side="left", padx=10)

    # Nom de rue
    adresse_rue = Entry(frame_adress, font=("Arial", 12), width=25)
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

    # Champ Marque
    Marque_text = Label(scrollable_frame, text="Marque :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    Marque_text.pack(pady=10, padx=10, anchor="w")

    # Récupération des marques disponibles
    choices_marque = []
    list_marque = sql.get_all_marque()
    for id_marque, marque in list_marque:
        choices_marque.append(f'{id_marque} - {marque}') 

    # Combobox pour sélectionner une marque
    marque_combobox = ttk.Combobox(scrollable_frame, values=choices_marque, state="readonly", font=("Arial", 12))
    marque_combobox.current(0) 
    marque_combobox.pack(pady=10, padx=10, fill='x')

    # Champ Modèle
    Modele_text = Label(scrollable_frame, text="Modèle :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    Modele_text.pack(pady=10, padx=10, anchor="w")

    # Combobox pour les modèles (rempli dynamiquement en fonction de la marque)
    model_combobox = ttk.Combobox(scrollable_frame, values=[], state="readonly", font=("Arial", 12))
    model_combobox.pack(pady=10, padx=10, fill='x')

    def update_models(event=None):
        """Met à jour la liste des modèles en fonction de la marque sélectionnée"""
        selected_marque = marque_combobox.get()
        marque_id = selected_marque.split(" - ")[0]  
        list_modeles = sql.get_all_modele_by_marque(marque_id)  
        choices_modele = [f"{id_modele} - {modele}" for id_modele, modele in list_modeles] 
        model_combobox['values'] = choices_modele  
        if choices_modele:
            model_combobox.current(0) 
        else:
            model_combobox.set('')  

    # Liaison de l'événement de sélection de marque
    marque_combobox.bind("<<ComboboxSelected>>", update_models)  
    update_models()  # Initialisation

    # Champ Nombre de sièges
    Nbre_siege = Label(scrollable_frame, text="Nombre de sièges :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    Nbre_siege.pack(pady=10, padx=10, anchor="w")

    frame_siege = Frame(scrollable_frame, bg="#F0F0F0") 
    frame_siege.pack(pady=5, padx=10, anchor="w", fill="x")

    # Slider pour sélectionner le nombre de sièges
    siege_scale = Scale(frame_siege, from_=1, to=50, orient="horizontal", bg="#F0F0F0", font=("Arial", 12), troughcolor="#99BBEE")
    siege_scale.set(1) 
    siege_scale.pack(side="left", padx=10, fill="x", expand=True)

    # Champ Forfait
    Forfait_text = Label(scrollable_frame, text="Forfait :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    Forfait_text.pack(pady=10, padx=10, anchor="w")

    frame_forfait = Frame(scrollable_frame, bg="#F0F0F0") 
    frame_forfait.pack(pady=5, padx=10, expand=True)

    # Boutons radio pour les types de forfaits
    forfait_var = StringVar(value="Forfait Complet") 
    forfait_int = Radiobutton(frame_forfait, text="Intérieur", variable=forfait_var, value="Forfait Intérieur", bg="#F0F0F0", font=("Arial", 12))
    forfait_int.pack(side="left", padx=10)

    forfait_ext = Radiobutton(frame_forfait, text="Extérieur", variable=forfait_var, value="Forfait Extérieur", bg="#F0F0F0", font=("Arial", 12))
    forfait_ext.pack(side="left", padx=10)

    forfait_comp = Radiobutton(frame_forfait, text="Complet", variable=forfait_var, value="Forfait Complet", bg="#F0F0F0", font=("Arial", 12))
    forfait_comp.pack(side="left", padx=10)

    # Champ Prix
    Prix_text = Label(scrollable_frame, text="Prix :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    Prix_text.pack(pady=10, padx=10, anchor="w")

    Prix_entry = Entry(scrollable_frame, font=("Arial", 12), width=25)
    Prix_entry.pack(padx=10, fill="x", expand=True)
    Prix_entry.config(state="readonly")  # Prix calculé automatiquement

    def recalcule_prix(*args):
        """Recalcule le prix en fonction des sélections"""
        try:
            id_modele = int(model_combobox.get().split("-")[0])  
        except Exception as e:
            id_modele = 0 
        nbre_siege = siege_scale.get()  
        forfait_choisi = forfait_var.get() 
        prix = prix_forfait.calcul_prix(id_modele, nbre_siege, forfait_choisi) 
        Prix_entry.config(state="normal") 
        Prix_entry.delete(0, END)  
        Prix_entry.insert(0, prix)  
        Prix_entry.config(state="readonly")  

    recalcule_prix()  # Calcul initial

    # Liaison des événements pour le recalcul du prix
    model_combobox.bind("<<ComboboxSelected>>", lambda event: recalcule_prix()) 
    siege_scale.config(command=lambda value: recalcule_prix()) 
    forfait_var.trace("w", lambda *args: recalcule_prix()) 

    # Champ Remarques
    text_remarque = Label(scrollable_frame, text="Remarques :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    text_remarque.pack(pady=10, padx=10, anchor="w")

    remarque = Text(scrollable_frame, height=5, font=("Arial", 12))
    remarque.pack(padx=10, fill="x", expand=True)
    remarque.insert("1.0", "Sans remarque")  # Valeur par défaut

    # Bouton d'ajout de rendez-vous
    ajouter_rdv_btn = Button(
        scrollable_frame, 
        text="Ajouter RDV", 
        bg="#4CAF50",  
        fg="white", 
        font=("Arial", 12),
        command=lambda: ajout_rdv_action()  
    )
    ajouter_rdv_btn.pack(pady=20, padx=10, fill="x")

    def ajout_rdv_action():
        """Action d'ajout d'un rendez-vous"""
        # Récupération des valeurs des champs
        client_id = int(client_combobox.get().split("-")[0])  
        entreprise_id = id_entreprise  
        date = date_entry.get()  
        heure = heure_entry.get()  
        etat = "Confirmé" 
        numero = adresse_numero.get() 
        rue = adresse_rue.get() 
        code_postale = cp_spinbox.get()  
        ville = ville_entry.get()  
        marque = str(marque_combobox.get().split("-")[1])  
        modele = str(model_combobox.get().split("-")[1]) 
        nbre_siege = siege_scale.get()  
        forfait = forfait_var.get()  
        montant = int(Prix_entry.get())  
        remarque_valeur = remarque.get("1.0", "end-1c") 

        # Formatage de l'adresse
        num_rue = f"{numero} {rue}"  

        # Validation des champs
        if client_id and entreprise_id and date and heure and etat and numero and rue and code_postale and ville and marque and modele and nbre_siege and forfait and montant and remarque_valeur:
            # Formatage du code postal si nécessaire
            if len(code_postale) < 5:  
                code_postale = "0" + code_postale

            # Ajout en base de données
            if sql.add_rdv(client_id, entreprise_id, date, heure, etat, num_rue, code_postale, ville, marque, modele, nbre_siege, forfait, montant, remarque_valeur):
                messagebox.showinfo("Succès", "✅ Le rendez-vous a été ajouté avec succès.")  
                ajout_rdv(frame, entreprise_id)  # Réinitialisation du formulaire
            else:
                messagebox.showerror("Erreur", "❌ Échec de l'ajout du rendez-vous. Veuillez réessayer.")  
                ajout_rdv(frame, entreprise_id) 
        else:
            messagebox.showerror("Erreur", "❌ Veuillez remplir tous les champs.")  
            ajout_rdv(frame, entreprise_id) 

def suppr_rdv(frame, id_entreprise):
    """Affiche l'interface de suppression des rendez-vous"""
    recup_rdv(frame, 'Suppr', id_entreprise)  

def passed_rdv_action(id_rdv, frame, id_entreprise):
    """Marque un rendez-vous comme passé"""
    if sql.pass_rdv(id_rdv) and creer_dossier_image(id_rdv):  
        messagebox.showinfo("Succès", "✅ Le rendez-vous a été modifié avec succès.")  
        liste_rdv(frame, id_entreprise)  
    else:
        messagebox.showerror("Erreur", "❌ Échec de la requete sql ou pendant la création du dossier. Veuillez réessayer.")  
        liste_rdv(frame, id_entreprise)  

def creer_dossier_image(id_rdv):
    """Crée un dossier pour stocker les images d'un rendez-vous"""
    try:
        date = sql.get_date_rdv(id_rdv)[0]
        nom_dossier = f'{date}_{id_rdv}'
        chemin_img_rdv = os.path.join(os.path.dirname(__file__), "IMG_RDV")
        chemin_complet = os.path.join(chemin_img_rdv, nom_dossier)
        os.makedirs(chemin_complet, exist_ok=True)
        return True
    except Exception as e:
        print(f"Erreur lors de la création du dossier : {e}")
        return False

def supp_rdv_action(id_rdv, frame, id_entreprise):
    """Supprime un rendez-vous"""
    if sql.delete_rdv(id_rdv):  
        messagebox.showinfo("Succès", "✅ Le rendez-vous a été supprimé avec succès.")  
        suppr_rdv(frame, id_entreprise)  
    else:
        messagebox.showerror("Erreur", "❌ Échec de l'ajout du rendez-vous. Veuillez réessayer.") 
        suppr_rdv(frame, id_entreprise)  

def modify_rdv(frame, rdv):
    """Affiche le formulaire de modification d'un rendez-vous"""
    # Création de la fenêtre popup
    top = Toplevel(frame)  
    top.title("Modifier le Rendez-vous") 
    top.geometry("600x450")  
    top.minsize(600, 450) 
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico") 
    top.configure(bg="#3CB1E4")
    
    title_label = Label(top, text="Modification du Rendez-vous", font=("Bold", 16), bg="#3CB1E4", fg="#2C3E50")
    title_label.pack(pady=20)  
    
    # Création du canvas avec scrollbar
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

    # Champ Client ID
    client_label = Label(form_frame, text="Client ID :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    client_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    client_entry = Entry(form_frame, font=("Arial", 12), width=30)
    client_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    client_entry.insert(0, str(rdv[1])) 

    # Champ Date
    date_label = Label(form_frame, text="Date :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    date_entry = Entry(form_frame, font=("Arial", 12), width=30)
    date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    date_entry.insert(0, rdv[3]) 

    date_button = Button(form_frame, text="Date", font=("Arial", 10), bg="#3CB1E4", fg="white", command=lambda: open_date_picker(date_entry))
    date_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    # Champ Heure
    heure_label = Label(form_frame, text="Heure :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    heure_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    heure_entry = Entry(form_frame, font=("Arial", 12), width=10)
    heure_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    heure_entry.insert(0, rdv[4])  

    heure_button = Button(form_frame, text="Heure", font=("Arial", 10), bg="#3CB1E4", fg="white", command=lambda: open_time_picker(heure_entry))
    heure_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

    # Champ Adresse
    adresse_label = Label(form_frame, text="Adresse :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    adresse_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    adresse_frame = Frame(form_frame, bg="#B2CCE4")
    adresse_frame.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="w")

    # Numéro de rue
    adresse_numero = Spinbox(adresse_frame, from_=1, to=9999, width=5, font=("Arial", 12))
    adresse_numero.pack(side="left", padx=(0, 5))
    adresse_numero.delete(0, "end")
    adresse_numero.insert(0, rdv[6].split(" ", 1)[0])

    # Nom de rue
    adresse_rue = Entry(adresse_frame, font=("Arial", 12), width=24)
    adresse_rue.pack(side="left")
    adresse_rue.insert(0, rdv[6].split(" ", 1)[1]) 

    # Champ Code postal et Ville
    cp_ville_label = Label(form_frame, text="Code postal et Ville :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    cp_ville_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    cp_ville_frame = Frame(form_frame, bg="#B2CCE4")
    cp_ville_frame.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="w")

    # Code postal
    cp_spinbox = Spinbox(cp_ville_frame, from_=1000, to=99999, width=5, font=("Arial", 12))
    cp_spinbox.pack(side="left", padx=(0, 5))
    cp_spinbox.delete(0, "end")
    cp_spinbox.insert(0, rdv[7])

    # Ville
    ville_entry = Entry(cp_ville_frame, font=("Arial", 12), width=24)
    ville_entry.pack(side="left")
    ville_entry.insert(0, rdv[8])

    # Champ Marque (lecture seule)
    marque_label = Label(form_frame, text="Marque :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    marque_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    marque_entry = Entry(form_frame, font=("Arial", 12), width=25)
    marque_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
    marque_entry.insert(0, rdv[9]) 
    marque_entry.config(state="readonly")  

    # Champ Modèle (lecture seule)
    modele_label = Label(form_frame, text="Modèle :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    modele_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

    modele_entry = Entry(form_frame, font=("Arial", 12), width=25)
    modele_entry.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
    modele_entry.insert(0, rdv[10])  
    modele_entry.config(state="readonly")  

    # Champ Nombre de sièges (lecture seule)
    siege_label = Label(form_frame, text="Nombre de sièges :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    siege_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")

    siege_scale = Scale(form_frame, from_=1, to=50, orient="horizontal", bg="#F0F0F0", font=("Arial", 12), troughcolor="#99BBEE")
    siege_scale.grid(row=7, column=1, padx=10, pady=10, sticky="ew")
    siege_scale.set(int(rdv[11])) 
    siege_scale.config(state="disabled")  

    # Champ Forfait
    forfait_label = Label(form_frame, text="Forfait :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    forfait_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

    forfait_var = StringVar(value=rdv[12])  

    forfait_frame = Frame(form_frame, bg="#B2CCE4")
    forfait_frame.grid(row=8, column=1, columnspan=3, padx=10, pady=5, sticky="w")

    # Boutons radio pour les forfaits
    forfait_int = Radiobutton(forfait_frame, text="Intérieur", variable=forfait_var, value="Forfait Intérieur", bg="#B2CCE4", font=("Arial", 12))
    forfait_int.pack(side="left", padx=5)

    forfait_ext = Radiobutton(forfait_frame, text="Extérieur", variable=forfait_var, value="Forfait Extérieur", bg="#B2CCE4", font=("Arial", 12))
    forfait_ext.pack(side="left", padx=5)

    forfait_comp = Radiobutton(forfait_frame, text="Complet", variable=forfait_var, value="Forfait Complet", bg="#B2CCE4", font=("Arial", 12))
    forfait_comp.pack(side="left", padx=5)

    # Champ Prix
    prix_label = Label(form_frame, text="Prix :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    prix_label.grid(row=9, column=0, padx=10, pady=10, sticky="w")

    prix_entry = Entry(form_frame, font=("Arial", 12), width=30)
    prix_entry.grid(row=9, column=1, padx=10, pady=10, sticky="ew")
    prix_entry.insert(0, rdv[13]) 

    # Champ Remarques
    remarque_label = Label(form_frame, text="Remarques :", font=("Arial", 12), bg="#B2CCE4", fg="#2C3E50")
    remarque_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")

    remarque_frame = Frame(form_frame, bg="#F0F0F0") 
    remarque_frame.grid(row=10, column=1, columnspan=2, padx=10, pady=5, sticky="w")

    remarque_text = Text(remarque_frame, height=3, width=40, font=("Arial", 12), wrap="word")  
    remarque_text.pack(fill="x")  
    remarque_text.insert("1.0", rdv[14])

    # Boutons Enregistrer/Annuler
    button_frame = Frame(top, bg="#3CB1E4")
    button_frame.pack(pady=20)

    save_button = Button(button_frame, text="Enregistrer", font=("Arial", 12), bg="#4CAF50", fg="white", command=lambda: modify_rdv_action())
    save_button.pack(side="left", padx=10)

    cancel_button = Button(button_frame, text="Annuler", font=("Arial", 12), bg="#FF4D4D", fg="white", command=top.destroy)
    cancel_button.pack(side="left", padx=10)

    def modify_rdv_action():
        """Action de modification d'un rendez-vous"""
        # Récupération des valeurs des champs
        id_rdv = rdv[0]
        client_id = client_entry.get()
        entreprise_id = rdv[2]
        date = date_entry.get()
        heure = heure_entry.get()
        etat = "Confirmé"
        numero = adresse_numero.get()
        rue = adresse_rue.get()
        code_postale = cp_spinbox.get()
        ville = ville_entry.get()
        marque = marque_entry.get()
        modele = modele_entry.get()
        nbre_siege = siege_scale.get()
        forfait = forfait_var.get()
        montant = int(prix_entry.get())
        remarque_valeur = remarque_text.get("1.0", "end-1c")

        # Formatage de l'adresse
        num_rue = f"{numero} {rue}"

        # Formatage du code postal si nécessaire
        if len(code_postale) < 5:
            code_postale = "0" + code_postale

        # Mise à jour en base de données
        if sql.update_rdv(client_id, entreprise_id, date, heure, etat, num_rue, code_postale, ville, marque, modele, nbre_siege, forfait, montant, remarque_valeur, id_rdv):
            messagebox.showinfo("Succès", "✅ Le rendez-vous a été modifié avec succès.")
            top.destroy()
            liste_rdv(frame, entreprise_id)
        else:
            messagebox.showerror("Erreur", "❌ Échec de la modification du rendez-vous. Veuillez réessayer.")

def recup_rdv(frame, fonc, id_entreprise):
    """
    Affiche la liste des rendez-vous avec des fonctionnalités différentes selon 'fonc'
    ('Suppr' pour suppression, 'Liste' pour visualisation/modification)
    """
    # Nettoyage du frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Récupération des rendez-vous selon la fonction demandée
    if fonc == 'Suppr':
        list_rdv = sql.get_rdv_confirmed_ie(id_entreprise)  # Rendez-vous confirmés seulement
        title_delete_rdv = Label(frame, text="Supprimer des Rendez-vous", fg='#2C3E50', bg=background_color, font=('Bold', 18))
        title_delete_rdv.pack(pady=20)  
    elif fonc == 'Liste':
        list_rdv = sql.get_rdv_ie(id_entreprise)  # Tous les rendez-vous
        title_list_rdv = Label(frame, text="Liste des Rendez-vous", fg='#2C3E50', bg=background_color, font=('Bold', 18))
        title_list_rdv.pack(pady=20) 

    # Tri des rendez-vous par date (du plus récent au plus ancien)
    list_rdv.sort(key=lambda x: x[3], reverse=True)

    # Création du champ de recherche
    search_frame = Frame(frame, bg='white')
    search_frame.pack(pady=10)  

    search_label = Label(search_frame, text="Recherchez par véhicule ou par date : ", font=("Arial", 12), bg='white')
    search_label.pack(side="left", padx=5) 

    search_entry = Entry(search_frame, font=("Arial", 12), width=30) 
    search_entry.pack(side="left", padx=5)  

    # Création du canvas avec scrollbar pour afficher les rendez-vous
    canvas_frame = Frame(frame, bg="white")
    canvas_frame.pack(pady=10, fill="both", expand=True) 

    canvas = Canvas(canvas_frame, bg="#B2CCE4")  
    scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)  
    scrollable_frame = Frame(canvas, bg="#B2CCE4") 

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")  
    canvas.pack(side="left", fill="both", expand=True)  
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") 

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  
    canvas.bind("<Configure>", lambda e: canvas.itemconfig("all", width=canvas.winfo_width())) 

    # Gestion de la molette de la souris pour le scroll
    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")  
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))  
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))  

    def update_results():
        """Met à jour les résultats affichés en fonction de la recherche"""
        for widget in scrollable_frame.winfo_children():
            widget.destroy()  

        search_text = search_entry.get().lower() 
        
        if list_rdv:  
            # Filtrage des rendez-vous selon le texte de recherche
            filtered_rdv = [
                rdv for rdv in list_rdv
                if search_text in rdv[3].lower() or search_text in rdv[9].lower() or search_text in rdv[10].lower()
            ]  
            
            # Affichage de chaque rendez-vous filtré
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

                # Création du frame pour un rendez-vous
                rdv_frame = Frame(scrollable_frame, bg="white", borderwidth=1, relief="solid")  
                rdv_frame.pack(fill="x", padx=10, pady=5) 

                # Affichage des informations
                rdv_label = Label(rdv_frame, text=rdv_text, font=("Arial", 12), bg="white", anchor="w", justify="left")  
                rdv_label.pack(fill="x", padx=10, pady=5) 

                # Frame pour les boutons d'action
                button_frame = Frame(rdv_frame, bg="white")  
                button_frame.pack(pady=5) 
                
                # Boutons différents selon la fonction demandée
                if fonc == 'Suppr':  
                    # Bouton de suppression
                    delete_button = Button(button_frame, text="Supprimer", bg="#5A9BD5", fg="white",
                                           activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                           command=lambda rdv=rdv:supp_rdv_action(rdv[0], frame, rdv[2])) 
                    delete_button.grid(row=0, column=1, padx=5) 
                elif fonc == 'Liste': 
                    if rdv[5] == "Confirmé":  
                        # Bouton pour marquer comme passé
                        passed_button = Button(button_frame, text="Rdv passé", bg="#5A9BD5", fg="white",
                                               activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                               command=lambda rdv=rdv:passed_rdv_action(rdv[0], frame, rdv[2]))  
                        passed_button.grid(row=0, column=0, padx=5)
                        
                        # Bouton de modification
                        modify_button = Button(button_frame, text="Modifier", bg="#5A9BD5", fg="white",
                                               activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                               command=lambda rdv=rdv:modify_rdv(frame, rdv))  
                        modify_button.grid(row=0, column=2, padx=5) 
                    elif rdv[5] == "Passé":  
                        # Bouton pour voir les images
                        image_button = Button(button_frame, text="Image", bg="#5A9BD5", fg="white", 
                                             activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                             command=lambda date=rdv[3], id_rdv=rdv[0]:lancer_photos(date, id_rdv))  
                        image_button.grid(row=0, column=3, padx=5)  

                # Bouton pour voir la fiche client
                client_button = Button(button_frame, text="Fiche client", bg="#5A9BD5", fg="white", 
                                      activebackground="#7FAEDA", font=("Arial", 10), width=18, 
                                      command=lambda frame=frame, id_client=rdv[1], id_entreprise=id_entreprise:
                                      fiche_client(frame, id_client, id_entreprise))
                client_button.grid(row=0, column=4, padx=5)  
        else:  
            # Message si aucun résultat
            no_results_label = Label(scrollable_frame, text="Aucun résultat trouvé.", 
                                   font=("Arial", 12, "italic"), bg="white", fg="gray")  
            no_results_label.pack(pady=10)  

    # Liaison de la recherche à la mise à jour des résultats
    search_entry.bind("<KeyRelease>", lambda event: update_results())  
    update_results()  # Affichage initial

def lancer_photos(date, id_rdv):
    """Ouvre le visionneur de photos pour un rendez-vous"""
    print(date, id_rdv)
    chemin = f"IMG_RDV/{date}_{id_rdv}/"
    print(chemin)
    photo.lancer_visionneur(chemin)