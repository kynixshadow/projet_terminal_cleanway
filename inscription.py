# Importation des modules nécessaires
from tkinter import *
from tkinter import messagebox
import module.sql as sql     # Module externe pour interagir avec la base de données
import connexion as co       # Module pour aller vers la page de connexion
import re                    # Pour les vérifications de formats (email, téléphone, etc.)

# Variables globales pour le suivi de l'étape actuelle et des widgets
etape_actuelle = 1
root = None
frame_contenu = None
btn_recommencer = None
btn_suivant = None
etape1_ind = None
etape2_ind = None
etape3_ind = None

# Dictionnaire pour stocker les données de l'utilisateur par étape
donnees_inscription = {
    'etape1': {},
    'etape2': {},
    'etape3': {}
}

# Champs d'entrée (déclarés globalement pour y accéder facilement)
nom_entry = None
prenom_entry = None
denomination_entry = None
num_rue_entry = None
nom_rue_entry = None
code_postal_entry = None
ville_entry = None
telephone_entry = None
email_entry = None
siret_entry = None
siren_entry = None
motdepasse_entry = None
confirmation_mdp_entry = None

# Fonctions de validation des champs
def valider_email(email):
    # Vérifie le format standard d'un email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def valider_telephone(telephone):
    # Nettoie les espaces/points puis valide un numéro français en format international
    tel_clean = re.sub(r'[\s.-]', '', telephone)
    if tel_clean.startswith('0'):
        tel_clean = '+33' + tel_clean[1:]
    return re.fullmatch(r'^\+33[6-7]\d{8}$', tel_clean) is not None

def valider_siret(siret):
    return len(siret) == 14 and siret.isdigit()

def valider_siren(siren):
    return len(siren) == 9 and siren.isdigit()

def valider_code_postal(code):
    return code.isdigit() and len(code) == 5

def valider_chiffres(texte):
    # Utilisé pour autoriser uniquement les chiffres dans certains champs
    return texte.isdigit() or texte == ""

# Navigation vers la page de connexion
def aller_connexion():
    root.destroy()
    co.main()

# Réinitialise le formulaire et les données
def recommencer_inscription():
    global etape_actuelle, donnees_inscription
    
    # Réinitialise les données
    donnees_inscription = {'etape1': {}, 'etape2': {}, 'etape3': {}}
    
    # Vide tous les champs de saisie
    for entry in [nom_entry, prenom_entry, denomination_entry, num_rue_entry, 
                 nom_rue_entry, code_postal_entry, ville_entry, telephone_entry,
                 email_entry, siret_entry, siren_entry, motdepasse_entry, 
                 confirmation_mdp_entry]:
        if entry and entry.winfo_exists(): 
            entry.delete(0, END)
    
    etape_actuelle = 1
    afficher_etape()
    messagebox.showinfo("Information", "Le formulaire a été réinitialisé.")

# Affiche les éléments selon l'étape actuelle
def afficher_etape():
    # Supprime les widgets précédents
    for widget in frame_contenu.winfo_children():
        widget.destroy()
    
    # Style des indicateurs d'étapes
    etape1_ind.config(bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14))
    etape2_ind.config(bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14))
    etape3_ind.config(bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14))
    
    # Affiche l'étape correspondante
    if etape_actuelle == 1:
        etape1_ind.config(bg='#1767AA', fg='white', font=("Roboto", 14, 'bold'))
        afficher_etape1()
        btn_suivant.config(text="Suivant")
    elif etape_actuelle == 2:
        etape2_ind.config(bg='#1767AA', fg='white', font=("Roboto", 14, 'bold'))
        afficher_etape2()
        btn_suivant.config(text="Suivant")
    else:
        etape3_ind.config(bg='#1767AA', fg='white', font=("Roboto", 14, 'bold'))
        afficher_etape3()
        btn_suivant.config(text="S'inscrire")

# ---------- ÉTAPE 1 ----------
def afficher_etape1():
    global nom_entry, prenom_entry, denomination_entry, num_rue_entry, nom_rue_entry
    
    # Champs nom, prénom, entreprise
    Label(frame_contenu, text="Nom", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    nom_entry = Entry(frame_contenu, width=50, font=("Roboto", 12))
    nom_entry.pack(pady=(0, 15), padx=20)
    
    Label(frame_contenu, text="Prénom", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    prenom_entry = Entry(frame_contenu, width=50, font=("Roboto", 12))
    prenom_entry.pack(pady=(0, 15), padx=20)
    
    Label(frame_contenu, text="Dénomination de l'entreprise", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    denomination_entry = Entry(frame_contenu, width=50, font=("Roboto", 12))
    denomination_entry.pack(pady=(0, 15), padx=20)
    
    # Champs adresse
    frame_adresse = Frame(frame_contenu, bg='#3CB1E4')
    frame_adresse.pack(pady=(0, 15), padx=20, fill=X)
    
    Label(frame_adresse, text="Adresse", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, pady=(0, 5))
    frame_rue = Frame(frame_adresse, bg='#3CB1E4')
    frame_rue.pack(fill=X)
    
    # Numéro de rue limité aux chiffres entre 1 et 999
    validate_num = frame_rue.register(valider_chiffres)
    num_rue_entry = Spinbox(frame_rue, from_=1, to=999, width=5, font=("Roboto", 12),
                            validate='key', validatecommand=(validate_num, '%P'))
    num_rue_entry.pack(side=LEFT, padx=(0, 10))
    
    nom_rue_entry = Entry(frame_rue, width=42, font=("Roboto", 12))
    nom_rue_entry.pack(side=LEFT)

# ---------- ÉTAPE 2 ----------
def afficher_etape2():
    global code_postal_entry, ville_entry, telephone_entry, email_entry
    
    # Champs pour code postal, ville, téléphone, email
    Label(frame_contenu, text="Code postal (5 chiffres)", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    validate_chiffres = frame_contenu.register(valider_chiffres)
    code_postal_entry = Entry(frame_contenu, width=50, font=("Roboto", 12),
                              validate='key', validatecommand=(validate_chiffres, '%P'))
    code_postal_entry.pack(pady=(0, 15), padx=20)
    
    Label(frame_contenu, text="Ville", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    ville_entry = Entry(frame_contenu, width=50, font=("Roboto", 12))
    ville_entry.pack(pady=(0, 15), padx=20)
    
    Label(frame_contenu, text="Téléphone (+33 6 12 34 56 78)", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    telephone_entry = Entry(frame_contenu, width=50, font=("Roboto", 12))
    telephone_entry.pack(pady=(0, 15), padx=20)
    
    Label(frame_contenu, text="Email", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    email_entry = Entry(frame_contenu, width=50, font=("Roboto", 12))
    email_entry.pack(pady=(0, 15), padx=20)

# ---------- ÉTAPE 3 ----------
def afficher_etape3():
    global siret_entry, siren_entry, motdepasse_entry, confirmation_mdp_entry
    
    # Champs pour SIRET, SIREN et mot de passe
    Label(frame_contenu, text="SIRET (14 chiffres)", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    siret_entry = Entry(frame_contenu, width=50, font=("Roboto", 12))
    siret_entry.pack(pady=(0, 15), padx=20)
    
    Label(frame_contenu, text="SIREN (9 chiffres)", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    siren_entry = Entry(frame_contenu, width=50, font=("Roboto", 12))
    siren_entry.pack(pady=(0, 15), padx=20)
    
    Label(frame_contenu, text="Mot de passe", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    motdepasse_entry = Entry(frame_contenu, show='*', width=50, font=("Roboto", 12))
    motdepasse_entry.pack(pady=(0, 15), padx=20)

    Label(frame_contenu, text="Confirmation mot de passe", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14)).pack(anchor=W, padx=20, pady=(0, 5))
    confirmation_mdp_entry = Entry(frame_contenu, show='*', width=50, font=("Roboto", 12))
    confirmation_mdp_entry.pack(pady=(0, 15), padx=20)

def valider_etape1():
    # Vérifie si tous les champs requis de l'étape 1 sont remplis
    if not nom_entry.get() or not prenom_entry.get() or not denomination_entry.get() or not num_rue_entry.get() or not nom_rue_entry.get():
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs de l'étape 1.")
        return False
    # Sauvegarde les données dans le dictionnaire
    donnees_inscription['etape1'] = {
        'nom': nom_entry.get(),
        'prenom': prenom_entry.get(),
        'denomination': denomination_entry.get(),
        'numero_rue': num_rue_entry.get(),
        'nom_rue': nom_rue_entry.get()
    }
    return True

def valider_etape2():
    # Vérifie les champs et leur format
    if not code_postal_entry.get() or not ville_entry.get() or not telephone_entry.get() or not email_entry.get():
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs de l'étape 2.")
        return False
    if not valider_code_postal(code_postal_entry.get()):
        messagebox.showerror("Erreur", "Code postal invalide.")
        return False
    if not valider_telephone(telephone_entry.get()):
        messagebox.showerror("Erreur", "Numéro de téléphone invalide.")
        return False
    if not valider_email(email_entry.get()):
        messagebox.showerror("Erreur", "Email invalide.")
        return False
    donnees_inscription['etape2'] = {
        'code_postal': code_postal_entry.get(),
        'ville': ville_entry.get(),
        'telephone': telephone_entry.get(),
        'email': email_entry.get()
    }
    return True

def valider_etape3():
    # Vérification des champs SIRET, SIREN, mot de passe
    if not siret_entry.get() or not siren_entry.get() or not motdepasse_entry.get() or not confirmation_mdp_entry.get():
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs de l'étape 3.")
        return False
    if not valider_siret(siret_entry.get()):
        messagebox.showerror("Erreur", "Numéro SIRET invalide.")
        return False
    if not valider_siren(siren_entry.get()):
        messagebox.showerror("Erreur", "Numéro SIREN invalide.")
        return False
    if motdepasse_entry.get() != confirmation_mdp_entry.get():
        messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
        return False
    donnees_inscription['etape3'] = {
        'siret': siret_entry.get(),
        'siren': siren_entry.get(),
        'motdepasse': motdepasse_entry.get()
    }
    return True

# Fonction appelée quand on clique sur "Suivant" ou "S'inscrire"
def suivant():
    global etape_actuelle
    if etape_actuelle == 1 and valider_etape1():
        etape_actuelle = 2
        afficher_etape()
    elif etape_actuelle == 2 and valider_etape2():
        etape_actuelle = 3
        afficher_etape()
    elif etape_actuelle == 3 and valider_etape3():
        # Enregistrement final dans la base de données
        sql.insert_inscription(donnees_inscription)
        messagebox.showinfo("Succès", "Inscription réussie !")
        root.destroy()
        co.main()

# Fonction principale pour lancer la fenêtre d'inscription
def main():
    global root, frame_contenu, btn_recommencer, btn_suivant
    global etape1_ind, etape2_ind, etape3_ind

    root = Tk()
    root.title("Inscription")
    root.geometry("600x700")
    root.configure(bg='#3CB1E4')

    # Titre principal
    Label(root, text="Inscription", font=("Roboto", 20, 'bold'), bg='#3CB1E4', fg='#2C3E50').pack(pady=(20, 10))

    # Indicateurs d'étapes
    frame_etapes = Frame(root, bg='#3CB1E4')
    frame_etapes.pack(pady=(0, 20))
    etape1_ind = Label(frame_etapes, text="1", width=5, pady=5)
    etape1_ind.pack(side=LEFT, padx=10)
    etape2_ind = Label(frame_etapes, text="2", width=5, pady=5)
    etape2_ind.pack(side=LEFT, padx=10)
    etape3_ind = Label(frame_etapes, text="3", width=5, pady=5)
    etape3_ind.pack(side=LEFT, padx=10)

    # Contenu principal
    frame_contenu = Frame(root, bg='#3CB1E4')
    frame_contenu.pack(fill=BOTH, expand=True)

    # Boutons d'action
    frame_btns = Frame(root, bg='#3CB1E4')
    frame_btns.pack(pady=20)
    btn_recommencer = Button(frame_btns, text="Recommencer", font=("Roboto", 12), command=recommencer_inscription)
    btn_recommencer.pack(side=LEFT, padx=10)
    btn_suivant = Button(frame_btns, text="Suivant", font=("Roboto", 12), command=suivant)
    btn_suivant.pack(side=LEFT, padx=10)
    Button(frame_btns, text="Retour à la connexion", font=("Roboto", 12), command=aller_connexion).pack(side=LEFT, padx=10)

    afficher_etape()  # Affiche la première étape au départ

    root.mainloop()  # Boucle principale Tkinter