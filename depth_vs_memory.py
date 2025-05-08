
import json
import matplotlib.pyplot as plt

# Load data
with open('stats.json') as f:
    ucs_data = json.load(f)
with open('stats1.json') as f:
    misplaced_data = json.load(f)
with open('stats2.json') as f:
    manhattan_data = json.load(f)

def extract(data):
    return [d['depth'] for d in data], [d['memory_kb'] for d in data]

ucs_x, ucs_y = extract(ucs_data)
mis_x, mis_y = extract(misplaced_data)
man_x, man_y = extract(manhattan_data)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(ucs_x, ucs_y, label='UCS', color='red', marker='o')
plt.plot(mis_x, mis_y, label='A* (Misplaced Tile)', color='blue', marker='o')
plt.plot(man_x, man_y, label='A* (Manhattan)', color='green', marker='o')
plt.xlabel('Depth')
plt.ylabel('Memory (KB)')
plt.title('Depth vs Memory')
plt.legend()
plt.grid(True)
plt.show()

