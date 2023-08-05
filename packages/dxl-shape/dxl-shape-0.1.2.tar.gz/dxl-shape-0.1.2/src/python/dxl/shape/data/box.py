from .base import Entity
from doufo.tensor import all_close, abs_, Vector, transpose
from doufo import dataclass
import numpy as np
import math
import attr


@dataclass
class Box(Entity):
    shape: Vector = attr.ib(converter=Vector)
    origin: Vector = attr.ib(converter=Vector, default=Vector([0.0, 0.0, 0.0]))
    normal: Vector = attr.ib(converter=Vector, default=Vector([0.0, 0.0, 1.0]))
    # __slots__ = ['shape', 'origin', 'normal']

    # def __init__(self,
    #              shape: Vector,
    #              origin: Vector = None,
    #              normal: Vector = None):
    #     self.shape = Vector(shape)
    #     if origin is None:
    #         origin = Vector([0.0, 0.0, 0.0])
    #     self.origin = Vector(origin)
    #     if normal is None:
    #         normal = Vector([0.0, 0.0, 1.0])
    #     self.normal = Vector(normal)

    # def rotate_on_direction(self, direction, theta):
    #     from .point import Point
    #     p_origin = Point(self.origin)
    #     p_normal = Point(self.normal)
    #     return self.replace(origin=p_origin._rotate_on_direction(direction, theta).origin,
    #                         normal=p_normal._rotate_on_direction(direction, theta).origin)

    def is_collision(self, p: 'Entity') -> bool:
        from dxl.shape.data.axis import Axis
        from dxl.shape.function.rotation.matrix import axis_to_z
        p_tran_rot = p.translate(-self.origin).origin @ transpose(
            axis_to_z(self.normal))
        if ((-self.shape.x / 2 <= p_tran_rot.x < self.shape.x / 2) and
            (-self.shape.y / 2 <= p_tran_rot.y < self.shape.y / 2) and
                (-self.shape.z / 2 <= p_tran_rot.z < self.shape.z / 2)):
            return True
        else:
            return False

    def fmap(self, f):
        return Box(self.shape, f(self.origin), f(self.normal))

    def __eq__(self, b):
        if not isinstance(b, Box):
            return False
        return all_close(self.shape, b.shape) and all_close(self.origin, b.origin) and all_close(self.normal, b.normal)



