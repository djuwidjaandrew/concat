import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate_mouse_speed(n_steps=200, base_speed=5, noise_level=0.2):
    return base_speed + np.random.normal(0, noise_level, n_steps)

class StableBayesianPredictor:
    def __init__(self, prior_mean=5, prior_std=0.5):
        self.mean = prior_mean
        self.std = prior_std
        self.perturbation = 0
        self.spike_duration = 20
        self.spike_counter = 0

    def update(self, observation):
        likelihood_mean = observation
        likelihood_std = 0.1
        posterior_mean = (self.mean / self.std**2 + likelihood_mean / likelihood_std**2) / (1 / self.std**2 + 1 / likelihood_std**2)
        posterior_std = np.sqrt(1 / (1 / self.std**2 + 1 / likelihood_std**2))
        self.mean = posterior_mean
        self.std = posterior_std

    def predict(self, frame):
        if frame % 60 == 0 and frame > 0:  # Changed from 40 to 60
            self.perturbation = np.random.uniform(0.5, 1.5)  # Positive perturbation
            self.spike_counter = self.spike_duration
        elif self.spike_counter > 0:
            self.perturbation *= 0.95  # Gradual decrease
            self.spike_counter -= 1
        else:
            self.perturbation *= 0.9  # Further decay when not in spike period

        return np.random.normal(self.mean, self.std) + self.perturbation

def create_mblr_display(seed=42):
    np.random.seed(seed)
    time_steps = 200
    actual_speeds = simulate_mouse_speed(time_steps)
    stable_predictions = np.zeros(time_steps)
    prediction_errors = np.zeros(time_steps)

    stable_predictor = StableBayesianPredictor()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
    plt.subplots_adjust(hspace=0.3)

    ax1.set_xlim(0, time_steps)
    ax1.set_ylim(0, 12)
    ax1.set_title("Stable Predictions with Periodic Spikes")
    ax1.set_xlabel("Time Steps")
    ax1.set_ylabel("Speed")
    actual_line, = ax1.plot([], [], 'r-', label='Actual Speed')
    predicted_line, = ax1.plot([], [], 'b-', label='Stable Prediction')
    uncertainty = ax1.fill_between([], [], [], alpha=0.3, color='blue')
    ax1.legend()

    ax1.text(60, 11.5, "minorcheck^", ha='center', va='bottom')
    ax1.text(120, 11.5, "minorcheck^", ha='center', va='bottom')
    ax1.text(180, 11.5, "minorcheck^", ha='center', va='bottom')

    ax2.set_xlim(0, time_steps)
    ax2.set_ylim(0, 5)
    ax2.set_title("Free Energy (Prediction Error)")
    ax2.set_xlabel("Time Steps")
    ax2.set_ylabel("Error")
    error_line, = ax2.plot([], [], 'g-')

    state_text = fig.text(0.5, 0.98, "at relative ease", ha='center', va='top')

    def update(frame):
        stable_predictor.update(actual_speeds[frame])
        stable_predictions[frame] = stable_predictor.predict(frame)
        prediction_errors[frame] = np.abs(stable_predictions[frame] - actual_speeds[frame])
        
        actual_line.set_data(range(frame+1), actual_speeds[:frame+1])
        predicted_line.set_data(range(frame+1), stable_predictions[:frame+1])
        
        for collection in ax1.collections:
            collection.remove()
        uncertainty = ax1.fill_between(range(frame+1), 
                                       stable_predictions[:frame+1] - stable_predictor.std,
                                       stable_predictions[:frame+1] + stable_predictor.std, 
                                       alpha=0.3, color='blue')
        
        error_line.set_data(range(frame+1), prediction_errors[:frame+1])
        
        return actual_line, predicted_line, uncertainty, error_line

    anim = FuncAnimation(fig, update, frames=time_steps, interval=50, blit=False)
    plt.tight_layout()
    return fig, anim

# Create and display multiple MBLR instances
num_instances = 1
figs_anims = [create_mblr_display(seed=i) for i in range(num_instances)]

plt.show()