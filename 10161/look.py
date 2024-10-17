import time
import pygame
import math

class LookStrategy:
    def update(self, cat_look):
        pass

    def on_food_eaten(self, cat_look):
        pass

class TimedRotationStrategy(LookStrategy):
    def __init__(self, rotation_interval):
        self.rotation_interval = rotation_interval
        self.last_rotation_time = time.time()

    def update(self, cat_look):
        current_time = time.time()
        if not cat_look.stress_vision and current_time - self.last_rotation_time >= self.rotation_interval:
            cat_look.rotate_look_direction()
            self.last_rotation_time = current_time

class PhaseBasedStrategy(LookStrategy):
    def __init__(self):
        self.last_bush_orientation_time = time.time()

    def update(self, cat_look):
        if cat_look.stress_vision:
            return  # Don't change direction during hunting mode

        current_time = time.time()
        if current_time - self.last_bush_orientation_time >= 5:
            cat_look.orient_to_nearest_bush()
            self.last_bush_orientation_time = current_time

        if cat_look.food_eaten > 0:
            cat_look.rotate_look_direction()
            cat_look.food_eaten = 0

        cat_look.check_phase_transition()

    def on_food_eaten(self, cat_look):
        cat_look.food_eaten += 1
        cat_look.update_phase(cat_look.cat.chasing[2])

class CatLook:
    def __init__(self, cat):
        self.cat = cat
        self.base_vision_size = 6
        self.chase_vision_size = 12
        self.forward_vision_length = 10
        self.phase = '1a'
        self.food_eaten = 0
        self.stress_vision = False
        self.look_direction = 'up'
        self.strategy = PhaseBasedStrategy()
        self.last_zone = None
        self.last_side = None

    def set_strategy(self, strategy):
        self.strategy = strategy

    def update(self):
        self.strategy.update(self)
        self.check_for_food_or_rat()
        
        # Maintain stress vision while chasing a rat
        if self.cat.chasing and self.cat.chasing[2] == 'rat':
            self.stress_vision = True
        
        print(f"Vision updated: phase={self.phase}, direction={self.look_direction}, stress={self.stress_vision}")

    def rotate_look_direction(self):
        directions = ['up', 'right', 'down', 'left']
        current_index = directions.index(self.look_direction)
        self.look_direction = directions[(current_index + 1) % 4]

    def orient_to_nearest_bush(self):
        nearest_bush = self.find_nearest_viable_bush()
        if nearest_bush:
            dx = nearest_bush[0] - self.cat.x
            dy = nearest_bush[1] - self.cat.y
            if abs(dx) > abs(dy):
                self.look_direction = 'right' if dx > 0 else 'left'
            else:
                self.look_direction = 'down' if dy > 0 else 'up'
            print(f"Oriented to nearest bush: {self.look_direction}")

    def find_nearest_viable_bush(self):
        nearest_bush = None
        min_distance = float('inf')
        for y in range(self.cat.world.grid_height):
            for x in range(self.cat.world.grid_size):
                cell = self.cat.world.grid[y][x]
                if isinstance(cell, tuple) and cell[0] == 'bush':
                    bush_name = cell[1]
                    if self.cat.bush_done[bush_name] < 4:
                        distance = math.sqrt((x - self.cat.x)**2 + (y - self.cat.y)**2)
                        if distance < min_distance:
                            min_distance = distance
                            nearest_bush = (x, y)
        return nearest_bush

    def get_vision_range(self):
        vision_range = set()
        if self.stress_vision:
            # Stress vision: 12x12 square centered on the cat
            for dy in range(-self.chase_vision_size // 2, self.chase_vision_size // 2 + 1):
                for dx in range(-self.chase_vision_size // 2, self.chase_vision_size // 2 + 1):
                    vision_range.add((self.cat.y + dy, self.cat.x + dx))
        else:
            # Normal vision: 6x6 square with directional extension
            for dy in range(-self.base_vision_size // 2, self.base_vision_size // 2 + 1):
                for dx in range(-self.base_vision_size // 2, self.base_vision_size // 2 + 1):
                    vision_range.add((self.cat.y + dy, self.cat.x + dx))
            
            # Extended vision based on look direction
            if self.look_direction == 'left':
                for dy in range(-self.base_vision_size // 2, self.base_vision_size // 2 + 1):
                    for dx in range(-self.forward_vision_length, 0):
                        vision_range.add((self.cat.y + dy, self.cat.x + dx))
            elif self.look_direction == 'right':
                for dy in range(-self.base_vision_size // 2, self.base_vision_size // 2 + 1):
                    for dx in range(1, self.forward_vision_length + 1):
                        vision_range.add((self.cat.y + dy, self.cat.x + dx))
            elif self.look_direction == 'up':
                for dy in range(-self.forward_vision_length, 0):
                    for dx in range(-self.base_vision_size // 2, self.base_vision_size // 2 + 1):
                        vision_range.add((self.cat.y + dy, self.cat.x + dx))
            elif self.look_direction == 'down':
                for dy in range(1, self.forward_vision_length + 1):
                    for dx in range(-self.base_vision_size // 2, self.base_vision_size // 2 + 1):
                        vision_range.add((self.cat.y + dy, self.cat.x + dx))
        
        return list(vision_range)

    def draw_vision(self, screen, CELL_SIZE):
        vision_range = self.get_vision_range()
        vision_surface = pygame.Surface((self.cat.world.grid_size * CELL_SIZE, self.cat.world.grid_height * CELL_SIZE), pygame.SRCALPHA)
        
        if self.stress_vision:
            color = (255, 0, 0, 100)  # Red with alpha for stress vision
        else:
            color = (200, 200, 200, 100)  # Light gray with alpha for normal vision
        
        for y, x in vision_range:
            if 0 <= x < self.cat.world.grid_size and 0 <= y < self.cat.world.grid_height:
                pygame.draw.rect(vision_surface, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        screen.blit(vision_surface, (0, 0))

    def check_for_food_or_rat(self):
        vision_range = self.get_vision_range()
        for y, x in vision_range:
            if 0 <= x < self.cat.world.grid_size and 0 <= y < self.cat.world.grid_height:
                cell = self.cat.world.grid[y][x]
                if isinstance(cell, tuple) and cell[0] in ['food', 'rat']:
                    self.cat.chasing = (x, y, cell[0])
                    if cell[0] == 'rat':
                        self.cat.chem_manager.get_pool('ChemA').add(5)  # STRESS^^^^
                        self.stress_vision = True
                        print(f"Stress vision activated: {self.stress_vision}")  # Debug print
                    else:
                        self.cat.chem_manager.get_pool('ChemA').add(1)  # STRESS^
                    self.strategy.on_food_eaten(self)
                    return True
        
        # If no food or rat found, and cat was previously chasing, reset stress vision
        if self.cat.chasing is None and self.stress_vision:
            self.stress_vision = False
            print(f"Stress vision deactivated: {self.stress_vision}")  # Debug print
        
        return False

    def update_phase(self, target_type):
        if target_type in ['food', 'rat']:
            if self.phase == '1a':
                self.phase = '1b'
            elif self.phase == '2':
                self.phase = '3'
            elif self.phase == '3':
                self.phase = '4'
            elif self.phase == '4':
                self.phase = '1a'
        
        if target_type == 'rat':
            self.stress_vision = False
        
        print(f"Phase updated to {self.phase}, target_type: {target_type}, position: ({self.cat.x}, {self.cat.y})")

    def check_phase_transition(self):
        current_zone = self.cat.y // (self.cat.world.grid_height // 10)
        current_side = 'left' if self.cat.x < self.cat.world.grid_size // 2 else 'right'

        if self.phase == '1b':
            if (self.last_zone is not None and current_zone != self.last_zone) or \
               (self.last_side is not None and current_side != self.last_side):
                self.phase = '2'
                self.rotate_look_direction()
                print(f"Transitioned to phase 2 at position: ({self.cat.x}, {self.cat.y})")

        self.last_zone = current_zone
        self.last_side = current_side