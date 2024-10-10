import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Topdown Ensemble Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def draw_node(screen, x, y, label, highlighted=False, status=""):
    color = RED if highlighted else BLACK
    pygame.draw.circle(screen, color, (x, y), 30, 2)
    text = font.render(label, True, color)
    screen.blit(text, (x - 10, y - 15))
    
    if status:
        status_text = small_font.render(status, True, GREEN)
        screen.blit(status_text, (x + 40, y - 10))

def draw_line(screen, start, end, highlighted=False):
    color = RED if highlighted else BLACK
    pygame.draw.line(screen, color, start, end, 2)

def draw_habits(screen, x, y):
    habits = ["hab1", "hab2", "hab3"]
    for i, habit in enumerate(habits):
        text = small_font.render(habit, True, BLACK)
        screen.blit(text, (x + i * 60, y))
        pygame.draw.circle(screen, GREEN, (x + i * 60 + 20, y + 30), 5)

def draw_homeostats(screen, x, y):
    homeostats = ["hom1", "hom2", "hom3"]
    colors = [GREEN, YELLOW, GREEN]
    for i, homeostat in enumerate(homeostats):
        text = small_font.render(homeostat, True, BLACK)
        screen.blit(text, (x + i * 60, y))
        pygame.draw.circle(screen, colors[i], (x + i * 60 + 20, y + 30), 5)

def main():
    nodes = [
        ('A', (200, 50)),
        ('B', (200, 150)),
        ('C', (200, 250)),
        ('D', (200, 350)),
        ('E', (200, 450))
    ]

    running = True
    step = 0
    node_statuses = [""] * 3  # For nodes A, B, C

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        # Draw connections
        for i in range(len(nodes) - 1):
            draw_line(screen, nodes[i][1], nodes[i+1][1], i < step)

        # Draw nodes
        for i, (label, pos) in enumerate(nodes):
            status = node_statuses[i] if i < 3 else ""
            draw_node(screen, pos[0], pos[1], label, i == step, status)

        # Draw habits for node D
        if step > 2:
            draw_habits(screen, 300, 350)

        # Draw homeostats for node E
        if step > 3:
            draw_homeostats(screen, 300, 450)

        pygame.display.flip()

        if step < len(nodes):
            time.sleep(1)
            if step < 3:
                node_statuses[step] = "txt ok"
            step += 1

    pygame.quit()

if __name__ == "__main__":
    main()