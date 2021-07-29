class Field:

    def __init__(self):
        self.field_size = 6
        self.field = [["O" for x in range(self.field_size)] for y in range(self.field_size)]

    def display_field(self):
        header = [f"{x + 1}" for x in range(self.field_size)]
        print("\n  | " + " | ".join(header) + " | ")

        index = 1
        for line in self.field:
            print(str(index) + " | " + " | ".join(line) + " | ")
            index += 1
        print("")
        
    def remove_ship_contours(self):
        for row_index, row in enumerate(self.field):
            for column_index, column in enumerate(row):
                if self.field[row_index][column_index] == "X":
                    self.field[row_index][column_index] = "O"

    def set_cell(self, position: list[int, int], value: str) -> None:
        self.field[position[0] - 1][position[1] - 1] = value

    def get_cell(self, position: list[int, int]) -> str:
        return self.field[position[0] - 1][position[1] - 1]
    
    def clear_field(self):
        self.field = [["O" for x in range(self.field_size)] for y in range(self.field_size)]
        
    def get_content(self):
        return self.field
    
    def hide_ships(self):
        for line in self.field:
            for item in line:
                if item == "\u25A0":
                    self.set_cell([self.field.index(line) + 1, line.index(item) + 1], "O")
                else:
                    continue