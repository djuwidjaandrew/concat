import pygame
from game_environment import GameEnvironment

def main():
    pygame.init()
    pygame.display.set_caption("Object Features Classifier Simulation")

    game_env = GameEnvironment()
    game_env.run()

    pygame.quit()

if __name__ == "__main__":
    main()