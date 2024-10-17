import math

class CatBush:
    def __init__(self, cat, world, chem_manager):
        self.cat = cat
        self.world = world
        self.chem_manager = chem_manager
        self.cat.initialize_bush_done()  # Initialize bush_done dict

    def check_bush_interaction(self):
        for dy in range(-self.cat.bush_interaction_radius, self.cat.bush_interaction_radius + 1):
            for dx in range(-self.cat.bush_interaction_radius, self.cat.bush_interaction_radius + 1):
                x = self.cat.x + dx
                y = self.cat.y + dy
                if 0 <= x < self.world.grid_size and 0 <= y < self.world.grid_height:
                    cell = self.world.grid[y][x]
                    if isinstance(cell, tuple) and cell[0] == 'bush':
                        bush_name = cell[1]
                        if bush_name not in self.cat.bush_done:
                            self.cat.bush_done[bush_name] = 0
                        if self.cat.bush_done[bush_name] < 4:
                            self.cat.bush_done[bush_name] += 1
                            self.chem_manager.get_pool(f'BushDone{bush_name[-1]}').add(1)
                            
                            if self.cat.bush_done[bush_name] == 4:
                                self.cat.bush_counter += 1
                                
                                if self.cat.bush_counter == len(self.cat.bush_done):
                                    self.reset_bush_interactions()
                        return

    def reset_bush_interactions(self):
        self.cat.bush_counter = 0
        for bush in self.cat.bush_done:
            self.cat.bush_done[bush] = 0
            self.chem_manager.get_pool(f'BushDone{bush[-1]}').reduce(4)
        print("Bush interactions reset")

    def find_nearest_bush(self):
        nearest_bush = None
        min_distance = float('inf')
        
        for y in range(self.world.grid_height):
            for x in range(self.world.grid_size):
                cell = self.world.grid[y][x]
                if isinstance(cell, tuple) and cell[0] == 'bush':
                    bush_name = cell[1]
                    if bush_name not in self.cat.bush_done:
                        self.cat.bush_done[bush_name] = 0
                    if self.cat.bush_done[bush_name] < 4:
                        distance = math.sqrt((x - self.cat.x)**2 + (y - self.cat.y)**2)
                        if distance < min_distance:
                            min_distance = distance
                            nearest_bush = (x, y)
        
        return nearest_bush

    def move_towards_bush(self):
        nearest_bush = self.find_nearest_bush()
        if nearest_bush:
            bush_x, bush_y = nearest_bush
            dx = bush_x - self.cat.x
            dy = bush_y - self.cat.y
            
            if abs(dx) > abs(dy):
                self.cat.x += 1 if dx > 0 else -1
            else:
                self.cat.y += 1 if dy > 0 else -1