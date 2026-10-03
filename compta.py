# Importations des modules nécessaires
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar  # Pour le sélecteur de date
from tkinter import messagebox
from module.menu_horizontal import ResponsiveMenu  # Menu personnalisé
import module.sql as sql  # Module pour les opérations SQL
import module.explorateur_de_fichier as exp  # Module pour l'explorateur de fichiers
from matplotlib.figure import Figure  # Pour les graphiques
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Intégration matplotlib avec tkinter
import numpy as np
import matplotlib.dates as mdates  # Pour la gestion des dates dans matplotlib
from datetime import datetime  # Pour la manipulation des dates

# Définition des couleurs
background_color = '#3CB1E4'
background_color_menu = '#1767AA'

def open_date_picker(date_entry):
    """
    Ouvre un sélecteur de date et insère la date sélectionnée dans un Entry
    Args:
        date_entry (Entry): Le champ Entry où insérer la date sélectionnée
    """
    def get_date():
        """Récupère la date sélectionnée et l'insère dans le champ Entry"""
        date = cal.get_date() 
        date_entry.delete(0, END)  
        date_entry.insert(0, date)  
        top.destroy() 

    # Création de la fenêtre popup
    top = Toplevel()  
    top.title("Sélection date")  
    top.geometry("400x300")  
    top.minsize(400, 300)  
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico") 
    
    # Widget Calendar pour sélectionner une date
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd') 
    cal.pack(pady=20) 
    
    # Bouton de validation
    button = Button(top, text="Sélectionner", command=get_date) 
    button.pack(pady=10)  

def open_time_picker(time_entry):
    """
    Ouvre un sélecteur d'heure et insère l'heure sélectionnée dans un Entry
    Args:
        time_entry (Entry): Le champ Entry où insérer l'heure sélectionnée
    """
    def get_time():
        """Récupère l'heure sélectionnée et l'insère dans le champ Entry"""
        hour = hour_combobox.get() 
        minute = minute_combobox.get()  
        time_entry.delete(0, END) 
        time_entry.insert(0, f"{hour}:{minute}") 
        top.destroy()

    # Création de la fenêtre popup
    top = Toplevel() 
    top.title("Sélection heure")  
    top.geometry("300x150") 
    top.minsize(300, 150)  
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico") 
    
    # Frame pour les combobox d'heure et minutes
    frame_time = Frame(top)
    frame_time.pack(pady=10) 

    # Combobox pour les heures (00-23)
    hour_combobox = ttk.Combobox(frame_time, values=[f"{i:02d}" for i in range(24)], width=3)  
    hour_combobox.set("00")  
    hour_combobox.pack(side="left", padx=5)  

    # Combobox pour les minutes (00-55 par pas de 5)
    minute_combobox = ttk.Combobox(frame_time, values=[f"{i:02d}" for i in range(0, 60, 5)], width=3) 
    minute_combobox.set("00") 
    minute_combobox.pack(side="left", padx=5) 

    # Bouton de validation
    button = Button(top, text="Sélectionner", command=get_time)  
    button.pack(pady=10)  

def page_compta(frame, entreprise_id):
    """
    Crée la page de comptabilité avec un menu et une zone de contenu
    Args:
        frame (Frame): Le frame parent où afficher la page
        entreprise_id (int): L'identifiant de l'entreprise
    """
    # Frame principal
    compta_frame = Frame(frame, bg='white')
    compta_frame.pack(fill=BOTH, expand=True, side=TOP)

    # Frame pour le menu
    menu_frame = Frame(compta_frame, bg=background_color_menu)
    menu_frame.pack(side=TOP, fill=X)

    # Frame pour le contenu
    content_frame = Frame(compta_frame, bg=background_color)
    content_frame.pack(fill=BOTH, expand=True)

    # Création du menu responsive
    menu = ResponsiveMenu(menu_frame, foreground_color='white', background_color=background_color_menu)
    menu.ajout_bouton("Statistique", lambda: statistique(content_frame, entreprise_id))
    menu.ajout_bouton("Compte", lambda: compte(content_frame, entreprise_id))
    menu.ajout_bouton("Facture", lambda: facture(content_frame))
    
    # Affichage par défaut des statistiques
    statistique(content_frame, entreprise_id)

def statistique(frame, id_entreprise):
    """
    Affiche les statistiques financières sous forme de graphiques
    Args:
        frame (Frame): Le frame où afficher les graphiques
        id_entreprise (int): L'identifiant de l'entreprise
    """
    # Nettoyage du frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Configuration de la grille
    for i in range(2):
        frame.rowconfigure(i, weight=1)
    for j in range(2):
        frame.columnconfigure(j, weight=1)

    def create_error_message(row, col, message):
        """
        Crée un message d'erreur dans une cellule de la grille
        Args:
            row (int): La ligne de la grille
            col (int): La colonne de la grille
            message (str): Le message d'erreur à afficher
        Returns:
            Frame: Le frame contenant le message d'erreur
        """
        error_frame = Frame(frame, bg='white')
        error_frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        error_label = Label(error_frame, text=message, 
                           fg='red', font=('Arial', 10), bg='white')
        error_label.pack(expand=True)
        return error_frame

    # Récupération des données depuis la base de données
    data_revenu = sql.get_stat_revenu(id_entreprise)
    data_depense = sql.get_stat_depense(id_entreprise)

    # Traitement des revenus par mois
    if data_revenu:
        monthly_data_revenue = {}
        for amount_revenue, date_str_revenue in data_revenu:
            try:
                date = datetime.strptime(date_str_revenue, "%Y-%m-%d %H:%M")
            except ValueError:
                date = datetime.strptime(date_str_revenue, "%Y-%m-%d %H:%M:%S")
            month_key_revenue = (date.year, date.month)
            if month_key_revenue in monthly_data_revenue:
                monthly_data_revenue[month_key_revenue] += amount_revenue
            else:
                monthly_data_revenue[month_key_revenue] = amount_revenue

        monthly_values_revenue = []
        monthly_dates_revenue = []
        for (year, month), amount in monthly_data_revenue.items():
            monthly_values_revenue.append(amount)
            monthly_dates_revenue.append(datetime(year, month, 1))

    # Traitement des dépenses par mois
    if data_depense:
        monthly_data_depense = {}
        for amount_depense, date_str_depense in data_depense:
            try:
                date = datetime.strptime(date_str_depense, "%Y-%m-%d %H:%M")
            except ValueError:
                date = datetime.strptime(date_str_depense, "%Y-%m-%d %H:%M:%S")
            month_key_depense = (date.year, date.month)
            if month_key_depense in monthly_data_depense:
                monthly_data_depense[month_key_depense] += amount_depense
            else:
                monthly_data_depense[month_key_depense] = amount_depense
        
        monthly_values_depense = []
        monthly_dates_depense = []
        for (year, month), amount in monthly_data_depense.items():
            monthly_values_depense.append(amount)
            monthly_dates_depense.append(datetime(year, month, 1))

    # Calcul des résultats et du solde cumulé si les deux jeux de données existent
    if data_depense and data_revenu:
        monthly_result = {}
        for (year, month), revenue in monthly_data_revenue.items():
            depense = monthly_data_depense.get((year, month), 0)
            monthly_result[(year, month)] = revenue - depense

        monthly_result_values = []
        monthly_result_dates = []
        for (year, month), result in monthly_result.items():
            monthly_result_values.append(result)
            monthly_result_dates.append(datetime(year, month, 1))

        # Calcul du solde cumulé
        monthly_result_sorted = sorted(monthly_result.items())
        solde_cumule = 0
        solde_values = []
        solde_dates = []
        for (year, month), result in monthly_result_sorted:
            solde_cumule += result
            solde_values.append(solde_cumule)
            solde_dates.append(datetime(year, month, 1))

    # Création du graphique des revenus
    try:
        fig1 = Figure(figsize=(5, 3), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.bar(monthly_dates_revenue, monthly_values_revenue, color='b', label="Revenus")
        ax1.set_title("Revenus par mois")
        ax1.set_xlabel("Mois")
        ax1.set_ylabel("Montant (€)")
        ax1.legend()
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        ax1.xaxis.set_major_locator(mdates.MonthLocator())
        fig1.autofmt_xdate()
        canvas1 = FigureCanvasTkAgg(fig1, master=frame)
        canvas_widget1 = canvas1.get_tk_widget()
        canvas_widget1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    except Exception as e:
        create_error_message(0, 0, f"Impossible de générer\nle graphique des revenus \n{e}")

    # Création du graphique des dépenses
    try:
        fig2 = Figure(figsize=(5, 3), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.bar(monthly_dates_depense, monthly_values_depense, color='r', label="Dépenses")
        ax2.set_title("Dépenses par mois")
        ax2.set_xlabel("Mois")
        ax2.set_ylabel("Montant (€)")
        ax2.legend()
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        ax2.xaxis.set_major_locator(mdates.MonthLocator())
        fig2.autofmt_xdate()
        canvas2 = FigureCanvasTkAgg(fig2, master=frame)
        canvas_widget2 = canvas2.get_tk_widget()
        canvas_widget2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    except Exception as e:
        create_error_message(0, 1, f"Impossible de générer\nle graphique des dépenses \n{e}")

    # Création du graphique des résultats (revenus - dépenses)
    try:
        fig3 = Figure(figsize=(5, 3), dpi=100)
        ax3 = fig3.add_subplot(111)
        ax3.bar(monthly_result_dates, monthly_result_values, color='g', label="Résultat")
        ax3.set_title("Résultat par mois\n(Revenus - Dépenses)")
        ax3.set_xlabel("Mois")
        ax3.set_ylabel("Montant (€)")
        ax3.legend()
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        ax3.xaxis.set_major_locator(mdates.MonthLocator())
        fig3.autofmt_xdate()
        canvas3 = FigureCanvasTkAgg(fig3, master=frame)
        canvas_widget3 = canvas3.get_tk_widget()
        canvas_widget3.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    except Exception as e:
        create_error_message(1, 0, f"Impossible de générer\nle graphique des résultats \n{e}")

    # Création du graphique du solde cumulé
    try:
        fig4 = Figure(figsize=(5, 3), dpi=100)
        ax4 = fig4.add_subplot(111)
        ax4.plot(solde_dates, solde_values, marker='o', linestyle='-', color='purple', label="Solde cumulé")
        ax4.set_title("Solde cumulé\nà la fin de chaque mois")
        ax4.set_xlabel("Mois")
        ax4.set_ylabel("Montant (€)")
        ax4.legend()
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        ax4.xaxis.set_major_locator(mdates.MonthLocator())
        fig4.autofmt_xdate()
        canvas4 = FigureCanvasTkAgg(fig4, master=frame)
        canvas4.get_tk_widget().grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    except Exception as e:
        create_error_message(1, 1, f"Impossible de générer\nle graphique du solde \n{e}")

def facture(frame):
    """
    Affiche la page de gestion des factures avec un explorateur de fichiers
    """
    # Nettoyage du frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Création du frame principal
    main_frame = Frame(frame, bg='white')
    main_frame.pack(fill=BOTH, expand=True)

    # Titre de la page
    Label(main_frame, text="Gestion des Factures", font=('Bold', 18), bg='white').pack(pady=20)

    # Frame pour l'explorateur de fichiers
    explorer_frame = Frame(main_frame, bg='white')
    explorer_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

    # Lancement de l'explorateur de fichiers
    exp.demarrer_explorateur(explorer_frame)
    
def compte(frame, id_entreprise):
    """
    Affiche la page de gestion des comptes avec la liste des transactions
    """
    # Nettoyage du frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Récupération et tri des transactions
    liste_transaction = sql.get_all_transaction(id_entreprise)
    liste_transaction.sort(key=lambda x: x[4], reverse=True)  # Tri par date (du plus récent)

    # Calcul du solde
    solde = 0
    for transaction in liste_transaction:
        if transaction[2] == "+":  # Crédit
            solde = solde + transaction[3]
        elif transaction[2] == "-":  # Débit
            solde = solde - transaction[3]

    # Frame pour l'en-tête (solde + boutons)
    frame_haut = Frame(frame, bg=background_color)
    frame_haut.pack(fill=X)

    # Configuration de la grille pour l'en-tête
    frame_haut.grid_columnconfigure(0, weight=1)
    frame_haut.grid_columnconfigure(1, weight=1)
    frame_haut.grid_columnconfigure(2, weight=1)

    # Affichage du solde
    title_solde = Label(frame_haut, text=f"Solde : {solde}", fg='#2C3E50', bg=background_color, font=('Bold', 18))
    title_solde.grid(row=0, column=1, sticky="nsew")

    # Bouton Supprimer
    btn_supp = Button(frame_haut, text="Supprimer", bg='red', fg='white', font=('Bold', 14), 
                     command=lambda: supprimer_transaction(frame, id_entreprise))
    btn_supp.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Bouton Ajouter
    btn_ajout = Button(frame_haut, text="Ajouter", bg='green', fg='white', font=('Bold', 14), 
                     command=lambda: ajout_transaction(frame, id_entreprise))
    btn_ajout.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

    # Frame pour la recherche
    search_frame = Frame(frame, bg='white')
    search_frame.pack(pady=10)

    # Champ de recherche
    search_label = Label(search_frame, text="Recherchez par date, montant ou description: ", 
                        font=("Arial", 12), bg='white')
    search_label.pack(side="left", padx=5)

    search_entry = Entry(search_frame, font=("Arial", 12), width=30)
    search_entry.pack(side="left", padx=5)

    # Frame pour le canvas avec scrollbar
    canvas_frame = Frame(frame, bg="white")
    canvas_frame.pack(pady=10, fill="both", expand=True)

    # Configuration du système de défilement
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

        # Filtrage des transactions
        search_text = search_entry.get().lower()
        filtered_transaction = [
            transaction for transaction in liste_transaction
            if (search_text in str(transaction[3]).lower() or  # Montant
                search_text in str(transaction[4]).lower() or  # Date
                search_text in str(transaction[6]).lower())    # ID Facture
        ]

        if filtered_transaction:
            # Affichage des transactions filtrées
            for transaction in filtered_transaction:
                id_facture = transaction[6] if len(transaction) > 6 and transaction[6] is not None else "None"

                # Formatage des informations de la transaction
                transaction_text = (
                    f"ID: {transaction[0]}\n"
                    f"Entreprise ID: {transaction[1]}\n"
                    f"Montant: {transaction[2]} {transaction[3]}\n"
                    f"Le : {transaction[4]}\n"
                    f"Description: {transaction[5]}\n"
                    f"ID Facture: {id_facture}\n"
                )

                # Création d'un frame pour chaque transaction
                transaction_frame = Frame(scrollable_frame, bg="white", borderwidth=1, relief="solid")
                transaction_frame.pack(fill="x", padx=10, pady=5)

                rdv_label = Label(transaction_frame, text=transaction_text, font=("Arial", 12), 
                                 bg="white", anchor="w", justify="left")
                rdv_label.pack(fill="x", padx=10, pady=5)
        else:
            # Message si aucun résultat
            no_results_label = Label(scrollable_frame, text="Aucun résultat trouvé.", 
                                   font=("Arial", 12, "italic"), bg="white", fg="gray")
            no_results_label.pack(pady=10)

    # Liaison de la recherche à la mise à jour des résultats
    search_entry.bind("<KeyRelease>", lambda event: update_results())
    update_results()  # Affichage initial

def ajout_transaction(frame, id_entreprise):
    """
    Ouvre une fenêtre pour ajouter une nouvelle transaction
    """
    # Création de la fenêtre popup
    top = Toplevel(frame)  
    top.title("Ajouter une transaction") 
    top.geometry("600x500") 
    top.minsize(600, 500) 
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico") 
    top.configure(bg="#F0F0F0")
    
    # Titre de la fenêtre
    title_label = Label(top, text="Ajouter une transaction", font=("Bold", 16), bg="#F0F0F0", fg="#2C3E50")
    title_label.pack(pady=10)

    # Frame pour le formulaire
    form_frame = Frame(top, bg="#F0F0F0")
    form_frame.pack(pady=5, padx=20, fill="x")

    # Configuration de la grille du formulaire
    form_frame.columnconfigure(1, weight=1)
    form_frame.columnconfigure(2, minsize=80)

    # Champ Type (+/-)
    type_label = Label(form_frame, text="Type :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    type_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    type_combobox = ttk.Combobox(form_frame, values=["+", "-"], state="readonly", font=("Arial", 12), width=5)
    type_combobox.current(0)  # Sélection par défaut
    type_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Champ Montant
    montant_label = Label(form_frame, text="Montant :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    montant_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    montant_spinbox = Spinbox(form_frame, from_=0.00, to=10000000.00, increment=0.01, font=("Arial", 12), width=10)
    montant_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Champ Date avec sélecteur
    date_label = Label(form_frame, text="Date :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    date_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    date_entry = Entry(form_frame, font=("Arial", 12), width=12)
    date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    date_button = Button(form_frame, text="Date", font=("Arial", 10), bg="#3CB1E4", fg="white", 
                         command=lambda: open_date_picker(date_entry), width=6)
    date_button.grid(row=2, column=2, padx=5, pady=5)

    # Champ Heure avec sélecteur
    heure_label = Label(form_frame, text="Heure :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    heure_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    heure_entry = Entry(form_frame, font=("Arial", 12), width=8)
    heure_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    heure_button = Button(form_frame, text="Heure", font=("Arial", 10), bg="#3CB1E4", fg="white", 
                          command=lambda: open_time_picker(heure_entry), width=6)
    heure_button.grid(row=3, column=2, padx=5, pady=5)

    # Champ Description
    description_label = Label(form_frame, text="Description :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    description_label.grid(row=4, column=0, padx=5, pady=5, sticky="nw")

    description_entry = Text(form_frame, height=3, font=("Arial", 12), width=30)
    description_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
    description_entry.insert("1.0", "Sans remarque")  # Valeur par défaut

    # Bouton de validation
    ajouter_btn = Button(top, text="Ajouter Transaction", font=("Arial", 12), bg="#4CAF50", fg="white", 
                         command=lambda: ajout_transaction_action())
    ajouter_btn.pack(pady=10, padx=20, fill="x")

    def ajout_transaction_action():
        """
        Valide et enregistre la nouvelle transaction
        """
        # Récupération des valeurs
        types = type_combobox.get().strip()  
        montant = montant_spinbox.get()
        date = date_entry.get()
        heure = heure_entry.get()
        date_heure = f"{date} {heure}"  # Combinaison date + heure
        description_text = description_entry.get("1.0", "end-1c")
        id_facture = None

        # Validation du type
        if types not in ['+', '-']:
            messagebox.showerror("Erreur", "❌ Le type doit être '+' ou '-'")
            return

        # Validation des champs obligatoires
        if types and montant and date and heure and description_text:
            # Enregistrement en base de données
            if sql.add_transaction(id_entreprise, types, montant, date_heure, description_text, id_facture):
                messagebox.showinfo("Succès", "✅ La transaction a été ajoutée avec succès.")
                top.destroy()
                compte(frame, id_entreprise)  # Rafraîchissement de la page
            else:
                messagebox.showerror("Erreur", "❌ Échec de l'ajout de la transaction. Veuillez réessayer.")
        else:
            messagebox.showerror("Erreur", "❌ Veuillez remplir tous les champs.")
            
def supprimer_transaction(frame, id_entreprise):
    """
    Ouvre une fenêtre pour supprimer une transaction spécifique
    """
    # Création de la fenêtre popup
    top = Toplevel(frame)  
    top.title("Supprimer une transaction") 
    top.geometry("500x400") 
    top.minsize(500, 400) 
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico") 
    top.configure(bg="#F0F0F0") 
    
    # Titre de la fenêtre
    title_label = Label(top, text="Supprimer une transaction", font=("Bold", 16), bg="#F0F0F0", fg="#2C3E50")
    title_label.pack(pady=20)  

    # Frame pour le formulaire de recherche
    form_frame = Frame(top, bg="#F0F0F0")
    form_frame.pack(pady=10, padx=20, fill="x")

    # Champ pour l'ID de la transaction
    id_label = Label(form_frame, text="ID de la transaction :", font=("Arial", 12), bg="#F0F0F0", fg="#2C3E50")
    id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Spinbox pour saisir l'ID
    id_spinbox = Spinbox(form_frame, from_=1, to=1000000, increment=1, font=("Arial", 12), width=10)
    id_spinbox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Bouton de recherche
    rechercher_btn = Button(form_frame, text="Rechercher", font=("Arial", 12), bg="#3CB1E4", fg="white", 
                          command=lambda: rechercher_transaction())
    rechercher_btn.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    # Frame pour afficher les informations de la transaction
    info_frame = Frame(top, bg="#FFFFFF", bd=2, relief="solid")
    info_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Label d'information (vide au départ)
    info_label = Label(info_frame, text="Aucune transaction sélectionnée.", font=("Arial", 12), 
                      bg="#FFFFFF", fg="#2C3E50", justify="left")
    info_label.pack(pady=20, padx=20)

    # Bouton de suppression (désactivé au départ)
    supprimer_btn = Button(top, text="Supprimer", font=("Arial", 12), bg="#FF4D4D", fg="white", 
                          state=DISABLED, command=lambda: confirmer_suppression())
    supprimer_btn.pack(pady=10, padx=20, fill="x")

    def rechercher_transaction():
        """
        Recherche une transaction par son ID et affiche ses informations
        """
        transaction_id = id_spinbox.get().strip()
        
        # Récupération de la transaction depuis la base de données
        transaction = sql.get_transaction_by_id(transaction_id)
        
        # Vérification si la transaction existe
        if not transaction:
            messagebox.showerror("Erreur", "❌ Aucune transaction trouvée avec cet ID.")
            info_label.config(text="Aucune transaction sélectionnée.", fg="#2C3E50")
            supprimer_btn.config(state=DISABLED)
            return

        # Formatage des informations de la transaction
        info_text = (
            f"ID: {transaction[0]}\n"
            f"Type: {transaction[2]}\n"
            f"Montant: {transaction[3]}\n"
            f"Date: {transaction[4]}\n"
            f"Description: {transaction[5]}\n"
            f"ID Facture: {transaction[6] if transaction[6] else 'Aucun'}"
        )

        # Mise à jour de l'affichage
        info_label.config(text=info_text, fg="#2C3E50")
        supprimer_btn.config(state=NORMAL)  # Activation du bouton supprimer

    def confirmer_suppression():
        """
        Confirme et exécute la suppression de la transaction
        """
        transaction_id = id_spinbox.get().strip()
        
        # Boîte de dialogue de confirmation
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette transaction ?"):
            # Tentative de suppression en base de données
            if sql.delete_transaction(transaction_id):
                messagebox.showinfo("Succès", "✅ La transaction a été supprimée avec succès.")
                top.destroy()
                compte(frame, id_entreprise)  # Rafraîchit la page des comptes
            else:
                messagebox.showerror("Erreur", "❌ Échec de la suppression de la transaction.")