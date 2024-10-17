import pygame
import random
import math
from config import CAT_SIZE, CAT_NORMAL_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, CAT_NORMAL_VISION, CAT_HUNTING_VISION, JUMP_MODES, PREDICTION_UPDATE_TIME, FPS, GREEN, LIGHT_RED, INITIAL_SPEED_PREDICTION

class Cat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CAT_SIZE
        self.speed = CAT_NORMAL_SPEED
        self.hunting = False
        self.vision = CAT_NORMAL_VISION
        self.predicted_speed = INITIAL_SPEED_PREDICTION
        self.last_prediction_update = 0
        self.jumps_attempted = 0
        self.distance_spent = 0
        self.last_jump_time = 0
        self.last_hit_time = 0
        self.is_jumping = False
        self.jump_start_pos = None
        self.jump_end_pos = None
        self.jump_progress = 0
        self.failed_jumps = 0
        self.free_energy = 0

    def move(self, rat, current_time):
        if rat is None:
            return

        dx = rat.x - self.x
        dy = rat.y - self.y
        distance = math.hypot(dx, dy)
        
        if abs(dx) <= self.vision and abs(dy) <= self.vision and not self.hunting:
            self.start_hunting()

        if self.hunting:
            if self.is_jumping:
                self.continue_jump()
            elif current_time - self.last_jump_time >= 1.0:
                self.start_jump(rat)
                self.last_jump_time = current_time
        else:
            direction = pygame.math.Vector2(dx, dy).normalize()
            self.x += direction.x * self.speed / FPS
            self.y += direction.y * self.speed / FPS

        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))

    def start_jump(self, rat):
        dx = rat.x - self.x
        dy = rat.y - self.y
        direction = pygame.math.Vector2(dx, dy).normalize()
        
        if self.predicted_speed >= JUMP_MODES[-1]:
            jump_distance = JUMP_MODES[-1]
        else:
            jump_distance = min([j for j in JUMP_MODES if j >= self.predicted_speed], key=lambda x: abs(x - self.predicted_speed))
        
        self.is_jumping = True
        self.jump_start_pos = pygame.math.Vector2(self.x, self.y)
        self.jump_end_pos = self.jump_start_pos + direction * jump_distance
        self.jump_progress = 0
        self.jumps_attempted += 1
        self.distance_spent += jump_distance

        print(f"Jumping with predicted speed: {self.predicted_speed/GRID_SIZE:.2f}, chosen jump distance: {jump_distance/GRID_SIZE}")

    def continue_jump(self):
        self.jump_progress += 0.1
        if self.jump_progress >= 1:
            self.x, self.y = self.jump_end_pos.x, self.jump_end_pos.y
            self.is_jumping = False
        else:
            pos = self.jump_start_pos.lerp(self.jump_end_pos, self.jump_progress)
            self.x, self.y = pos.x, pos.y

    def update_prediction(self, elapsed_time, rat_speed):
        if self.hunting:
            if elapsed_time - self.last_prediction_update >= PREDICTION_UPDATE_TIME:
                if self.predicted_speed > rat_speed:
                    self.predicted_speed = max(self.predicted_speed - GRID_SIZE / 2, JUMP_MODES[0])
                elif self.predicted_speed < rat_speed or self.failed_jumps >= 6:
                    self.predicted_speed = min(self.predicted_speed + GRID_SIZE / 2, JUMP_MODES[-1])
                    if self.failed_jumps >= 6:
                        self.free_energy += 1
                    self.failed_jumps = 0
                self.last_prediction_update = elapsed_time
                print(f"Updated predicted speed: {self.predicted_speed/GRID_SIZE:.2f}, Free Energy: {self.free_energy}")

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.size, self.size))
        vision_rect = pygame.Rect(self.x - self.vision, self.y - self.vision, 
                                  2 * self.vision + self.size, 2 * self.vision + self.size)
        pygame.draw.rect(screen, LIGHT_RED if self.hunting else (200, 200, 200), vision_rect, 2)

    def check_collision(self, rat, current_time):
        if rat is None or self.is_jumping:
            return False
        collision = (self.x < rat.x + rat.size and
                     self.x + self.size > rat.x and
                     self.y < rat.y + rat.size and
                     self.y + self.size > rat.y)
        if collision and current_time - self.last_hit_time >= 0.5:
            self.last_hit_time = current_time
            return True
        elif self.is_jumping and self.jump_progress >= 1:
            self.failed_jumps += 1
        return False

    def start_hunting(self):
        self.hunting = True
        self.vision = CAT_HUNTING_VISION
        self.predicted_speed = INITIAL_SPEED_PREDICTION