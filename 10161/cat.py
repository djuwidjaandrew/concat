import random
import pygame
import math
from init import RED, GRID_SIZE
from look import CatLook
from catbush import CatBush
from walkchase import CatWalkChase
from collision import CollisionHandler, apply_collision_rules

class Cat:
    def __init__(self, x, y, world, chem_manager):
        self.x = x
        self.y = y
        self.world = world
        self.chem_manager = chem_manager
        self.look = CatLook(self)
        self.bush = None  # Will be set in main.py
        self.policies = None  # Will be set in main.py
        self.chasing = None
        self.bush_interaction_radius = 2
        self.bush_done = {}  # We'll populate this dynamically
        self.bush_counter = 0
        self.color = (255, 0, 0)  # Red color for the cat
        self.collision_handler = CollisionHandler(world)

    def initialize_bush_done(self):
        for y in range(self.world.grid_height):
            for x in range(self.world.grid_size):
                cell = self.world.grid[y][x]
                if isinstance(cell, tuple) and cell[0] == 'bush':
                    bush_name = cell[1]
                    if bush_name not in self.bush_done:
                        self.bush_done[bush_name] = 0

    def update(self):
        self.look.update()
        if self.chasing:
            target_x, target_y, target_type = self.chasing
            if self.x == target_x and self.y == target_y:
                if target_type == 'rat':
                    self.world.remove_rat(target_x, target_y)
                self.chasing = None
                self.look.stress_vision = False
                print("Cat caught the target, stress vision deactivated")
            else:
                new_x, new_y = self.policies.chase_target()
                apply_collision_rules(self, new_x, new_y, self.collision_handler)
        else:
            new_x, new_y = self.policies.random_walk()
            apply_collision_rules(self, new_x, new_y, self.collision_handler)
        self.bush.check_bush_interaction()

    def check_for_food_or_rat(self):
        return self.look.check_for_food_or_rat()

    def chase_target(self):
        self.policies.chase_target()

    def eat_target(self, target_type):
        self.policies.eat_target(target_type)

    def check_bush_interaction(self):
        self.bush.check_bush_interaction()

    def reset_bush_interactions(self):
        self.bush.reset_bush_interactions()

    def draw(self, screen, CELL_SIZE):
        pygame.draw.rect(screen, self.color, (self.x*CELL_SIZE, self.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_vision(self, screen, CELL_SIZE):
        self.look.draw_vision(screen, CELL_SIZE)

class CatMapper:
    def __init__(self, grid_size, grid_height):
        self.grid_size = grid_size
        self.grid_height = grid_height
        self.map = [[0 for _ in range(grid_size)] for _ in range(grid_height)]

    def update(self, cat, world):
        vision_range = cat.look.get_vision_range()
        for y, x in vision_range:
            if 0 <= x < self.grid_size and 0 <= y < self.grid_height:
                if world.grid[y][x]:
                    self.map[y][x] = 1

    def save_map(self, run_id):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 13))
        plt.imshow(self.map, cmap='gray_r')
        plt.title(f'Cat\'s Map - Run {run_id}')
        plt.savefig(f'cat_maps/run_{run_id}_map.png')
        plt.close()

class Rat:
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.patrol_radius = 4
        self.patrol_area = self.get_patrol_area()
        self.is_alive = True

    def get_patrol_area(self):
        x_start = max(0, self.x - self.patrol_radius)
        x_end = min(self.world.grid_size - 1, self.x + self.patrol_radius)
        y_start = max(0, self.y - self.patrol_radius)
        y_end = min(self.world.grid_height - 1, self.y + self.patrol_radius)
        return [(x, y) for x in range(x_start, x_end + 1) for y in range(y_start, y_end + 1)]

    def move(self):
        if not self.is_alive:
            return
        self.world.grid[self.y][self.x] = None
        new_x, new_y = random.choice(self.patrol_area)
        self.x, self.y = new_x, new_y
        self.world.grid[self.y][self.x] = ('rat', f'rat_{chr(97 + self.world.rats.index(self))}')

    def die(self):
        self.is_alive = False
        self.world.grid[self.y][self.x] = None
        print(f"Rat at ({self.x}, {self.y}) has died.")