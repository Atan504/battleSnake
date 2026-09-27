from api import *


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


class MyBot(CodeBattlesBot):
    times = []
    me = None
    my_head = None
    step_start_time = None

    def get_available_options(self):
        # returns all non killing coordinates for next move
        options = self.get_all_options()
        to_del = []
        # goes over all options, removes only problematic ones (or does it?)
        for direction, coord in options.items():
            if coord in self.context.get_occupied_tiles() or not self.context.in_bounds(
                coord
            ):
                to_del.append(direction)
        for direction in to_del:
            del options[direction]

        return options

    def get_all_options(self):
        # returns all coordinates for next move
        x, y = self.my_head
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

    def initialize_variables(self):
        # helper function to set variables that will not change during the step
        self.step_start_time = time.time()
        self.me = self.context.get_myself()
        self.my_head = self.context.get_position(self.me)[-1]

    def run(self) -> None:
        self.initialize_variables()

        move = "U"
        options = self.get_available_options()
        if len(options) > 0:
            # takes the a random available option which should not kill him
            move = list(options.keys())[random.randint(0, len(options) - 1)]
        self.context.set_direction(move)

        self.times.append(time.time() - self.step_start_time)
        # prints the average time every 100 steps:
        if len(self.times) % 100 == 0:
            average = sum(self.times) / len(self.times)
            self.context.log_info(f"average time per turn : {average}")

    def setup(self) -> None:
        pass
