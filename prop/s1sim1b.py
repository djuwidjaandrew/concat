import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import norm

def simulate_mouse_speed(n_steps=200, base_speed=5, noise_level=0.2):
    return base_speed + np.random.normal(0, noise_level, n_steps)

class BayesianPredictor:
    def __init__(self, prior_mean=5, prior_std=2):
        self.mean = prior_mean
        self.std = prior_std
        self.panic_level = 3

    def update(self, observation):
        likelihood_mean = observation
        likelihood_std = 0.2
        posterior_mean = (self.mean / self.std**2 + likelihood_mean / likelihood_std**2) / (1 / self.std**2 + 1 / likelihood_std**2)
        posterior_std = np.sqrt(1 / (1 / self.std**2 + 1 / likelihood_std**2))
        self.mean = posterior_mean
        self.std = posterior_std

    def predict(self, frame):
        base_prediction = np.random.normal(self.mean, self.std)
        if frame < 25:
            return base_prediction + self.panic_level + np.random.normal(0, 1)  # More randomness
        elif frame < 50:
            self.panic_level = max(2, self.panic_level - 0.04)
            return base_prediction + self.panic_level
        elif frame < 75:
            self.panic_level = max(1, self.panic_level - 0.04)
            return base_prediction + self.panic_level
        else:
            self.panic_level = max(0.2, self.panic_level - 0.02)
            return base_prediction + self.panic_level

np.random.seed(42)
time_steps = 200
actual_speeds = simulate_mouse_speed(time_steps)
cat_predictions = np.zeros(time_steps)
prediction_errors = np.zeros(time_steps)

predictor = BayesianPredictor()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))
plt.subplots_adjust(hspace=0.4)

ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.set_title("Cat watching Mouse")
cat, = ax1.plot([], [], 'go', markersize=20)
mouse, = ax1.plot([], [], 'ro', markersize=10)

ax2.set_xlim(0, time_steps)
ax2.set_ylim(0, 12)
ax2.set_title("Speed Predictions")
ax2.set_xlabel("Time Steps")
ax2.set_ylabel("Speed")
actual_line, = ax2.plot([], [], 'r-', label='Actual Speed')
predicted_line, = ax2.plot([], [], 'b-', label='Cat\'s Prediction')
uncertainty = ax2.fill_between([], [], [], alpha=0.3, color='blue')
ax2.legend()

ax2.text(25, 11.5, "panic^^^ to panic^^", ha='center', va='bottom')
ax2.text(50, 11, "panic^^ to panic^", ha='center', va='bottom')

ax3.set_xlim(0, time_steps)
ax3.set_ylim(0, 5)
ax3.set_title("Free Energy (Prediction Error)")
ax3.set_xlabel("Time Steps")
ax3.set_ylabel("Error")
error_line, = ax3.plot([], [], 'g-')

actual_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes)
predicted_text = ax1.text(0.02, 0.90, '', transform=ax1.transAxes)

def update(frame):
    predictor.update(actual_speeds[frame])
    cat_predictions[frame] = predictor.predict(frame)
    prediction_errors[frame] = np.abs(cat_predictions[frame] - actual_speeds[frame])
    
    mouse_y = 5 + actual_speeds[frame] / 2
    mouse.set_data([5], [mouse_y])
    cat.set_data([5], [5])
    
    actual_line.set_data(range(frame+1), actual_speeds[:frame+1])
    predicted_line.set_data(range(frame+1), cat_predictions[:frame+1])
    
    for collection in ax2.collections:
        collection.remove()
    uncertainty = ax2.fill_between(range(frame+1), 
                                   cat_predictions[:frame+1] - predictor.std,
                                   cat_predictions[:frame+1] + predictor.std, 
                                   alpha=0.3, color='blue')
    
    error_line.set_data(range(frame+1), prediction_errors[:frame+1])
    
    actual_text.set_text(f'Actual Speed: {actual_speeds[frame]:.2f}')
    predicted_text.set_text(f'Predicted Speed: {cat_predictions[frame]:.2f}')
    
    return cat, mouse, actual_line, predicted_line, error_line, actual_text, predicted_text, uncertainty

anim = FuncAnimation(fig, update, frames=time_steps, interval=50, blit=False)

plt.tight_layout()
plt.show()
