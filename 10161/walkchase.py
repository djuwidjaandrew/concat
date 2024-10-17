import random
from collision import apply_collision_rules

class CatWalkChase:
    def __init__(self, cat, world, chem_manager):
        self.cat = cat
        self.world = world
        self.chem_manager = chem_manager

    def random_walk(self):
        for _ in range(2):  # Two random steps
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x = self.cat.x + dx
                new_y = self.cat.y + dy
                
                if apply_collision_rules(self.cat, new_x, new_y, self.cat.collision_handler):
                    break
            
            self.cat.check_for_food_or_rat()
            if self.cat.chasing:
                break
        
        return self.cat.x, self.cat.y

    def chase_target(self):
        target_x, target_y, target_type = self.cat.chasing
        dx = target_x - self.cat.x
        dy = target_y - self.cat.y
        
        if abs(dx) > abs(dy):
            new_x = self.cat.x + (1 if dx > 0 else -1)
            new_y = self.cat.y
        else:
            new_x = self.cat.x
            new_y = self.cat.y + (1 if dy > 0 else -1)
        
        apply_collision_rules(self.cat, new_x, new_y, self.cat.collision_handler)
        
        if self.cat.x == target_x and self.cat.y == target_y:
            self.eat_target(target_type)
        
        return self.cat.x, self.cat.y

    def eat_target(self, target_type):
        self.world.grid[self.cat.y][self.cat.x] = None
        self.cat.chasing = None
        if target_type == 'rat':
            self.chem_manager.get_pool('ChemA').reduce(5)  # Remove STRESS^^^^
            for rat in self.world.rats:
                if rat.x == self.cat.x and rat.y == self.cat.y and rat.is_alive:
                    rat.die()
                    print(f"Rat eaten at ({self.cat.x}, {self.cat.y})")
                    break
        else:
            self.chem_manager.get_pool('ChemA').reduce(1)  # Remove STRESS^
        self.cat.look.update_phase(target_type)