import pygame
import random
import math
from config import RAT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, RAT_SPEEDS, GRID_SIZE, RAT_HP, FPS, BLUE, RED
from config import RAT_BURST_A_DURATION, RAT_BURST_A_COOLDOWN, RAT_BURST_B_HP_THRESHOLD, RAT_BURST_C_DURATION, RAT_BURST_SPEED_MULTIPLIER

class Rat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = RAT_SIZE
        self.base_speed = random.choice(RAT_SPEEDS)
        self.speed = self.base_speed
        self.hp = RAT_HP
        self.hunted = False
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.color = BLUE
        self.wall_hits = 0
        self.burst_a_time = 0
        self.burst_a_cooldown = 0
        self.burst_b_active = False
        self.burst_c_time = 0
        self.hit_count = 0
        self.speed_multiplier = 1

    def move(self, cat_pos):
        self.update_speed_multiplier()
        if self.burst_a_time > 0:
            self.burst_move()
        else:
            self.normal_move(cat_pos)
        self.check_hp()
        self.update_timers()

    def normal_move(self, cat_pos):
        if self.hunted:
            try:
                self.direction = (pygame.math.Vector2(self.x, self.y) - cat_pos).normalize()
            except ValueError:
                self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        
        new_x = self.x + self.direction.x * self.speed * self.speed_multiplier / FPS
        new_y = self.y + self.direction.y * self.speed * self.speed_multiplier / FPS

        corner_buffer = 3 * GRID_SIZE
        if self.is_in_corner(new_x, new_y, corner_buffer):
            self.avoid_corner()
        else:
            if new_x <= 0 or new_x >= SCREEN_WIDTH - self.size:
                self.direction.x *= -1
                self.wall_hits += 1
            if new_y <= 0 or new_y >= SCREEN_HEIGHT - self.size:
                self.direction.y *= -1
                self.wall_hits += 1

        if self.wall_hits >= 3 and self.burst_a_cooldown == 0:
            self.start_burst_a()

        self.x = max(0, min(new_x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(new_y, SCREEN_HEIGHT - self.size))

    def burst_move(self):
        center = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        to_center = (center - pygame.math.Vector2(self.x, self.y)).normalize()
        self.direction = to_center.rotate(random.uniform(-30, 30))
        
        self.x += self.direction.x * self.speed * self.speed_multiplier / FPS
        self.y += self.direction.y * self.speed * self.speed_multiplier / FPS
        
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))

    def is_in_corner(self, x, y, buffer):
        return ((x <= buffer and y <= buffer) or
                (x <= buffer and y >= SCREEN_HEIGHT - buffer) or
                (x >= SCREEN_WIDTH - buffer and y <= buffer) or
                (x >= SCREEN_WIDTH - buffer and y >= SCREEN_HEIGHT - buffer))

    def avoid_corner(self):
        center = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        to_center = (center - pygame.math.Vector2(self.x, self.y)).normalize()
        angle = random.uniform(-30, 30)
        self.direction = to_center.rotate(angle)

    def start_burst_a(self):
        self.burst_a_time = RAT_BURST_A_DURATION
        self.burst_a_cooldown = RAT_BURST_A_COOLDOWN
        self.wall_hits = 0

    def start_burst_c(self):
        self.burst_c_time = RAT_BURST_C_DURATION
        self.hit_count = 0

    def update_speed_multiplier(self):
        self.speed_multiplier = 1
        if self.burst_a_time > 0 or self.burst_b_active or self.burst_c_time > 0:
            self.speed_multiplier = RAT_BURST_SPEED_MULTIPLIER

    def check_hp(self):
        if self.hp <= RAT_BURST_B_HP_THRESHOLD and not self.burst_b_active:
            self.burst_b_active = True
            self.color = RED

    def update_timers(self):
        self.burst_a_time = max(0, self.burst_a_time - 1)
        self.burst_a_cooldown = max(0, self.burst_a_cooldown - 1)
        self.burst_c_time = max(0, self.burst_c_time - 1)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def get_hit(self):
        self.hp -= 1
        self.hunted = True
        self.hit_count += 1
        if self.hit_count >= 5:
            self.start_burst_c()
        return self.hp <= 0
    
    def get_actual_speed(self):
        return self.base_speed * self.speed_multiplier