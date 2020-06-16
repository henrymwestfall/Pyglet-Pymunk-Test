import random
import math

import pymunk
from pymunk.pyglet_util import DrawOptions

import pyglet
from pyglet.window import key

from engine.body import Group, Body, Circle, Segment

window = pyglet.window.Window(900, 600, "Pymunk Tester", resizable=False)
keys = key.KeyStateHandler()
options = DrawOptions()

space = pymunk.Space()
space.gravity = 0, -5

# lander
mass = 1
lander = pymunk.Body(mass)
vertices = [(0, 0), (15, 30), (30, 0)]
lander_shape = pymunk.Poly(lander, vertices)
lander.moment = pymunk.moment_for_poly(mass, vertices)
lander.position = 450, 600
lander.elasticity = 0.1
lander.friction = 0.8
space.add(lander, lander_shape)

fuel = 100
integrity = 100

# terrain
base = 20
previous = (0, random.randint(0, 500) // 10 + base)
segments = []
while previous[0] < 900:
    x = random.randint(previous[0] + 10, previous[0] + 50)
    y = 100 * math.sin(x) + 100 + base#random.randint(0, 500) // 5 + base
    diff = (x - previous[0], y - previous[1])
    shape = pymunk.Segment(space.static_body, previous, (x, y), 3)
    shape.body.elasticity = 0.1
    shape.body.friction = 10.0
    space.add(shape)
    segments.append(shape)
    previous = x, y

# labels
y_vel_label = pyglet.text.Label("Vertical Velocity: 0 mps",
                                color=(255, 255, 255, 255),
                                font_size=10,
                                x=8, y=592,
                                anchor_x='left', anchor_y='top'
)
x_vel_label = pyglet.text.Label("Horizontal Velocity: 0 mps",
                                color=(255, 255, 255, 255),
                                font_size=10,
                                x=8, y=572,
                                anchor_x='left', anchor_y='top'
)
rotation_label = pyglet.text.Label("Rotation: 0 degrees, 0 radians",
                                color=(255, 255, 255, 255),
                                font_size=10,
                                x=8, y=552,
                                anchor_x='left', anchor_y='top'
)
fuel_label = pyglet.text.Label("Fuel: 100%",
                                color=(255, 255, 255, 255),
                                font_size=10,
                                x=8, y=532,
                                anchor_x='left', anchor_y='top'
)
integrity_label = pyglet.text.Label("Lander Integrity: 100%",
                                color=(255, 255, 255, 255),
                                font_size=10,
                                x=8, y=512,
                                anchor_x='left', anchor_y='top'
)

@window.event
def on_draw():
    window.clear()
    y_vel_label.draw()
    x_vel_label.draw()
    rotation_label.draw()
    fuel_label.draw()
    integrity_label.draw()
    space.debug_draw(options)

# history of frame length
dts = []

# keys pressed last frame
last_keys_pressed = set()

def update(dt):
    global fuel, integrity

    window.push_handlers(keys)
    if fuel > 0:
        if keys[key.W]:
            lander.apply_impulse_at_local_point((0, 50 * dt))
            last_keys_pressed.add(key.W)
            fuel -= 10 * dt
        elif key.W in last_keys_pressed:
            last_keys_pressed.remove(key.W)

        if keys[key.A]:
            lander.apply_impulse_at_local_point((100 * dt, 0), (0, -10))
            last_keys_pressed.add(key.A)
            fuel -= 4 * dt
        elif key.A in last_keys_pressed:
            lander.angular_velocity = 0
            last_keys_pressed.remove(key.A)

        if keys[key.D]:
            lander.apply_impulse_at_local_point((-100 * dt, 0), (0, -10))
            last_keys_pressed.add(key.D)
            fuel -= 4 * dt
        elif key.D in last_keys_pressed:
            lander.angular_velocity = 0
            last_keys_pressed.remove(key.D)
    else:
        fuel = 0.0

    if lander.position.x > 900:
        lander.position.x = 0
    elif lander.position.x < 0:
        lander.position.x = 900

    y_vel_label.text = f"Vertical Velocity:\t{round(lander.velocity.y)} mps"
    x_vel_label.text = f"Horizontal Velocity:\t{round(lander.velocity.x)} mps"
    rotation_label.text = f"Rotation: {round(math.degrees(lander.angle))} degrees, {round(lander.angle, 3)} radians"
    fuel_label.text = f"Fuel: {round(fuel, 1)}%"
    integrity_label.text = f"Lander Condition: {round(integrity, 1)}%"
    

    for seg in segments:
        if len(lander_shape.shapes_collide(seg).points) > 0:
            integrity -= lander.velocity.length * dt

    space.step(dt)
    dts.append(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60.0)
    pyglet.app.run()
    print(1 / (sum(dts) / len(dts)))