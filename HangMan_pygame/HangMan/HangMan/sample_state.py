from random import randint
import sys


class State:
    
    def render(self):
        raise NotImplementedError
    
    def handle_input(self, input_code):
        raise NotImplementedError


class Menu(State):
    
    OPTIONS = [
        "Adin",
        "Dwa"
    ]
    
    def __init__(self):
        self.selected_index = 0

    def move_down(self):
        self.selected_index = self._next_index()
    
    def _next_index(self):
        max = len(self.OPTIONS)
        return (self.selected_index + 1) % max
    
    def handle_input(self, input_code):
        """
        This is a bit tricky, but ideally we want the interface to be as simple as possible,
        i.e. only one method to handle user input. Since we want the user to be able to
        change the state (i.e. go from Menu -> Game), this method should be able to return a new state.
        
        There are many ways to approach this, but one way is to simply always return the current state:
            - `self` if user's action didn't move to a totally different state
            - a new state if it did
        """
        # Let's just move down if input_code is 0 and select otherwise
        if input_code == 0:
            self.move_down()
            return self
        else:
            return self.select()
    
    def render(self):
        selected_marker = ">"
        unselected_marker = " "
        
        # Zip each option with a marker
        options_zip_markers = [
            (option, selected_marker if index == self.selected_index else unselected_marker)
            for index, option in enumerate(self.OPTIONS)
        ]
        
        # Format each line as a string
        lines = [
            "{marker} {option}".format(marker=marker, option=option)
            for option, marker in options_zip_markers
        ]
        
        # Convert to a single string with newlines inbetween elements
        renderable = "\n".join(lines)
        print(renderable)
    
    def select(self):
        # Let's say the first choice starts a game...
        if (self.selected_index) == 0:
            return Game()
        # and the second one exits the program
        else:
            sys.exit()


class Game(State):
    def __init__(self):
        self.position = (25, 25)
    
    def handle_input(self, input_code):
        if input_code == 0:
            return Menu()
        else:
            self._do_some_random_stuff()
            return self
    
    def _do_some_random_stuff(self):
        limits = (0, 100)
        new_x = randint(*limits)
        new_y = randint(*limits)
        self.position = (new_x, new_y)
    
    def render(self):
        print("Game at position: {}".format(self.position))

# Initial state
state = Menu()
state.render()

# Some moves
input_codes = [0, 0, 1, 1, 0, 1, 0, 0, 1]

for code in input_codes:
    print("\n----\n")
    state = state.handle_input(code)
    state.render()