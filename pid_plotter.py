import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Configuration ---
# CHANGE THIS to your Arduino's port (e.g., 'COM3' or '/dev/ttyUSB0')
SERIAL_PORT = 'COM3' 
BAUD_RATE = 9600
WINDOW_SIZE = 200  # Number of data points to show on the screen at once

# --- Initialization ---
# Arrays to store the data
target_data = []
actual_data = []

# Setup the serial connection
try:
    print(f"Connecting to {SERIAL_PORT} at {BAUD_RATE} baud...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Give the Arduino time to reset after opening the port
    print("Connected! Waiting for data...")
except Exception as e:
    print(f"Error opening serial port: {e}")
    print("Make sure the Arduino Serial Monitor is closed and the port is correct.")
    exit()

# Setup the Matplotlib figure
fig, ax = plt.subplots(figsize=(10, 6))
fig.canvas.manager.set_window_title('Live PID Step Response')

ax.set_title('DC Motor PID Control - Live Plot')
ax.set_xlabel('Time (samples)')
ax.set_ylabel('Speed (RPM / Counts)')
ax.grid(True, linestyle='--', alpha=0.7)

# Create empty lines for target and actual speed
line_target, = ax.plot([], [], label='Target Speed (Setpoint)', color='red', linestyle='--', linewidth=2)
line_actual, = ax.plot([], [], label='Actual Speed (Encoder)', color='blue', linewidth=2)
ax.legend(loc='upper right')

# --- Animation Function ---
def update_plot(frame):
    # Read all available lines from the serial buffer
    while ser.in_waiting > 0:
        try:
            # Read line, decode bytes to string, and remove trailing whitespace
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                # Expecting format: "Target Actual" (e.g., "100.0 98.5")
                values = line.split()
                if len(values) == 2:
                    target = float(values[0])
                    actual = float(values[1])
                    
                    target_data.append(target)
                    actual_data.append(actual)
                    
                    # Keep the lists constrained to the WINDOW_SIZE
                    if len(target_data) > WINDOW_SIZE:
                        target_data.pop(0)
                        actual_data.pop(0)
        except ValueError:
            # Ignore garbled serial data during startup
            pass
        except Exception as e:
            print(f"Read error: {e}")

    # Update the lines with the new data
    x_data = list(range(len(target_data)))
    line_target.set_data(x_data, target_data)
    line_actual.set_data(x_data, actual_data)
    
    # Dynamically scale the axes
    ax.set_xlim(0, max(WINDOW_SIZE, len(target_data)))
    
    if target_data and actual_data:
        all_y = target_data + actual_data
        min_y, max_y = min(all_y), max(all_y)
        # Add a 20% margin to the top and bottom of the Y axis
        margin = max(abs(max_y - min_y) * 0.2, 10) 
        ax.set_ylim(min_y - margin, max_y + margin)

    return line_target, line_actual

# --- Run the Animation ---
# Update every 50ms to match the Arduino's 20Hz loop
ani = animation.FuncAnimation(fig, update_plot, interval=50, blit=False, cache_frame_data=False)

# This blocks execution until the window is closed
plt.tight_layout()
plt.show()

# Clean up when the window is closed
ser.close()
print("Serial port closed.")
