import math
import sys
import random

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import DrawOptions, to_pygame

import pygame
from pygame.locals import *

import numpy as np

def create_pogo(space, x, y):
    pos = Vec2d(x, y)

    # carriage
    mass = 100
    size = (50, 30)
    moment = pymunk.moment_for_box(mass, size)
    carriage_b = pymunk.Body(mass, moment)
    carriage_s = pymunk.Poly.create_box(carriage_b, size)
    carriage_s.color = 255, 0, 0
    carriage_s.friction = 0.4
    space.add(carriage_b, carriage_s)
    sprites.append((carriage_b, carriage_s))

    carriage_b.position = pos

def create_pogo1(space, x, y):
    pos = Vec2d(x, y)

    # carriage
    mass = 100
    size = (50, 30)
    moment = pymunk.moment_for_box(mass, size)
    carriage_b = pymunk.Body(mass, moment)
    carriage_s = pymunk.Poly.create_box(carriage_b, size)
    carriage_s.color = 255, 0, 0
    space.add(carriage_b, carriage_s)
    sprites.append((carriage_b, carriage_s))

    # left leg
    mass = 20
    left_leg_b = pymunk.Body(mass)
    size = (10, 100)
    left_leg_s = pymunk.Poly.create_box(left_leg_b, size)
    left_leg_s.color = 255, 0, 0
    space.add(left_leg_b, left_leg_s)
    sprites.append((left_leg_b, left_leg_s))


    # right leg
    mass = 20
    right_leg_b = pymunk.Body(mass)
    size = (10, 100)
    right_leg_s = pymunk.Poly.create_box(right_leg_b, size)
    right_leg_s.color = 255, 0, 0
    space.add(right_leg_b, right_leg_s)
    sprites.append((right_leg_b, right_leg_s))

    # left wheel
    mass = 10
    radius = 10
    moment = pymunk.moment_for_circle(mass, 0, radius)
    wheel1_b = pymunk.Body(mass, moment)
    wheel1_s = pymunk.Circle(wheel1_b, radius)
    wheel1_s.friction = 1.0
    wheel1_s.color = 0, 0, 0
    space.add(wheel1_b, wheel1_s)
    sprites.append((wheel1_b, wheel1_s))

    # right wheel
    mass = 10
    radius = 10
    moment = pymunk.moment_for_circle(mass, 0, radius)
    wheel2_b = pymunk.Body(mass, moment)
    wheel2_s = pymunk.Circle(wheel2_b, radius)
    wheel2_s.friction = 1.0
    wheel2_s.color = 0, 0, 0
    space.add(wheel2_b, wheel2_s)
    sprites.append((wheel2_b, wheel2_s))

    # stick
    mass = 20
    size = (40, 150)
    stick_b = pymunk.Body(mass)
    stick_s = pymunk.Poly.create_box(stick_b, size)
    stick_s.color = 0, 0, 255
    space.add(stick_b, stick_s)
    sprites.append((stick_b, stick_s))

    carriage_b.position = pos + (0, 100)
    left_leg_b.position = pos + (-25, 50)
    right_leg_b.position = pos + (25, 50)
    wheel1_b.position = pos + (-25, -50)
    wheel2_b.position = pos + (25, -50)
    stick_b.position = pos + (0, -50)

    space.add([
        pymunk.PinJoint(carriage_b, left_leg_b, (0, 0), (0, 100)),
        pymunk.PinJoint(carriage_b, left_leg_b, (25, 0), (0, 100)),

        pymunk.PinJoint(carriage_b, right_leg_b, (0, 0), (0, 100)),
        pymunk.PinJoint(carriage_b, right_leg_b, (25, 0), (0, 100)),

        pymunk.PinJoint(left_leg_b, wheel1_b, (5, 0), (0, 0)),
        pymunk.PinJoint(right_leg_b, wheel2_b, (5, 0), (0, 0))
    ])

    return carriage_b


def create_rover(space, x, y):
    pos = Vec2d(x, y)

    wheel_color = 0, 0, 0

    # first wheel
    mass = 10
    radius = 25
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel1_b = pymunk.Body(mass, moment)
    wheel1_s = pymunk.Circle(wheel1_b, radius)
    wheel1_s.friction = 1.5
    wheel1_s.color = wheel_color
    space.add(wheel1_b, wheel1_s)
    sprites.append((wheel1_b, wheel1_s))

    # second wheel
    mass = 10
    radius = 25
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel2_b = pymunk.Body(mass, moment)
    wheel2_s = pymunk.Circle(wheel2_b, radius)
    wheel2_s.friction = 1.5
    wheel2_s.color = wheel_color
    space.add(wheel2_b, wheel2_s)
    sprites.append((wheel2_b, wheel2_s))

    # third wheel
    mass = 10
    radius = 25
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel3_b = pymunk.Body(mass, moment)
    wheel3_s = pymunk.Circle(wheel3_b, radius)
    wheel3_s.friction = 1.5
    wheel3_s.color = wheel_color
    space.add(wheel3_b, wheel3_s)
    sprites.append((wheel3_b, wheel3_s))

    # chassis
    mass = 100
    size = (50, 30)
    moment = pymunk.moment_for_box(mass, size)
    chassis_b = pymunk.Body(mass, moment)
    chassis_s = pymunk.Poly.create_box(chassis_b, size)
    space.add(chassis_b, chassis_s)
    sprites.append((chassis_b, chassis_s))

    # plow
    mass = 50
    vertices = [(0, 0), (0, 50), (25, 0)]
    moment = pymunk.moment_for_poly(mass, vertices)
    plow_b = pymunk.Body(mass, moment)
    plow_s = pymunk.Poly(plow_b, vertices)
    space.add(plow_b, plow_s)
    sprites.append((plow_b, plow_s))

    wheel1_b.position = pos + (-55, 0)
    wheel2_b.position = pos + (55, 0)
    wheel3_b.position = pos + (0, 90)
    chassis_b.position = pos + (0, 30)
    plow_b.position = pos + (95, -20)

    space.add(
        pymunk.PinJoint(wheel1_b, chassis_b, (0, 0), (-25, -15)),
        pymunk.PinJoint(wheel1_b, chassis_b, (0, 0), (-25,  15)),
        pymunk.PinJoint(wheel2_b, chassis_b, (0, 0), (25,  -15)),
        pymunk.PinJoint(wheel2_b, chassis_b, (0, 0), (25,   15)),
        pymunk.PinJoint(wheel3_b, chassis_b, (0, 0), (-25, 15)),
        pymunk.PinJoint(wheel3_b, chassis_b, (0, 0), (25, 15)),
        pymunk.PinJoint(chassis_b, plow_b, (25, 25), (0, 50)),
        pymunk.PinJoint(wheel2_b, plow_b, (0, 0), (0, 0)),
        pymunk.PinJoint(wheel2_b, plow_b, (0, 0), (0, 50))
    )

    speed = 0
    motors = [
        pymunk.SimpleMotor(wheel1_b, chassis_b, speed),
        pymunk.SimpleMotor(wheel2_b, chassis_b, speed),
        pymunk.SimpleMotor(wheel3_b, chassis_b, speed)
    ]
    space.add(*motors)
    return motors, chassis_b

fps = 60
pygame.init()
screen = pygame.display.set_mode((900, 600))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

draw_options = DrawOptions(screen)

space = pymunk.Space()
space.gravity = 0, -1000

sprites = []

previous = (-100, 100)

while previous[0] < 9000:
    x = previous[0] + random.randint(100, 500)
    y = previous[1] + random.randint(-100, 100)

    floor = pymunk.Segment(space.static_body, previous, (x, y), 5)
    floor.friction = 1.0
    space.add(floor)
    sprites.append((floor.body, floor))

    previous = (x, y)

pog_car = create_pogo(space, 400, 600)
create_pogo(space, 400, 500)
create_pogo(space, 400, 700)

motors, car = create_rover(space, 200, 600)
acc = 8
dec = 8
max_speed = 20
motor_speed = 0

scroll = Vec2d(0, 0)

t = 0

frames = []

running = True
while running:
    dt = clock.tick(fps) * 0.001
    t += dt

    for evt in pygame.event.get():
        if evt.type == QUIT:
            pygame.quit()
            running = False
    
    if not running:
        break

    keys = pygame.key.get_pressed()
    if keys[K_d]:
        motor_speed -= acc * dt
        motor_speed = max(motor_speed, -max_speed)
    elif keys[K_a]:
        motor_speed += acc * dt
        motor_speed = min(motor_speed, max_speed)
    else:
        sign = math.copysign(1, motor_speed)
        motor_speed += (dec * dt) * -sign
        if math.copysign(1, motor_speed) != sign:
            motor_speed = 0

    for m in motors:
        m.rate = motor_speed

    space.step(dt)
    scroll = Vec2d(screen_rect.center) - to_pygame(car.position, screen)

    screen.fill(pygame.color.THECOLORS["white"])
    
    for body, shape in sprites:
        if isinstance(shape, pymunk.Circle):
            screen_center = to_pygame(body.position, screen) + scroll
            pygame.draw.circle(screen, (0, 0, 0), screen_center, shape.radius)
            edge = to_pygame(body.position + Vec2d(shape.radius, 0).rotated(body.angle), screen) + scroll
            pygame.draw.line(screen, (255, 255, 255), screen_center, edge)
        elif isinstance(shape, pymunk.Poly):
            vertices = shape.get_vertices()
            transformed_vertices = [v.rotated(body.angle) + body.position for v in vertices]
            try:
                screen_vertices = [to_pygame(v, screen) + scroll for v in transformed_vertices]
            except Exception as e:
                print(body.angle)
                print(vertices)
                print(transformed_vertices)
                raise e
            pygame.draw.polygon(screen, (255, 0, 0), screen_vertices)
        elif isinstance(shape, pymunk.Segment):
            vertices = shape.a, shape.b
            transformed_vertices = [v.rotated(body.angle) + body.position for v in vertices]
            screen_vertices = [to_pygame(v, screen) + scroll for v in transformed_vertices]
            pygame.draw.line(screen, (0, 255, 0), *screen_vertices, int(shape.radius))
    # space.debug_draw(draw_options)

    pygame.display.flip()
