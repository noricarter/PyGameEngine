# Planet is just an object in the world. No drawing here; appearance only.

from components.physics_body import PhysicsBody

class Planet:
    def __init__(self, x, y, radius=40, color=(0, 120, 255), mass=5000, static=True):
        self.body = PhysicsBody(x, y, mass=mass, radius=radius)
        self.appearance = {"type": "circle", "color": color}
        self.static = static

    @property
    def x(self): return self.body.x
    @x.setter
    def x(self, v): self.body.x = v

    @property
    def y(self): return self.body.y
    @y.setter
    def y(self, v): self.body.y = v

    @property
    def vx(self): return self.body.vx
    @vx.setter
    def vx(self, v): self.body.vx = v

    @property
    def vy(self): return self.body.vy
    @vy.setter
    def vy(self, v): self.body.vy = v

    @property
    def mass(self): return self.body.mass

    @property
    def radius(self): return self.body.radius
