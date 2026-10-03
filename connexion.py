# Importation des modules nécessaires
from tkinter import *
from tkinter import messagebox
import module.sql as sql  # Module pour les opérations SQL
import inscription as ins  # Module pour la page d'inscription
import app  # Module pour l'application principale
import re  # Module pour les expressions régulières

def valider_email(email):
    """
    Valide le format d'un email à l'aide d'une expression régulière
    """
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    match = re.match(regex, email)
    return match is not None

def verifier_utilisateur(email, mdp):
    """
    Vérifie si l'utilisateur existe et si le mot de passe correspond
    """
    mdp_db = sql.get_mdp_with_mail(email)  # Récupère le mot de passe associé à l'email
    
    # Compare le mot de passe saisi avec celui en base de données
    if mdp == mdp_db:
        return True
    else:
        return False

def connexion_action(email, mdp, root):
    """
    Gère l'action de connexion lorsque l'utilisateur clique sur le bouton
    """
    email_txt = email.get()
    mdp_txt = mdp.get()
    
    # Vérification que les champs ne sont pas vides
    if not email_txt or not mdp_txt:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return
    
    # Validation de l'email
    if valider_email(email_txt):
        # Vérification des identifiants
        if verifier_utilisateur(email_txt, mdp_txt):
            messagebox.showinfo("Succès", "Connexion réussie !")
            id = sql.get_id_with_mail(email_txt)  # Récupération de l'ID utilisateur
            print(id)
            root.destroy()  # Fermeture de la fenêtre de connexion
            app.main(id)  # Lancement de l'application principale
        else:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")
    else:
        messagebox.showerror("Erreur", "L'email saisi est invalide.")

def aller_inscrir(root):
    """
    Redirige vers la page d'inscription
    """
    root.destroy()
    ins.main()  # Lancement de la page d'inscription

def main():
    """
    Fonction principale qui crée et configure la fenêtre de connexion
    """
    # Création et configuration de la fenêtre principale
    root = Tk()
    root.title("CleanWay | Connexion")
    root.geometry("1150x650")
    root.minsize(1150, 650)
    root.config(background='#4065A4')  # Couleur de fond bleu foncé

    # Création du cadre principal pour le formulaire de connexion
    connexion = Frame(root, bg='#3CB1E4', bd=10, relief=RAISED)
    connexion.place(relx=0.5, rely=0.5, anchor=CENTER)  # Centrage du cadre

    # Titre de la page de connexion
    titre_connexion = Label(connexion, text="Connexion", font=("Roboto", 24, 'bold'), bg='#3CB1E4', fg='#2C3E50')
    titre_connexion.pack(pady=(20, 30))

    # Champ pour l'email
    email_label = Label(connexion, text="Email", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14))
    email_label.pack(anchor=W, padx=20)

    email = Entry(connexion, width=50, font=("Roboto", 12))
    email.pack(pady=(0, 20), padx=20)

    # Champ pour le mot de passe
    mdp_label = Label(connexion, text="Mot de passe", bg='#3CB1E4', fg='#2C3E50', font=("Roboto", 14))
    mdp_label.pack(anchor=W, padx=20)

    mdp = Entry(connexion, width=50, font=("Roboto", 12), show='*')  # Les caractères sont masqués
    mdp.pack(pady=(0, 20), padx=20)

    # Bouton de connexion
    connexion_button = Button(connexion, text="Se connecter", font=("Roboto", 14, 'bold'), 
                            bg='#1767AA', fg='white', relief=FLAT, 
                            command=lambda: connexion_action(email, mdp, root))
    connexion_button.pack(pady=20)

    # Lien vers la page d'inscription
    btn_connexion = Button(connexion, text="Pas inscrit ? S'inscrire", 
                         font=("Roboto", 10, "underline"), bg='#3CB1E4', fg='#2C3E50',
                         bd=0, command=lambda: aller_inscrir(root), cursor="hand2")
    btn_connexion.pack()

    # Lancement de la boucle principale
    root.mainloop()