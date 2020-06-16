import pymunk # physics engine
from pymunk.vec2d import Vec2d
import pyglet # graphics engine


# group
class Group(object):
    def __init__(self):
        self.children = []
    
    def add(self, child):
        if not (child in self.children) and isinstance(child, Body):
            self.children.append(child)

    def add_all(self, children):
        for child in children:
            self.add(child)

    def set_attribute(self, attribute, value):
        for child in self.children:
            if hasattr(child, attribute):
                setattr(child, attribute, value)

    def add_to_space(self, space):
        for child in self.children:
            child.add_to_space(space)


# bodies
class Body(object):
    DYNAMIC = pymunk.Body.DYNAMIC
    KINEMATIC = pymunk.Body.KINEMATIC
    STATIC = pymunk.Body.STATIC
    
    def __init__(self, x, y, mass, body_type):
        self.mass = mass

        self.body_type = body_type
        self.body = pymunk.Body(self.mass, 0, body_type=self.body_type)

        self.body.position = x, y

    def add_to_space(self, space):
        space.add(*self.add_properties)

    @property
    def x(self):
        return self.body.position.x

    @x.setter
    def x(self, x):
        self.body.position.x = x

    @property
    def y(self):
        return self.body.position.y

    @y.setter
    def y(self, y):
        self.body.position.y = y

    @property
    def moment(self):
        return self.body.moment

    @moment.setter
    def moment(self, moment):
        if self.body_type != Body.STATIC:
            self.body.moment = moment

    @property
    def position(self):
        return self.body.position

    @position.setter
    def position(self, position):
        self.body.position = position

    @property
    def friction(self):
        return self.shape.friction

    @friction.setter
    def friction(self, friction):
        self.shape.friction = friction

    @property
    def elasticity(self):
        return self.shape.elasticity

    @elasticity.setter
    def elasticity(self, elasticity):
        self.shape.elasticity = elasticity
    

class Circle(Body):
    def __init__(self, x, y, radius, mass=1, moment="default", body_type=Body.DYNAMIC):
        super().__init__(x, y, mass, body_type)

        self.radius = radius

        if moment == "default":
            # TODO: handle inner radius
            moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        else:
            moment = moment
            try:
                float(self.moment)
            except ValueError:
                raise ValueError("explicitely defined moment must be castable to float")

        self.moment = moment
        self.shape = pymunk.Circle(self.body, self.radius)

        self.add_properties = (self.body, self.shape)


class Rectangle(Body):
    def __init__(self, x, y, width, height, mass=1, moment="default", body_type=Body.DYNAMIC):
        super().__init__(x, y, mass, body_type)

        vertices = ((x, y), (x + width, y), (x, y + height), (x + width, y + height))

        self.__width = width
        self.__height = height

        if moment == "default":
            moment = pymunk.moment_for_poly(self.mass, vertices)
        else:
            moment = moment
            try:
                float(self.moment)
            except ValueError:
                raise ValueError("explicitely defined moment must be castable to float")

        self.moment = moment
        self.shape = pymunk.Poly(self.body, vertices)

        self.add_properties = (self.body, self.shape)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height


class Segment(Body):
    def __init__(self, a, b, thickness=1, mass=1, moment="default", body_type=Body.DYNAMIC):
        super().__init__(*a, mass, body_type)

        self.__thickness = thickness

        diff = Vec2d(b) - Vec2d(a)

        if moment == "default":
            moment = pymunk.moment_for_segment(self.mass, (0, 0), diff, self.thickness)
        else:
            moment = moment
            try:
                float(self.moment)
            except ValueError:
                raise ValueError("explicitely defined moment must be castable to float")

        self.moment = moment
        self.shape = pymunk.Segment(self.body, (0, 0), diff, self.radius)

        self.add_properties = (self.body, self.shape)

    @property
    def radius(self):
        return self.__thickness

    @property
    def thickness(self):
        return self.__thickness