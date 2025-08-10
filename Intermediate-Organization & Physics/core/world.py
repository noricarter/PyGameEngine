# World = the universe/orchestrator (no physics inside yet)
# For me I want to think of it like the Marvel Universe we live in the totality of the story we want to have our
# objects live in
class World:
    def __init__(self):
        self.objects = []  # everything that exists in the universe

    def add(self, obj):
        self.objects.append(obj)

    def update(self, dt):
        # If you want World-driven updates, call them here.
        # (We currently let main call player.update(dt) directly.)
        for o in self.objects:
            if hasattr(o, "world_update"):
                o.world_update(dt)

    def render(self, screen, camera):
        """
        Orchestrates drawing:
        - Queries each object for its 'appearance' & position (world space)
        - Transforms to screen coords via camera
        - Draws in a simple back-to-front order (by optional 'z' or radius)
        """
        import pygame

        # Simple z-order: larger radius first (planets under smaller stuff)
        def z_key(o):
            return getattr(o, "radius", 0)

        for o in sorted(self.objects, key=z_key, reverse=True):
            if not hasattr(o, "appearance"):
                continue
            app = o.appearance
            sx, sy = camera.world_to_screen(o.x, o.y)

            # Minimal appearance protocol: type + params
            if app.get("type") == "circle":
                color = app.get("color", (255, 255, 255))
                r = int(getattr(o, "radius", 8))
                pygame.draw.circle(screen, color, (int(sx), int(sy)), r)

            elif app.get("type") == "sprite":
                # Future: blit sprite with angle/scale, etc.
                sprite = app.get("surface")
                if sprite:
                    rect = sprite.get_rect(center=(int(sx), int(sy)))
                    screen.blit(sprite, rect)

            # You can extend with polygons, lines, text, etc.
