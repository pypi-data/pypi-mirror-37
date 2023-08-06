import random


class Color(object):
    BLACK = '000000'
    RED = 'FF0000'


class Particle(object):
    def __init__(self, rx: float=None, ry: float=None, vx: float=None, vy: float=None, radius: float=None,
                 mass: float=None, color: Color=None):
        self.vx = vx if vx else random.uniform(-0.005, 0.005)
        self.vy = vy if vy else random.uniform(-0.005, 0.005)
        self.rx = rx if rx else random.uniform(0.0, 1.0)
        self.ry = ry if ry else random.uniform(0.0, 1.0)
        self.radius = radius if radius else 0.01
        self.mass = mass if mass else 0.5
        self.color = color if color else Color.BLACK

    def move(self, dt: float) -> None:
        self.rx += self.vx * dt
        self.ry += self.vy * dt

    def draw(self) -> None:
        pass

