import os
#change user and pwd values with yours

user='youremail@gmail.com'
pwd='yoursecretpassword'



#change these names with ones that are close to your name in the attendance list ( as soon as one of them types 'present' you will type it too)
closestud = ["Ahmed SOLOFAN","Abdel MOULA", "John CENA"]





def clearscreen():
    try:
        os.system("clear")
    except:
        os.system("cls")

def selectteam():
    ans=True
    while ans:
        print ("""
        1.PROGRAMMATION-MOBILE_4 IIR 1
        2.BASES-DONNEES-AVANCEES_4 IIR 1
        3.DATA-WERHOUSE_4 IIR 1
        4.SECURITE-RESEAUX_4 IIR1
        5.ADMINISTRATION-WINDOWS_4 IIR 1
        6.J2EE_4 IIR 1
        7.COMMUNICATION-PROFESSIONNELLE_4 IIR 1
        8.ENTREPRENARIAT_4 IIR 1
        9.Management_4IIR1
        10.PROGRAMMATION WEB_4 IIR 1
        11.ANGLAIS_4 IIR 1
        12.VIRTUALISATION_4 IIR 1
        13.ADMINISTRATION-ORACLE_4 IIR 1
        14.GENIE-LOGICIEL_4 IIR 1

        15. TEST Team 'yyyyyy'
        
        16.exit
        """)
        ans=input("Please choose a team by its number: ") 
        if ans=="1":
            clearscreen()
            print("you selected 'PROGRAMMATION-MOBILE_4 IIR 1' !")
            return 'PROGRAMMATION-MOBILE_4 IIR 1'
        elif ans=="2":
            clearscreen()
            print("you selected 'BASES-DONNEES-AVANCEES_4 IIR 1' !")
            return 'BASES-DONNEES-AVANCEES_4 IIR 1'
        elif ans=="3":
            clearscreen()
            print("you selected 'DATA-WERHOUSE_4 IIR 1' !")
            return 'DATA-WERHOUSE_4 IIR 1'
        elif ans=="4":
            clearscreen()
            print("you selected 'SECURITE-RESEAUX_4 IIR1' !")
            return 'SECURITE-RESEAUX_4 IIR1'
        elif ans=="5":
            clearscreen()
            print("you selected 'ADMINISTRATION-WINDOWS_4 IIR 1' !")
            return 'ADMINISTRATION-WINDOWS_4 IIR 1'
        elif ans=="6":
            clearscreen()
            print("you selected 'J2EE_4 IIR 1' !")
            return 'J2EE_4 IIR 1'
        elif ans=="7":
            clearscreen()
            print("you selected 'COMMUNICATION-PROFESSIONNELLE_4 IIR 1' !")
            return 'COMMUNICATION-PROFESSIONNELLE_4 IIR 1'
        elif ans=="8":
            clearscreen()
            print("you selected 'ENTREPRENARIAT_4 IIR 1' !")
            return 'ENTREPRENARIAT_4 IIR 1'
        elif ans=="9":
            clearscreen()
            print("you selected 'Management_4IIR1' !")
            return 'Management_4IIR1'
        elif ans=="10":
            clearscreen()
            print("you selected 'PROGRAMMATION WEB_4 IIR 1' !")
            return 'PROGRAMMATION WEB_4 IIR 1'
        elif ans=="11":
            clearscreen()
            print("you selected 'ANGLAIS_4 IIR 1' !")
            return 'ANGLAIS_4 IIR 1'
        elif ans=="12":
            clearscreen()
            print("you selected 'VIRTUALISATION_4 IIR 1' !")
            return 'VIRTUALISATION_4 IIR 1'
        elif ans=="13":
            clearscreen()
            print("you selected 'ADMINISTRATION-ORACLE_4 IIR 1' !")
            return 'ADMINISTRATION-ORACLE_4 IIR 1'
        elif ans=="14":
            clearscreen()
            print("you selected 'GENIE-LOGICIEL_4 IIR 1' !")
            return 'GENIE-LOGICIEL_4 IIR 1'
        elif ans=="15":
            clearscreen()
            print("you selected 'yyyyyy' !")
            return 'yyyyyy'
        elif ans=="16":
            clearscreen()
            print("\n Goodbye")
            exit()
        elif ans !="":
            clearscreen()
            print("\n Not Valid Choice Try again")

 
