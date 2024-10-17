import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, FPS, GRID_SIZE, GREEN, BLACK
from rat import Rat
from cat import Cat

class GameEnvironment:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.rat = Rat(random.randint(0, SCREEN_WIDTH - 30), random.randint(0, SCREEN_HEIGHT - 30))
        self.cat = Cat(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.font = pygame.font.Font(None, 24)
        self.collision_points = []
        self.game_over = False
        self.elapsed_time = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()
            pygame.display.flip()
            self.elapsed_time += self.clock.tick(FPS) / 1000.0

    def update(self):
        if self.rat:
            self.rat.move(pygame.math.Vector2(self.cat.x, self.cat.y))
        self.cat.move(self.rat, self.elapsed_time)
        if self.rat:
            self.cat.update_prediction(self.elapsed_time, self.rat.get_actual_speed())
        else:
            self.cat.update_prediction(self.elapsed_time, 0)

        if self.rat and self.cat.check_collision(self.rat, self.elapsed_time):
            if self.rat.get_hit():
                self.rat = None
                self.game_over = True
            else:
                self.collision_points.append((self.rat.x, self.rat.y))

    def draw(self):
        self.screen.fill(WHITE)
        if self.rat:
            self.rat.draw(self.screen)
        self.cat.draw(self.screen)

        for point in self.collision_points:
            pygame.draw.line(self.screen, GREEN, (point[0] - 5, point[1] - 5), (point[0] + 5, point[1] + 5), 2)
            pygame.draw.line(self.screen, GREEN, (point[0] - 5, point[1] + 5), (point[0] + 5, point[1] - 5), 2)

        # Draw stats
        stats = [
            f"Rat HP: {self.rat.hp if self.rat else 'N/A'}",
            f"Rat predicted speed: {self.cat.predicted_speed / GRID_SIZE if self.cat.predicted_speed is not None else 'N/A'}",
            f"Rat actual speed: {self.rat.get_actual_speed() / GRID_SIZE if self.rat else 'N/A'}",
            f"Jumps attempted: {self.cat.jumps_attempted}",
            f"Distance spent: {self.cat.distance_spent / GRID_SIZE:.2f}",
            # f"Free Energy: {self.cat.free_energy}",  # Commented out to hide FE counter
        ]
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, BLACK)
            self.screen.blit(text, (10, 10 + i * 30))

        if self.game_over:
            game_over_text = self.font.render("Game Over! Rat has been caught!", True, BLACK)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)