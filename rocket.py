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
        self.vertices = []

        self.mount = Part.STACKED

        self.mass = 0
        self.radial_size = 0 # only applies to circular parts
        self.height = 0


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
        body.moment = pymunk.moment_for_poly(mass, vertices, offset)
        body.position = 450, 300

        return body, shape, body.local_to_world(com)

pod = Part()
pod.vertices = [(0, 0), (45, 90), (90, 0)]
pod.mass = 5

engine = Part()
engine.vertices = [(0, 0), (90, 0), (0, -100), (90, -100)]
engine.mass = 15

rocket = Rocket()
rocket.parts = [pod, engine]

body, shape, com = rocket.get_body_and_shape()
space.add(body, shape)

label = pyglet.text.Label("Center Of Mass",
                          font_size=8,
                          x=com[0], y=com[1],
                          anchor_x="center", anchor_y="center")
        

@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)
    label.draw()

def update(dt):
    space.step(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60.0)
    pyglet.app.run()
