import json
import os
from datetime import datetime

class ColorLogger:
    def __init__(self):
        self.combinations = {}
        self.log_folder = "logs"
        self.create_log_folder()
        self.filename = self.generate_filename()

    def create_log_folder(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

    def generate_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.log_folder, f"color_combinations_{timestamp}.json")

    def log_combination(self, colors):
        color_key = tuple(colors)
        if color_key not in self.combinations:
            self.combinations[color_key] = len(self.combinations) + 1
            self.save_to_file()

    def save_to_file(self):
        with open(self.filename, 'w') as f:
            json.dump({str(k): v for k, v in self.combinations.items()}, f, indent=2)