import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulate_mouse_speed(n_steps=200, base_speed=5, noise_level=0.2):
    return base_speed + np.random.normal(0, noise_level, n_steps)

def cat_prediction_model(frame, actual_speed):
    base_prediction = actual_speed + np.random.normal(0, 0.2)  # Randomized prediction
    if frame < 25:
        return base_prediction + 3  # High prediction
    elif frame < 50:
        return base_prediction + 2  # Gradually lowering
    elif frame < 75:
        return base_prediction + 1  # Further lowering
    else:
        return base_prediction + 0.2  # Stabilized

np.random.seed(42)
time_steps = 200
actual_speeds = simulate_mouse_speed(time_steps)
cat_predictions = np.zeros(time_steps)
prediction_errors = np.zeros(time_steps)

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
ax2.legend()

# Add panic text to the second subplot
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
    cat_predictions[frame] = cat_prediction_model(frame, actual_speeds[frame])
    prediction_errors[frame] = np.abs(cat_predictions[frame] - actual_speeds[frame])
    
    mouse_y = 5 + actual_speeds[frame] / 2
    mouse.set_data([5], [mouse_y])
    cat.set_data([5], [5])
    
    actual_line.set_data(range(frame+1), actual_speeds[:frame+1])
    predicted_line.set_data(range(frame+1), cat_predictions[:frame+1])
    
    error_line.set_data(range(frame+1), prediction_errors[:frame+1])
    
    actual_text.set_text(f'Actual Speed: {actual_speeds[frame]:.2f}')
    predicted_text.set_text(f'Predicted Speed: {cat_predictions[frame]:.2f}')
    
    return cat, mouse, actual_line, predicted_line, error_line, actual_text, predicted_text

anim = FuncAnimation(fig, update, frames=time_steps, interval=50, blit=True)

plt.tight_layout()
plt.show()
