import random

from api import *


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


class MyBot(CodeBattlesBot):
    times = []
    me = None
    my_head = None
    step_start_time = None

    def get_all_options(self, coords):
        # returns all coordinates for next move
        x, y = coords
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

    def initialize_variables(self):
        # helper function to set variables that will not change during the step
        self.step_start_time = time.time()
        self.me = self.context.get_myself()
        self.my_head = self.context.get_position(self.me)[-1]

    GOTO_FACTOR = 10

    def goto(self, coord: tuple[int, int]):
        res = {"U": 0, "D": 0, "L": 0, "R": 0}
        dx = self.my_head[0] - coord[0]
        dy = self.my_head[1] - coord[1]
        dirX = "R" if dx < 0 else "L"
        dirY = "U" if dy < 0 else "D"
        sum = dx + dy
        if sum == 0:
            return res
        res[dirX] = abs(dx / sum * self.GOTO_FACTOR)
        res[dirY] = abs(dy / sum * self.GOTO_FACTOR)
        return res

    def nearest_tile(self, tiles: list[tuple[int, int]]):
        return min(tiles, key=lambda a: manhattan_distance(a, self.my_head))

    def is_non_weighted(self, weights: dict):
        return sum(weights.values()) == 0

    def filter_non_weighted(self, weights: dict[str, int]):
        res = {}
        for dir, weight in weights.items():
            if weight != 0:
                res[dir] = weight
            else:
                res[dir] = 0.1
        return res

    def get_death_tiles(self):
        heads = [player.head for player in self.context.get_active_players() if player.length >= self.me.length and player is not self.me]
        res = []
        for head in heads:
            res.extend(self.get_all_options(head).values())
        return res

    def is_valid_dir(self, dir):
        coords = self.get_all_options(self.my_head).get(dir)
        if coords in self.context.get_occupied_tiles():
            return False
        if not self.context.in_bounds(coords):
            return False
        if coords in self.get_death_tiles():
            return False
        return True

    def filter_non_valid(self, weights: dict[str, int]):
        res = {}
        for dir, weight in weights.items():
            if self.is_valid_dir(dir):
                res[dir] = weight
        return res

    def get_goal(self):
        if self.me.health < 40:
            return self.nearest_tile(self.context.get_apples())
        else:
            return self.nearest_tile([player.head for player in self.context.get_active_players() if player is not self.me])

    def run(self) -> None:
        self.initialize_variables()
        goal = self.get_goal()
        # self.context.log_info(str(goal))
        dirs = self.goto(goal)
        move = "U"
        dirs = self.filter_non_weighted(dirs)
        dirs = self.filter_non_valid(dirs)
        if not self.is_non_weighted(dirs):
            move = random.choices(list(dirs.keys()), weights=list(dirs.values()), k=1)
        self.context.log_info(str(self.get_death_tiles()))
        self.context.set_direction(move[0])

    def setup(self) -> None:
        pass
