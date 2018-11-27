# Text adventure style game where the player leads an army through an invasion
# in which they have to take over territory and recruit as they go. Plays similar
# to Oregon Trail but you can get new members and there aren't random events, every
# run will have the same options at the same areas
import random
SAVE_FILE = 'save.txt'


def main():
    repeat = True
    while repeat:
        choose_game = input('[N]ew Game?\n[C]ontinue?\n[E]xit\n').lower()
        while choose_game != 'n' and choose_game != 'c' and choose_game != 'e':
            choose_game = input('Choose a valid option\n').lower()

        if choose_game == 'n':
            repeat = False
            new_save()
            start()
        elif choose_game == 'c':
            try:
                save = open(SAVE_FILE, 'r')
            except IOError:
                print('No save file found, please choose [N] to create a new game')
            else:
                if save.readline() == '':
                    print('No save data found, please choose [N] to create a new game')
                    save.close()
                else:
                    repeat = False
                    print('Save found')
                    save.close()
                    start()
        elif choose_game == 'e':
            exit()


# Creates or updates the save file into its blank, default, state
def new_save():
    save = open(SAVE_FILE, 'w')
    # File saved with these stats, split by commas
    # save_data[0] Men (0-50)
    # save_data[1] Money (0-infinity)
    # save_data[2] Food (0-infinity)
    # save_data[3:] Claimed Territory (0 or 1) in this order
    # Homeland 0 (Purchase food & men)
    # Forest 0 (Hunt for food, encounter bandits, lose random numbers of men (0-4))
    # Village 0 (Recruit men (Get 0-3 men), buy food, threaten for food and men (Get 0-6 men, 0-20 food, lose 0-2 men))
    # Mountain Pass 0 (Set up camp or continue, if continued, skip to the next forest but lose men from the conditions)
    # Mountain 0 (Continue to forest)
    # Forest 0 (Hunt for food)
    # Village 0 (Recruit men (Get 0-3 men), buy food, threaten for food and men (Get 0-6 men, 0-20 food, lose 0-2 men))
    # Plains 0 (Empty)
    # PreCastle 0 (Set up camp/prep for battle or go to battle immediately)
    # Castle 0 (Lose 8-20 men, if survived you win)
    # Castle after camp 0 (Lose 5-12 men, if survived you win)
    save_data = ['10', '20', '20', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    for val in save_data:
        save.write(val + ',')
    save.close()


def start():
    save = open(SAVE_FILE, 'r')
    save_data = save.readline().split(',')
    save.close()
    for i in range(50):
        print()
    game_loop(save_data)


def game_loop(save_data):
    while int(save_data[0]) > 0 and int(save_data[2]) > 0:
        show_stats(save_data)
        choices(save_data)
        game_over_check(save_data)
        save_game(save_data)


def save_game(save_data):
    save = open(SAVE_FILE, 'w')
    for val in save_data:
        save.write(str(val) + ',')
    save.close()


def show_stats(save_data):
    men = save_data[0]
    gold = save_data[1]
    food_loss = str(int(men) // 2)
    food = save_data[2]
    print('Men: ' + men + '/50     Gold: ' + gold + '     Food: ' + food + '(-' + food_loss + '/travel)\n')


def choices(save_data):
    if save_data[3] == '0':
        level1(save_data)
    elif save_data[4] == '0':
        level2(save_data)
    elif save_data[5] == '0':
        level3(save_data)
    elif save_data[6] == '0':
        level4(save_data)
    elif save_data[7] == '0':
        level5(save_data)
    elif save_data[8] == '0':
        level6(save_data)
    elif save_data[9] == '0':
        level7(save_data)
    elif save_data[10] == '0':
        level8(save_data)
    elif save_data[11] == '0':
        level9(save_data)
    elif save_data[12] == '0':
        level10(save_data)
    else:
        print()
        print('Congratulations you won!')
        play_or_exit()

    food_loss = str(int(save_data[0]) // 2)
    save_data[2] = str(int(save_data[2]) - int(food_loss))


# Homeland
def level1(save_data):
    print('You and your men begin preparing for their invasion on Castle Bhutan.')
    print("Stepping into the marketplace you wonder what supplies you'll need for")
    print('the journey ahead or if you should hire any more loyal men.')
    print()
    choice = ''
    while choice != 'c':
        choice = (input('[B]uy 5 Food (5 gold)     [H]ire Men (10 gold)     [C]ontinue Onward\n')).lower()
        while choice != 'b' and choice != 'h' and choice != 'c':
            choice = (input('Choose a valid option\n')).lower()

        if choice == 'b' and int(save_data[1]) >= 5:
            save_data[2] = str(int(save_data[2]) + 5)
            save_data[1] = str(int(save_data[1]) - 5)
            print(save_data[1] + ' gold left')
        elif choice == 'b' and int(save_data[1]) < 5:
            print("You don't have enough gold for that!")

        if choice == 'h' and int(save_data[1]) >= 10:
            save_data[0] = str(int(save_data[0]) + 1)
            save_data[1] = str(int(save_data[1]) - 10)
            print(save_data[1] + ' gold left')
        elif choice == 'h' and int(save_data[1]) < 10:
            print("You don't have enough gold for that!")
    print()
    print('You and your men set off on their invasion.')
    save_data[3] = 1


# Forest 1
def level2(save_data):
    print('You enter the nearby forest that leads to the main roads.')
    print('This forest is known for its bandits, some say that they steal')
    print('from the rich and give to the poor. Must not be big fans of yours.')
    print()
    investigated = False
    choice = ''
    while choice != 'c':
        choice = (input('[H]unt for Food     [I]nvestigate Bandits     [C]ontinue Onward\n')).lower()
        while choice != 'h' and choice != 'i' and choice != 'c':
            choice = (input('Choose a valid option\n')).lower()

        if choice == 'h':
            men_lost = random.randint(2, 4)
            food_gained = random.randint(5, 15)
            save_data[0] = str(int(save_data[0]) - men_lost)
            save_data[2] = str(int(save_data[2]) + food_gained)
            print('While hunting for food, your men encountered a party of bandits.')
            print('During the strife,', men_lost, 'men were killed.')
            print('The hunting party returned with', food_gained, 'food.')

        if choice == 'i' and not investigated:
            men_lost = random.randint(0, 1)
            gold_gained = random.randint(3, 12)
            save_data[0] = str(int(save_data[0]) - men_lost)
            save_data[1] = str(int(save_data[1]) + gold_gained)
            print('Your men set out to investigate the forest.')
            print('They stumbled upon the bandit camp unseen and decided to take something back.')
            print('The party returned with', gold_gained, 'stolen gold.')
            if men_lost > 0:
                print('However during the raid,', men_lost, 'man was lost')
            investigated = True
        elif choice == 'i' and investigated:
            print("Your men don't want to go back to the bandit camp.")

        show_stats(save_data)
        game_over_check(save_data)

    print()
    print('Exiting the forest you and your men set off to a village along the road.')
    save_data[4] = 1


# Village 1
def level3(save_data):
    print('The village was lively, having had a good harvest the year before.')
    print('You overhear some of your men question if the villagers needed it all for themselves.')
    print('You walk up to the village elder.')
    print()
    recruited = False
    choice = ''
    while choice != 'c':
        choice = (input('[B]uy 5 Food (4 gold)     [R]ecruit Men     [T]hreaten for Men and Food     [C]ontinue Onward\n')).lower()
        while choice != 'b' and choice != 'r' and choice != 't' and choice != 'c':
            choice = (input('Choose a valid option\n')).lower()

        if choice == 'b' and int(save_data[1]) >= 4:
            save_data[2] = str(int(save_data[2]) + 5)
            save_data[1] = str(int(save_data[1]) - 4)
            print(save_data[1] + ' gold left')
        elif choice == 'b' and int(save_data[1]) < 4:
            print("You don't have enough gold for that!")

        if choice == 'r' and not recruited:
            men_gained = random.randint(0, 3)
            save_data[0] = str(int(save_data[0]) + men_gained)
            print(str(men_gained), 'men want to join your cause.')
            recruited = True
        elif choice == 'r' and recruited:
            print('No more villagers wish to join you.')

        if choice == 't':
            men_gained = random.randint(0, 6)
            men_lost = random.randint(0, 3)
            food_gained = random.randint(3, 10)
            save_data[0] = str(int(save_data[0]) + men_gained)
            save_data[0] = str(int(save_data[0]) - men_lost)
            save_data[2] = str(int(save_data[2]) + food_gained)
            print('You demand food and men from the village elder.')
            print('The villagers around jumped into action.')
            if men_lost > 0:
                print('The villagers bested', str(men_lost), 'of your men.')
            if men_gained > 0:
                print('However you prevailed, taking', str(men_gained), 'villagers into your party.')
            print('After the assault your men took', str(food_gained), 'food from the villagers.')
            choice = (input('[C]ontinue Onward\n')).lower()
            while choice != 'c':
                choice = (input('Choose a valid option\n')).lower()

        show_stats(save_data)
        game_over_check(save_data)

    print()
    print('You and your men adventure off towards the mountain pass.')
    save_data[5] = 1


# Mountain Pass
def level4(save_data):
    print('After some hours of hiking your me begin to grow tired.')
    print('As you see dark clouds coming towards the mountain you wonder')
    print('if you should stop for camp now or push through towards the next village.')
    print()
    choice = (input('[S]et up Camp     [C]ontinue Onward\n')).lower()
    while choice != 's' and choice != 'c':
        choice = (input('Choose a valid option\n')).lower()

    if choice == 's':
        save_data[2] = str(int(save_data[2]) - int(save_data[0]) // 2)
        print('You decide to set up camp and wait out the storm.')
        print('The storm is gone by the morning and you begin traveling again.')
        print('During the night your men ate their ration of food.')
        print('You hastily exit the pass spotting a road.')

    if choice == 'c':
        men_lost = random.randint(1, 3)
        save_data[0] = str(int(save_data[0]) - men_lost)
        print('You travel quickly trying to avoid the incoming storm.')
        print('However it catches up quickly,', str(men_lost), 'men sustain injuries from falls and cuts.')
        print('These men drop out of your party as you exit the mountain pass,')
        print('no longer in any condition to battle.')

    show_stats(save_data)
    game_over_check(save_data)

    print()
    print('The road outside of the mountain pass suddenly cuts off, leading towards a forest.')
    save_data[6] = 1


# Forest 2
def level5(save_data):
    print('You enter the forest, following a small trail.')
    print('Your party knows they have to hurry towards Castle Bhutan,')
    print('wanting to be there within 3 days, not willing to sacrifice much time.')
    print()
    hunted = False
    choice = ''
    while choice != 'c':
        choice = (input('[H]unt for Food     [C]ontinue Onward\n')).lower()
        while choice != 'h' and choice != 'i' and choice != 'c':
            choice = (input('Choose a valid option\n')).lower()

        if choice == 'h' and not hunted:
            food_gained = random.randint(5, 15)
            save_data[2] = str(int(save_data[2]) + food_gained)
            print('This forest appears relatively safe, however the party')
            print('wishes to not waste anymore time here.')
            print('The hunting party returned with', food_gained, 'food.')
        elif choice == 'h' and hunted:
            print('While this forest appears relatively safe, the party')
            print('wishes to not waste anymore time here.')

    print()
    print('The forest trail comes to an end, opening up to a clearing.')
    print('A small village sits not far from here.')
    save_data[7] = 1


# Village 2
def level6(save_data):
    print('The village was quiet, not seeing many travellers come through.')
    print('They appear to have an abundance of food, despite being so empty.')
    print('You walk up to the village elder.')
    print()
    recruited = False
    choice = ''
    while choice != 'c':
        choice = (input(
            '[B]uy 5 Food (6 gold)     [R]ecruit Men     [T]hreaten for Men and Food     [C]ontinue Onward\n')).lower()
        while choice != 'b' and choice != 'r' and choice != 't' and choice != 'c':
            choice = (input('Choose a valid option\n')).lower()

        if choice == 'b' and int(save_data[1]) >= 6:
            save_data[2] = str(int(save_data[2]) + 5)
            save_data[1] = str(int(save_data[1]) - 6)
            print(save_data[1] + ' gold left')
        elif choice == 'b' and int(save_data[1]) < 6:
            print("You don't have enough gold for that!")

        if choice == 'r' and not recruited:
            men_gained = random.randint(0, 3)
            save_data[0] = str(int(save_data[0]) + men_gained)
            print(str(men_gained), 'men want to join your cause.')
            recruited = True
        elif recruited:
            print('No more villagers wish to join you.')

        if choice == 't':
            men_gained = random.randint(0, 6)
            men_lost = random.randint(0, 3)
            food_gained = random.randint(3, 10)
            save_data[0] = str(int(save_data[0]) + men_gained)
            save_data[0] = str(int(save_data[0]) - men_lost)
            save_data[2] = str(int(save_data[2]) + food_gained)
            print('You demand food and men from the village elder.')
            print('The villagers around jumped into action.')
            if men_lost > 0:
                print('The villagers bested', str(men_lost), 'of your men.')
            if men_gained > 0:
                print('However you prevailed, taking', str(men_gained), 'villagers into your party.')
            print('After the assault your men took', str(food_gained), 'food from the villagers.')
            choice = (input('[C]ontinue Onward\n')).lower()
            while choice != 'c':
                choice = (input('Choose a valid option\n')).lower()

        show_stats(save_data)
        game_over_check(save_data)

    print()
    print('You and your men travel into the clearing outside the village.')
    save_data[8] = 1


# Plains
def level7(save_data):
    print('You enter the vast plains.')
    print('It dawns on you that the rolling hills are completely empty.')
    print('Some of the ground appears scorched and the grass dead.')
    print()
    choice = ''
    while choice != 'c':
        choice = (input('[C]ontinue Onward\n')).lower()
        while choice != 'c':
            choice = (input('Choose a valid option\n')).lower()

    print()
    print('The castle makes itself obvious in the distance.')
    print('Its gigantic framework towering over the horizon.')
    save_data[9] = 1


# PreCastle
def level8(save_data):
    print('Unsure of how your supplies will last during the invasion you set up camp')
    print('near the castle. Staying and discussing strategies will waste valuable food,')
    print("however you aren't sure how prepared your men are for the battle.")
    print()
    choice = (input('[S]tay and Plan     [C]harge the Castle\n')).lower()
    while choice != 's' and choice != 'c':
        choice = (input('Choose a valid option\n')).lower()

    if choice == 's':
        save_data[2] = str(int(save_data[2]) - int(save_data[0]) // 2)
        print('You stop to discuss strategies. By the time morning comes your men')
        print('feel far more confident about the battle to come. Over the night')
        print('they ate their days worth of rations.')
        save_data[12] = 1

    if choice == 'c':
        print('Your men bolster your confidence and you charge immediately')
        print('towards the castle.')
        save_data[11] = 1

    game_over_check(save_data)

    print()
    print("Outside of the castle gates the king's men stand ready to defend.")
    save_data[2] = str(int(save_data[2]) + int(save_data[0]) // 2)
    save_data[10] = 1


# Castle Camp
def level9(save_data):
    men_lost = random.randint(3, 7)
    print('You push through into the castle!')
    print('Your men seem to know exactly what to do, easily overtaking the enemy.')
    print('During the battle you lose', str(men_lost), 'men.')
    save_data[0] = str(int(save_data[0]) - men_lost)
    save_data[2] = str(int(save_data[2]) + int(save_data[0]) // 2)
    game_over_check(save_data)
    print('You storm into the throne room.')
    print()
    choice = (input('[T]ake the Crown\n')).lower()
    while choice != 't':
        choice = (input('Choose a valid option\n')).lower()

    print()
    print('You quickly slay the king.')
    print('Taking the crown, you make yourself the new king.')
    save_data[11] = 1


# Castle no Camp
def level10(save_data):
    men_lost = random.randint(7, 15)
    print('You push through into the castle!')
    print('Your men struggle to overcome the enemy.')
    print('During the battle you lose', str(men_lost), 'men.')
    save_data[0] = str(int(save_data[0]) - men_lost)
    save_data[2] = str(int(save_data[2]) + int(save_data[0]) // 2)
    game_over_check(save_data)
    print('You storm into the throne room.')
    print()
    choice = (input('[T]ake the Crown\n')).lower()
    while choice != 't':
        choice = (input('Choose a valid option\n')).lower()

    print()
    print('You quickly slay the king.')
    print('Taking the crown, you make yourself the new king.')
    save_data[12] = 1


def game_over_check(save_data):
    if int(save_data[0]) <= 0:
        print('Losing your last men, you find yourself alone.')
        print('You cannot continue the invasion by yourself.')
        print('GAME OVER')
        play_or_exit()

    if int(save_data[2]) <= 0:
        print('With your food supplies dwindling, your men return home.')
        print('You cannot continue the invasion by yourself.')
        print('GAME OVER')
        play_or_exit()


def play_or_exit():
    choice = (input('[P]lay Again?     [E]xit\n')).lower()
    while choice != 'p' and choice != 'e':
        choice = (input('Choose a valid option\n')).lower()
    if choice == 'p':
        new_save()
        start()
    if choice == 'e':
        exit()


main()
