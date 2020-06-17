import math

import pymunk
from pymunk.pyglet_util import DrawOptions

import pyglet

window = pyglet.window.Window(900, 600, "Rocketry", resizable=False)
options = DrawOptions()

space = pymunk.Space()
space.gravity = 0, 0


class Part:
    STACKED = 0
    RADIAL = 1

    def __init__(self, space, body, shape):
        self.body = body
        self.shape = shape
        self.space = space
        self.space.add(self.body, self.shape)
        self.joints = []

        self.mount = Part.STACKED

        self.radial_size = 0 # only applies to circular parts
        self.height = 0

        # neighbor Parts
        self.part_below = (None, [])
        self.part_above = (None, [])
        self.mounted_parts = set()

    def connect_to(self, other):
        """
        Connect the parts (only works for certain stacked parts currently)
        """

        if self.mount == Part.STACKED:
            left_joint = pymunk.PinJoint(self.body, other.body, anchor_a=(self.radial_size, 0))
            right_joint = pymunk.PinJoint(self.body, other.body, anchor_b=(other.radial_size, 0))
            joints = [left_joint, right_joint]
            self.space.add(*joints)

            self.joints += joints

            if (other.part_above[0] != self) or (other.part_below[0] != self):
                other.joints += [left_joint, right_joint]
                if self.body.position.y > other.body.position.y: # we are above them
                    for j in joints:
                        j.distance = math.hypot(self.height, self.radial_size)
                    other.part_above = (self, joints)
                    self.part_below = (other, joints)
                else:
                    for j in joints:
                        j.distance = math.hypot(other.height, other.radial_size)
                    other.part_below = (self, joints)
                    self.part_above = (other, joints)

    def disconnect_from(self, other):
        joints = None
        if other is self.part_above:
            joints = self.part_above[1]
            self.part_above = (None, [])
            other.part_below = (None, [])
        elif other is self.part_below:
            joints = self.part_below[1]
            self.part_below = (None, [])
            other.part_above = (None, [])
        
        if not (joints is None):
            for j in joints:
                other.joints.remove(j)
                self.joints.remove(j)
                self.space.remove(j)


# pod part
mass = 10000
pod = pymunk.Body(mass)
vertices = [(0, 0), (45, 90), (90, 0)]
shape = pymunk.Poly(pod, vertices)
pod.moment = pymunk.moment_for_poly(mass, vertices)
pod.position = 450, 300
pod_part = Part(space, pod, shape)
pod_part.radial_size = 90

# random box part
mass = 10
box = pymunk.Body(mass)
vertices = [(0, 0), (90, 0), (90, 30), (0, 30)]
shape = pymunk.Poly(box, vertices)
box.moment = pymunk.moment_for_poly(mass, shape.get_vertices())
box.position = 450, 270
box_part = Part(space, box, shape)
box_part.radial_size = 90
box_part.height = 30

pod_part.connect_to(box_part)

@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)

def update(dt):
    space.step(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0 / 60.0)
    pyglet.app.run()