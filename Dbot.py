from api import *


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


class MyBot(CodeBattlesBot):
    times = []
    me = None
    my_head = None
    step_start_time = None
    direction_to_letter = {(0, -1): "D", (0, 1): "U", (1, 0): "R", (-1, 0): "L"}

    def is_valid(self, tile: tuple[int, int]):
        return not (tile in self.context.get_occupied_tiles() or not self.context.in_bounds(tile))

    def get_kill_tiles(self):
        return [player.head for player in self.context.get_active_players() if player.length < self.context.get_myself().length]

    def get_non_killing_occupied_tiles(self):
        return [tile for tile in self.context.get_occupied_tiles() if tile not in self.get_kill_tiles()]

    def get_tail_direction(self):
        pos = self.context.get_position(self.context.get_myself())
        if len(pos) == 1:
            return (-1, -1)
        tail_dir = pos[-2]
        for dir, coords in self.get_all_options().items():
            if coords == tail_dir:
                return (dir, coords)

    def get_available_options(self):
        # returns all non killing coordinates for next move
        options = self.get_all_options()
        to_del = []
        # goes over all options, removes only problematic ones (or does it?)
        for direction, coord in options.items():
            if coord in self.get_non_killing_occupied_tiles() or not self.context.in_bounds(coord) or coord == self.get_tail_direction()[1]:
                to_del.append(direction)
        for direction in to_del:
            del options[direction]

        return list(options.values())

    def calc_weight(self, tile: tuple[int, int], turn):
        if turn == 0:
            return 1 if self.is_valid(tile) else 0
        weight = 0
        for op in self.get_all_options_by_tile(tile):
            if self.is_valid(op):
                weight += self.calc_weight(op, turn - 1)
        return weight

    def get_all_options(self):
        # returns all coordinates for next move
        x, y = self.my_head
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

    def get_all_options_by_tile(self, tile: tuple[int, int]):
        # returns all coordinates for next move
        x, y = tile
        return {(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)}

    def get_dir_weights(self, turn: int):
        d = {}
        for dir, tile in self.get_all_options().items():
            if self.is_valid(tile):
                d[dir] = self.calc_weight(tile, turn)
        return d

    def initialize_variables(self):
        # helper function to set variables that will not change during the step
        self.step_start_time = time.time()
        self.me = self.context.get_myself()
        self.my_head = self.context.get_position(self.me)[-1]

    def run(self) -> None:
        self.initialize_variables()

        direction = self.move_to_eat()
        move = self.direction_to_letter[direction]
        self.context.set_direction(move)
        self.context.log_info(str(self.get_dir_weights(3)))
        self.times.append(time.time() - self.step_start_time)
        # prints the average time every 100 steps:
        if len(self.times) % 100 == 0:
            average = sum(self.times) / len(self.times)
            self.context.log_info(f"average time per turn : {average}")

    def find_closest_apple(self):
        apples = self.context.get_apples()
        dists = [manhattan_distance(apples[i], self.my_head) for i in range(len(apples))]
        best_apple_index = dists.index(min(dists))
        return apples[best_apple_index]

    def move_to_eat(self):
        apple_cords = self.find_closest_apple()
        x_direction = apple_cords[0] - self.my_head[0]
        y_direction = +apple_cords[1] - self.my_head[1]

        options = self.get_available_options()
        directions = []
        for i in range(len(options)):
            directions.append((options[i][0] - self.my_head[0], options[i][1] - self.my_head[1]))
        # check if we need only 1 direction to go

        if x_direction == 0:
            # self.context.log_info("DONT NEED X DIRECTION")
            if y_direction != 0 and (0, y_direction // abs(y_direction)) in directions:
                return (0, y_direction // abs(y_direction))
            return random.choice(directions)
        if y_direction == 0:
            # self.context.log_info("DONT NEED Y DIRECTION")
            if x_direction != 0 and (x_direction // abs(x_direction), 0) in directions:
                return (x_direction // abs(x_direction), 0)
            return random.choice(directions)

        # we need both direction
        # check both are options
        x_move = (x_direction // abs(x_direction), 0)
        y_move = (0, y_direction // abs(y_direction))
        if x_move in directions:
            if y_move in directions:
                move = random.choices([x_move, y_move], weights=(abs(x_direction), abs(y_direction)), k=1)[0]
                return move
            return x_move
        if y_move in directions:
            return y_move
        return random.choice(directions)

    def setup(self) -> None:
        pass
