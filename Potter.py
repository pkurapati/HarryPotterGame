class Duel:
    def __init__(self,wizard1,wizard2):
        """ Get the initial spell list"""
        with open('Spells.json') as data_file:
            data = json.load(data_file)
        self.SpellList = data['Spells']
        self.wizard1 = wizard1
        self.wizard2 = wizard2

    def spell_selector(self):
        """ Asks Harry to select a spell. Checks for frequency of usage"""
        for spell in self.SpellList:
            print("{} : {}".format(spell['id'], spell['name']))
        while True:
            try:
                h_spell = input("Which spell do you want to choose?")
                h_spell = h_spell.lower()
                if h_spell == "q":
                    # The user wants to quit
                    return 0
                else:
                    # Convert to integer
                    h_spell = int(h_spell)
                if h_spell not in list(range(1,10)):
                    raise Exception("Please choose from the list of spells")
                else:
                    h_freq = int(self.SpellList[h_spell - 1]['frequency']) -1
                    if h_freq < 0:
                        raise Exception("You have reached max frequency of this spell")
                    else:
                        self.SpellList[h_spell - 1]['frequency'] = h_freq
                        return h_spell
            except Exception as e:
                print("Wrong choice. Exception was \"{}\". Try again!".format(e))
    def random_spell_selector(self,wizard2):
        """ The other wizard fires spells randomly to make the game interesting"""
        v_spell_list = list(range(1,9))
        v_spell_id = random.choice(v_spell_list)
        return v_spell_id

    def get_spell_damage(self,h_spell):
        """ Returns the damage of a given spell id"""
        spell_damage = int(self.SpellList[h_spell - 1]['power'])
        return spell_damage

    def take_damage(self,wizard1,wizard2,damage,spell_id):
        """ Wizard1 takes damage based on the wizard2's spell"""
        # If the spell is "Avada Kedavra", then it is the death spell
        if spell_id == 5:
            wizard1.life -= 1
            if wizard1.life <=0:
                print("{} is dead and there are no more bonus lives".format(wizard1.alias))
                wizard1.health = 0
                return 0
            else:
                print("{} was dead! But has more lives, so re-appeared".format(wizard1.alias))
                # Start wizard's new life with a health of at least 1000
                if wizard1.health < 1000:
                    wizard1.health = 1000
                # Credit wizard2 for delivering a death blow to wizard1
                wizard2.health += 1000
                return 1

        else:
            print("{} took {} damage".format(wizard1.alias,damage))
            wizard1.health -= damage
            if wizard1.health > 0:
                return 1
            elif wizard1.health <= 0:
                wizard1.life -= 1
                if wizard1.life <= 0:
                    print("{} is dead and there are no more bonus lives".format(wizard1.alias))
                    wizard1.health = 0
                    return 0
                else:
                    print("{} was dead! But has more lives, so re-appeared".format(wizard1.alias))
                    # Start wizard's new life with a health of at least 1000
                    if wizard1.health < 1000:
                        wizard1.health = 1000
                    return 1


class Wizard:
    def __init__(self,name,alias,health=10,life=1):
        self.health = health
        self.life = life
        self.stage = 1
        self.wand = 3
        self.name = name
        self.alias = alias
        self.position = [0,0]
        self.wand_multiplier = 1
    def __str__(self):
        return self.name
    def select_wand(self):
        """ Displays choice of wands for user to pick"""
        while True:
            try:
                print("Please pick a wand from the below list.")
                print("Choose wisely! Wand impacts the power of spells \n")
                print("1. Phoenix Feather, 11 inches")
                print("2. Thestral tail core, 15 inches")
                print("3. Dragon heartstring, 18 inches")
                print("4. Hawthron 10 inches")
                print("5. Mahogany 11 inches")
                print("6. Walnut, 12.75 inches\n")
                wand = int(input("Enter the wand number: "))
                if(wand == 1):
                    print("\nGood Choice! This is Harry Potter's selection too")
                    self.wand_multiplier = 2
                elif(wand == 2):
                    print("\nGreat choice! This is the elder wand!")
                    self.wand_multiplier = 3
                elif(wand == 3):
                    print("\nMeh! This was originally Voldemort's wand. Not so great in Harry's hands. Let's see how it performs!")
                    self.wand_multiplier = 0.5
                elif(wand == 4):
                    print("\nMeh! This is Draco Malfoy's wand! Not so great in Harry's hands. Let's see how it performs!")
                    self.wand_multiplier = 0.5
                elif(wand == 5):
                    print("\nGood choice! This is James Potter's wand.")
                    self.wand_multiplier = 1
                elif(wand == 6):
                    print("\nMeh! This is Bellatrix's wand! Not so great in Harry's hands. Let's see how it performs")
                    self.wand_multiplier = 0.5
                else:
                    raise Exception("Wrong wand")
                self.wand = wand
                break
            except Exception as e:
                print("Exception was \"{}\". Try again!".format(e))

class Board:
    def __init__(self,size):
        """ Initialize the Minefield object with attributes"""
        self.size = size
        self.wz_id = "H"
        self.position = [0,0]
        self.number_of_attempts = 1
        self.BoardList = list()
        self.WizardList = list()
        templist = list()
        for x in range(size):
            for y in range(size):
                templist.append('\u26aa')
            self.BoardList.append(templist)
            templist = []
    def reset_position(self,wizard_char):
        """ Reset the board position to the beginning place"""
        self.number_of_attempts += 1
        for x in range(self.size):
            for y in range(self.size):
                if self.BoardList[x][y] != wizard_char:
                    self.BoardList[x][y] = "\u26aa"


    def insert_wizard(self,wizard,position,name='0'):
        """ Inserts the wizard in to the minefield"""
        if name == "0":
            wizard_name = wizard.name
        else:
            wizard_name = name 
        i = position[0]
        j = position[1]
        # Position it in the requested row
        if self.BoardList[i][j] == '\u26aa':
            self.BoardList[i][j] = wizard_name
        else:
            self.BoardList[i][j] += wizard_name
        self.WizardList.append(wizard)
        wizard.position = [i,j]
    def print_board(self):
        print("\n")
        for k in self.BoardList:
            print(*k,sep = "   ")
        print("\n")
    def insert_bombs(self,position):
        x = position[0]
        y = position[1]
        self.BoardList[x][y] = "X"
    def make_move(self,wizard,B2,wizard_char):
        """ Makes one forward move for the Wizard in the board. Returns success or failure"""
        w_x = wizard.position[0]
        w_y = wizard.position[1]
        while True:
            try:
                print("You have three choices below.")
                print("1. Move one-step down.")
                print("2. Move one-step right and one-step down")
                print("q. Quit the game")
                option = str(input("Pick a choice: "))
                option = option.lower()
                if option != "1" and option != "2" and option != "q":
                    raise Exception("Bad option. Please choose the correct choice")
                elif option == "q":
                    sure = input("Are you sure you want to quit? Y/N")
                    sure = sure.upper()
                    if sure == "N":
                        raise Exception("OK, let us try again!")
                    elif sure == "Y":
                        return 3
                else:
                    break

            except Exception as e:
                print("Wrong choice. Exception was \"{}\". Try again!".format(e))

        # Reset the current position
        self.BoardList[w_x][w_y] = "\u26aa"
        if option == "1":
            w_x += 1
        elif option == "2":
            w_x += 1
            w_y += 1

        # Do checks on new position
        # If the new position has reached the horcrux, it is a success. Return 0
        # Else, if the new position is a bomb, or if it is a last row, deduct life and return 1
        # Else, it is just another valid step. Return 2

        if self.BoardList[w_x][w_y] == wizard_char:
            self.BoardList[w_x][w_y] = '\u2606' 
            self.print_board()
            print("##################################################")
            print("# Congratulations!! You have reached the Horcrux #")
            print("##################################################")
            time.sleep(3)
            return 0
        elif B2.BoardList[w_x][w_y] == "X":
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("x  Oh Oh! You just stepped on a bomb!  x")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            wizard.life -= 1
            time.sleep(3)
            # Reset the wizard position to previous value
            return 1
        elif w_x == self.size - 1 and self.BoardList[w_x][w_y] != wizard_char:
            print("You reached the end of the board")
            wizard.life -= 1
            return 1
        else:
            self.BoardList[w_x][w_y] = wizard.name
            wizard.position = [w_x, w_y]
            return 2



import unicodedata
import os
import random
import time
import json
import numpy as np
import itertools
import sys

def make_move_in_loop(B1,B2,Potter,wizard_char):
    """
    Makes move in the loop until the user quits or the game is over
    :param Board:
    :return: None
    """

    while True:
        try:
            B1.print_board()
            move_result = B1.make_move(Potter,B2,wizard_char)
            if move_result == 0:
                return 1
            elif move_result == 1:
                if Potter.life != 0:
                    Potter.health -= 500
                    B1.reset_position(wizard_char)
                    B1.insert_wizard(Potter,[0,0])
                    continue
                else:
                    raise Exception("No more lives left!")
            elif move_result == 2:
                continue
            elif move_result == 3:
                raise Exception("OK, Quitting the game. Good Bye!")

        except Exception as e:
            print(e)
            return 0

def Stage1(Potter,Dolohov):
    """This is Stage 1 of Harry Potter's quest for Voldemort's Horcrux"""
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("     Entering Stage-1 of the game")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print()
    print("You have just found Tom Riddle's Diary in the chamber of secrets")
    time.sleep(2)
    print("But, you have to duel with Antonin Dolohov before you can enter the chamber of secrets \n")
    time.sleep(2)
    print("Duel is a contest between two wizards using different magic spells. Each spell has different power")
    time.sleep(2)
    print("Remember, the wand you selected will also impact the power of the spell.")
    print("Duel using below spells!! \n")
    time.sleep(2)
    D1 = Duel(Potter,Dolohov)

    while True:
        try:
            h_spell = D1.spell_selector()
            if h_spell == 0:
                print("Quitting the game. Good bye!")
                return 0
            d_spell = D1.random_spell_selector(Dolohov)
            print("################################")
            print("#   Harry-> {}            ".format(D1.SpellList[h_spell -1]['name']))
            print("#   Dolohov-> {}          ".format(D1.SpellList[d_spell - 1]['name']))
            print("################################")
            time.sleep(2)

            h_damage = D1.get_spell_damage(h_spell) * Potter.wand_multiplier
            d_damage = D1.get_spell_damage(d_spell)
            h_status = D1.take_damage(Potter,Dolohov,d_damage,d_spell)
            d_status = D1.take_damage(Dolohov,Potter,h_damage,h_spell)

            print("###################################")
            print("#   Harry: Health {} Life {}      ".format(Potter.health,Potter.life))
            print("#   Dolohov: Health {} Life {}      ".format(Dolohov.health,Dolohov.life))
            print("###################################")

            # Check for status to determine to continue for another spell
            if h_status == 0:
                print("End of game! Good Bye!")
                return 0
            elif d_status == 0:
                print("#########################################")
                print("#    You won the Duel against Dolohov!  #")
                print("#########################################")
                Potter.health += 2000
                time.sleep(2)
                return 1
            else:
                raise Exception("keep firing spells...")
        except Exception as e:
            print(e)

def Stage2(Potter,Bellatrix):
    """This is Stage 2 of Harry Potter's quest for Voldemort's Horcrux"""
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("     Entering Stage-2 of the game")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print()
    print("You have just found Salazar Slytherin’s Locket inside Bellatrix's locker at Gringott's bank")
    time.sleep(2)
    print("But, you have to duel with Bellatrix Lestrange before you can claim the locket")
    time.sleep(2)
    print("Duel using below spells!! \n")
    time.sleep(2)
    D1 = Duel(Potter,Bellatrix)

    while True:
        try:
            h_spell = D1.spell_selector()
            if h_spell == 0:
                print("Quitting the game. Good bye!")
                return 0
            d_spell = D1.random_spell_selector(Bellatrix)
            print("################################")
            print("#   Harry-> {}            ".format(D1.SpellList[h_spell -1]['name']))
            print("#   Bellatrix-> {}          ".format(D1.SpellList[d_spell - 1]['name']))
            print("################################")
            time.sleep(2)

            h_damage = D1.get_spell_damage(h_spell) * Potter.wand_multiplier
            d_damage = D1.get_spell_damage(d_spell)
            h_status = D1.take_damage(Potter,Bellatrix,d_damage,d_spell)
            d_status = D1.take_damage(Bellatrix,Potter,h_damage,h_spell)

            print("###################################")
            print("#   Harry: Health {} Life {}      ".format(Potter.health,Potter.life))
            print("#   Bellatrix: Health {} Life {}      ".format(Bellatrix.health,Bellatrix.life))
            print("###################################")

            # Check for status to determine to continue for another spell
            if h_status == 0:
                print("End of game! Good Bye!")
                return 0
            elif d_status == 0:
                print("#########################################")
                print("#  You won the Duel against Bellatrix!  #")
                print("#########################################")
                Potter.health += 2000
                time.sleep(2)
                return 1
            else:
                raise Exception("Keep firing spells...")
        except Exception as e:
            print(e)


def Stage3(Potter,Voldemort):
    """This is Stage 3 of Harry Potter's quest for Voldemort"""
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("     Entering Stage-3 of the game")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print()
    print("You are now entering a minefield")
    time.sleep(2)

    # Preparing the Board with bombs and wizards
    # This stage is a simple 5x5
    B1 = Board(5)
    # We need the second board, only for storing Bombs.
    # This is because, we do not want the user to see where the bombs are hidden
    B2 = Board(5)
    h_position = (0,0)
    v_position = (4,2)
    # Insert Harry and Voldemort into the game
    B1.insert_wizard(Potter,h_position)
    B1.insert_wizard(Voldemort,v_position,'\u2622')
    # Insert bombs into the board B2
    Bomb_positions = [[1,1],[2,0],[3,2]]
    for b_pos in Bomb_positions:
        B2.insert_bombs(b_pos)

    print(" \n Your task is to catch Helga HufflePuff's cup at the bottom of the maze")

    success = make_move_in_loop(B1,B2,Potter,'\u2622')
    if success == 0:
        print("End of game! Good Bye")
        return 0
    else:
        print("You have cleared Stage 3 challenge!")
        print("Potter just destroyed Hufflepuff's cup and earned 2000 health points")
        time.sleep(3)
        Potter.health += 2000
        # If the user cleared it in single attempt, Potter gets additional life
        if B1.number_of_attempts == 1:
            Potter.life += 1
            print("Potter earned an extra life by clearing the level in first attempt")

        print("############################################")
        print("#       HEALTH: {} LIVES : {}".format(Potter.health,Potter.life))
        print("############################################")
        time.sleep(3)

        return 1

def Stage4(Potter,Voldemort):
    """This is Stage 4 of Harry Potter's quest for Voldemort"""
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("     Entering Stage-4 of the game")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print()
    print("You are now entering a minefield")
    time.sleep(2)

    # Preparing the Board with bombs and wizards
    # This stage is a simple 7x7
    B1 = Board(7)
    # We need the second board, only for storing Bombs.
    # This is because, we do not want the user to see where the bombs are hidden
    B2 = Board(7)
    h_position = (0,0)
    v_position = (6,3)
    # Insert Harry and Voldemort into the game
    B1.insert_wizard(Potter,h_position)
    B1.insert_wizard(Voldemort,v_position,'\u2620')
    # Insert bombs into the board B2
    Bomb_positions = [[1,0],[2,2],[3,1],[4,3],[5,3]]
    for b_pos in Bomb_positions:
        B2.insert_bombs(b_pos)

    print(" \n Your task is to catch Rowena Ravenclaw's diadem at the bottom of the maze")

    #B1.print_board()
    success = make_move_in_loop(B1,B2,Potter,'\u2620')
    if success == 0:
        print("End of game! Good Bye")
        return 0
    else:
        print("Potter just destroyed Rovena Ravenclaw's diadem and earned 3000 health points")
        Potter.health += 3000
        print("Potter's health is {} points ".format(Potter.health))
        # If the user cleared it in single attempt, Potter gets additional life
        if B1.number_of_attempts == 1:
            print("Potter earned an additional life since you cleared in single attempt")
            Potter.life += 1
            print("Potter's number of lives pending are {}".format(Potter.life))
        return 1

def Stage5(Potter,Voldemort):
    """This is Stage 5 of Harry Potter's quest for Voldemort"""
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("     Entering Stage-5 of the game")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print()
    print("You are now entering a minefield")
    time.sleep(2)

    # Preparing the Board with bombs and wizards
    # This stage is a simple 9x9
    B1 = Board(9)
    # We need the second board, only for storing Bombs.
    # This is because, we do not want the user to see where the bombs are hidden
    B2 = Board(9)
    h_position = (0,0)
    v_position = (8,4)
    # Insert Harry and Voldemort into the game
    B1.insert_wizard(Potter,h_position)
    B1.insert_wizard(Voldemort,v_position,'\u2622')
    # Insert bombs into the board B2
    Bomb_positions = [[1,0],[2,2],[3,1],[4,3],[5,2],[6,4],[7,4]]
    for b_pos in Bomb_positions:
        B2.insert_bombs(b_pos)

    print(" \n Your task is to catch Nagini snake at the bottom of the maze")

    success = make_move_in_loop(B1,B2,Potter,'\u2622')
    if success == 0:
        print("End of game! Good Bye")
        return 0
    else:
        print("Potter just destroyed Nagini Snake and earned 3000 health points")
        Potter.health += 3000
        print("Potter's health is {} points ".format(Potter.health))
        # If the user cleared it in single attempt, Potter gets additional life
        if B1.number_of_attempts == 1:
            print("Potter earned an additional life since you cleared in single attempt")
            Potter.life += 1
            print("Potter's number of lives pending are {}".format(Potter.life))
        return 1
def Stage6(Potter,Voldemort):
    """This is final stage of Harry Potter's quest for Voldemort's Horcrux"""
    print()
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("     Entering FINAL STAGE of the game")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print()
    print("You have killed all the horcruxes. Voldemort is FURIOUS!!")
    time.sleep(2)
    print("You have to duel with Voldemort, the most powerful wizard living")
    time.sleep(2)
    print("Duel using below spells!! \n")
    time.sleep(2)
    D1 = Duel(Potter,Voldemort)

    while True:
        try:
            h_spell = D1.spell_selector()
            if h_spell == 0:
                print("Quitting the game. Good bye!")
                return 0
            d_spell = D1.random_spell_selector(Voldemort)
            print("################################")
            print("#   Harry-> {}            ".format(D1.SpellList[h_spell -1]['name']))
            print("#   Voldemort-> {}          ".format(D1.SpellList[d_spell - 1]['name']))
            print("################################")
            time.sleep(2)

            h_damage = D1.get_spell_damage(h_spell) * Potter.wand_multiplier
            d_damage = D1.get_spell_damage(d_spell)
            h_status = D1.take_damage(Potter,Voldemort,d_damage,d_spell)
            d_status = D1.take_damage(Voldemort,Potter,h_damage,h_spell)

            print("###################################")
            print("#   Harry: Health {} Life {}      ".format(Potter.health,Potter.life))
            print("#   Voldemort: Health {} Life {}      ".format(Voldemort.health,Voldemort.life))
            print("###################################")

            # Check for status to determine to continue for another spell
            if h_status == 0:
                print("End of game! Good Bye!")
                return 0
            elif d_status == 0:
                print("#########################################")
                print("#  You won the Duel against Voldemort!  #")
                print("#########################################")
                time.sleep(2)
                return 1
            else:
                raise Exception("Keep firing spells...")
        except Exception as e:
            print(e)

def main():
    # Start Potter with 2 Lives
    Potter = Wizard("\u26d1","Harry",2000,2)
    Voldemort = Wizard("V","Voldemort",5000,3)
    Bellatrix = Wizard("B","Bellatrix",1150,2)
    Dolohov = Wizard("D","Dolohov",1050,1)

    print("J.K Rowling created the wizarding world of Harry Potter.\n")
    time.sleep(3)
    print("Harry Potter is the boy wizard who survived the brutal attack by Voldemort when he was still a baby.\n")
    time.sleep(2)
    print("His mother died protecting Harry, and the encounter left Voldemort weakened. \n")
    time.sleep(2)
    print("Voldemort is back with full powers and wants to take a revenge and kill Harry. \n")
    time.sleep(2)
    print("Harry must kill Voldemort before he kills him. Harry just learnt that Voldemort has created 6 Horcruxes. \n")
    time.sleep(2)
    print("A horcrux is a part of soul and life that gets separated and stored in an object.")
    time.sleep(2)
    print("Dumbledore has killed 1 Horcrux that was stored in Marvolo Gaunt’s Ring.")
    time.sleep(2)
    print("Remaining 5 Horcruxes need to be destroyed.")
    time.sleep(2)
    print("Harry just found them to be in the below :")
    print("1. Tom Riddle’s Diary")
    print("2. Salazar Slytherin’s Locket")
    print("3. Helga Hufflepuff's cup")
    print("4. Rowena Ravenclaw’s diadem")
    print("5. Nagini the snake")

    time.sleep(3)
    print("You are Harry Potter! Find the horcruxes, destroy them and kill Voldemort. Good Luck! ")
    time.sleep(3)

    Potter.select_wand()

    success = Stage1(Potter,Dolohov)
    if success == 0:
        print("You could not pass stage-1. Good luck next time!")
        sys.exit()

    # Now, let us call Stage2
    success = Stage2(Potter,Bellatrix)
    if success == 0:
        print("You could not pass stage-2. Good luck next time!")
        sys.exit()

    # Now, let us call Stage3
    success = Stage3(Potter, Voldemort)
    if success == 0:
        print("You could not pass stage-3. Good luck next time!")
        sys.exit()

    # Now, let us call Stage4
    success = Stage4(Potter, Voldemort)
    if success == 0:
        print("You could not pass stage-4. Good luck next time!")
        sys.exit()
    # Now, let us call Stage5
    success = Stage5(Potter, Voldemort)
    if success == 0:
        print("You could not pass stage-5. Good luck next time!")
        sys.exit()
    # Now, let us call Stage6, the last and final stage
    success = Stage6(Potter, Voldemort)
    if success == 0:
        print("You could not pass stage-6. Good luck next time!")
        sys.exit()
    else:
        print("You finished the final stage. That is the end of the game")
if __name__ == "__main__":
    main()













