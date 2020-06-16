import random

import pymunk
from pymunk.pyglet_util import DrawOptions

import pyglet
from pyglet.window import key

from engine.body import Group, Body, Circle, Segment

window = pyglet.window.Window(900, 600, "Pymunk Tester", resizable=False)
keys = key.KeyStateHandler()
options = DrawOptions()

space = pymunk.Space()
space.gravity = 0, -100

# lander
mass = 1
body = pymunk.Body(mass)
vertices = [(0, 0), (15, 25), (30, 0)]
shape = pymunk.Poly(body, vertices)
body.moment = pymunk.moment_for_poly(mass, vertices)
body.position = 450, 300
space.add(body, shape)

# terrain
base = 20
previous = (0, random.randint(0, 500) // 10 + base)
while previous[0] < 900:
    x = random.randint(previous[0] + 100, previous[0] + 200)
    y = random.randint(0, 500) // 5 + base
    diff = (x - previous[0], y - previous[1])
    shape = pymunk.Segment(space.static_body, previous, (x, y), 3)
    space.add(shape)
    previous = x, y


@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)

dts = []

def update(dt):
    window.push_handlers(keys)
    space.step(dt)
    dts.append(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60.0)
    pyglet.app.run()
    print(1 / (sum(dts) / len(dts)))