# Planet is just an object in the world. No drawing here; appearance only.

class Planet:
    def __init__(self, x, y, radius=40, color=(0, 120, 255), mass=5000):
        self.x = x
        self.y = y

        # Future physics: can move if you want; default static
        self.vx = 0.0
        self.vy = 0.0
        self.radius = radius
        self.mass = mass

        # Appearance data (World will use this to draw)
        self.appearance = {"type": "circle", "color": color}