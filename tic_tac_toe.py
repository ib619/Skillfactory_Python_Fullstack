from random import randrange

def create_field(size):
    Field = [["-" for x in range(size)] for y in range(size)]
    return Field

def display_header(size):
    header = " "
    for i in range(size):
        header = header + " " + str(i)
    print(header)

def display_field(Field):
    i = 0
    for line in Field:
        row = ' '.join(line)
        print(str(i) + " " + row)
        i += 1
    print("")

def player_turn(player, Field):

    if player == 'X':
        print("Player X turn: ")
    elif player == 'O':
        print("Player O turn: ")
    while True:
        row = int(input("Select Row: "))
        collumn = int(input("Select Collumn: "))
        if Field[row][collumn] != '-':
            print("This cell is not empty! Please choose another one.")
        else: break

    if player == 'X':
        Field[row][collumn] = "x"
    else:
        Field[row][collumn] = "o"
    print("")

def check_rows(Field):
    win = True
    element = ''
    for line in Field:
        element = line[0]
        for item in line:
            if element != item or element == '-':
                win = False
                break
            else: win = True
        if win and element != '-': break
    if win:
        display_header(field_size)
        display_field(myField)
        print("Player " + element.capitalize() + " Wins!\n")

    return win


def check_collumns(Field, size):
    win = True
    element = Field[0][0]
    for i in range(size):
        element = Field[0][i]
        for j in range(size):
            if Field[j][i] != element:
                win = False
                break
            else: win = True
        if win and element != '-': break
    if win and element != '-':
        display_header(field_size)
        display_field(myField)
        print("Player " + element.capitalize() + " Wins!\n")


def mirror(Field, size):
    result = create_field(size)
    for i in range(size):
        for j in range(size):
            result[i][j] = Field[i][size - 1 - j]
    return result


def check_diagonal(Field, size):
    win = True
    element = Field[0][0]
    for i in range(size):
        if Field[i][i] != element or element == '-':
            win = False
            break
    if win:
        display_header(field_size)
        display_field(myField)
        print("Player " + element.capitalize() + " Wins!\n")

    return win

def check_draw(Field):
    draw = False
    summary = ''
    for line in Field:
        summary += ''.join(line)
    if '-' in summary:
        draw = False
    else:
        draw = True
        print("Draw!")
    return draw




def check_win(Field, size):

    return check_rows(myField) or check_collumns(myField, size) or check_diagonal(myField, size) or check_diagonal(mirror(myField,size), size)


field_size = 3
myField = create_field(field_size)
myPlayer = "X"
game_on = True
setup = True

while game_on:
    if setup:
        if randrange(10) % 2 == 0:
            myPlayer = "X"
        else: myPlayer = "O"

        field_size = int(input("Enter Field size: "))
        myField = create_field(field_size)
        setup = False

    display_header(field_size)
    display_field(myField)

    player_turn(myPlayer, myField)

    if myPlayer == 'X': myPlayer = 'O'
    else: myPlayer = 'X'

    if check_win(myField, field_size) or check_draw(myField):
        choice = input("Next Game?[Y/N]")
        if choice == 'Y':
            setup = True
            game_on = True
        else:
            game_on = False
            print("Thank you for playing! Goodbye!")