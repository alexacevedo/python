# coding: utf8
# SQLite with Python

"""
programme: musique_bd.py

- Le programme qui va afficher à l'écran la liste numérotée des artistes dans la BD.

- Le programme va afficher la liste des albums d'un artiste en particulier (en saisissant son numéro au clavier)

- Le fichier input_data.txt contient des données sur des albums de musique. Chaque ligne correspond à un album, avec 3 champs :

    le premier champ est le nom de l'artiste;
    le deuxième champ est le nom de l'album;
    le troisième champ est l'année de publication de l'album. Les champs sont séparés par un |.

- Le programme qui va lire le fichier et ajouter ces albums à la base de données.

- Si l'artiste existe déjà, le programme utlise l'id de l'artiste existant, sinon crée un nouvel artiste.

"""
import sqlite3

connect_db = sqlite3.connect("musique.db")
cursor = connect_db.cursor()


def get_nom_artiste(artiste_id):
    sql = "SELECT * FROM artiste WHERE id=?"
    cursor.execute(sql, [(artiste_id)])
    return cursor.fetchone()[1]


def get_id_artiste(nom):
    sql = "SELECT * FROM artiste WHERE nom=?"
    cursor.execute(sql, [(nom)])
    return cursor.fetchone()[0]


def verifier_existence_artiste(nom):
    sql = "SELECT 1 FROM artiste WHERE nom=?"
    if cursor.execute(sql, [nom]).fetchone() == None:
        return False
    else:
        return True


def ajouter_album(titre, annee, artiste_id, maison_disque_id):
    sql = "INSERT INTO album(titre, annee, artiste_id, maison_disque_id) VALUES(?, ?, ?, ?)"
    cursor.executemany(sql, [(titre, annee, artiste_id, maison_disque_id)])
    connect_db.commit()


def ajouter_artiste(nom, est_solo, nombre_individus):
    if not verifier_existence_artiste(nom):
        sql = "INSERT INTO artiste(nom, est_solo, nombre_individus) VALUES(?, ?, ?)"
        cursor.executemany(sql, [(nom, est_solo, nombre_individus)])
        connect_db.commit()


def lire_input_data():
    fichier_input_data = open("input/input_data")
    for ligne in fichier_input_data:
        ligne = ligne.rstrip().split("|")
        ajouter_artiste(ligne[0], 1, 1)  # inventez les valeurs que vous ne connaissez pas
        ajouter_album(ligne[1],ligne[2], get_id_artiste(ligne[0]), 1)  # prenez n'importe quel maison d'édition
    fichier_input_data.close()


def afficher_liste_artistes():
    cursor.execute("SELECT * FROM artiste")
    print "Voici la liste des artistes dans notre Base de Données\n"
    for row in cursor:
        identifier, artiste_id, est_solo, nombre_individus = row
        print "%d - %s" % (identifier, artiste_id)


def afficher_albums_artiste(artiste_id):
    print "\nLa liste des albums de %s est:\n" % (get_nom_artiste(artiste_id))
    sql1 = "SELECT * FROM album WHERE artiste_id=?"
    cursor.execute(sql1, [(artiste_id)])
    for row in cursor:
        album_id, titre, annee, artiste_id, maison_disque_id = row
        print "%s - %d" % (titre, annee)


def menu_bd():
    selection= raw_input("""
    - 'v' pour consulter les artistes de notre Base de Données
    - 'a' pour consulter les albums d'un artiste en particulier
    - 'c' pour charger des données d'un fichier - input.txt
    - 'q' pour quiter le programme\n
    Entrez votre sélection:
    """)
    while selection != 'q':
        if selection == 'v':
            afficher_liste_artistes()
        elif selection == 'a':
            artiste_id = int(raw_input("Entrez le numéro de l'artiste:"))
            afficher_albums_artiste(artiste_id)
        elif selection == 'c':
            lire_input_data()
            print "Les données ont été chargés avec succès\n"
        selection = raw_input("""
            - 'v' pour consulter les artistes de notre Base de Données
            - 'a' pour consulter les albums d'un artiste en particulier
            - 'c' pour charger des données d'un fichier - input_data.txt
            - 'q' pour quiter le programme\n
            Entrez votre sélection:
            """)

    print "FIN NORMAL DU PROGRAMME"


menu_bd()











