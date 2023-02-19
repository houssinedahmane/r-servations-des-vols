from reservations import ReservationSystem

def main():
    # instanciation de la class  ``ReservationSystem``
    systeme_reservation = ReservationSystem(db_file="reservations.db")

    while True:
        print("\n")
        print("==================== SYSTEME DE RESERVATION ==========================")
        print("======================================================================")
        print("\n")

        commande = input(" Veuillez choisir une option :  \n\n \
                         1: Ajouter un avion \n \
                         2: Afficher les siéges \n \
                         3: Reserver un vol  \n \
                         4: Modifier ma réservation \n \
                         5: Afficher ma réservation \n \
                         6: Quitter \n")
        
        # La premiére option permet d'interroger  la fonction ``ajouter_avion``
        # :input: numero_vol, avion_type, taille, siege
        if commande == "1":
            numero_vol = input("Entrez le numéro de vol : ")
            avion_type = input("Entrez le type d\'avion : ")
            taille = input("Entrez la taille de l'avion (ex: 3x4) : ")
            siege = "O" * (int(taille[0]) * 3 * int(taille[2]))
            systeme_reservation.ajouter_avion(numero_vol, avion_type, taille, siege)

        # La 2éme  option permet d'interroger  la fonction ``afficher_sieges``
        # :input: numero_vol
        elif commande == "2":
            numero_vol = input("Entrez le numéro de vol : ")
            systeme_reservation.afficher_sieges(numero_vol)

        # La 3éme option permet d'interroger  la fonction ``reserver_siege``
        # :input: nom,prenom,numero_vol,siege
        elif commande == "3":
            nom = input("Entrez votre nom : ")
            prenom = input("Entrez votre prénom : ")
            numero_vol = input("Entrez le numéro de vol : ")
            siege = input("Entrez le siège souhaité (ex: 2A) : ")
            systeme_reservation.reserver_siege(nom,prenom,numero_vol,siege)

        # La 4éme option permet d'interroger  la fonction ``modifier_siege``
        # :input: nom, prenom, siege_actuel, nouveau_siege
        elif commande == "4":
            nom = input("Entrez votre nom : ")
            prenom = input("Entrez votre prénom : ")
            siege_actuel = input("Entrez le numéro de votre siege actuel (ex: 2A) : ")
            nouveau_siege = input("Entrez le numéro du nouveau siège souhaité (ex: 3B) : ")
            systeme_reservation.modifier_siege(nom, prenom, siege_actuel, nouveau_siege) 

        
        # La 5éme option permet d'interroger  la fonction ``afficher_reservation``
        # :input: nom,prenom   
        elif commande == "5":
            nom = input("Veuillez Entrez votre nom : ")
            prenom = input("Veuillez Entrez votre prénom : ")
            systeme_reservation.afficher_reservation(nom,prenom)


        # La 6éme option permet de quitter le menu
        elif commande == "6":
            break

        # Un message sera affiché pour toutes autres entrées.
        else : 
            print ('\n' '\x1b[0;37;41m' +  'Vous devez choisir une option valide !' +  '\x1b[0m')



if __name__ == "__main__":
    main()