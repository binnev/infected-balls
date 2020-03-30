from math import sqrt
from random import random

import numpy as np
from matplotlib.patches import Circle

from conf import HEALTHY, INFECTED, RECOVERED, COLORS, DEFAULT_SPEED, INFECTION_DURATION


class Ball:
    _health = None

    def __init__(
        self,
        position=None,
        velocity=None,
        radius=0.1,
        mass=None,
        boundaries=None,
        health=HEALTHY,
        styles=None,
    ):
        self._time_infected = None

        self.position = position if position else [0, 0]
        self.velocity = velocity if velocity else [0, 0]
        self.radius = radius
        self.mass = mass if mass else radius**2
        if not styles:
            styles = {"fill": True}
        self.styles = styles
        self.boundaries = boundaries
        self.artist = None
        self.health = health

    def __str__(self):
        return (f"{self.health} ball @ position {self.position} with velocity"
                f" {self.velocity}")

    def update_artist(self):
        if self.artist:
            self.artist.center = self.x, self.y
            self.artist.radius = self.radius

    def update(self):
        # reflect balls off walls
        if (self.x + self.radius > self.boundaries["right"] and
                self.u > 0) or (self.x - self.radius < self.boundaries["left"]
                                and self.u < 0):
            self.u *= -1
        if (self.y + self.radius > self.boundaries["top"] and self.v > 0) or (
                self.y - self.radius < self.boundaries["bottom"]
                and self.v < 0):
            self.v *= -1

        self.position = self.position + self.velocity
        self.update_artist()

        # update infection
        if self._time_infected:  # recover?
            if self._time_infected > INFECTION_DURATION:
                self.health = RECOVERED
            else:  # or increment infection timer
                self._time_infected += 1

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, new_value):
        self._health = new_value
        if self.artist:
            self.artist.set_color(self.color)

        # start the timer for infection
        if new_value == INFECTED and self._time_infected is None:
            self._time_infected = 1

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = np.array(new_position, dtype=float)

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, new_velocity):
        self._velocity = np.array(new_velocity, dtype=float)

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position[0] = value

    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position[1] = value

    @property
    def u(self):
        return self.velocity[0]

    @u.setter
    def u(self, value):
        self.velocity[0] = value

    @property
    def v(self):
        return self.velocity[1]

    @v.setter
    def v(self, value):
        self.velocity[1] = value

    @property
    def color(self):
        return COLORS[self.health]

    def draw(self, ax):
        circle = Circle(xy=self.position,
                        radius=self.radius,
                        color=self.color,
                        **self.styles)
        self.artist = ax.add_patch(circle)
        return circle


class SensibleBall(Ball):
    def update(self):
        if self.health == INFECTED:
            self.velocity = (0, 0)
        super().update()


class IrresponsibleBall(Ball):
    size_increase = 4

    # double in size when infected
    def update(self):
        if self._time_infected == 1:
            self.radius *= self.size_increase

        super().update()

    # shrink again when recovered
    @Ball.health.setter
    def health(self, new_value):
        # this works because Ball now has a default _health = None, so this setter isn't
        # trying to access a nonexistent self._health property the first time it is called.
        if self.health == INFECTED and new_value == RECOVERED:
            self.radius /= self.size_increase
        Ball.health.fset(self, new_value)  # fset is the parent class setter function


class Canvas:
    def __init__(
        self,
        balls=None,
        boundaries=None,
        styles=None,
    ):
        self.boundaries = boundaries
        self.balls = []
        if balls:
            for ball in balls:
                self.add_balls(ball)

    def add_balls(self, *balls):
        for ball in balls:
            self.balls.append(ball)
            if not ball.boundaries:
                ball.boundaries = self.boundaries

    def pop_ball(self, ball):
        return self.balls.pop(ball)

    def update_balls_position(self):
        for ball in self.balls:
            ball.update()

    def draw_balls(self, ax):
        return [ball.draw(ax) for ball in self.balls]

    @classmethod
    def distance(cls, ball1, ball2):
        return sqrt((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2)

    @classmethod
    def collision(cls, ball1, ball2):
        # if the distance between the balls is less than or equal to the sum of the radii
        return cls.distance(ball1, ball2) <= ball1.radius + ball2.radius

    def generate_random_balls(
        self,
        n=10,
        x_range=None,
        y_range=None,
        speed=None,
        ball_class=None,
        ball_kwargs=None,
    ):
        x_range = x_range if x_range else (self.boundaries["left"],
                                           self.boundaries["right"])
        y_range = y_range if y_range else (self.boundaries["bottom"],
                                           self.boundaries["top"])
        ball_kwargs = ball_kwargs if ball_kwargs else dict()
        ball_class = ball_class if ball_class else Ball
        speed = DEFAULT_SPEED if speed is None else speed
        angle = random() * 2 * np.pi
        u = speed * np.cos(angle)
        v = speed * np.sin(angle)
        x_width = x_range[1] - x_range[0]
        y_width = y_range[1] - y_range[0]
        for ii in range(n):
            self.add_balls(
                ball_class(
                    position=(x_range[0] + random() * x_width,
                              y_range[0] + random() * y_width),
                    velocity=(u, v),
                    **ball_kwargs,
                ))

    def _get_collisions(self):
        collisions = []
        for ball1 in self.balls:
            for ball2 in self.balls:
                if (ball1 == ball2  # ignore balls "colliding" with themselves
                        # ignore collisions that we've already found
                        or [ball1, ball2] in collisions or [ball2, ball1
                                                            ] in collisions):
                    continue
                if self.collision(ball1, ball2):
                    collisions.append([ball1, ball2])
        return collisions

    def _handle_collision(self, collision):
        ball1, ball2 = collision
        mass1, mass2 = ball1.mass, ball2.mass
        total_mass = mass1 + mass2
        position1, position2 = ball1.position, ball2.position
        velocity1, velocity2 = ball1.velocity, ball2.velocity
        d = np.linalg.norm(position1 - position2)**2

        # update velocities
        ball1.velocity = velocity1 - 2 * mass2 / total_mass * np.dot(
            velocity1 - velocity2,
            position1 - position2) / d * (position1 - position2)

        ball2.velocity = velocity2 - 2 * mass1 / total_mass * np.dot(
            velocity2 - velocity1,
            position2 - position1) / d * (position2 - position1)

        ## stop balls clipping through each other
        # find the unit vector that passes through their centers
        delta_p = ball2.position - ball1.position
        while self.collision(ball1, ball2):  # while they're overlapping
            # move each of them away from one another along that vector
            ball2.position += delta_p / 100
            ball1.position -= delta_p / 100

    def handle_collisions(self):
        for collision in self._get_collisions():
            self._handle_collision(collision)

    def handle_infections(self):
        for collision in self._get_collisions():
            self._handle_infection(collision)

    def _handle_infection(self, collision):
        ball1, ball2 = collision
        health_states = {ball.health for ball in collision}
        if health_states == {INFECTED, HEALTHY}:
            # if an infected person collides with a healthy person, the healthy person
            # becomes infected.
            healthy_person = [
                ball for ball in collision if ball.health == HEALTHY
            ].pop()
            healthy_person.health = INFECTED

    @property
    def population(self):
        return len(self.balls)

    @property
    def population_health(self):
        output = {HEALTHY: 0, INFECTED: 0, RECOVERED: 0}
        for ball in self.balls:
            output[ball.health] += 1
        return output

    @property
    def population_health_percentages(self):
        output = self.population_health
        output = {
            health: count / self.population * 100
            for health, count in output.items()
        }
        return output


class PopulationHealth():
    def __init__(self):
        self.data = {
            HEALTHY: [],
            INFECTED: [],
            RECOVERED: [],
        }

    def append(self, new_data):
        for key, value in new_data.items():
            self.data[key].append(value)

    @property
    def healthy(self):
        return self.data[HEALTHY]

    @property
    def infected(self):
        return self.data[INFECTED]

    @property
    def recovered(self):
        return self.data[RECOVERED]
