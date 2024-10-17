import random
import pygame
import math
from init import GRID_SIZE, WHITE, BLACK, RED, GREEN, BLUE

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
        new_x, new_y = random.choice(self.patrol_area)
        self.x, self.y = new_x, new_y

    def die(self):
        self.is_alive = False
        print(f"Rat at ({self.x}, {self.y}) has died.")

class World:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.grid_height = int(GRID_SIZE * 1.3)  # 30% longer upward
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_height)]
        self.rats = []
        self.create_environment()

    def create_environment(self):
        self.create_separator()
        self.create_bridge()
        self.create_bushes()
        self.create_food()
        self.create_rats()

    def create_separator(self):
        separator_x = self.grid_size // 2
        separator_start = int(self.grid_height * 0.4)  # Start 40% from the top
        separator_end = int(self.grid_height * 0.8)    # End 80% from the top
        for y in range(separator_start, separator_end):
            self.grid[y][separator_x] = 'separator'

    def create_bridge(self):
        bridge_y = self.grid_height // 4
        for x in range(self.grid_size // 4, 3 * self.grid_size // 4):
            self.grid[bridge_y][x] = 'bridge'

    def create_bushes(self):
        bush_colors = [
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (128, 0, 128)   # Purple
        ]
        bush_positions = [
            (self.grid_size // 8, self.grid_height // 6),
            (self.grid_size // 8, self.grid_height // 2),
            (self.grid_size // 8, 5 * self.grid_height // 6),
            (7 * self.grid_size // 8, self.grid_height // 6),
            (7 * self.grid_size // 8, self.grid_height // 2),
            (7 * self.grid_size // 8, 5 * self.grid_height // 6)
        ]
        for i, ((x, y), color) in enumerate(zip(bush_positions, bush_colors)):
            bush_name = f'Bush{chr(65+i)}'  # BushA, BushB, etc.
            self.grid[y][x] = ('bush', bush_name, color)
            self.grid[y][x+1] = ('bush', bush_name, color)

    def create_food(self):
        food_positions = [
            (self.grid_size // 4, self.grid_height // 2),
            (3 * self.grid_size // 4, self.grid_height // 2),
            (self.grid_size // 8, 3 * self.grid_height // 4)
        ]
        for i, (x, y) in enumerate(food_positions):
            self.grid[y][x] = ('food', f'food_{chr(97+i)}')

    def create_rats(self):
        rat_positions = [
            (7 * self.grid_size // 8, self.grid_height // 4),
            (3 * self.grid_size // 4, 3 * self.grid_height // 4)
        ]
        for i, (x, y) in enumerate(rat_positions):
            rat = Rat(x, y, self)
            self.rats.append(rat)
            self.grid[y][x] = ('rat', f'rat_{chr(97+i)}')

    def draw(self, screen, CELL_SIZE):
        pygame.draw.rect(screen, (240, 230, 220), (0, 0, self.grid_size * CELL_SIZE // 2, self.grid_height * CELL_SIZE))
        pygame.draw.rect(screen, (220, 210, 200), (self.grid_size * CELL_SIZE // 2, 0, self.grid_size * CELL_SIZE // 2, self.grid_height * CELL_SIZE))

        for y in range(self.grid_height):
            for x in range(self.grid_size):
                cell = self.grid[y][x]
                if cell:
                    if cell == 'separator':
                        color = BLACK
                    elif cell == 'bridge':
                        color = (150, 75, 0)  # Brown
                    elif isinstance(cell, tuple):
                        if cell[0] == 'bush':
                            color = cell[2]  # Use the bush's color
                        elif cell[0] == 'food':
                            color = (255, 165, 0)  # Orange
                        elif cell[0] == 'rat':
                            color = RED
                    else:
                        color = WHITE
                    pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw only living rats
        for rat in self.rats:
            if rat.is_alive:
                pygame.draw.rect(screen, RED, (rat.x*CELL_SIZE, rat.y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def update_rats(self):
        for rat in self.rats:
            if rat.is_alive:
                self.grid[rat.y][rat.x] = None
                rat.move()
                self.grid[rat.y][rat.x] = ('rat', f'rat_{chr(97 + self.rats.index(rat))}')

    def remove_dead_rats(self):
        self.rats = [rat for rat in self.rats if rat.is_alive]