#!/usr/bin/env python3.5
#-- coding: utf-8 --
#uid badge valide [1, 52, 79, 115, 9]
##################################LIBRAIRIES#############################################
import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs
from pirc522 import RFID
from pirc522 import util
import time
from gpiozero import Buzzer

##################################SETUPS et VARIABLES######################################
GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
#GPIO.setwarnings(False) #On désactive les messages d'alerte
GPIO.setup(36,GPIO.OUT) #led alerte

rc522 = RFID() #On instancie la lib
id_carte_authorise = [1, 52, 79, 115, 9] #on définit un bagde authorisé
badge_etat = "FALSE" #On determine si le badge lu correspond a un badge authoriser

anomalie_detecte = "TRUE" #vrai si un patient est detecté au sol
##################################FONCTIONS#############################################
def etat_alerte():
    print("Alerte")
    GPIO.output(36, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(36, GPIO.LOW)
    time.sleep(1)

def lecture_badge():
    print('En attente d\'un badge (pour quitter, Ctrl + c): ') #On affiche un message demandant à l'utilisateur de passer son badge

    #On va faire une boucle infinie pour lire en boucle
    while True :
        etat_alerte()
        rc522.wait_for_tag() #On attnd qu'une puce RFID passe à portée
        (error, tag_type) = rc522.request() #Quand une puce a été lue, on récupère ses infos

        if not error : #Si on a pas d'erreur
            print("Tag detected")
            (error, uid) = rc522.anticoll() #On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps

            if not error : #Si on a réussi à nettoyer
                print('Vous avez passé le badge avec l\'id : {}'.format(uid)) #On affiche l'identifiant unique du badge RFID

                if uid == id_carte_authorise :
                    rc522.stop_crypto()
                    badge_etat = 'TRUE'
                    return badge_etat
                    #break

                if uid != id_carte_authorise :
                    rc522.stop_crypto()
                    badge_etat = 'FALSE'
                    return badge_etat
                    #break

                time.sleep(1) #On attend 1 seconde pour ne pas lire le tag des centaines de fois en quelques milli-secondes


#######################################MAIN PROGRAM#############################################
if anomalie_detecte=="TRUE" :
    fin_alerte = "FALSE"
    while fin_alerte == "FALSE":
        badge_etat = lecture_badge() #on attend la lecture d'un badge et on verifie s'il est authoriser
        if badge_etat == 'TRUE' :
            print("Arret alerte : Bagde valide")
            fin_alerte ="TRUE"
        else :
            print("Badge non valide")
            fin_alerte ="FALSE"
