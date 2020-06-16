import time

import pymunk
from pymunk.pyglet_util import DrawOptions

import pyglet

from engine.body import Group, Body, Circle, Segment

window = pyglet.window.Window(900, 600, "Pymunk Tester", resizable=False)
options = DrawOptions()

space = pymunk.Space()
space.gravity = 0, -1000

circles = Group()
circles.add_all([
    Circle(450, 400, 30, 2),
    Circle(452, 300, 30)
])
circles.set_attribute("elasticity", 0.98)
circles.set_attribute("friction", 1.0)
circles.add_to_space(space)

segments = Group()
segments.add_all([
    Segment((50, 50), (850, 50), 2, body_type=Body.STATIC),
    Segment((50, 550), (50, 50), 2, body_type=Body.STATIC),
    Segment((50, 550), (850, 550), 2, body_type=Body.STATIC),
    Segment((850, 550), (850, 50), 2, body_type=Body.STATIC)
])
segments.set_attribute("elasticity", 0.98)
segments.set_attribute("friction", 1.0)
segments.add_to_space(space)


@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)

def update(dt):
    space.step(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60.0)
    pyglet.app.run()