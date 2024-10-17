import pygame
import random
from init import WHITE, CELL_SIZE, GRID_SIZE
from world import World
from cat import Cat, CatMapper
from chem_manager import ChemManager
from look import TimedRotationStrategy, PhaseBasedStrategy
from catbush import CatBush
from walkchase import CatWalkChase

def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, int(GRID_SIZE * 1.3 * CELL_SIZE)))
    pygame.display.set_caption("Cat Simulation")
    clock = pygame.time.Clock()
    running = True

    world = World()
    chem_manager = ChemManager()
    cat = Cat(world.grid_size // 2, world.grid_height - 1, world, chem_manager)
    cat_mapper = CatMapper(world.grid_size, world.grid_height)

    # Initialize CatBush and CatWalkChase separately
    cat.bush = CatBush(cat, world, chem_manager)
    cat.policies = CatWalkChase(cat, world, chem_manager)
    
    cat.initialize_bush_done() 

    # Uncomment the next line to use timed rotation instead of phase-based
    # cat.look.set_strategy(TimedRotationStrategy(10))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        world.update_rats()
        world.remove_dead_rats()
        world.draw(screen, CELL_SIZE)

        cat.update()

        if cat.chasing:
            cat.policies.chase_target()
        else:
            if random.random() < 0.7:  # 70% chance to seek a bush
                cat.bush.move_towards_bush()
            else:
                cat.policies.random_walk()

        cat.draw(screen, CELL_SIZE)
        cat.look.draw_vision(screen, CELL_SIZE)

        cat_mapper.update(cat, world)

        pygame.display.flip()
        clock.tick(5)  # 5 FPS for slower simulation

    pygame.quit()

if __name__ == "__main__":
    main()