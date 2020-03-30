import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

from conf import INFECTED, HEALTHY, RECOVERED, COLORS, DEFAULT_SPEED
from objects import Canvas, Ball, PopulationHealth

# ========== make axes =============
fig, axes = plt.subplots(2, 1, figsize=(5, 7))
ax = axes[0]
ax.axis("off")

# ================================== inputs here =======================================
# define cities
UTRECHT = dict(top=5, bottom=1, left=1, right=5)
BILTHOVEN = dict(top=5.5, bottom=4.5, left=6, right=7)
AMERSFOORT = dict(top=9, bottom=7, left=7, right=9)
ax.add_patch(Rectangle(xy=(0, 0), width=10, height=10, color="k"))
ax.text(UTRECHT["left"],
        UTRECHT["top"],
        "UTRECHT",
        color="w",
        fontsize="x-small")
ax.add_patch(
    Rectangle(
        xy=(UTRECHT["left"], UTRECHT["bottom"]),
        width=UTRECHT["right"] - UTRECHT["left"],
        height=UTRECHT["top"] - UTRECHT["bottom"],
        facecolor="none",
        edgecolor="w",
    ))
ax.text(BILTHOVEN["left"],
        BILTHOVEN["top"],
        "BILTHOVEN",
        color="w",
        fontsize="x-small")
ax.add_patch(
    Rectangle(
        xy=(BILTHOVEN["left"], BILTHOVEN["bottom"]),
        width=BILTHOVEN["right"] - BILTHOVEN["left"],
        height=BILTHOVEN["top"] - BILTHOVEN["bottom"],
        facecolor="none",
        edgecolor="w",
    ))
ax.text(AMERSFOORT["left"],
        AMERSFOORT["top"],
        "AMERSFOORT",
        color="w",
        fontsize="x-small")
ax.add_patch(
    Rectangle(
        xy=(AMERSFOORT["left"], AMERSFOORT["bottom"]),
        width=AMERSFOORT["right"] - AMERSFOORT["left"],
        height=AMERSFOORT["top"] - AMERSFOORT["bottom"],
        facecolor="none",
        edgecolor="w",
    ))

# create objects
canvas = Canvas(boundaries=dict(left=0, bottom=0, right=10, top=10))
patient_zero = Ball(position=(3, 3),
                    velocity=(-DEFAULT_SPEED, 0),
                    health="infected")
canvas.add_balls(patient_zero)
canvas.generate_random_balls(
    50,
    # ball_class=IrresponsibleBall,
    x_range=(UTRECHT["left"], UTRECHT["right"]),
    y_range=(UTRECHT["bottom"], UTRECHT["top"]),
    ball_kwargs={"boundaries": UTRECHT},
)
canvas.generate_random_balls(
    5,
    # ball_class=IrresponsibleBall,
    x_range=(BILTHOVEN["left"], BILTHOVEN["right"]),
    y_range=(BILTHOVEN["bottom"], BILTHOVEN["top"]),
    ball_kwargs={"boundaries": BILTHOVEN},
)
canvas.generate_random_balls(
    20,
    # ball_class=IrresponsibleBall,
    x_range=(AMERSFOORT["left"], AMERSFOORT["right"]),
    y_range=(AMERSFOORT["bottom"], AMERSFOORT["top"]),
    ball_kwargs={"boundaries": AMERSFOORT},
)
# roaming balls
canvas.generate_random_balls(10)

simulation_name = "Cities"

# ======================== plotting ============================
artists = canvas.add_balls_to_axis(ax)
plt.setp(ax, xlim=(0, 10), ylim=(0, 10))
ax.axis("equal")
ax.set_title(simulation_name)

# initialise stacked area plot
population_health = PopulationHealth()
labels = [INFECTED, HEALTHY, RECOVERED]
series = [population_health.data[label] for label in labels]
colors = [COLORS[label] for label in labels]
plt.sca(axes[1])
sp = plt.stackplot(range(len(series[0])),
                   *series,
                   labels=labels,
                   colors=colors)
plt.legend(loc="upper left", fontsize="x-small")
plt.title("population health")
axes[1].axis("off")


def update(frame_number):
    canvas.update()
    population_health.append(canvas.population_health_percentages)
    series = [population_health.data[label] for label in labels]
    plt.sca(axes[1])
    plt.gca().collections.clear()
    sp = plt.stackplot(range(len(series[0])),
                       *series,
                       labels=labels,
                       colors=colors)


animation = FuncAnimation(fig, update, interval=60, frames=range(300))
plt.show()
# animation.save("cities2.mp4")
