class Player:
    def __init__(self, world_x, world_y, radius=10):
        self.world_x = world_x
        self.world_y = world_y
        self.radius = radius
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.is_jumping = False

    def update(self, ground_y):
        # Apply gravity
        self.velocity_y += self.gravity
        self.world_y += self.velocity_y

        # Apply horizontal movement
        self.world_x += self.velocity_x

        # Ground collision (adjust for radius)
        if self.world_y + self.radius >= ground_y:
            self.world_y = ground_y - self.radius
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_strength
            self.is_jumping = True
