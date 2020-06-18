import math

import pymunk
from pymunk.pyglet_util import DrawOptions
from pymunk.vec2d import Vec2d

import pyglet

window = pyglet.window.Window(900, 600, "Rocketry", resizable=False)
options = DrawOptions()

space = pymunk.Space()
space.gravity = 0, 0

def centroid(vertices, weights=None):
    num = len(vertices)
    if weights is None:
        weights = [1 / num] * num
    
    xsum = 0
    ysum = 0
    for i, v in enumerate(vertices):
        xsum += v[0] * weights[i]
        ysum += v[1] * weights[i]
    
    return (xsum, ysum)


class Part:
    STACKED = 0
    RADIAL = 1

    def __init__(self):
        self.vertices = [(0, 0)]

        self.mount = Part.STACKED

        self.mass = 0
        self.radial_size = 0 # only applies to circular parts
        self.height = 0

        self.impact_tolerance = 0 # mps
        self.heat_tolerance = 0

    def move_to(self, x, y):
        self.vertices = [(v[0] + x, v[1] + y) for v in self.vertices]


class Engine(Part):
    def __init__(self):
        super().__init__()

        self.radial_size = 90
        self.height = 180

        self.mass = 150
        self.burn = 8.8
        self.burning = False
        self.atm_thrust = 162.91
        self.vac_thrust = 192.0

    def engage(self):
        self.burning = True

    def get_impulse(self, dt):
        if self.burning:
            self.burn -= dt
            bottom_left = self.vertices[0]
            impulse_x = bottom_left[0] + self.radial_size // 2
            impulse_y = bottom_left[1] - self.height // 2
            return (impulse_x, impulse_y, self.atm_thrust)
        else:
            return (0, 0, 0)


class Rocket:
    def __init__(self):
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)

    def get_body_and_shape(self):
        # compile part data
        vertices = []
        mass = 0
        centroids_map = {}
        for p in self.parts:
            vertices += p.vertices
            mass += p.mass
            centroids_map[centroid(p.vertices)] = p.mass

        # calculate center of mass
        weighted_centroids_map = {c: m / mass for c, m in centroids_map.items()}
        centroids = list(weighted_centroids_map.keys())
        weights = [weighted_centroids_map[c] for c in centroids]
        com = centroid(centroids, weights)

        # calculate offset
        vertices = list(set(vertices))
        center = centroid(vertices)
        offset = Vec2d(center) - Vec2d(com)

        # create body
        body = pymunk.Body(mass)
        shape = pymunk.Poly(body, vertices)
        body.moment = pymunk.moment_for_poly(mass, vertices)
        body.center_of_gravity = com
        body.position = 450, 300

        return body, shape, body.local_to_world(com)

pod = Part()
pod.vertices = [(0, 0), (45, 90), (90, 0)]
pod.mass = 10

engine = Engine()
engine.vertices = [(0, 0), (0, -engine.height), (engine.radial_size, -engine.height), (engine.radial_size, 0)]
engine.engage()

rocket = Rocket()
rocket.parts = [pod, engine]

body, shape, com = rocket.get_body_and_shape()
space.add(body, shape)

label = pyglet.text.Label("Center Of Mass",
                          font_size=8,
                          x=com[0], y=com[1],
                          anchor_x="center", anchor_y="center")
x, y = body.local_to_world((45, 90))
label2 = pyglet.text.Label("(45, 90)",
                          font_size=8,
                          x=x, y=y,
                          anchor_x="center", anchor_y="center")
        

@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)
    label.draw()
    label2.draw()

def update(dt):
    global label2

    impulse_x, impulse_y, impulse_amount = engine.get_impulse(dt)
    x, y = body.local_to_world((impulse_x, impulse_y))
    label2 = pyglet.text.Label("Impulse",
                          font_size=8,
                          x=x, y=y,
                          anchor_x="center", anchor_y="center")

    impulse_x, impulse_y, impulse_amount = engine.get_impulse(dt)
    body.apply_impulse_at_local_point((0, impulse_amount), (impulse_x, impulse_y))
    space.step(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60.0)
    pyglet.app.run()
