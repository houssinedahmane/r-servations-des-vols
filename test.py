import sqlite3
import unittest
from reservations import ReservationSystem

class TestReservationSystem(unittest.TestCase):

    def get_query(self,query):
        """ 
            helper function 
            :param : Query 
            :return : cursor
        """ 
        cursor = self.connection.cursor() 
        cursor.execute(query)
        return cursor
        


    @classmethod
    def setUpClass(self):
        test_db = "test.db"
        self.reservation_system = ReservationSystem(test_db)
        self.connection = sqlite3.connect(test_db)
        # Creation des deux tables ``avions`` et ``reservations``.
        self.get_query(self,query="""CREATE TABLE IF NOT EXISTS avions 
                                    (numero_vol TEXT,avion_type TEXT, taille TEXT, siege TEXT);
                                    """)
        self.get_query(self,query='''CREATE TABLE IF NOT EXISTS reservations 
                                    (nom_passager TEXT, prenom_passager TEXT , numero_vol TEXT,siege TEXT ,FOREIGN KEY (numero_vol) 
                                    REFERENCES avions(numero_vol))
                                    ''')
        self.connection.commit()
        
     
    
        
    def test_a_is_instance(self):
        # S'assurer que l'objet `reservation_system` est une instance de `ReservationSystem`.
        self.assertIsInstance(self.reservation_system ,ReservationSystem)




    def test_b_tables_created(self):
        #Assurer que les tables `avions` & `reservations` ont été créées correctement
        result = self.get_query(query=''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='avions' ''').fetchone()
        # si le nombre est 1, alors la table existe
        self.assertEqual(result[0], 1)


    def test_c_ajouter_avion(self):
        """ 
            Cette fonction permet de tester l'ajout d'un avion 
            :param : numero_vol, avion_type, taille, siege    
        """
        # Initialisation de la fonction afin de tester l'ajout d'un avion 
        self.reservation_system.ajouter_avion("100","Boeing 700","3x1","OOOOOOOOO")
        # obtenir les lignes ou le numero de vol = 100
        result = self.get_query(query=''' SELECT * FROM avions WHERE numero_vol="100" ''').fetchone()
        # Tester SI le resultat n'est pas vide
        self.assertIsNotNone(result)
        # S'assurer que le 1er element contient la valeur ``100`` qui correspond au numero de vol
        self.assertEqual(result[0],"100")
        # S'assurer que le 2eme element contient la valeur ``Boeing 700`` qui correspond au type d'avion
        self.assertEqual(result[1],"Boeing 700")
        # S'assurer que le 3eme element contient la valeur ``3x1`` qui correspond a la taille  de l'avion
        self.assertEqual(result[2],"3x1")
        # S'assurer que le 4 eme elmeent contient la valeur ``OOOOOOOOO`` qui correspond au sieges de l'avion ( O : vide ,  X : réservé )
        self.assertEqual(result[3],"OOOOOOOOO")

    
    def test_d_afficher_sieges(self):
        """ 
            Cette fonction permet de tester l'affichage des sieges de l'avion crée precedement
            :param : numero_vol
        """
        # Initialisation de la fonction ``afficher_sieges`` afin de tester l'affichage des sieges d'un avion donné
        self.reservation_system.afficher_sieges("100") 
        # Obtenir toutes les lignes de la table ``avions`` ou le numero de vol ``numero_vol = 100``
        result = self.get_query(query=''' SELECT * FROM avions WHERE numero_vol="100" ''').fetchone()
        # Tester SI le resultat n'est pas vide
        self.assertIsNotNone(result)
        # S'assurer que le 4eme element contient la valeur ``OOOOOOOOO`` qui correspond au sieges de l'avion qui a comme taille ``3x1``
        self.assertEqual(result[3],"OOOOOOOOO")




    def test_e_reserver_siege(self):
        """ 
            Cette fonction permet de tester SI un passager peut réserver un siege dans un avion donné
            :param : nom_passager , prenom_passager, numero_vol, siege
        """
        # Initialiser la fonction ``reserver_siege`` pour tester le réservation d'un sieges pour un passager
        self.reservation_system.reserver_siege('DAHMANE','Houssine','100','2A')

        # Obtenir toutes les lignes de la table ``avions`` ou le ``numero_vol = 100``
        result = self.get_query(query=''' SELECT * FROM avions WHERE numero_vol="100" ''').fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[3],"OOOXOOOOO")

        # Obtenir toutes les lignes de la table ``reservations`` ou  ``nom_passager = DAHMANE``
        result = self.get_query(query=''' SELECT * FROM reservations WHERE nom_passager="DAHMANE" ''').fetchone()
        self.assertIsNotNone(result)
        # S'assurer que le 4eme element contient la valeur ``2A`` qui correspond au numero de siege reservé par le passager 
        self.assertEqual(result[3],"2A")
    




    def test_f_modifier_siege(self):
        """ 
            Fonction qui permet de tester SI un passager peut modifier son siege (Ex: from 2A to 3A )
            :param : nom_passager , prenom_passager, ancien_siege, nouveau_siege
        """
        # Initialiser la fonction ``modifier_siege`` afin de modifié un sieges pour un passager
        self.reservation_system.modifier_siege('DAHMANE','Houssine','2A','3A')  
        # Obtenir toutes les lignes de la table ``avions`` ou  le ``numero_vol="100"``
        result = self.get_query(query=''' SELECT * FROM avions WHERE numero_vol="100" ''').fetchone()
        # Tester SI le resultat n'est pas vide
        self.assertIsNotNone(result)
        # S'assurer que le 4eme element de la table ``avions`` contient la valeur nouvelle valeur ``OOOOOOXOO`` 
        self.assertEqual(result[3],"OOOOOOXOO")

        # Obtenir toutes les lignes de la table ``reservations`` ou  le ``nom_passager="DAHMANE"  et le  ``"prenom_passager="Houssine"``
        result = self.get_query(query=''' SELECT * FROM reservations WHERE nom_passager="DAHMANE"  AND prenom_passager="Houssine" ''').fetchone()
        # Tester SI le resultat n'est pas vide
        self.assertIsNotNone(result)
        # S'assurer que le 4eme element de la table ``reservations`` contient la valeur nouvelle valeur "3A"
        self.assertEqual(result[3],"3A")


    def test_g_afficher_reservation(self):# nom_passager,prenom_passager
        """ 
            Fonction qui permet de tester l'affichage des informations de reservation
            :param : nom_passager , prenom_passager
        """
        self.reservation_system.afficher_reservation('DAHMANE','Houssine')
        result = self.get_query(query=''' SELECT * FROM reservations WHERE nom_passager="DAHMANE" AND prenom_passager="Houssine" ''').fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0],"DAHMANE")
        self.assertEqual(result[1],"Houssine")
        self.assertEqual(result[2],"100")
        self.assertEqual(result[3],"3A")





    @classmethod
    def tearDownClass(self):
        self.connection.close()

if __name__ == '__main__':
    unittest.main()
