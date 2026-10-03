CleanWay

Présentation

CleanWay est un projet développé en Python dans le cadre de la NSI.

L'application permet de gérer différentes fonctionnalités liées à l'activité de l'entreprise, notamment les clients, les rendez-vous, la comptabilité et les factures.

Le projet utilise également une base de données SQLite pour stocker les informations nécessaires au fonctionnement de l'application.

Lancement du projet

Pour lancer l'application, il faut exécuter le fichier :

main.py

Depuis un terminal placé dans le dossier du projet, utilisez :

python main.py

Important : main.py est le fichier principal du projet. C'est celui qui doit être lancé pour démarrer l'application.

Organisation du projet  

CleanWay/  
│  
├── main.py                 # Fichier principal à lancer  
├── app.py                  # Gestion de l'application (menu)  
├── accueil.py              # Page d'accueil  
├── client.py               # Gestion des clients  
├── compta.py               # Gestion de la comptabilité  
├── connexion.py            # Connexion  
├── inscription.py          # Inscription  
├── para.py                 # Paramètres  
├── photos.py               # Gestion des photos  
├── rdv.py                  # Gestion des rendez-vous  
│  
├── DB/  
│   ├── CleanWay.db         # Base de données  
│   └── DB.py               # Gestion de la base de données  
│  
├── module/  
│   ├── explorateur_de_fichier.py  
│   ├── info_client.py  
│   ├── menu_horizontal.py  
│   ├── prix_forfait.py  
│   └── sql.py  
│  
├── IMG/  
│   └── ICONE/              # Icônes et images de l'application  
│  
└── factures/               # Fichiers liés aux factures  
  
Technologies utilisées  
  
Python
  
SQLite  
  
Tkinter pour l'interface graphique  
  
Git / GitHub pour la gestion du projet  
  
Base de données  

La base de données du projet se trouve dans le dossier DB :  

DB/CleanWay.db  

Elle est utilisée pour stocker les données nécessaires à l'application.  
