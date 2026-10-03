import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Variables globales pour la gestion des images
images = []  # Liste des chemins d'images
index = 0    # Index de l'image courante
label_image = None  # Label pour afficher l'image
root = None  # Fenêtre principale
btn_prec = None  # Bouton précédent
btn_suiv = None  # Bouton suivant
btn_supp = None  # Bouton supprimer
message_label = None  # Label pour les messages

def ouvrir_dossier(chemin_dossier):
    """Charge les images d'un dossier dans la liste"""
    global images, index
    if not os.path.exists(chemin_dossier):
        afficher_message("Le dossier spécifié n'existe pas.")
        return

    # Filtrage des fichiers image
    extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp")
    images[:] = [os.path.join(chemin_dossier, f) for f in os.listdir(chemin_dossier) if f.lower().endswith(extensions)]
    images.sort()
    index = 0

    if images:
        afficher_image()
        # Activation des boutons
        btn_prec.config(state=NORMAL)
        btn_suiv.config(state=NORMAL)
        btn_supp.config(state=NORMAL)
    else:
        afficher_message("Aucune image trouvée dans ce dossier.")
        # Désactivation des boutons
        btn_prec.config(state=DISABLED)
        btn_suiv.config(state=DISABLED)
        btn_supp.config(state=DISABLED)

def afficher_image():
    """Affiche l'image courante avec redimensionnement adaptatif"""
    global label_image
    if not images:
        label_image.config(image='')
        label_image.image = None
        return

    image_path = images[index]
    try:
        # Ouverture de l'image avec PIL
        img = Image.open(image_path)

        # Calcul des dimensions adaptées à la fenêtre
        largeur_fenetre = max(root.winfo_width(), 100)
        hauteur_fenetre = max(root.winfo_height() - 100, 100)

        # Conservation du ratio
        img_ratio = img.width / img.height
        fenetre_ratio = largeur_fenetre / hauteur_fenetre

        if img_ratio > fenetre_ratio:
            new_width = largeur_fenetre - 40
            new_height = int(new_width / img_ratio)
        else:
            new_height = hauteur_fenetre - 40
            new_width = int(new_height * img_ratio)

        # Redimensionnement
        new_width = max(new_width, 1)
        new_height = max(new_height, 1)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        # Affichage
        label_image.config(image=photo)
        label_image.image = photo
        root.title(f"Visionneur - {os.path.basename(image_path)}")
    except Exception as e:
        afficher_message(f"Erreur d'ouverture de l'image : {e}")

def precedent():
    """Affiche l'image précédente"""
    global index
    if index > 0:
        index -= 1
        afficher_image()

def suivant():
    """Affiche l'image suivante"""
    global index
    if index < len(images) - 1:
        index += 1
        afficher_image()

def supprimer_image():
    """Supprime l'image courante après confirmation"""
    global index
    if not images:
        return

    image_path = images[index]
    nom = os.path.basename(image_path)

    # Confirmation de suppression
    confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer l'image '{nom}' ?")
    if confirmation:
        try:
            os.remove(image_path)  # Suppression physique
            del images[index]  # Retrait de la liste
            if index >= len(images):
                index = max(0, len(images) - 1)
            afficher_image()
            if not images:
                afficher_message("Toutes les images ont été supprimées.")
                btn_prec.config(state=DISABLED)
                btn_suiv.config(state=DISABLED)
                btn_supp.config(state=DISABLED)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer l'image : {e}")

def afficher_message(message):
    """Affiche un message à l'utilisateur"""
    global message_label
    if message_label:
        message_label.config(text=message)
    else:
        message_label = Label(root, text=message, fg="red", font=("Arial", 14), bg="#34495E")
        message_label.pack(pady=20)

def lancer_visionneur(chemin_dossier):
    """Lance le visionneur d'images"""
    global root, label_image, btn_prec, btn_suiv, btn_supp, message_label

    # Création de la fenêtre
    root = Toplevel()
    root.geometry("800x600")
    root.minsize(300, 200)
    root.configure(bg="#34495E")
    root.title("Photos Rendez-vous")
    root.iconbitmap("IMG/ICONE/logo_sans_fond.ico")  

    # Label pour l'image
    label_image = Label(root, bg="#34495E")
    label_image.pack(expand=True)

    # Frame pour les boutons
    frame_btn = Frame(root, bg="#34495E")
    frame_btn.pack(pady=10)

    # Bouton précédent
    btn_prec = Button(frame_btn, text="⬅ Précédent", command=precedent, state=DISABLED)
    btn_prec.pack(side=LEFT, padx=10)

    # Bouton supprimer
    btn_supp = Button(frame_btn, text="🗑 Supprimer", command=supprimer_image, state=DISABLED)
    btn_supp.pack(side=LEFT, padx=10)

    # Bouton suivant
    btn_suiv = Button(frame_btn, text="Suivant ➡", command=suivant, state=DISABLED)
    btn_suiv.pack(side=LEFT, padx=10)

    # Chargement initial des images
    ouvrir_dossier(chemin_dossier)
    root.bind("<Configure>", lambda e: afficher_image())

    root.mainloop()