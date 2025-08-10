class Camera:
    def __init__(self, screenW, screenH, x=0.0, y=0.0, mode="follow", target=None):
        self.screenW, self.screenH = screenW, screenH
        self.x, self.y = x, y
        self.mode = mode
        self.target = target

    def update(self, dt):
        if self.mode == "follow" and self.target is not None:
            # simple follow; later you can add smoothing
            self.x = self.target.x
            self.y = self.target.y
        # else: free-fly or scripted camera leaves x,y as-is

    def world_to_screen(self, wx, wy):
        return (wx - self.x + self.screenW/2, wy - self.y + self.screenH/2)
