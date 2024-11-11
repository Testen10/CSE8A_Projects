import time
from char import Character
import random as r
"""
character rpg

init char setting
    1. choose job
        ㄴ swordman(balance), archer(ATK high), warrior(DEF, HP high)
    2. state decide - random
        ㄴ atk / def / hp
    3. enter name

Can select 2: go to stage or take a rest
stage / random, 4 types
    1. item / weapon(ATK + 1) or armor(DEF + 1) or portion(portion +1)
    2. Fight with monster
        win: random stat +2
        lose: HP-3
    3. trap (HP-1 or HP-2)
    4. Nothing

rest
    HP + 1

After n turns, PVP
choice: attack or use poriton
ㄴ attack: miss / normal / critical
ㄴ portion: recover all HP

HP = 0 --> defeat
"""    
TYELLOW = '\033[33m'
ENDC = '\033[m'

def game_start(max_turn, p1_color, p2_color):
    """
    main function that operates the game

    1. create character
    2. stage explore
    3. pvp

    input: max_turn(int), p1_color(str), p2_color(str)
    output: None
    """
    character_list = []

    for elem in "Welcome To Project3_RPG.":
        time.sleep(0.05)
        print('\033[33m'+elem, end='', flush=True)
    print("", ENDC)

    time.sleep(1)

    print(TYELLOW+"Create your own Character, go for an adventure, and fight with the other player!")
    time.sleep(0.3)
    print("Number of player: 2", ENDC)
    time.sleep(0.5)


    character_list.append(create_character(1, p1_color)) # player 1 character
    time.sleep(1)
    character_list.append(create_character(2, p2_color)) # player 2 character
    time.sleep(1)

    adventure_tutorial()

    turn = 0
    while turn<max_turn: # max turn pre-defined in "__main__"
        print("")
        print(character_list[turn%2].text_color + "** Player {}'s Turn **".format(turn%2+1), ENDC)
        print("Are you going to move {}?".format(character_list[turn%2].name))

        while True:
            select = input("Select by number 1. Yes // 2. No : ")
            try:
                select = int(select)
            except:
                print("Enter integer value.")

            if not(select==1 or select ==2):
                    print("Choose proper integer")
            else:
                print("")
                if select == 1:
                    temp = r.randint(0,3)
                    stage(temp, character_list, turn)
                else:
                    print(TYELLOW+"{} decided to take a rest.".format(character_list[turn%2].name), ENDC)
                    character_list[turn%2].change_HP(2)
                break

        time.sleep(0.5)
        character_list[turn%2].print_charInfo() # show the updated characters state
        time.sleep(1)

        turn += 1
    
    pvp_tuorial()

    turn = 0
    while True: # pvp is continued until one of the character's remaining HP becomes 0.
        pvp(turn, character_list)
        check_defeat(character_list)
        turn +=1
        print("")

def create_character(player_num, p_color):
    """docstring
    gets name & job from user & creates and returns character based on that info
    
    input: player num
    output: Character obj
    """
    print(" ")

    while True:
        name = input(p_color + "Player{} , enter character name: ".format(player_num))
        if len(name) == 0: print("Enter the proper name.") # when nothing is entered
        else: break

    char = Character(name, p_color) # create character object

    print(ENDC, end ="")
    print("-----")
    print(TYELLOW+"1. Swordman"+ENDC+": Balance type")
    print(TYELLOW+"2. Archer"+ENDC+": high ATK, low HP")
    print(TYELLOW+"3. Warrior"+ENDC+": DEF&HP, low ATK")
    print("-----")
    while True:
        job = input("Player{} , choose the character's job by number: ".format(player_num))

        try:
            job = int(job)

            if not (job==1 or job==2 or job==3): print("Choose a proper number.")
            else:
                print("Your character is created.")
                break
        except:
            print("Input a integer")


    char.set_initstate(job)
    char.print_charInfo()

    return char

def stage(stage_type, character_list, turn):
    """docstring
    function where stage exploration is operated

    input: stage_type(int), character_list(list of Character object), turn(int)
    output: None
    """
    character = character_list[turn%2]
    if stage_type == 0: # get item
        event_type = r.randint(0,2) # decide the type of item the character will get

        if event_type == 0:
            print(TYELLOW+"{} found a new weapon!".format(character.name), ENDC)
            character.state_up(character.state_list[0], 1)
        elif event_type == 1:
            print(TYELLOW+"{} found a new armor!".format(character.name), ENDC)
            character.state_up(character.state_list[1], 1)
        else:
            print(TYELLOW+"{} found a portion!".format(character.name), ENDC)
            character.get_portion()

    elif stage_type == 1: # fight with monster
        print(TYELLOW+"{} encountered a monster!".format(character.name),ENDC)
        time.sleep(1)
        print(".")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)

        win_lose = r.randint(0,1) # decide wheter the character will win or lose

        if win_lose == 0:
            print("The monster was too strong. {} fled...". format(character.name))
            character.change_HP(-3)
        else:
            print("{} won!". format(character.name))

            increase_type = r.randint(0,2) # decide the type of state that will increase

            print("Level up! {}'s {} increased by 2!". format(character.name, character.state_list[increase_type]))
            
            character.state_up(character.state_list[increase_type], 2)
            character.change_HP(-1)

    elif stage_type == 2: # trap 
        print(TYELLOW+"There was a trap. {} got hurt.". format(character.name), ENDC)
        character.change_HP(-1*r.randint(1,2)) # randomly decrease character's remaining HP by 1 or 2

    else: # nothing 
        print(TYELLOW+"Nothing happenend.", ENDC)
    
    check_defeat(character_list)
        
def pvp(turn, character_list):
    char = character_list[turn%2]
    enemy = character_list[int(not(turn%2))]
    
    print(character_list[turn%2].text_color+"** Player {}'s Turn **".format(turn%2+1), ENDC)
    print("{}, what are you going to do?".format(char.name))

    while True:
        print("Choose by number 1. Attack", end = ' ')
        if char.remain_portion > 0:
            print("2. Use Portion (remaining: {})".format(char.remain_portion), end = "")

        action = input(": ")

        try:
            action = int(action)
        except:
            print("Enter an appropriate integer.")
            continue

        if action in [1,2]:
            if action == 1: # attack
                print("{}'s attack!".format(char.name))
                time.sleep(0.5)
                char.attack(r.randint(0,10), enemy) # the random number decides the type of attack(miss,normal,critical)
                break

            elif action == 2 and char.remain_portion>0: # use portion, only if there is remaining function
                print(TYELLOW+"{} used portion!".format(char.name),ENDC)
                char.use_portion()
                break
        
        print("Select between the given choices.")
    
    time.sleep(0.5)
    check_defeat(character_list)

    # print updated character info.
    # Since the player only need to know the HP & remaining portion during pvp, print simplified version
    character_list[0].print_charInfo_simple()
    character_list[1].print_charInfo_simple()

def check_defeat(character_list):
    """docstring
    check if character's HP is 0 // if HP = 0, end game
    """
    if character_list[0].check_defeat(): # check if the character's remaining HP is 0
        print("")
        print(character_list[0].text_color+"{} is unable to move!".format(character_list[0].name), ENDC)
        time.sleep(0.5)
        print(character_list[1].text_color+"{} won the PVP!!".format(character_list[1].name), ENDC)
        time.sleep(0.5)
        print(TYELLOW+"Congrats, Player {}!".format(2),ENDC)
        
        exit()

    elif character_list[1].check_defeat(): # check if the character's remaining HP is 0
        print("")
        print(character_list[1].text_color+"{} is unable to move!".format(character_list[1].name), ENDC)
        time.sleep(0.5)
        print(character_list[0].text_color+"{} won the PVP!!".format(character_list[0].name), ENDC)
        time.sleep(0.5)
        
        print(TYELLOW+"Congrats, Player {}!".format(1),ENDC)
        
        exit()

def adventure_tutorial():
    for elem in "!!! Adventure time !!!":
        time.sleep(0.05)
        print(TYELLOW+elem, end='', flush=True)
    print("",ENDC)

    time.sleep(0.5)
    
    print("You have two chocies: moving your character or taking a rest.")
    time.sleep(0.2)
    print("If you choose to move, your character will encounter four types of stages randomly.")
    time.sleep(0.2)
    print("")
    print(TYELLOW+"   1. Finding a new item", ENDC)
    print("      : You will either find a new weapon(ATK+1), a new armor(DEF+1), or a portion(remaining portion+1)")
    time.sleep(0.2)
    print(TYELLOW+"   2. Fighting with a monster", ENDC)
    print("      : If you win, one of your ATK, DEF, or HP will increase by 2, and your remaining HP will decrease by 1.")
    print("        If you lose, your remaining HP will decrease by 3.")
    time.sleep(0.2)
    print(TYELLOW+"   3. Trap", ENDC)
    print("      : Your remaining HP decreases by either 1 or 2.")
    time.sleep(0.2)
    print(TYELLOW+"   4. Nothing", ENDC)
    print("      : Nothing changes.")
    time.sleep(0.2)
    print("")
    print("If you choose to take a rest, your remaining HP will increase by 2.")
    time.sleep(0.2)

def pvp_tuorial():
    print("")
    for elem in "!!! PVP TIME !!!":
        time.sleep(0.05)
        print(TYELLOW+elem, end='', flush=True)
    print("",ENDC)
    time.sleep(1)

    print("In you turn, you have two choices.")
    time.sleep(0.2)
    print("")
    print(TYELLOW+"   1. Attack",ENDC)
    print("      : Attack your enemy! The type of attacks are " +TYELLOW+"miss, normal, or critical."+ENDC)
    time.sleep(0.2)
    print(TYELLOW+"   2. Use Portion",ENDC)
    print("      : The portion will"+TYELLOW+" fully restore your remaining HP.",ENDC)
    print("")
    time.sleep(0.5)

if __name__ == '__main__':
    turn = 2
    p1_color = '\033[31m'
    p2_color = '\033[34m'
    game_start(turn, p1_color, p2_color)