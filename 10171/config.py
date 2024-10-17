import pygame

# Screen settings
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 384
GRID_SIZE = 3
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_RED = (255, 200, 200)

# Game settings
RAT_SIZE = 8
CAT_SIZE = 8
CAT_NORMAL_SPEED = 5 * GRID_SIZE
RAT_SPEEDS = [5 * GRID_SIZE, 7 * GRID_SIZE, 9 * GRID_SIZE]
RAT_HP = 20

# Rat settings
RAT_BURST_A_DURATION = 1.5 * FPS  # 1.5 seconds for corner burst
RAT_BURST_A_COOLDOWN = 6 * FPS  # 6 seconds cooldown for corner burst
RAT_BURST_B_HP_THRESHOLD = 5  # HP threshold for speed increase
RAT_BURST_C_DURATION = 2 * FPS  # 2 seconds for hit burst
RAT_BURST_SPEED_MULTIPLIER = 2

# Vision settings
CAT_NORMAL_VISION = 9 * GRID_SIZE  # Updated to 7
CAT_HUNTING_VISION = 12 * GRID_SIZE

# Jumping modes
JUMP_MODES = [5 * GRID_SIZE, 7 * GRID_SIZE, 9 * GRID_SIZE, 11 * GRID_SIZE, 13 * GRID_SIZE, 15 * GRID_SIZE, 17 * GRID_SIZE]

# Prediction settings
PREDICTION_UPDATE_TIME = 1.5  # Updated to 1.5
INITIAL_SPEED_PREDICTION = 17 * GRID_SIZE  # Updated to 17