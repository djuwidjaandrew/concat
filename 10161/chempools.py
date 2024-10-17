class ChemPool:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def add(self, amount):
        self.value += amount

    def reduce(self, amount):
        self.value = max(0, self.value - amount)

    def get_value(self):
        return self.value

class ChemPoolManager:
    def __init__(self):
        self.pools = {
            'ChemA': ChemPool('ChemA'),  # Stress pool
            'BushDoneA': ChemPool('BushDoneA'),
            'BushDoneB': ChemPool('BushDoneB'),
            'BushDoneC': ChemPool('BushDoneC'),
            'BushDoneD': ChemPool('BushDoneD'),
            'BushDoneE': ChemPool('BushDoneE'),
            'BushDoneF': ChemPool('BushDoneF'),
        }

    def get_pool(self, name):
        return self.pools.get(name)

    def update_stress(self, cat, world):
        chem_a = self.get_pool('ChemA')
        vision_range = 3
        for dy in range(-vision_range, vision_range + 1):
            for dx in range(-vision_range, vision_range + 1):
                x, y = cat.x + dx, cat.y + dy
                if 0 <= x < world.grid_size and 0 <= y < world.grid_height:
                    cell = world.grid[y][x]
                    if isinstance(cell, tuple) and cell[0] == 'rat':
                        chem_a.add(5)  # STRESS^^^^
                    elif isinstance(cell, tuple) and cell[0] == 'food':
                        chem_a.add(1)  # STRESS^

    def update_pools(self):
        # Placeholder for future token-to-token interactions
        pass