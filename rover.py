import math
import sys
import random

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import DrawOptions, to_pygame

import pygame
from pygame.locals import *

from cv2 import VideoWriter, VideoWriter_fourcc

import numpy as np

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

    wheel1_b.position = pos + (-55, 0)
    wheel2_b.position = pos + (55, 0)
    wheel3_b.position = pos + (0, 90)
    chassis_b.position = pos + (0, 30)

    space.add(
        pymunk.PinJoint(wheel1_b, chassis_b, (0, 0), (-25, -15)),
        pymunk.PinJoint(wheel1_b, chassis_b, (0, 0), (-25,  15)),
        pymunk.PinJoint(wheel2_b, chassis_b, (0, 0), (25,  -15)),
        pymunk.PinJoint(wheel2_b, chassis_b, (0, 0), (25,   15)),
        pymunk.PinJoint(wheel3_b, chassis_b, (0, 0), (-25, 15)),
        pymunk.PinJoint(wheel3_b, chassis_b, (0, 0), (25, 15))
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
            screen_vertices = [to_pygame(v, screen) + scroll for v in transformed_vertices]
            pygame.draw.polygon(screen, (255, 0, 0), screen_vertices)
        elif isinstance(shape, pymunk.Segment):
            vertices = shape.a, shape.b
            transformed_vertices = [v.rotated(body.angle) + body.position for v in vertices]
            screen_vertices = [to_pygame(v, screen) + scroll for v in transformed_vertices]
            pygame.draw.line(screen, (0, 255, 0), *screen_vertices, int(shape.radius))
            

    pygame.display.flip()

    frames.append(pygame.surfarray.array3d(screen))


# write video
fourcc = VideoWriter_fourcc(*'MPEG')
video = VideoWriter("./demo.avi", fourcc, float(fps), (900, 600))

for frame in frames:
    frame.dtype = np.uint8
    video.write(frame)

video.release()