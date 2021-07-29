from abc import ABC, abstractmethod
from ships import Ship, TwoSquareShip, ThreeSquareShip, OneSquareShip, ShipPositionError
from field import Field
from random import randint


class Player(ABC):
    
    def __init__(self, my_field: Field, opponent_field: Field):
        self.my_field = my_field
        self.opponent_field = opponent_field
        self.my_ships = []
        self.previously_attacked = [[0,0]]

    def add_ship(self, ship: Ship):
        self.my_ships.append(ship)
    
    @abstractmethod
    def place_ships(self):
        pass
    

class HumanPlayer(Player):

    def place_ships(self):
        # place three deck ship
        while True:
            print("Place BATTLESHIP(3 squares)\n")
            while True:
                try:
                    print("Placing Head:")
                    head_position = [int(input("Choose row: ")),int(input("Choose column: "))]
                except ValueError:
                    print("Not an integer! Try again!\n")
                    continue
                else:
                    break

            while True:
                try:
                    print("\nPlacing Tail:")
                    tail_position = [int(input("Choose row: ")), int(input("Choose column: "))]
                except ValueError:
                    print("Not an integer! Try again!\n")
                    continue
                else:
                    break
            
            try:
                self.add_ship(ThreeSquareShip(head_position, tail_position, self.my_field))
            
            except ShipPositionError:
                print("\nThis position is not valid! Please try again:\n")
            else:
                self.my_field.display_field()
                break

        # place two deck ships
        number_of_cruisers = 0
        while number_of_cruisers < 2:
            print("Place CRUISER(2 squares)\n")
            while True:
                try:
                    print("Placing Head:")
                    head_position = [int(input("Choose row: ")), int(input("Choose column: "))]
                except ValueError:
                    print("Not an integer! Try again!\n")
                    continue
                else:
                    break

            while True:
                try:
                    print("\nPlacing Tail:")
                    tail_position = [int(input("Choose row: ")), int(input("Choose column: "))]
                except ValueError:
                    print("Not an integer! Try again!\n")
                    continue
                else:
                    break

            try:
                self.add_ship(TwoSquareShip(head_position, tail_position, self.my_field))

            except ShipPositionError:
                print("\nThis position is not valid! Please try again:\n")
            else:
                self.my_field.display_field()
                number_of_cruisers += 1

        # place one deck ships
        number_of_destroyers = 0
        while number_of_destroyers < 4:
            print("Place DESTROYER(1 square)\n")
            while True:
                try:
                    print("Placing Ship:")
                    position = [int(input("Choose row: ")), int(input("Choose column: "))]
                except ValueError:
                    print("Not an integer! Try again!\n")
                    continue
                else:
                    break

            try:
                self.add_ship(OneSquareShip(position, self.my_field))

            except ShipPositionError:
                print("\nThis position is not valid! Please try again:\n")
            else:
                self.my_field.display_field()
                number_of_destroyers += 1

        print("All ships are placed, get ready for battle!\n")

    def check_loss(self) -> bool:
        loss = True
        for ship in self.my_ships:
            if ship.alive:
                loss = False
                break
        return loss


class EasyModeHumanPlayer(HumanPlayer):

    def ask_opponent(self) -> bool:
        miss = True

        while True:
            row = randint(1, 6)
            column = randint(1, 6)
            if [row, column] in self.previously_attacked:
                continue
            else:
                self.previously_attacked.append([row, column])
                break

        for ship in self.my_ships:
            if ship.is_part([row, column]):
                miss = False
                self.my_field.set_cell([row, column], "X")
            ship.is_defeated(self.my_field)

        if miss:
            self.my_field.set_cell([row, column], "T")
            
        return miss


class HardModeHumanPlayer(HumanPlayer):

    def ask_opponent(self) -> bool:
        miss = True
        possible_strikes = []
        possible_attacks = []

        first_x_found = False
        first_x_row = None
        first_x_column = None

        second_x_found = False
        second_x_row = None
        second_x_column = None

        shot = []

        for line in self.my_field.get_content():
            for item in line:
                if item == "X":
                    first_x_found = True
                    first_x_row = self.my_field.get_content().index(line) + 1
                    first_x_column = line.index(item) + 1

                    if first_x_row == 1 and first_x_column == 1:
                        possible_strikes = [[1, 2], [2, 1]]
                    elif first_x_row == 1 and first_x_column == 6:
                        possible_strikes = [[1, 5], [2, 6]]
                    elif first_x_row == 6 and first_x_column == 6:
                        possible_strikes = [[6, 5], [5, 6]]
                    elif first_x_row == 6 and first_x_column == 1:
                        possible_strikes = [[5, 1], [6, 2]]
                    elif first_x_row == 1 and 1 < first_x_column < 6:
                        possible_strikes = [[1, first_x_column - 1], [1, first_x_column + 1], [2, first_x_column]]
                    elif first_x_row == 6 and 1 < first_x_column < 6:
                        possible_strikes = [[6, first_x_column - 1], [6, first_x_column + 1], [5, first_x_column]]
                    elif 1 < first_x_row < 6 and first_x_column == 1:
                        possible_strikes = [[first_x_row - 1, 1], [first_x_row + 1, 1], [first_x_row, 2]]
                    elif 1 < first_x_row < 6 and first_x_column == 6:
                        possible_strikes = [[first_x_row - 1, 6], [first_x_row + 1, 6], [first_x_row, 5]]
                    else:
                        possible_strikes = [[first_x_row, first_x_column - 1], [first_x_row, first_x_column + 1],
                                            [first_x_row - 1, first_x_column], [first_x_row + 1, first_x_column]]
                    break
                else:
                    continue
            if first_x_found:
                break

        if first_x_found:
            for strike in possible_strikes:
                if self.my_field.get_cell(strike) == "X":
                    second_x_found = True
                    second_x_row = strike[0]
                    second_x_column = strike[1]

        if second_x_found:

            vertical_condition = first_x_column == second_x_column
            if vertical_condition:
                if first_x_row < second_x_row:
                    possible_attacks = [[first_x_row - 1, first_x_column], [second_x_row + 1, first_x_column]]
                else:
                    possible_attacks = [[second_x_row - 1, first_x_column], [first_x_row + 1, first_x_column]]
            else:
                if first_x_column < second_x_column:
                    possible_attacks = [[first_x_row, first_x_column - 1], [first_x_row, second_x_column + 1]]
                else:
                    possible_attacks = [[first_x_row, second_x_column - 1], [first_x_row, first_x_column + 1]]

            for position in possible_attacks:
                if position[0] > 0 and position[1] > 0:
                    try:
                        target = self.my_field.get_cell(position)
                    except IndexError:
                        continue
                    else:
                        if not target in ["X", "#", "T"]:
                            for ship in self.my_ships:
                                if ship.is_part(position) and miss:
                                    miss = False
                                    self.my_field.set_cell(position, "X")
                                    ship.is_defeated(self.my_field)
                                    break

                            if miss:
                                self.my_field.set_cell(position, "T")
                                break


        elif first_x_found:
            for position in possible_strikes:
                if position[0] > 0 and position[1] > 0:
                    try:
                        target = self.my_field.get_cell(position)
                    except IndexError:
                        continue
                    else:
                        if not target in ["X", "#", "T"]:
                            for ship in self.my_ships:
                                if ship.is_part(position) and miss:
                                    miss = False
                                    self.my_field.set_cell(position, "X")
                                    ship.is_defeated(self.my_field)
                                    break

                            if miss:
                                self.my_field.set_cell(position, "T")
                                break

        else:
            while True:
                row = randint(1, 6)
                column = randint(1, 6)

                if self.my_field.get_cell([row, column]) in ["X", "#", "T"]:
                    continue
                else:
                    break

            for ship in self.my_ships:
                if ship.is_part([row, column]):
                    miss = False
                    self.my_field.set_cell([row, column], "X")
                ship.is_defeated(self.my_field)

            if miss:
                self.my_field.set_cell([row, column], "T")
                
        return miss


class AIPlayer(Player):

    def place_ships(self):

        while True:
            # place three deck ship
            while True:
                head_position = [randint(1,6), randint(1, 6)]
                tail_position = [0,0]
                #decide on tail position
                row_random = randint(0,1)
                column_random = randint(0,1)
                if column_random == 0:
                    # chosen horizontal
                    tail_position[0] = head_position[0]
                    if row_random == 0:
                        # chosen right
                        tail_position[1] = head_position[1] + 2
                    elif row_random == 1:
                        # chosen left
                        tail_position[1] = head_position[1] - 2
                elif column_random == 1:
                    # chosen vertical
                    tail_position[1] = head_position[1]
                    if row_random == 0:
                        # chosen down
                        tail_position[0] = head_position[0] + 2
                    elif row_random == 1:
                        # chosen up
                        tail_position[0] = head_position[0] - 2

                try:
                    self.add_ship(ThreeSquareShip(head_position, tail_position, self.my_field))
                except ShipPositionError:
                    continue
                else:
                    break

            # place two deck ships
            number_of_cruisers = 0
            while number_of_cruisers < 2:
                head_position = [randint(1, 6), randint(1, 6)]
                tail_position = [0, 0]
                # decide on tail position
                row_random = randint(0, 1)
                column_random = randint(0, 1)
                if column_random == 0:
                    # chosen horizontal
                    tail_position[0] = head_position[0]
                    if row_random == 0:
                        # chosen right
                        tail_position[1] = head_position[1] + 1
                    elif row_random == 1:
                        # chosen left
                        tail_position[1] = head_position[1] - 1
                elif column_random == 1:
                    # chosen vertical
                    tail_position[1] = head_position[1]
                    if row_random == 0:
                        # chosen down
                        tail_position[0] = head_position[0] + 1
                    elif row_random == 1:
                        # chosen up
                        tail_position[0] = head_position[0] - 1

                try:
                    self.add_ship(TwoSquareShip(head_position, tail_position, self.my_field))
                except ShipPositionError:
                    continue
                else:
                    number_of_cruisers += 1

            # place one deck ships
            number_of_destroyers = 0
            number_of_tries = 0
            while number_of_destroyers < 4:
                position = [randint(1, 6), randint(1, 6)]

                try:
                    self.add_ship(OneSquareShip(position, self.my_field))
                except ShipPositionError:
                    number_of_tries += 1
                    continue
                else:
                    number_of_destroyers += 1
                finally:
                    if number_of_tries >= 1000:
                        break

            if number_of_destroyers == 4:
                break
            else:
                self.my_field.clear_field()
                self.my_ships = []
                continue

    def ask_opponent(self) -> bool:
        miss = True

        while True:
            while True:
                try:
                    row = int(input("Choose attack row: "))
                    column = int(input("Choose attack column: "))
                except ValueError:
                    print("Not an integer, please try again: ")
                    continue
                else:
                    break

            if not 0 < row <= 6 or not 0 < column <= 6:
                print("Invalid position! Please try again:\n")
                continue
            else:
                break

        for ship in self.my_ships:
            if ship.is_part([row, column]):
                miss = False
                self.my_field.set_cell([row, column], "X")
            ship.is_defeated(self.my_field)

        if miss:
            self.my_field.set_cell([row, column], "T")
            
        return miss

    def check_loss(self) -> bool:
        loss = True
        for ship in self.my_ships:
            if ship.alive:
                loss = False
                break
        return loss





"""
# TODO:
#       design game loop with turn repeats
#       TEST TEST TEST
"""