from components.physics_body import PhysicsBody

class Player:
    def __init__(self, x, y, controller, color=(255, 255, 0), radius =10, mass=1.0):
        self.controller = controller
        self.body = PhysicsBody(x, y, mass, radius)
        self.appearance = {"type": "circle", "color": color}
        self.move_speed = 3.0

    # forwarders so World/Camera/Physics can use a uniform interface
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

    def update(self, dt):
        self.thrust = 0.1  # tweak for feel

        # Apply thrust based on controller
        if self.controller.up:
            self.vy -= self.thrust
        if self.controller.down:
            self.vy += self.thrust
        if self.controller.left:
            self.vx -= self.thrust
        if self.controller.right:
            self.vx += self.thrust

        # Brake (hold either shift)
        if getattr(self.controller, "shift", 0):
            self.vx *= 0.92
            self.vy *= 0.92