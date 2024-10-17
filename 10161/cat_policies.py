import random
import math

class CatPolicies:
    def __init__(self, cat, world, chem_manager):
        self.cat = cat
        self.world = world
        self.chem_manager = chem_manager

    def random_walk(self):
        # Policy A: 4 random walk steps
        for _ in range(4):
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            
            # Ensure at least 1 step forward and at most 1 step backward
            if dy > 0 or (dy == 0 and random.random() < 0.5):
                dy = 1
            elif dy < 0:
                dy = -1

            new_x = max(0, min(self.world.grid_size - 1, self.cat.x + dx))
            new_y = max(0, min(self.world.grid_size - 1, self.cat.y + dy))
            
            self.cat.x, self.cat.y = new_x, new_y

    def approach_nearest_bush(self):
        # Policy B: Tendency to approach the nearest bush
        nearest_bush = self.find_nearest_bush()
        if nearest_bush:
            dx = 1 if nearest_bush[0] > self.cat.x else -1 if nearest_bush[0] < self.cat.x else 0
            dy = 1 if nearest_bush[1] > self.cat.y else -1 if nearest_bush[1] < self.cat.y else 0
            
            new_x = max(0, min(self.world.grid_size - 1, self.cat.x + dx))
            new_y = max(0, min(self.world.grid_size - 1, self.cat.y + dy))
            
            self.cat.x, self.cat.y = new_x, new_y

    def pause_for_food(self):
        # Policy C: Pause when food is seen or stress is present
        chem_a = self.chem_manager.get_pool('ChemA')
        if self.food_in_sight() or chem_a.get_value() > 0:
            return True  # Pause
        return False  # Continue moving

    def find_nearest_bush(self):
        nearest_bush = None
        min_distance = float('inf')
        for y in range(self.world.grid_size):
            for x in range(self.world.grid_size):
                if self.world.grid[y][x] and self.world.grid[y][x][0] == 'bush':
                    distance = math.sqrt((x - self.cat.x)**2 + (y - self.cat.y)**2)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_bush = (x, y)
        return nearest_bush

    def food_in_sight(self):
        # Check if food is in the cat's field of view
        # This should be implemented based on your cat's vision system
        pass

# Usage:
# policies = CatPolicies(cat, world, chem_manager)
# policies.random_walk()
# policies.approach_nearest_bush()
# if not policies.pause_for_food():
#     # Continue with other actions