import random
import numpy as np
from pyglet.gl import *
from pyglet import shapes


class Particles:
    def __init__(self):
        self.particles = []

    def create_particles(self, n):

        position = [random.randint(600, 680), random.randint(245, 255)]
        movement = [np.random.normal(0, 1), random.uniform(0, 3)]
        color = [255, 0, 0]
        radius = 20
        age = 0
        lifetime = random.randrange(100)
        particle_circle = [position, radius, movement, color, lifetime, age]
        self.particles.append(particle_circle)

        position = [random.randint(950, 980), random.randint(245, 255)]
        movement = [np.random.normal(0, 1), random.uniform(0, 3)]
        color = [0, 0, 255]
        radius = 20
        age = 0
        lifetime = random.randrange(100)
        particle_circle = [position, radius, movement, color, lifetime, age]
        self.particles.append(particle_circle)

    def delete_particles(self):
        if self.particles:
            particle_new = [particle for particle in self.particles if (particle[1] > 5 and particle[5] < particle[4])]
            self.particles = particle_new

    def emit_particles(self):
        if self.particles:
            for particle in self.particles:
                particle[0][0] += particle[2][0]  # x koord
                particle[0][1] += particle[2][1]  # y koord
                particle[1] -= 0.25  # radius
                if particle[3][1] < 215:  # color
                    particle[3][1] += 6
                circle = shapes.Circle(x=particle[0][0], y=particle[0][1], radius=particle[1], color=tuple(particle[3]))

                circle.draw()

    def increase_age(self):
        for particle in self.particles:
            particle[5] += 1


window = pyglet.window.Window(width=1280, height=720, caption="Particles")
particles = Particles()


def update(*args):
    pass


@window.event
def on_draw():
    glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    particles.create_particles(1)
    particles.delete_particles()
    particles.emit_particles()
    particles.increase_age()


def main():
    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.app.run()


if __name__ == '__main__':
    main()
