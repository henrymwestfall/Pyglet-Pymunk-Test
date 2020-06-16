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
mass = 1000
lander = pymunk.Body(mass)
vertices = [(0, 0), (15, 30), (30, 0)]
lander_shape = pymunk.Poly(lander, vertices)
lander.moment = pymunk.moment_for_poly(mass, vertices)
lander.position = 450, 600
lander.elasticity = 0.0
lander.friction = 0.8
space.add(lander, lander_shape)

fuel = 100
integrity = 100

# terrain
base = 20
previous = (0, random.randint(0, 500) // 10 + base)
segments = []
slope_angles = []
while previous[0] < 900:
    x = random.randint(previous[0] + 10, previous[0] + 50)
    y = 100 * math.sin(x) + 100 + base#random.randint(0, 500) // 5 + base
    diff = (x - previous[0], y - previous[1])
    angle = math.atan2(*diff)
    slope_angles.append(angle)
    shape = pymunk.Segment(space.static_body, previous, (x, y), 1)
    shape.body.elasticity = 0.0
    shape.body.friction = 1.0
    space.add(shape)
    segments.append(shape)
    previous = x, y

score_multiplier = 1#min(slope_angles) / math.pi * 0.5

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
score_label = pyglet.text.Label("Score: 0",
                                color=(255, 255, 255, 255),
                                font_size=24,
                                x=window.width // 2, y=window.height // 2,
                                anchor_x="center", anchor_y="center"
)
help_text = """
Press Left/Right to use steering thrusters and up to engage the main thruster. \n
The lander must be moving at less than 4 mps for 5 seconds in order to use the landing gear. \n
Press SPACE to begin.
"""
help_text = pyglet.text.Label(help_text,
                            color=(255, 255, 255, 255),
                            font_size=16,
                            x=window.width // 2, y=window.height // 2,
                            anchor_x="center", anchor_y="bottom",
                            multiline=True,
                            width=400
)

in_help_mode = True

landed = False
landed_time = 0

@window.event
def on_draw():
    window.clear()
    y_vel_label.draw()
    x_vel_label.draw()
    rotation_label.draw()
    fuel_label.draw()
    integrity_label.draw()
    if landed:
        score_label.draw()
    if in_help_mode:
        help_text.draw()
    space.debug_draw(options)

# history of frame length
dts = []

# keys pressed last frame
last_keys_pressed = set()

def update(dt):
    global fuel, integrity, landed, landed_time, in_help_mode

    window.push_handlers(keys)
    if in_help_mode and keys[key.SPACE]:
        in_help_mode = False

    if in_help_mode:
        return

    if fuel > 0:
        if keys[key.W]:
            lander.apply_impulse_at_local_point((0, 50 * dt))
            last_keys_pressed.add(key.W)
            fuel -= 20 * dt
        elif key.W in last_keys_pressed:
            last_keys_pressed.remove(key.W)

        if keys[key.A]:
            lander.apply_impulse_at_local_point((100 * dt, 0), (0, -10))
            last_keys_pressed.add(key.A)
            fuel -= 8 * dt
        elif key.A in last_keys_pressed:
            lander.angular_velocity = 0
            last_keys_pressed.remove(key.A)

        if keys[key.D]:
            lander.apply_impulse_at_local_point((-100 * dt, 0), (0, -10))
            last_keys_pressed.add(key.D)
            fuel -= 8 * dt
        elif key.D in last_keys_pressed:
            lander.angular_velocity = 0
            last_keys_pressed.remove(key.D)
    else:
        fuel = 0.0

    if lander.position.x > 900:
        lander.position.x = 0
    elif lander.position.x < 0:
        lander.position.x = 900

    if not landed:
        y_vel_label.text = f"Vertical Velocity:\t{round(lander.velocity.y)} mps"
        x_vel_label.text = f"Horizontal Velocity:\t{round(lander.velocity.x)} mps"
        rotation_label.text = f"Rotation: {round(math.degrees(lander.angle))} degrees, {round(lander.angle, 3)} radians"
        fuel_label.text = f"Fuel: {round(fuel, 1)}%"
        integrity_label.text = f"Lander Condition: {round(integrity, 1)}%"
    
    colliding_with_ground = False
    for seg in segments:
        if len(lander_shape.shapes_collide(seg).points) > 0:
            integrity -= lander.velocity.length * dt * 0.5
            colliding_with_ground = True
    
    if colliding_with_ground and round(lander.velocity.length) <= 4.0 and not landed:
        score = round(integrity * 1000 * score_multiplier)
        score_label.text = f"Score: {score}"
        landed_time += dt
        landed = landed_time > 5
    else:
        landed_time = 0

    if not landed:
        space.step(dt)
    dts.append(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60.0)
    pyglet.app.run()
    print(1 / (sum(dts) / len(dts)))