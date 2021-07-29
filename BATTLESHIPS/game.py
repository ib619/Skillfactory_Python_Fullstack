from field import Field
from player import HardModeHumanPlayer, EasyModeHumanPlayer, AIPlayer
from random import randint
import time


# main game loop
while True:
    my_field = Field()
    opponent_field = Field()

    ai_player = AIPlayer(opponent_field, my_field)
    my_player = None

    # choice of difficulty
    while True:
        print("WELCOME TO BATTLESHIPS!!!\n")

        difficulty_choice = input("Please choose the difficulty [EASY/HARD]: ")
        if difficulty_choice == "EASY":
            print("You have chosen the " + difficulty_choice + " difficulty!\n")
            my_player = EasyModeHumanPlayer(my_field, opponent_field)
            break
        elif difficulty_choice == "HARD":
            print("You have chosen the " + difficulty_choice + " difficulty!\n")
            my_player = HardModeHumanPlayer(my_field, opponent_field)
            break
        else:
            print("Invalid choice, please try again!\n")
            continue

    # placing ships
    print("Now place your ships, captain!")
    my_field.display_field()
    my_player.place_ships()
    ai_player.place_ships()

    # removing ship contours
    my_field.remove_ship_contours()
    opponent_field.remove_ship_contours()

    # hiding opponents ships
    opponent_field.hide_ships()

    # attack loop
    human_player_turn = True
    while True:
        # displaying both fields
        print("My Field")
        my_field.display_field()
        print("Opponent's Field")
        opponent_field.display_field()

        if human_player_turn:
            print("It is your turn! Choose the attack target: \n")
            miss = ai_player.ask_opponent()
            print("")
            if miss:
                print("Looks like you've missed!\n")
                human_player_turn = False
            else:
                print("Good shot! You've hit the opponent's ship.\n ")
                human_player_turn = True
                if ai_player.check_loss():
                    print("Yay! You win!\n")
                    print("Opponent's Field")
                    opponent_field.display_field()
                    break
                else:
                    print("You get an extra round!\n ")
        else:
            print("It is your opponent's turn! Your opponent is thinking...\n")
            time.sleep(randint(4, 8))
            print("Your opponent has fired!\n")
            miss = my_player.ask_opponent()
            if miss:
                print("You are lucky! Your opponent missed!\n")
                human_player_turn = True
            else:
                print("Unfortunately, your ship was hit!\n")
                human_player_turn = False
                if my_player.check_loss():
                    print("Oh no! You have lost!\n")
                    print("Your Field")
                    my_field.display_field()
                    break
                else:
                    print("Your opponent gets an extra round!\n ")

    another_game = input("Want to play again? Just write <Y>! ")
    if another_game == "Y":
        continue
    else:
        print("\nThank you for playing. Goodbye!")
        break


