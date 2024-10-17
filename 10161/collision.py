class CollisionHandler:
    def __init__(self, world):
        self.world = world

    def is_valid_move(self, x, y):
        # Check if the position is within the grid
        if not (0 <= x < self.world.grid_size and 0 <= y < self.world.grid_height):
            return False

        # Check for collision with bridge
        if self.is_bridge(x, y):
            return False

        # Check for collision with separator
        if self.is_separator(x, y):
            return False

        return True

    def is_bridge(self, x, y):
        # Assuming the bridge is at the center of the grid
        bridge_y = self.world.grid_height // 2
        bridge_width = self.world.grid_size // 5  # Adjust this value based on your bridge width
        bridge_start = (self.world.grid_size - bridge_width) // 2
        bridge_end = bridge_start + bridge_width

        return y == bridge_y and bridge_start <= x < bridge_end

    def is_separator(self, x, y):
        # Assuming the separator is a vertical line in the middle of the grid
        separator_x = self.world.grid_size // 2
        return x == separator_x and y != self.world.grid_height // 2  # Allow movement on the bridge level

def apply_collision_rules(cat, new_x, new_y, collision_handler):
    if collision_handler.is_valid_move(new_x, new_y):
        cat.x, cat.y = new_x, new_y
        return True
    return False