import sqlite3

db_file = "reservations.db"


class ReservationSystem:
    def __init__(self,db_file):
        """
        __init__(): Initialise l'objet et crée les deux base de données `avions` et `reservations`.
        """
        #se connecte à la base de données, j'ai choisi `reservations` comme nom pour la BD.
        self.connection = sqlite3.connect(db_file)
        self.c = self.connection.cursor()
        #self.c.execute('''DROP TABLE IF EXISTS avions''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS avions (numero_vol TEXT,avion_type TEXT, taille TEXT, siege TEXT)''')
        #self.c.execute('''DROP TABLE IF EXISTS reservations''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS reservations (nom_passager TEXT, prenom_passager TEXT , numero_vol TEXT, siege TEXT ,FOREIGN KEY (numero_vol) REFERENCES avions(numero_vol))''')



    
    def ajouter_avion(self, numero_vol, avion_type,taille, siege):
        """
        @ajouter_avion() : permet l'ajout d'un avion à la base de données.
        :param : numero_vol, avion_type,taille, siege
        """
        self.c.execute("INSERT INTO avions (numero_vol, avion_type,taille, siege) VALUES (?, ?, ?,?)",
                       (numero_vol, avion_type, taille, siege))
        self.connection.commit()
        print('\x1b[5;37;42m' + 'Avion ajouté avec succée ! ' + '\x1b[0m')


    def afficher_sieges(self, numero_vol):
        """
        @afficher_sieges() : permet l'affichage des siéges d'un avion donné.
        :param: numero_vol
        """
        try :
            self.c.execute("SELECT siege FROM avions WHERE numero_vol=?", (numero_vol,))
            siege = self.c.fetchone()[0]
            for i in range(len(siege)):
                if i % 3 == 0:
                    print("")
                print(siege[i], end=" ")
            print("\n")
        except :
            print('\x1b[0;37;43m' + 'Aucun Vol avec ce numéro ' + '\x1b[0m')



    def reserver_siege(self,  nom_passager , prenom_passager, numero_vol, siege):
        """
        @reserver_siege() : permet la reservation des siéges par un ou plusieurs passagers.
        :param: nom_passager , prenom_passager, numero_vol, siege
        """
        try : 
            self.c.execute("SELECT siege FROM avions WHERE numero_vol=?", (numero_vol,))
            sieges = list(self.c.fetchone()[0])
            if sieges[ord(siege[1])-65+(int(siege[0])-1)*3] == "X":
                print('\x1b[0;37;43m' + 'Nous somme désolé ! Ce siège est déjà réservé.' + '\x1b[0m')
            else:
                sieges[ord(siege[1])-65+(int(siege[0])-1)*3] = "X"
                self.c.execute("UPDATE avions SET siege=? WHERE numero_vol=?", ("".join(sieges), numero_vol))
                self.c.execute("INSERT INTO reservations VALUES (?, ?, ?, ?)", (nom_passager,prenom_passager, numero_vol, siege))
                self.connection.commit()
                print('\x1b[6;30;42m' + 'Réservation réussie.!' + '\x1b[0m')
        except : 
            print ('\n' '\x1b[0;37;41m' +  'Nous somme désolé ! ce siége n\'est pas disponible.' +  '\x1b[0m')



    def modifier_siege(self, nom_passager, prenom_passager, ancien_siege, nouveau_siege):
        """
        @reserver_siege() : permet la reservation des siéges par un ou plusieurs passagers.
        :param: nom_passager , prenom_passager, numero_vol, siege
        """
        self.c.execute("SELECT * FROM reservations WHERE nom_passager=? AND prenom_passager=?", (nom_passager,prenom_passager))
        res = self.c.fetchone()
        if not res:
            print ('\n' '\x1b[0;37;41m' +  'Aucune n\'avons pas trouvé votre réservation ! Veuillez s\'assurer que les informations sont correcte !' +  '\x1b[0m')        
        else :
            ancien_numero_vol, ancien_siege = res[2], res[3]
            self.c.execute("SELECT siege FROM avions WHERE numero_vol=?", (ancien_numero_vol,))
            sieges = list(self.c.fetchone()[0])
            sieges[ord(ancien_siege[1])-65+(int(ancien_siege[0])-1)*3] = "O"
            sieges[ord(nouveau_siege[1])-65+(int(nouveau_siege[0])-1)*3] = "X"
            self.c.execute("UPDATE avions SET siege=? WHERE numero_vol=?", ("".join(sieges), ancien_numero_vol))
            self.c.execute("UPDATE reservations SET siege=? WHERE nom_passager=? AND prenom_passager=?", (nouveau_siege, nom_passager,prenom_passager))
            self.connection.commit()
            print('\x1b[6;30;42m' + 'Changement de siège réussi.' + '\x1b[0m')



    def afficher_reservation(self, nom_passager,prenom_passager):
        """
        @afficher_reservation() : permet l'affichage des details d'une ou plusieurs reservations.
        :param: nom_passager , prenom_passager
        """
        self.c.execute("SELECT * FROM reservations WHERE nom_passager=? AND prenom_passager=?", 
                       (nom_passager, prenom_passager))
        res = self.c.fetchone()
        if not res:
            print ('\n' '\x1b[0;37;41m' +  'Aucune réservation trouvée pour ce nom.' +  '\x1b[0m')
            self.c.execute("SELECT * FROM reservations")
        else:
            print('DETAILS DE RESERVATION  : \n')
            print('\x1b[6;30;42m' + "Réservation de", res[0],  res[1] ,"pour le vol", res[2], "au siège", res[3], ".\n" + '\x1b[0m')


    def close(self):
        """
        @close() : ferme le fichier de la base de donnée ouvert.
        """
        self.connection.close()




