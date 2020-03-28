import matplotlib.pyplot as plt
import numpy as np

from objects import Canvas, Ball, HEALTHY, INFECTED, COLORS


def test_instantiate_canvas_with_balls():
    canvas = Canvas(balls=[Ball(), Ball(), Ball()])
    assert len(canvas.balls) == 3


def test_canvas_generate_random_balls():
    canvas = Canvas()
    canvas.generate_random_balls(n=20)
    assert len(canvas.balls) == 20


def test_collision_pairs():
    # test that only intersecting balls produce a collision
    canvas = Canvas(
        balls=[
            Ball(position=(0, 0)),
            Ball(position=(0.5, 0.5)),
            Ball(position=(999, 2342)),
        ]
    )
    collisions = list(canvas._get_collisions())
    assert len(collisions) == 1, (
        "there is only one collision; between ball1 and "
        "ball2. There should not be an entry for each ball "
        "e.g. ((ball1, ball2), (ball2, ball1)) "
    )

    # test that three intersecting balls produce three collisions
    canvas = Canvas(
        balls=[
            Ball(position=(0, 0)),
            Ball(position=(0.5, 0.5)),
            Ball(position=(0.3, 0.3)),
        ]
    )
    collisions = list(canvas._get_collisions())
    assert len(collisions) == 3, (
        "there are 3 balls all within collision distance of one another. This should "
        "produce 3 collision objects; ball1-ball2, ball1-ball3, ball2-ball3"
    )

    # test that two non-intersecting balls don't produce any collisions
    canvas = Canvas(balls=[Ball(position=(0, 0)), Ball(position=(99, 99))])
    collisions = list(canvas._get_collisions())
    assert len(collisions) == 0


def test_handle_collisions():
    # ball1 should end up stationary and ball2 should end up moving
    ball1 = Ball(position=(0, 0), velocity=(1, 0))
    ball2 = Ball(position=(0.5, 0), velocity=(0, 0))
    canvas = Canvas(balls=[ball1, ball2])
    canvas.handle_collisions()
    assert np.all(ball1.velocity == (0, 0))
    assert np.all(ball2.velocity == (1, 0))


def test_set_position():
    # check position is numpy.array type
    ball = Ball()
    assert np.all(ball.position == np.array([0, 0]))

    # check position tuple passed at instantiation is stored as np.array type
    ball = Ball(position=(6, 9))
    assert np.all(ball.position == np.array([6, 9]))

    # check position tuple passed after instantiation is stored as np.array type
    ball = Ball()
    ball.position = (6, 9)
    assert np.all(ball.position == np.array([6, 9]))


def test_set_x_y_u_v():
    ball = Ball(position=(6, 9))
    ball.x = 10
    assert ball.x == 10
    assert np.all(ball.position == (10, 9))

    ball = Ball(position=(6, 9))
    ball.y = 10
    assert ball.y == 10
    assert np.all(ball.position == (6, 10))

    ball = Ball(velocity=(6, 9))
    ball.u = 10
    assert ball.u == 10
    assert np.all(ball.velocity == (10, 9))

    ball = Ball(velocity=(6, 9))
    ball.v = 10
    assert ball.v == 10
    assert np.all(ball.velocity == (6, 10))

def test_health_change_changes_color():
    ball = Ball(health=HEALTHY)
    fig, ax = plt.subplots()
    artist = ball.draw(ax)
    ball.health = INFECTED
    assert ball.color == COLORS[INFECTED]
    assert artist.color == COLORS[INFECTED]