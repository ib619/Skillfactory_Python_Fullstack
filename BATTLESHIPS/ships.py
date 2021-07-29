from abc import ABC, abstractmethod
from field import Field


class ShipPositionError(Exception):
    def __init__(self, message='Invalid Ship Position'):
        super(ShipPositionError, self).__init__(message)


class Ship(ABC):

    @abstractmethod
    def __init__(self, head_position: list[int, int], tail_position: list[int, int]):
        pass

    @abstractmethod
    def place(self, field: Field) -> None:
        pass

    @abstractmethod
    def mark_area(self, field: Field) -> None:
        pass

    @abstractmethod
    def check_position_validity(self, head_position: list[int, int], tail_position: list[int, int], field: Field) -> bool:
        pass
    
    @abstractmethod
    def is_part(self, position: list[int, int]) ->bool:
        pass
    
    @abstractmethod
    def is_defeated(self, field: Field) -> bool:
        pass
    

class OneSquareShip(Ship):

    def __init__(self, position: list[int, int], field: Field):
        position_valid = self.check_position_validity(position, field)
        if not position_valid:
            raise ShipPositionError()
        self.position = position
        self.place(field)
        self.mark_area(field)
        self.alive = True


    def place(self, field: Field) -> None:
        field.set_cell(self.position, "\u25A0")

    def mark_area(self, field: Field) -> None:
        start_position = [self.position[0] - 1, self.position[1] - 1]
        finish_position = [self.position[0] + 1, self.position[1] + 1]

        for row in range(start_position[0], finish_position[0] + 1):
            for collumn in range(start_position[1], finish_position[1] + 1):
                try:
                    if row > 0 and collumn > 0:
                        if [row, collumn] != self.position:
                            field.set_cell([row, collumn], "X")
    
                except IndexError:
                    pass



    def check_position_validity(self, position: list[int, int], field: Field) -> bool:
        # check that input is in the field bounds
        for item in position:
            if 0 < item <= field.field_size:
                continue
            else:
                return False

        # check for valid cell:
        if field.get_cell(position) != "O":
            return False
        else:
            return True
        
    def is_part(self, position: list[int, int]) ->bool:
        if position == self.position:
            return True
        else:
            return False
        
    def is_defeated(self, field: Field):
        if not self.alive:
            self.alive = self.alive
        elif field.get_cell(self.position) == "X":
            field.set_cell(self.position, "#")
            self.alive = False
        else:
            self.alive = True
        

class TwoSquareShip(Ship):

    def __init__(self, head_position: list[int, int], tail_position: list[int, int], field: Field):
        self.orientation = ""
        position_valid = self.check_position_validity(head_position, tail_position, field)
        if not position_valid:
            raise ShipPositionError()
        self.head_position = head_position
        self.tail_position = tail_position
        self.place(field)
        self.mark_area(field)
        self.alive = True

    def place(self, field: Field) -> None:
        field.set_cell(self.head_position, "\u25A0")
        field.set_cell(self.tail_position, "\u25A0")

    def mark_area(self, field: Field) -> None:

        start_position: list[int, int]
        finish_position: list[int, int]
        if self.orientation == "vertical":
            if self.head_position[0] < self.tail_position[0]:
                start_position = [self.head_position[0] - 1, self.head_position[1] - 1]
                finish_position = [self.tail_position[0] + 1, self.tail_position[1] + 1]
            else:
                start_position = [self.tail_position[0] - 1, self.tail_position[1] - 1]
                finish_position = [self.head_position[0] + 1, self.head_position[1] + 1]

        elif self.orientation == "horizontal":
            if self.head_position[1] < self.tail_position[1]:
                start_position = [self.head_position[0] - 1, self.head_position[1] - 1]
                finish_position = [self.tail_position[0] + 1, self.tail_position[1] + 1]
            else:
                start_position = [self.tail_position[0] - 1, self.tail_position[1] - 1]
                finish_position = [self.head_position[0] + 1, self.head_position[1] + 1]


        for row in range(start_position[0], finish_position[0] + 1):
            for collumn in range(start_position[1], finish_position[1] + 1):
                try:
                    if row > 0 and collumn > 0:
                        if [row, collumn] != self.tail_position and [row, collumn] != self.head_position:
                            field.set_cell([row, collumn], "X")

                except IndexError:
                    pass

    def check_position_validity(self, head_position: list[int, int], tail_position: list[int, int], field: Field) -> bool:

        position_list = head_position + tail_position

        # check that input is in the field bounds
        for item in position_list:
            if 0 < item <= field.field_size:
                continue
            else:
                return False

        # check for vertical/horizontal
        if head_position[0] == tail_position[0]:
            self.orientation = "horizontal"
        elif head_position[1] == tail_position[1]:
            self.orientation = "vertical"
        else:
            return False
        
        # check adjacent
        if self.orientation == "horizontal":
            if abs(head_position[1] - tail_position[1]) > 1:
                return False
        elif self.orientation == "vertical":
            if abs(head_position[0] - tail_position[0]) > 1:
                return False

        # check for valid cell:
        if field.get_cell(head_position) != "O" or field.get_cell(tail_position) != "O":
            return False
        else:
            return True
        
    def is_part(self, position: list[int, int]) ->bool:
        if position in [self.head_position, self.tail_position]:
            return True
        else:
            return False
        
    def is_defeated(self, field: Field):
        is_defeated = True
        if not self.alive:
            self.alive = self.alive
        else:
            position_data = [self.head_position, self.tail_position]
            for position in position_data:
                if field.get_cell(position) != "X":
                    is_defeated = False
                    break
                    
            if is_defeated:
                for position in position_data:
                    field.set_cell(position, "#")
                self.alive = False
                


class ThreeSquareShip(Ship):
    middle_position: list[int, int]
    
    def __init__(self, head_position: list[int, int], tail_position: list[int, int], field: Field):
        self.TYPE = 3
        self.orientation = ""
        position_valid = self.check_position_validity(head_position, tail_position, field)
        if not position_valid:
            raise ShipPositionError()
        self.head_position = head_position
        self.tail_position = tail_position
        self.place(field)
        self.mark_area(field)
        self.alive = True
        
    def place(self, field: Field) -> None:
        field.set_cell(self.head_position, "\u25A0")
        field.set_cell(self.tail_position, "\u25A0")
        
        if self.orientation == "horizontal":
            if self.head_position[1] < self.tail_position[1]:
                self.middle_position = [self.head_position[0], self.head_position[1] + 1]
                field.set_cell(self.middle_position, "\u25A0")
            else:
                self.middle_position = [self.head_position[0], self.head_position[1] - 1]
                field.set_cell(self.middle_position, "\u25A0")
        elif self.orientation == "vertical":
            if self.head_position[0] < self.tail_position[0]:
                self.middle_position = [self.head_position[0] + 1, self.head_position[1]]
                field.set_cell(self.middle_position, "\u25A0")
            else:
                self.middle_position = [self.head_position[0] - 1, self.head_position[1]]
                field.set_cell(self.middle_position, "\u25A0")
            
    
    def mark_area(self, field: Field) -> None:
        
        start_position: list[int, int]
        finish_position: list[int, int]
        if self.orientation == "vertical":
            if self.head_position[0] < self.tail_position[0]:
                start_position = [self.head_position[0] - 1, self.head_position[1] - 1]
                finish_position = [self.tail_position[0] + 1, self.tail_position[1] + 1]
            else:
                start_position = [self.tail_position[0] - 1, self.tail_position[1] - 1]
                finish_position = [self.head_position[0] + 1, self.head_position[1] + 1]

        elif self.orientation == "horizontal":
            if self.head_position[1] < self.tail_position[1]:
                start_position = [self.head_position[0] - 1, self.head_position[1] - 1]
                finish_position = [self.tail_position[0] + 1, self.tail_position[1] + 1]
            else:
                start_position = [self.tail_position[0] - 1, self.tail_position[1] - 1]
                finish_position = [self.head_position[0] + 1, self.head_position[1] + 1]

        for row in range(start_position[0], finish_position[0] + 1):
            for collumn in range(start_position[1], finish_position[1] + 1):
                try:
                    if row > 0 and collumn > 0:
                        if [row, collumn] != self.tail_position and [row, collumn] != self.head_position and [row, collumn] != self.middle_position:
                            field.set_cell([row, collumn], "X")

                except IndexError:
                    pass
    
    def check_position_validity(self, head_position: list[int, int], tail_position: list[int, int], field: Field) -> bool:
        position_list = head_position + tail_position

        # check that input is in the field bounds
        for item in position_list:
            if 0 < item <= field.field_size:
                continue
            else:
                return False

        # check for vertical/horizontal
        if head_position[0] == tail_position[0]:
            self.orientation = "horizontal"
        elif head_position[1] == tail_position[1]:
            self.orientation = "vertical"
        else:
            return False

        # check adjacent
        if self.orientation == "horizontal":
            if abs(head_position[1] - tail_position[1]) > 2:
                return False
        elif self.orientation == "vertical":
            if abs(head_position[0] - tail_position[0]) > 2:
                return False

        # check for valid cell:
        if field.get_cell(head_position) != "O" or field.get_cell(tail_position) != "O":
            return False
        else:
            return True
        
    def is_part(self, position: list[int, int]) ->bool:
        if position in [self.tail_position, self.head_position, self.middle_position]:
            return True
        else:
            return False
        
    def is_defeated(self, field: Field):
        is_defeated = True
        if not self.alive:
            self.alive = self.alive
        else:
            position_data = [self.head_position, self.tail_position, self.middle_position]
            for position in position_data:
                if field.get_cell(position) != "X":
                    is_defeated = False
                    break
                    
            if is_defeated:
                for position in position_data:
                    field.set_cell(position, "#")
                self.alive = False
                
        