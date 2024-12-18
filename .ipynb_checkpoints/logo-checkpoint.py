import matplotlib.pyplot as plt

# Data for plotting
x = [1, 2, 3, 4, 5]  # X-axis values
y = [1, 4, 9, 16, 25]  # Y-axis values

# Create the plot
plt.plot(x, y, marker='o', linestyle='-', color='b', label='y = x^2')

# Add labels, title, and legend
plt.xlabel('X-axis')  # Label for the X-axis
plt.ylabel('Y-axis')  # Label for the Y-axis
plt.title('Simple Line Plot')  # Title of the plot
plt.legend()  # Show legend

# Show grid
plt.grid(True)

# Display the plot
plt.show()
