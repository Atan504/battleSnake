from api import *


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])

DANGER_DISTANCE = 1
MAP_SIZE = 12

def is_in_map(coord: Tuple[int, int], map_size: int) -> bool:
    return 0 <= coord[0] < map_size and 0 <= coord[1] < map_size

def get_surrounding_tiles(danger_distance: int, player_head : Tuple[int, int]) -> List[Tuple[int, int]]:
    surrounding_tiles : List[Tuple[int, int]] = []
    start_x = player_head[0]
    start_y = player_head[1]
    for i in range(-danger_distance,danger_distance+1):
        for j in range(-danger_distance,danger_distance+1):
            if is_in_map((start_x + i, start_y + j), MAP_SIZE):
                surrounding_tiles.append((start_x + i, start_y + j))
    return surrounding_tiles

def get_danger_map_for_player(danger_distance: int, player_heads: Tuple[int, int]) -> list[tuple[tuple[int,int], int]]:
    danger_list : list[tuple[tuple[int,int], int]] = []
    surrounding_tiles = get_surrounding_tiles(danger_distance, player_heads)
    for surrounding_tile in surrounding_tiles:
        danger_list.append((surrounding_tile, manhattan_distance(surrounding_tile, player_heads)))
    return danger_list

def get_total_danger_map(danger_maps : list[tuple[tuple[int, int], int]]) -> list[tuple[tuple[int,int],int]]:
    total_danger_map = [tile for one_map in danger_maps for tile in one_map]
    print(total_danger_map)
    filtered_danger_map : list[tuple[tuple[int, int], int]] = []

    for i, tile in enumerate(total_danger_map):
        has_got_in : bool = False
        for tile_2 in total_danger_map[i+2::]:
            print(tile_2)
            print(tile)
            if tile[0] == tile_2[0]:
                filtered_danger_map.append(min(tile,tile_2,key=lambda x: x[1]))
                total_danger_map.remove(tile_2)
                has_got_in = True
        if not has_got_in:
            filtered_danger_map.append(tile)
    return filtered_danger_map

def distance_direction_from_self(body: list[tuple[int, int]], player_head: tuple[int,int]) -> dict[str, int]:
    direction_weight : dict[str, int] = {"D" : MAP_SIZE, "U" : MAP_SIZE, "L" : MAP_SIZE, "R" : MAP_SIZE}
    for i in range(0, player_head[0]):
        if (player_head[0],i) in body:
            direction_weight["D"] = min(abs(player_head[1] - i), direction_weight["D"])
    for i in range(player_head[0], MAP_SIZE):
        if (player_head[0], i) in body:
            direction_weight["U"] = min(abs(i - player_head[1]), direction_weight["U"])
    for i in range(0,player_head[1]):
        if (i,player_head[1]) in body:
            direction_weight["L"] = min(abs(player_head[0] - i), direction_weight["L"])
    for i in range(player_head[1], MAP_SIZE):
        if (i,player_head[1]) in body:
            direction_weight["R"] = min(abs(i - player_head[0]), direction_weight["R"])
    print(direction_weight)
    return direction_weight


if __name__ == '__main__':
    # print([((0, 0), 0), ((0, 1), 1), ((0, 2), 2), ((1, 0), 1), ((1, 1), 2), ((1, 2), 3), ((2, 0), 2), ((2, 1), 3), ((2, 2), 4)][4::])
    print(distance_direction_from_self([(0,5), (2,5),(1,0),(1,12)],(1,5)))



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
