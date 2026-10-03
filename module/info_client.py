# Importation des modules nécessaires
from tkinter import *  
import module.sql as sql  

# Fonction pour afficher la fiche d'un client
def fiche_client(frame, id_client, id_entreprise):
    # Crée une nouvelle fenêtre pop-up
    top = Toplevel(frame)
    top.title(f"Fiche client numéro : {id_client}")  # Titre avec l'ID client
    top.geometry("600x600")  # Taille initiale
    top.minsize(600, 600)  # Taille minimale
    top.configure(bg="#3CB1E4")  # Couleur de fond bleue
    top.iconbitmap("IMG/ICONE/logo_sans_fond.ico")  # Icône de l'application

    # Récupère les informations du client depuis la base de données
    info_client = sql.get_info_client(id_client, id_entreprise)

    # Titre "Informations du client"
    title_label_client = Label(top, text="Informations du client", font=("Bold", 16), bg="#3CB1E4", fg="#2C3E50")
    title_label_client.pack(pady=10)  # Ajoute un espace vertical

    # Cadre pour afficher les infos client
    client_frame = Frame(top, bg="white", borderwidth=1, relief="solid", padx=10, pady=10)
    client_frame.pack(padx=20, pady=10, fill="x")  # Remplit horizontalement

    # Si des infos client existent
    if info_client:
        # Formatage des informations client
        client_text = (
            f"ID Client : {info_client[0]}\n"
            f"Nom : {info_client[2]}\n"
            f"Prénom : {info_client[3]}\n"
            f"Téléphone : {info_client[4]}\n"
            f"Adresse : {info_client[5]} {info_client[6]} {info_client[7]}\n"
            f"Statut : {info_client[8]}"
        )

        # Affichage des infos client
        client_label = Label(client_frame, text=client_text, font=("Arial", 12), bg="white", anchor="w", justify="left")
        client_label.pack(fill="x")
    else:
        # Message si aucun client trouvé
        no_client_label = Label(client_frame, text="Aucune information trouvée pour ce client.", font=("Arial", 12), bg="white")
        no_client_label.pack()

    # Titre "Liste des Rendez-vous"
    title_label_rdv = Label(top, text="Liste des Rendez-vous", font=("Bold", 16), bg="#3CB1E4", fg="#2C3E50")
    title_label_rdv.pack(pady=20)

    # Cadre pour la recherche
    search_frame = Frame(top, bg='white')
    search_frame.pack(pady=10)

    # Label "Recherchez par date"
    search_label = Label(search_frame, text="Recherchez par date : ", font=("Arial", 12), bg='white')
    search_label.pack(side="left", padx=5)

    # Champ de saisie pour la recherche
    search_entry = Entry(search_frame, font=("Arial", 12), width=30)
    search_entry.pack(side="left", padx=5)

    # Zone avec ascenseur pour afficher les RDV
    canvas_frame = Frame(top, bg="white")
    canvas_frame.pack(pady=10, fill="both", expand=True)

    # Canvas (zone dessin) pour le défilement
    canvas = Canvas(canvas_frame, bg="#B2CCE4")
    scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#B2CCE4")  # Cadre qui contiendra les RDV

    # Configuration du défilement
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Gestion du redimensionnement
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig("all", width=canvas.winfo_width()))

    # Fonction pour le défilement avec la molette
    def on_mousewheel(event):
        canvas.yview_scroll(-1 * int(event.delta / 120), "units")
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # Fonction pour mettre à jour les résultats des RDV
    def update_results():
        # Efface les anciens résultats
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Récupère le texte de recherche
        search_text = search_entry.get().lower()
       
        # Récupère tous les RDV du client
        list_rdv = sql.get_rdv_fiche_client(id_client, id_entreprise)

        if list_rdv:
            # Filtre les RDV selon la recherche
            filtered_rdv = [
                rdv for rdv in list_rdv
                if search_text in rdv[3]  # Recherche dans la date
            ]

            # Affiche chaque RDV filtré
            for rdv in filtered_rdv:
                # Formatage des infos RDV
                rdv_text = (
                    f"ID Rendez-vous: {rdv[0]}\n"
                    f"Date : {rdv[3]}\n"
                    f"Heure : {rdv[4]}\n"
                    f"Etat : {rdv[5]}\n"
                    f"Adresse : {rdv[6]} {rdv[7]} {rdv[8]}\n"
                    f"Véhicule : {rdv[9]} {rdv[10]} à {rdv[11]} places\n"
                    f"Forfait : {rdv[12]}\n"
                    f"Montant : {rdv[13]}\n"
                    f"Remarque : {rdv[14]}\n"
                )

                # Cadre pour un RDV
                rdv_frame = Frame(scrollable_frame, bg="white", borderwidth=1, relief="solid")
                rdv_frame.pack(fill="x", padx=10, pady=5)

                # Affichage des infos RDV
                rdv_label = Label(rdv_frame, text=rdv_text, font=("Arial", 12), bg="white", anchor="w", justify="left")
                rdv_label.pack(fill="x", padx=10, pady=5)

        else:
            # Message si aucun RDV trouvé
            no_results_label = Label(scrollable_frame, text="Aucun résultat trouvé.", font=("Arial", 12, "italic"), bg="white", fg="gray")
            no_results_label.pack(pady=10)

    # Met à jour les résultats quand on tape dans la recherche
    search_entry.bind("<KeyRelease>", lambda event: update_results())
    # Appel initial pour afficher tous les RDV
    update_results()