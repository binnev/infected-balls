import matplotlib.pyplot as plt

# import pandas as pd
from objects import Ball, Canvas, INFECTED, RECOVERED, PopulationHealth, HEALTHY, COLORS

population_health = PopulationHealth()

canvas = Canvas(balls=[
    Ball(position=(2, 2), health=HEALTHY),
])
population_health.append(canvas.population_health_percentages)
for _ in range(10):
    canvas.add_balls(Ball(health=INFECTED))
    population_health.append(canvas.population_health_percentages)

for _ in range(10):
    canvas.add_balls(Ball(health=RECOVERED))
    population_health.append(canvas.population_health_percentages)

# ================ plots ===================
percentages = population_health.data

# Make the plot
labels = [
    INFECTED,
    HEALTHY,
    RECOVERED,
]
series = [percentages[label] for label in labels]
colors = [COLORS[label] for label in labels]

sp = plt.stackplot(range(len(series[0])),
                   *series,
                   labels=labels,
                   colors=colors)
plt.legend(loc="upper left")
plt.margins(0, 0)
plt.title("population health")
plt.show()
