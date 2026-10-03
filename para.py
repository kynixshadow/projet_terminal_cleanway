# Importation des modules nécessaires
from tkinter import *
from tkinter import ttk, messagebox
import re
import module.sql as sql

# Définition des couleurs utilisées dans l'interface
background_color = '#3CB1E4'
background_color_menu = '#1767AA'
text_color = '#2C3E50'
entry_bg = '#FFFFFF'
button_color = '#5A9BD5'

def page_para(frame, id_entreprise):
    """
    Fonction principale pour afficher la page des paramètres de l'entreprise
    Args:
        frame: Le frame parent où afficher le contenu
        id_entreprise: L'identifiant de l'entreprise à afficher
    """
    # Nettoyage du frame avant d'afficher le nouveau contenu
    for widget in frame.winfo_children():
        widget.destroy()

    # Création d'un canvas avec barre de défilement
    canvas = Canvas(frame, bg=background_color, highlightthickness=0)
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)

    # Création des conteneurs pour le contenu défilable
    container = Frame(canvas, bg=background_color)
    scrollable_frame = Frame(container, bg=background_color)
    
    # Configuration du canvas et de la scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Placement du conteneur dans le canvas
    canvas.create_window((frame.winfo_width()//2, 0), window=container, anchor="n")
    scrollable_frame.pack(expand=True)

    def on_configure(event):
        """Fonction pour gérer le redimensionnement et le défilement"""
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(1, width=event.width)
    
    # Liaison des événements de redimensionnement
    container.bind("<Configure>", on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(1, width=e.width))

    # Titre de la page
    Label(scrollable_frame, text="Paramètres", 
          font=('Bold', 24), bg=background_color, fg=text_color).pack(pady=20)

    # Récupération des données de l'entreprise depuis la base de données
    data_entreprise = sql.get_entreprise_data(id_entreprise)

    # Création du bloc principal pour les informations
    green_block = Frame(scrollable_frame, bg=entry_bg, bd=2, relief="groove")
    green_block.pack(pady=10, padx=10, fill="x", expand=True)

    # ID Entreprise (affichage seul)
    id_label = Label(green_block, text="ID Entreprise", bg=entry_bg, font=("Arial", 12, "bold"))
    id_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    ID_Label = Entry(green_block, width=30, font=("Arial", 12), state="normal")
    ID_Label.insert(0, str(data_entreprise[0]))
    ID_Label.config(state="readonly")
    ID_Label.grid(row=1, column=0, padx=5, pady=5)

    # Nom Entreprise (avec bouton de modification)
    name_label = Label(green_block, text="Nom Entreprise", bg=entry_bg, font=("Arial", 12, "bold"))
    name_label.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    Name_Entry = Entry(green_block, width=30, font=("Arial", 12), state="normal")
    Name_Entry.insert(0, data_entreprise[1])
    Name_Entry.config(state="readonly")
    Name_Entry.grid(row=3, column=0, padx=5, pady=5)

    Name_Modify = ttk.Button(green_block, text="Modifier", style='Param.TButton',
                            command=lambda: modify("Modifier le nom", "Name", Name_Entry.get(), data_entreprise[0], frame))
    Name_Modify.grid(row=3, column=1, padx=5, pady=5)

    # Adresse (avec bouton de modification)
    address_label = Label(green_block, text="Adresse", bg=entry_bg, font=("Arial", 12, "bold"))
    address_label.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

    address_entry = Entry(green_block, width=30, font=("Arial", 12), state="normal")
    address_entry.insert(0, data_entreprise[2])
    address_entry.config(state="readonly")
    address_entry.grid(row=5, column=0, padx=5, pady=5)

    address_modify = ttk.Button(green_block, text="Modifier", style='Param.TButton',
                               command=lambda: modify("Modifier l'adresse", "Adresse", address_entry.get(), data_entreprise[0], frame))
    address_modify.grid(row=5, column=1, padx=5, pady=5)

    # Code Postal (avec bouton de modification)
    zip_label = Label(green_block, text="Code Postal", bg=entry_bg, font=("Arial", 12, "bold"))
    zip_label.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

    zip_entry = Entry(green_block, width=30, font=("Arial", 12), state="normal")
    zip_entry.insert(0, data_entreprise[3])
    zip_entry.config(state="readonly")
    zip_entry.grid(row=7, column=0, padx=5, pady=5)

    zip_modify = ttk.Button(green_block, text="Modifier", style='Param.TButton',
                           command=lambda: modify("Modifier le code postal", "CP", zip_entry.get(), data_entreprise[0], frame))
    zip_modify.grid(row=7, column=1, padx=5, pady=5)

    # Ville (avec bouton de modification)
    city_label = Label(green_block, text="Ville", bg=entry_bg, font=("Arial", 12, "bold"))
    city_label.grid(row=8, column=0, padx=10, pady=5, sticky="ew")

    city_entry = Entry(green_block, width=30, font=("Arial", 12), state="normal")
    city_entry.insert(0, data_entreprise[4])
    city_entry.config(state="readonly")
    city_entry.grid(row=9, column=0, padx=5, pady=5)

    city_modify = ttk.Button(green_block, text="Modifier", style='Param.TButton',
                            command=lambda: modify("Modifier la ville", "Ville", city_entry.get(), data_entreprise[0], frame))
    city_modify.grid(row=9, column=1, padx=5, pady=5)

    # Téléphone (avec bouton de modification)
    phone_label = Label(green_block, text="Téléphone", bg=entry_bg, font=("Arial", 12, "bold"))
    phone_label.grid(row=10, column=0, padx=10, pady=5, sticky="ew")

    phone_entry = Entry(green_block, width=30, font=("Arial", 12), state="normal")
    phone_entry.insert(0, data_entreprise[5])
    phone_entry.config(state="readonly")
    phone_entry.grid(row=11, column=0, padx=5, pady=5)

    phone_modify = ttk.Button(green_block, text="Modifier", style='Param.TButton',
                             command=lambda: modify("Modifier le téléphone", "Num", phone_entry.get(), data_entreprise[0], frame))
    phone_modify.grid(row=11, column=1, padx=5, pady=5)

    # Email (avec bouton de modification)
    email_label = Label(green_block, text="Email", bg=entry_bg, font=("Arial", 12, "bold"))
    email_label.grid(row=12, column=0, padx=10, pady=5, sticky="ew")

    email_entry = Entry(green_block, width=30, font=("Arial", 12), state="normal")
    email_entry.insert(0, data_entreprise[6])
    email_entry.config(state="readonly")
    email_entry.grid(row=13, column=0, padx=5, pady=5)

    email_modify = ttk.Button(green_block, text="Modifier", style='Param.TButton',
                             command=lambda: modify("Modifier l'email", "Email", email_entry.get(), data_entreprise[0], frame))
    email_modify.grid(row=13, column=1, padx=5, pady=5)

    # SIRET (avec bouton de modification)
    siret_label = Label(green_block, text="SIRET", bg=entry_bg, font=("Arial", 12, "bold"))
    siret_label.grid(row=14, column=0, padx=10, pady=5, sticky="ew")

    siret_entry = Entry(green_block, width=30, font=("Arial", 12), state="normal")
    siret_entry.insert(0, data_entreprise[7])
    siret_entry.config(state="readonly")
    siret_entry.grid(row=15, column=0, padx=5, pady=5)

    siret_modify = ttk.Button(green_block, text="Modifier", style='Param.TButton',
                             command=lambda: modify("Modifier le SIRET", "Siret", siret_entry.get(), data_entreprise[0], frame))
    siret_modify.grid(row=15, column=1, padx=5, pady=5)

    # SIREN (avec bouton de modification)
    siren_label = Label(green_block, text="SIREN", bg=entry_bg, font=("Arial", 12, "bold"))
    siren_label.grid(row=16, column=0, padx=10, pady=5, sticky="ew")

    siren_entry = Entry(green_block, width=30, font=("Arial", 12), state="normal")
    siren_entry.insert(0, data_entreprise[8])
    siren_entry.config(state="readonly")
    siren_entry.grid(row=17, column=0, padx=5, pady=5)

    siren_modify = ttk.Button(green_block, text="Modifier", style='Param.TButton',
                             command=lambda: modify("Modifier le SIREN", "Siren", siren_entry.get(), data_entreprise[0], frame))
    siren_modify.grid(row=17, column=1, padx=5, pady=5)

    # Mot de passe (avec bouton de modification)
    password_label = Label(green_block, text="Mot de passe", bg=entry_bg, font=("Arial", 12, "bold"))
    password_label.grid(row=18, column=0, padx=10, pady=5, sticky="w")

    password_entry = Entry(green_block, width=30, font=("Arial", 12), state="normal", show="*")
    password_entry.insert(0, data_entreprise[9])
    password_entry.config(state="readonly")
    password_entry.grid(row=19, column=0, padx=5, pady=5)

    password_modify = ttk.Button(green_block, text="Modifier", style='Param.TButton',
                               command=lambda: modify("Modifier le mot de passe", "Mdp", password_entry.get(), data_entreprise[0], frame))
    password_modify.grid(row=19, column=1, padx=5, pady=5)

    # Gestion du défilement avec la molette de la souris
    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta/120), "units")
    
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

def verification_nom(nom):
    """Vérifie si le nom est dans le format attendu"""
    pattern = r"^M\. [A-Z][a-z]+ [A-Z][a-z]+ \([A-Z]{2,10}\) \| .+$"
    return re.match(pattern, nom)

def verification_adresse(adresse):
    """Vérifie si l'adresse est dans le format attendu"""
    pattern = r"^\d+\s+[A-Za-zÀ-ÖØ-öø-ÿ\s\-']+$"
    return re.match(pattern, adresse)

def verification_num(num):
    """Vérifie si le numéro de téléphone est dans le format attendu"""
    tel_clean = re.sub(r'[\s.-]', '', num)
    if tel_clean.startswith('0'):
        tel_clean = '+33' + tel_clean[1:]
    return re.fullmatch(r'^\+33[6-7]\d{8}$', tel_clean) is not None

def verification_mail(mail):
    """Vérifie si l'email est dans le format attendu"""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, mail) is not None

def modify(titre, parametre, valeur, id_entreprise, frame):
    """
    Affiche une fenêtre de modification pour un paramètre donné
    Args:
        titre: Titre de la fenêtre
        parametre: Le paramètre à modifier
        valeur: La valeur actuelle du paramètre
        id_entreprise: L'identifiant de l'entreprise
        frame: Le frame parent pour rafraîchir après modification
    """
    top = Toplevel()
    top.title(titre)
    top.geometry("500x400")
    top.configure(bg=background_color)
    top.resizable(False, False)
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico") 

    content_frame = Frame(top, bg=background_color)
    content_frame.pack(pady=20, padx=20)

    # Affichage de l'ancienne valeur
    Label(content_frame, text=f"Ancien {parametre}:", 
         font=('Arial', 12), bg=background_color, fg=text_color).pack(anchor=W)
    
    old_entry = Entry(content_frame, font=('Arial', 12), width=30, bg=entry_bg)
    old_entry.insert(0, valeur)
    old_entry.pack(pady=5)

    # Champ pour la nouvelle valeur
    Label(content_frame, text=f"Nouveau {parametre}:", 
         font=('Arial', 12), bg=background_color, fg=text_color).pack(anchor=W)
    
    new_entry = Entry(content_frame, font=('Arial', 12), width=30, bg=entry_bg)
    new_entry.pack(pady=5)

    # Champ de confirmation
    Label(content_frame, text=f"Confirmer {parametre}:", 
         font=('Arial', 12), bg=background_color, fg=text_color).pack(anchor=W)
    
    confirm_entry = Entry(content_frame, font=('Arial', 12), width=30, bg=entry_bg)
    confirm_entry.pack(pady=5)

    # Boutons de validation/annulation
    btn_frame = Frame(content_frame, bg=background_color)
    btn_frame.pack(pady=20)
    
    ttk.Button(btn_frame, text="Valider", style='Modif.TButton',
              command=lambda: enregistrer_modif()).pack(side=LEFT, padx=10)
    
    ttk.Button(btn_frame, text="Annuler", style='Modif.TButton',
              command=top.destroy).pack(side=LEFT, padx=10)

    def enregistrer_modif():
        """Fonction pour valider et enregistrer les modifications"""
        ancien = old_entry.get()
        nouveau1 = new_entry.get()
        nouveau2 = confirm_entry.get()

        # Vérification des champs remplis
        if not ancien or not nouveau1 or not nouveau2:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return
        
        # Vérification que l'ancienne valeur correspond
        if ancien != valeur:
            messagebox.showerror("Erreur", "L'ancienne valeur est incorrecte")
            return
        
        # Vérification que les nouvelles valeurs correspondent
        if nouveau1 != nouveau2:
            messagebox.showerror("Erreur", "Les nouvelles valeurs ne correspondent pas")
            return

        # Validation spécifique selon le type de paramètre
        if parametre == "Name":
            if not verification_nom(nouveau1):
                messagebox.showerror("Erreur", "Format de nom invalide")
                return
            if not sql.update_name_entreprise(nouveau1, id_entreprise):
                messagebox.showerror("Erreur", "Échec de la mise à jour")
                return
        
        elif parametre == "Adresse":
            if not verification_adresse(nouveau1):
                messagebox.showerror("Erreur", "Format d'adresse invalide")
                return
            if not sql.update_adresse_entreprise(nouveau1, id_entreprise):
                messagebox.showerror("Erreur", "Échec de la mise à jour")
                return
        
        elif parametre == "CP":
            if not nouveau1.isdigit() or len(nouveau1) != 5:
                messagebox.showerror("Erreur", "Code postal invalide (5 chiffres requis)")
                return
            if not sql.update_CP_entreprise(nouveau1, id_entreprise):
                messagebox.showerror("Erreur", "Échec de la mise à jour")
                return
        
        elif parametre == "Ville":
            if not sql.update_ville_entreprise(nouveau1, id_entreprise):
                messagebox.showerror("Erreur", "Échec de la mise à jour")
                return
        
        elif parametre == "Num":
            if not verification_num(nouveau1):
                messagebox.showerror("Erreur", "Format de téléphone invalide")
                return
            if not sql.update_num_entreprise(nouveau1, id_entreprise):
                messagebox.showerror("Erreur", "Échec de la mise à jour")
                return
        
        elif parametre == "Email":
            if not verification_mail(nouveau1):
                messagebox.showerror("Erreur", "Format d'email invalide")
                return
            if not sql.update_email_entreprise(nouveau1, id_entreprise):
                messagebox.showerror("Erreur", "Échec de la mise à jour")
                return
        
        elif parametre == "Siret":
            if not nouveau1.isdigit() or len(nouveau1) != 14:
                messagebox.showerror("Erreur", "SIRET invalide (14 chiffres requis)")
                return
            if not sql.update_siret_entreprise(nouveau1, id_entreprise):
                messagebox.showerror("Erreur", "Échec de la mise à jour")
                return
        
        elif parametre == "Siren":
            if not nouveau1.isdigit() or len(nouveau1) != 9:
                messagebox.showerror("Erreur", "SIREN invalide (9 chiffres requis)")
                return
            if not sql.update_siren_entreprise(nouveau1, id_entreprise):
                messagebox.showerror("Erreur", "Échec de la mise à jour")
                return
        
        elif parametre == "Mdp":
            if not sql.update_mdp_entreprise(nouveau1, id_entreprise):
                messagebox.showerror("Erreur", "Échec de la mise à jour")
                return

        # Affichage du succès et rafraîchissement de la page
        messagebox.showinfo("Succès", "Modification enregistrée avec succès")
        top.destroy()
        page_para(frame, id_entreprise)