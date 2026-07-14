You will need to install the pyserial and matplotlib libraries if you don't already have them. Open your terminal or command prompt and run:
*pip install pyserial matplotlib*

_How It Works_
1. Non-Blocking Reads: The update_plot function checks ser.in_waiting to process all data that has arrived since the last frame. This prevents the plot from lagging behind the Arduino.
2. Robust Parsing: It safely wraps the .split() and float() conversions in a try...except block. Serial connections often produce a garbled half-line when first connected, and this ensures the script doesn't crash on the first corrupted data point.
3. Dynamic Y-Axis: The script calculates the minimum and maximum values currently in the data arrays and applies a 20% padding margin so the plot automatically scales as you change your target speed in the Arduino code.
