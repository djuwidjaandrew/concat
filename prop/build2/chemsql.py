import pygame
import sqlite3
import random
import time
import os
from collections import deque

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ChemTemp Hab1 Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 24)

# Configurable parameters
PACE = 2
TOKENWOW_APPEAR_TIMESTEP = 300

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'token_rules.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class Token:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.text = ""
        self.timer = 0
        self.load_rules()
        if self.name == 'tokenwow':
            self.state = ''  # Ensure tokenwow starts with an empty state

    def load_rules(self):
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM token_rules WHERE token_name = ?", (self.name,))
            rules = cur.fetchone()
        
        self.update_interval = rules['update_interval']
        self.state = rules['initial_state']
        self.state_progression = rules['state_progression'].split(',')
        self.special_behavior = rules['special_behavior'].split(',')
        self.max_tokens = rules['max_tokens']

    def update(self, timestep, chemtemp):
        self.timer += 1
        if self.timer >= self.update_interval * PACE:
            self.timer = 0
            self.update_state()
        
        self.apply_special_behavior(timestep, chemtemp)

    def update_state(self):
        if self.state not in self.state_progression:
            self.state = self.state_progression[0]
        else:
            current_index = self.state_progression.index(self.state)
            next_index = (current_index + 1) % len(self.state_progression)
            self.state = self.state_progression[next_index]

    def apply_special_behavior(self, timestep, chemtemp):
        if 'regenerate' in self.special_behavior:
            # Tokenease regeneration logic is handled in ChemTemp1Hab1
            pass
        elif 'attach_vision' in self.special_behavior:
            # Tokenprobe vision attachment logic (to be implemented)
            pass
        elif 'appear_on_event' in self.special_behavior:
            if self.name == 'tokenwow' and timestep == TOKENWOW_APPEAR_TIMESTEP * PACE and not self.state:
                self.state = self.state_progression[0]  # Set to '^^^'
        elif 'affect_tokenease' in self.special_behavior:
            if self.name == 'tokenwow' and self.state:
                max_ease = min(self.state_progression.index(self.state) + 1, 3)
                chemtemp.limit_tokenease(max_ease)

    def draw(self, screen):
        if self.state:  # Only draw if the token has a state
            text = font.render(f"{self.name}{self.state}", True, BLACK)
            screen.blit(text, (self.x, self.y))

class ChemTemp1Hab1:
    def __init__(self):
        self.tokens = [
            Token("tokenprobe", 50, 80),
            Token("tokenprobe", 50, 110),
        ]
        self.tokenease = [Token("tokenease", 50, 140 + i * 30) for i in range(3)]
        self.tokens[0].text = "v3"
        self.tokens[1].text = "v4"
        self.timestep = 0
        self.tokenwow = Token("tokenwow", 50, 200)
        self.token_display_order = deque(self.tokens + self.tokenease)  # Remove tokenwow from initial display
        self.max_tokenease = 3  # Set initial max tokenease to 3

    def update(self):
        self.timestep += 1
        for token in self.tokens + self.tokenease + [self.tokenwow]:
            token.update(self.timestep, self)

        self.manage_tokenease()

        # Update token_display_order
        self.token_display_order = deque(self.tokens + self.tokenease)
        if self.tokenwow.state:
            self.token_display_order.appendleft(self.tokenwow)

    def manage_tokenease(self):
        if self.timestep % (60 * PACE) == 0:
            if self.tokenwow.state:
                self.max_tokenease = min(self.tokenwow.state_progression.index(self.tokenwow.state) + 1, 3)
            else:
                self.max_tokenease = 3  # Default max when tokenwow is not active
            
            self.limit_tokenease(self.max_tokenease)

            if len(self.tokenease) < self.max_tokenease:
                new_tokenease = Token("tokenease", 50, 140 + 30 * len(self.tokenease))
                self.tokenease.append(new_tokenease)

    def limit_tokenease(self, max_ease):
        while len(self.tokenease) > max_ease:
            self.tokenease.pop()

    def get_tokenwow_weight(self):
        if not self.tokenwow.state:
            return 0
        weights = {'^^^': 3, '^^': 2, '^': 1, '~': 1}
        return weights.get(self.tokenwow.state, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (30, 30, 300, 250))
        pygame.draw.rect(screen, BLACK, (30, 30, 300, 250), 2)
        text = font.render("ChemTemp1Hab1", True, BLACK)
        screen.blit(text, (35, 35))
        
        # Draw tokens based on the display order
        for i, token in enumerate(self.token_display_order):
            token.y = 80 + i * 30
            token.draw(screen)

class ChemTemp2Hab1:
    def __init__(self):
        self.components = [0, 0, 0]
        self.last_update = 0

    def update(self, chemtemp1):
        current_time = time.time()
        if current_time - self.last_update >= 1 * PACE:  # Update every second * PACE
            tokenwow_weight = chemtemp1.get_tokenwow_weight()
            self.components = [
                tokenwow_weight,
                sum(1 for t in chemtemp1.tokens if t.name == "tokenprobe"),
                len(chemtemp1.tokenease)
            ]
            self.last_update = current_time

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (350, 30, 300, 250))
        pygame.draw.rect(screen, BLACK, (350, 30, 300, 250), 2)
        text = font.render("ChemTemp2Hab1", True, BLACK)
        screen.blit(text, (355, 35))
        text = font.render("on mind:", True, BLACK)
        screen.blit(text, (355, 60))
        text = font.render("second level highlighting", True, BLACK)
        screen.blit(text, (355, 85))

        total = sum(self.components)
        if total > 0:
            heights = [c / total * 180 for c in self.components]
            colors = [RED, GREEN, BLUE]
            y = 110
            for h, color in zip(heights, colors):
                pygame.draw.rect(screen, color, (400, y, 200, h))
                y += h

        # Draw quarter-circle dividing lines
        for i in range(1, 3):
            y = 110 + i * 180 // 3
            pygame.draw.arc(screen, BLACK, (350, y - 50, 100, 100), 0, 3.14159 / 2, 2)

def draw_scenario(screen, timestep, tokenease_count, tokenwow_state):
    # Time graph
    pygame.draw.rect(screen, WHITE, (30, 300, 940, 100))
    pygame.draw.rect(screen, BLACK, (30, 300, 940, 100), 2)
    pygame.draw.line(screen, BLACK, (50, 380), (950, 380), 2)
    for i in range(0, 1201, 120):
        x = 50 + i * 3 // 4
        pygame.draw.line(screen, BLACK, (x, 375), (x, 385), 2)
        text = font.render(str(i), True, BLACK)
        screen.blit(text, (x - 10, 390))
    
    # Current timestep marker
    x = 50 + min(timestep // PACE, 1200) * 3 // 4
    pygame.draw.line(screen, RED, (x, 310), (x, 370), 2)
    
    # Rat appears marker
    if timestep >= TOKENWOW_APPEAR_TIMESTEP * PACE:
        x_rat = 50 + TOKENWOW_APPEAR_TIMESTEP * 3 // 4
        pygame.draw.line(screen, GREEN, (x_rat, 310), (x_rat, 370), 2)
        text = font.render("rat appears", True, GREEN)
        screen.blit(text, (x_rat - 30, 320))

    # Cat and objects visualization
    pygame.draw.rect(screen, WHITE, (30, 420, 940, 150))
    pygame.draw.rect(screen, BLACK, (30, 420, 940, 150), 2)
    
    # Neutral objects (yellow dots)
    for i in range(3):
        color = YELLOW if i < tokenease_count else GREY
        pygame.draw.circle(screen, color, (200 + i * 100, 490), 10)
        text = font.render("n", True, BLACK)
        screen.blit(text, (195 + i * 100, 470))
    
    # Cat (green dot)
    pygame.draw.circle(screen, GREEN, (350, 540), 20)
    
    # (!) beside the cat when rat appears, color changes based on tokenwow state
    if timestep >= TOKENWOW_APPEAR_TIMESTEP * PACE:
        if tokenwow_state == "^^^":
            color = RED
            text = "(!)"
        elif tokenwow_state == "^^":
            color = YELLOW
            text = "(!)"
        elif tokenwow_state == "^":
            color = YELLOW
            text = "(~)"
        elif tokenwow_state == "~":
            color = GREEN
            text = "(~) eased"
        else:
            color = BLACK
            text = ""
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (375, 530))
    
    # Rat (red dot)
    if timestep >= TOKENWOW_APPEAR_TIMESTEP * PACE:
        pygame.draw.circle(screen, RED, (600, 540), 20)
        text = font.render("rat", True, BLACK)
        screen.blit(text, (590, 520))

def main():
    chemtemp1 = ChemTemp1Hab1()
    chemtemp2 = ChemTemp2Hab1()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        chemtemp1.update()
        chemtemp2.update(chemtemp1)
        chemtemp1.draw(screen)
        chemtemp2.draw(screen)
        tokenwow_state = chemtemp1.tokenwow.state
        draw_scenario(screen, chemtemp1.timestep, len(chemtemp1.tokenease), tokenwow_state)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()