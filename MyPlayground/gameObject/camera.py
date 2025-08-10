class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera_x = 0
        self.camera_y = 0

    def follow(self, target):
        """Centers camera on a target object with world_x/world_y."""
        self.camera_x = target.world_x - (self.width // 2)
        self.camera_y = target.world_y - (self.height // 2)

    def follow_x(self, target):
        """Centers camera on a target object with world_x"""
        self.camera_x = target.world_x - (self.width // 2)

    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates."""
        return world_x - self.camera_x, world_y - self.camera_y
