from api import *


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])

def get_moves(head):
        x, y = head
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

class MyBot(CodeBattlesBot):
    times = []
    me = None
    my_head = None
    step_start_time = None
    direction_to_letter = {(0,-1): "D", (0,1): "U", (1,0): "R", (-1,0): "L"}

    def is_valid(self, tile: tuple[int, int]):
        return not (tile in self.context.get_occupied_tiles() or not self.context.in_bounds(tile))

    def get_kill_tiles(self):
        return [get_moves(player.head).values() for player in self.context.get_active_players() if player.length < self.context.get_myself().length]

    
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

    def get_all_options(self):
        # returns all coordinates for next move
        x, y = self.my_head
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

    
    def get_all_options_by_tile(self, tile: tuple[int, int]):
        # returns all coordinates for next move
        x, y = tile
        return {(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)}

    def get_dir_weights(self, turn: int):
        d = {"U": 0, "D": 0, "R": 0, "L": 0}
        for dir, tile in self.get_all_options().items():
            if self.is_valid(tile):
                d[dir] = self.calc_weight(tile, turn)
        r = {}
        s = 0
        for dir, weight in d.items():
            s += weight
        for dir, weight in d.items():
            if s==0:
                r[dir]=1
            else:
                r[dir] = weight / s * 40
        return r


    
    def calc_weight(self, tile: tuple[int, int], turn):
        if turn == 0:
            return 1 if self.is_valid(tile) else 0
        weight = 0
        for op in self.get_all_options_by_tile(tile):
            if self.is_valid(op):
                weight += self.calc_weight(op, turn - 1)
        return weight


    def initialize_variables(self):
        # helper function to set variables that will not change during the step
        self.step_start_time = time.time()
        self.me = self.context.get_myself()
        self.my_head = self.context.get_position(self.me)[-1]

    def run(self) -> None:
        self.initialize_variables()

        direction_weights = self.get_dir_weights(5)
        #self.context.log_info(str(len(direction_weights)))
        direction = self.make_move(direction_weights)
        move = self.direction_to_letter[direction]
        self.context.set_direction(move)

        self.times.append(time.time() - self.step_start_time)
        # prints the average time every 100 steps:
        if len(self.times) % 100 == 0:
            average = sum(self.times) / len(self.times)
            self.context.log_info(f"average time per turn : {average}")

    

    def find_closest_apple(self):
        apples = self.context.get_apples()
        dists = [manhattan_distance(apples[i],self.my_head) for i in range(len(apples))]
        best_apple_index = dists.index(min(dists))
        return apples[best_apple_index]

    def make_move(self,direction_weights):
        if self.context.get_myself().health<81:
            return self.move_to_eat(direction_weights)
        else:
            pos = [6,6]
            if self.my_head==(6,6):
                pos=random.choice([(6,5),(5,6),(5,5),(6,7),(7,6)])
            return self.move_to_pos(pos,direction_weights)
    
    def move_to_pos(self,cords,direction_weights):
        x_direction = cords[0] - self.my_head[0]
        y_direction = cords[1] - self.my_head[1]
        HEALTH_FACTOR = 1/2+(50/self.me.health)**5

        #update weights
        if x_direction!=0:
            x_move = (x_direction//abs(x_direction),0)
            if direction_weights[self.direction_to_letter[x_move]]!=0:
                direction_weights[self.direction_to_letter[x_move]]+=abs(x_direction)
                direction_weights[self.direction_to_letter[x_move]]*=HEALTH_FACTOR
        
        if y_direction!=0:
            y_move = (y_direction//abs(y_direction),0)
            if direction_weights[self.direction_to_letter[y_move]]!=0:
                direction_weights[self.direction_to_letter[y_move]]+=abs(y_direction)
                direction_weights[self.direction_to_letter[y_move]]*=HEALTH_FACTOR

        options = self.get_available_options()
        directions=[]
        """
        for i in range(len(options)):
            directions.append((options[i][0]-self.my_head[0],options[i][1]-self.my_head[1]))
        """
        #check if we need only 1 direction to go
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        weight=[]
        for direction in directions:
            weight.append(direction_weights[self.direction_to_letter[direction]])
        return random.choices(directions,weights=weight,k=1)[0]

    def move_to_eat(self,direction_weights):
        return self.move_to_pos(self.find_closest_apple(),direction_weights)
    
    def setup(self) -> None:
        pass