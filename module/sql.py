
# Importation du module SQLite
from sqlite3 import *

# Connexion à la base de données
conn = connect('DB/CleanWay.db')
# Création d'un curseur pour exécuter les requêtes
cur = conn.cursor()

def get_rdv_ie(id):
    """
    Récupère tous les rendez-vous d'une entreprise
    """
    try:
        # Exécution de la requête SQL
        cur.execute('SELECT * FROM Rendezvous WHERE entreprise_id = ?', (id,))
        rdv_list = cur.fetchall()
        if rdv_list:
            return rdv_list
        else:
            print('Aucune information trouvé : get_rdv_ie')
            return None
    except OperationalError as e:
        print(f'Erreur SQL get_rdv_ie : {e}')

def get_date_rdv(id):
    """
    Récupère la date et l'heure d'un rendez-vous spécifique
    """
    try:
        cur.execute('SELECT date, heure FROM Rendezvous WHERE id = ?', (id,))
        rdv = cur.fetchone()
        if rdv:
            return rdv
        else:
            print('Aucune information trouvé : get_date_rdv')
            return None
    except OperationalError as e:
        print(f'Erreur SQL get_date_rdv : {e}')

def get_rdv_confirmed_ie(id):
    """
    Récupère les rendez-vous confirmés d'une entreprise
    """
    try:
        cur.execute('SELECT * FROM Rendezvous WHERE entreprise_id = ? AND etat = "Confirmé"', (id,))
        rdv_list = cur.fetchall()
        if rdv_list:
            return rdv_list
        else:
            print('Aucune information trouvé : get_rdv_confirmed_ie')
            return None
    except OperationalError as e:
        print(f'Erreur SQL get_rdv_confirmed_ie : {e}')

def pass_rdv(id_rdv):
    """
    Marque un rendez-vous comme "Passé"
    """
    try:
        # Vérification que le rendez-vous existe
        cur.execute("SELECT id FROM Rendezvous WHERE id = ?", (id_rdv,))
        if not cur.fetchone():
            print(f"Aucun rendez-vous trouvé avec l'ID {id_rdv}. (pass_rdv)")
            return False

        # Mise à jour du statut
        cur.execute("UPDATE Rendezvous SET etat = 'Passé' WHERE id = ?", (id_rdv,))
        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False

    except OperationalError as e:
        print(f"Erreur SQL add_rdv : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité add_rdv : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def delete_rdv(id_rdv):
    """
    Supprime un rendez-vous
    """
    try:
        # Vérification que le rendez-vous existe
        cur.execute("SELECT id FROM Rendezvous WHERE id = ?", (id_rdv,))
        if not cur.fetchone():
            print(f"Aucun rendez-vous trouvé avec l'ID {id_rdv}. (delete_rdv)")
            return False

        # Suppression du rendez-vous
        cur.execute("DELETE FROM Rendezvous WHERE id = ?", (id_rdv,))
        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False

    except OperationalError as e:
        print(f"Erreur SQL delete_rdv : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité delete_rdv : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def update_rdv(client_id, entreprise_id, date, heure, etat, num_rue, code_postale, ville, marque, modele, nbre_siege, forfait, montant, remarque_valeur, id_rdv):
    """
    Met à jour les informations d'un rendez-vous
    """
    try:
        # Mise à jour complète du rendez-vous
        cur.execute("""UPDATE Rendezvous
                    SET client_id = ?, entreprise_id = ?, date = ?, heure = ?, etat = ?, num_rue = ?,
                    code_postale = ?, ville = ?, marque = ?, modele = ?, nbre_siege = ?,
                    forfait = ?, montant = ?, remarque = ?
                    WHERE id = ?""", (client_id, entreprise_id, date, heure, etat, num_rue, code_postale, ville, marque, modele, nbre_siege, forfait, montant, remarque_valeur, id_rdv))

        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False

    except OperationalError as e:
        print(f"Erreur SQL update_rdv : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_rdv : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def get_rdv_fiche_client(id_client, id_entreprise):
    """
    Récupère les rendez-vous d'un client spécifique pour une entreprise
    """
    try:
        cur.execute('SELECT * FROM Rendezvous WHERE client_id = ? AND entreprise_id = ?', (id_client, id_entreprise,))
        rdv_list = cur.fetchall()
        if rdv_list:
            return rdv_list
        else:
            print('Aucune information trouvé : get_rdv_fiche_client')
            return None
    except OperationalError as e:
        print(f'Erreur SQL get_rdv_fiche_client : {e}')

def add_rdv(client_id, entreprise_id, date, heure, etat, num_rue, code_postale, ville, marque, modele, nbre_siege, forfait, montant, remarque):
    """
    Ajoute un nouveau rendez-vous
    """
    try:
        # Insertion du nouveau rendez-vous
        cur.execute("""INSERT INTO Rendezvous(client_id, entreprise_id, date, heure, etat, num_rue, code_postale, ville, marque, modele, nbre_siege, forfait, montant, remarque)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (client_id, entreprise_id, date, heure, etat, num_rue, code_postale, ville, marque, modele, nbre_siege, forfait, montant, remarque,))
        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL add_rdv : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité add_rdv : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def get_all_id_name(id):
    """
    Récupère les ID, noms et prénoms de tous les clients d'une entreprise
    """
    try:
        cur.execute("SELECT id, nom, prenom FROM Clients WHERE entreprise_id = ?", (id,))
        list_client = cur.fetchall()
        if list_client:
            return list_client
        else:
            print('Aucun information trouvé : get_all_id_name')
            return None
    except OperationalError as e:
        print(f'Erreur SQL get_all_id_name : {e}')

def get_all_client_with_id(id_entreprise):
    """
    Récupère tous les clients actifs d'une entreprise
    """
    try:
        cur.execute("SELECT * FROM Clients WHERE entreprise_id = ? AND statut = 1", (id_entreprise,))
        list_client = cur.fetchall()
        if list_client:
            return list_client
        else:
            print('Aucun information trouvé : get_all_client_with_id')
            return None
    except OperationalError as e:
        print(f'Erreur SQL get_all_client : {e}')

def get_info_client(id_client, id_entreprise):
    """
    Récupère les informations détaillées d'un client spécifique
    """
    try:
        cur.execute("SELECT * FROM Clients WHERE id = ? AND entreprise_id = ?", (id_client, id_entreprise,))
        info_client = cur.fetchone()
        if info_client:
            return info_client
        else:
            print('Aucun information trouvé : get_info_client')
            return None
    except OperationalError as e:
        print(f'Erreur SQL get_all_client : {e}')

def update_client(id, nom, prenom, telephone, num_rue, code_postale, ville):
    """
    Met à jour les informations d'un client
    """
    try:
        cur.execute("""UPDATE Clients
                    SET nom = ?, prenom = ?, telephone = ?, num_rue = ?, code_postale = ?, ville = ?
                    WHERE id = ?""", (nom, prenom, telephone, num_rue, code_postale, ville, id))
       
        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False

    except OperationalError as e:
        print(f"Erreur SQL update_client : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_client : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def delete_client(id_client, id_entreprise):
    """
    Désactive un client (soft delete) en mettant statut à 0
    """
    try:
        cur.execute("UPDATE Clients SET statut = 0 WHERE id = ? AND entreprise_id = ?", (id_client, id_entreprise))
        conn.commit()

        if cur.rowcount == 1:  
            return True  
        else:
            return False  

    except OperationalError as e:
        print(f"Erreur SQL delete_client : {e}")  
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité delete_client : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def add_client(entreprise_id, nom, prenom, telephone, num_rue, code_postale, ville):
    """
    Ajoute un nouveau client
    """
    try:
        statut = True  # Client actif par défaut
        cur.execute("""INSERT INTO Clients (entreprise_id, nom, prenom, telephone, num_rue, code_postale, ville, statut)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (entreprise_id, nom, prenom, telephone, num_rue, code_postale, ville, statut))

        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL add_client : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité add_client : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue add_client : {e}")
        return False

def get_all_marque():
    """
    Récupère toutes les marques disponibles
    """
    try:
        cur.execute("SELECT * FROM Marque")
        list_marque = cur.fetchall()
        if list_marque:
            return list_marque
        else:
            print('Aucun information trouvé : get_all_marque')
            return None
    except OperationalError as e:
        print(f'Erreur SQL get_all_marque : {e} ')

def add_marque(nom_marque):
    """
    Ajoute une nouvelle marque
    """
    try:
        cur.execute("INSERT INTO Marque (Marques) VALUES (?)", (nom_marque,))
        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f'Erreur SQL add_marque : {e} ')

def get_all_modele_by_marque(id_marque):
    """
    Récupère tous les modèles d'une marque spécifique
    """
    try:
        cur.execute("SELECT ID_Modele, Modeles FROM Modele WHERE ID_Marque = ?", (id_marque,))
        list_modele = cur.fetchall()
        if list_modele:
            return list_modele
        else:
            print('Aucun information trouvé : get_all_modele_by_marque')
            return None
    except OperationalError as e:
        print(f'Erreur SQL get_all_modele_by_marque : {e}')

def add_modele(nom_modele, id_marque, longueur, largeur, hauteur):
    """
    Ajoute un nouveau modèle avec ses dimensions
    """
    try:
        cur.execute("""INSERT INTO Modele (Modeles, ID_Marque, Longueur, Largeur, Hauteur)
                    VALUES (?, ?, ?, ?, ?)""",
                    (nom_modele, id_marque, longueur, largeur, hauteur))
        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f'Erreur SQL add_modele : {e} ')

def get_all_transaction(id_entreprise):
    """
    Récupère toutes les transactions d'une entreprise spécifique
    """
    try:
        cur.execute("SELECT * FROM Transactions WHERE entreprise_id = ?", (id_entreprise,))
        liste_transaction = cur.fetchall()
        if liste_transaction:
            return liste_transaction
        else:
            print('Aucun information trouvé : get_all_transaction')
            return None
    except OperationalError as e:
        print(f"Erreur SQL get_all_transaction : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue get_all_transaction : {e}")
        return False

def add_transaction(id_entreprise, types, montant, date, description, id_facture):
    """
    Ajoute une nouvelle transaction dans la base de données
    """
    try:
        cur.execute("""INSERT INTO Transactions (entreprise_id, type, montant, date, description, id_facture)
                        VALUES (?, ?, ?, ?, ?, ?)""", (id_entreprise, types, montant, date, description, id_facture,))
        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL add_transaction : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité add_transaction : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue add_transaction : {e}")
        return False

def delete_transaction(transaction_id):
    """
    Supprime une transaction de la base de données
    """
    try:
        cur.execute("DELETE FROM Transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erreur lors de la suppression de la transaction : {e}")
        return False

def get_transaction_by_id(transaction_id):
    """
    Récupère une transaction spécifique par son ID
    """
    try:
        cur.execute("SELECT * FROM Transactions WHERE id = ?", (transaction_id,))
        transaction =  cur.fetchone()
        return transaction
    except Exception as e:
        print(f"Erreur lors de la récupération de la transaction : {e}")
        return None

def get_stat_revenu(id_entreprise):
    """
    Récupère les statistiques de revenus d'une entreprise
    """
    try:
        cur.execute("SELECT montant, date FROM Transactions WHERE type = '+' AND entreprise_id = ?", (id_entreprise,))
        liste_stat = cur.fetchall()
        if liste_stat:
            return liste_stat
        else:
            print("Aucun resultat trouvé avec cette id : get_stat_revenu")
    except OperationalError as e:
        print(f"Erreur SQL get_all_transaction : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def get_stat_depense(id_entreprise):
    """
    Récupère les statistiques de dépenses d'une entreprise
    """
    try:
        cur.execute("SELECT montant, date FROM Transactions WHERE type = '-' AND entreprise_id = ?", (id_entreprise,))
        liste_stat = cur.fetchall()
        if liste_stat:
            return liste_stat
        else:
            print("Aucun resultat trouvé avec cette id : get_stat_depense")
    except OperationalError as e:
        print(f"Erreur SQL get_all_transaction : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def get_mdp_with_mail(mail):
    """
    Récupère le mot de passe hashé d'une entreprise via son email
    """
    mail = mail.lower()
    try:
        cur.execute("SELECT motdepasse FROM Entreprises WHERE email = ?", (mail,))
        mdp = cur.fetchone()
        if mdp:
            return mdp[0]
        else:
            print("Aucun resultat trouvé avec ce mail : get_mdp_with_mail")
    except OperationalError as e:
        print(f"Erreur SQL get_mdp_with_mail : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def get_id_with_mail(mail):
    """
    Récupère l'ID d'une entreprise via son email
    """
    mail = mail.lower()
    try:
        cur.execute("SELECT id FROM Entreprises WHERE email = ?", (mail,))
        id = cur.fetchone()
        if id:
            return id[0]
        else:
            print("Aucun resultat trouvé avec ce mail : get_id_with_mail")
    except OperationalError as e:
        print(f"Erreur SQL get_id_with_mail : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def add_entreprise(denomination, num_rue, cp, ville, telephone, email, siret, siren, mdp):
    """
    Ajoute une nouvelle entreprise dans la base de données
    """
    try:
        cur.execute("""INSERT INTO Entreprises (denomination, num_rue, code_postale, ville, telephone, email, siret, siren, motdepasse)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (denomination, num_rue, cp, ville, telephone, email, siret, siren, mdp, ))
        conn.commit()

        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL add_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité add_transaction : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def get_denomination(id_entreprise):
    """
    Récupère le nom d'une entreprise via son ID
    """
    try:
        cur.execute("SELECT denomination FROM Entreprises WHERE id = ?", (id_entreprise,))
        denomination = cur.fetchone()
        if denomination:
            return denomination[0]
        else:
            print("Aucun resultat trouvé avec cette id : get_denomination")
            return False
    except OperationalError as e:
        print(f"Erreur SQL get_denomincation : {e}")
        return False
    except Exception as e:
        print(f'Erreur inattendu : {e}')
        return False

def get_entreprise_data(id_entreprise):
    """
    Récupère toutes les données d'une entreprise
    """
    try:
        cur.execute("SELECT * FROM Entreprises WHERE id = ?", (id_entreprise,))
        data_entreprise = cur.fetchone()
        if data_entreprise:
            return data_entreprise
        else:
            return None
    except Exception as e:
        print(f"Erreur get_entreprise_data: {e}")
        return None

def update_name_entreprise(nom, id_entreprise):
    """Met à jour le nom d'une entreprise"""
    try:
        cur.execute("""UPDATE Entreprises SET denomination = ? WHERE id = ?""", (nom, id_entreprise))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL update_name_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_name_entreprise : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def update_adresse_entreprise(adresse, id_entreprise):
    """Met à jour l'adresse d'une entreprise"""
    try:
        cur.execute("""UPDATE Entreprises SET num_rue = ? WHERE id = ?""", (adresse, id_entreprise))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL update_adresse_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_adresse_entreprise : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def update_CP_entreprise(CP, id_entreprise):
    """Met à jour le code postal d'une entreprise"""
    try:
        cur.execute("""UPDATE Entreprises SET code_postale = ? WHERE id = ?""", (CP, id_entreprise))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL update_CP_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_CP_entreprise : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def update_ville_entreprise(ville, id_entreprise):
    """Met à jour la ville d'une entreprise"""
    try:
        cur.execute("""UPDATE Entreprises SET ville = ? WHERE id = ?""", (ville, id_entreprise))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL update_ville_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_ville_entreprise : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def update_num_entreprise(num, id_entreprise):
    """Met à jour le numéro de téléphone d'une entreprise"""
    try:
        cur.execute("""UPDATE Entreprises SET telephone = ? WHERE id = ?""", (num, id_entreprise))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL update_num_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_num_entreprise : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def update_email_entreprise(email, id_entreprise):
    """Met à jour l'email d'une entreprise"""
    try:
        cur.execute("""UPDATE Entreprises SET email = ? WHERE id = ?""", (email, id_entreprise))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL update_email_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_email_entreprise : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def update_siret_entreprise(siret, id_entreprise):
    """Met à jour le SIRET d'une entreprise"""
    try:
        cur.execute("""UPDATE Entreprises SET siret = ? WHERE id = ?""", (siret, id_entreprise))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL update_siret_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_siret_entreprise : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def update_siren_entreprise(siren, id_entreprise):
    """Met à jour le SIREN d'une entreprise"""
    try:
        cur.execute("""UPDATE Entreprises SET siren = ? WHERE id = ?""", (siren, id_entreprise))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL update_siren_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_siren_entreprise : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False

def update_mdp_entreprise(mdp, id_entreprise):
    """Met à jour le mot de passe d'une entreprise"""
    try:
        cur.execute("""UPDATE Entreprises SET motdepasse = ? WHERE id = ?""", (mdp, id_entreprise))
        conn.commit()
        if cur.rowcount == 1:
            return True
        else:
            return False
    except OperationalError as e:
        print(f"Erreur SQL update_mdp_entreprise : {e}")
        return False
    except IntegrityError as e:
        print(f"Erreur d'intégrité update_mdp_entreprise : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False