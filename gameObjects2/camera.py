class Camera:
    def __init__(self, screenW, screenH):
        self.cam_x = 0
        self.cam_y = 0
        self.screenW = screenW
        self.screenH = screenH

    def update(self, player):
        self.cam_x = player.x - (self.screenW / 2)
        self.cam_y = player.y - (self.screenH / 2)

    def apply(self, world_x, world_y):
        return world_x - self.cam_x, world_y - self.cam_y
