import matplotlib.pyplot as plt
import io
import base64

# Create a sample bar chart
data = [3, 7, 9, 2, 6]
labels = ['A', 'B', 'C', 'D', 'E']
plt.bar(labels, data)
plt.xlabel('Categories')
plt.ylabel('Values')

# Save the chart as a base64-encoded image
buffer = io.BytesIO()
plt.savefig(buffer, format='png')
chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
buffer.close()

# Print the base64-encoded chart data
print(chart_data)
