from celluloid import Camera
from matplotlib import pyplot as plt

from objects import Canvas, Ball


def main():
    fig, ax = plt.subplots()
    # draw boundary
    x = [0, 0, 10, 10, 0]
    y = [0, 10, 10, 0, 0]
    camera = Camera(fig)
    canvas = Canvas(boundaries=dict(left=0, bottom=0, right=10, top=10))
    patient_zero = Ball(
        position=(3, 3), velocity=(-0.1, -0.2), health="infected"
    )
    canvas.add_balls(patient_zero)
    canvas.generate_random_balls(25)
    artists = canvas.draw_balls(ax)

    for frame in range(100):
        canvas.update_balls_position()
        canvas.handle_collisions()
        canvas.handle_infections()
        ax.text(0, 0, str(canvas.population_health_percentages), va="top")
        ax.plot(x, y, "-k")
        plt.setp(ax, xlim=(0, 10), ylim=(0, 10))
        ax.axis("equal")
        plt.draw()
        camera.snap()

    animation = camera.animate(interval=50,)
    animation.save("simple_ball.gif", writer="imagemagick")
    print("done!")


if __name__ == "__main__":
    main()
