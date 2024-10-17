class ChemPool:
    def __init__(self, initial_value=0):
        self.value = initial_value

    def add(self, amount):
        self.value += amount

    def reduce(self, amount):
        self.value = max(0, self.value - amount)

class ChemManager:
    def __init__(self):
        self.pools = {
            'ChemA': ChemPool(),
            # Add other chemical pools as needed
        }

    def get_pool(self, name):
        return self.pools.get(name, ChemPool())