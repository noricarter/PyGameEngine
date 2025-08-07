class World:
    def __init__(self, ground_level):
        self.ground_level = ground_level
        self.platforms = []

    def add_platform(self, platform):
        self.platforms.append(platform)

    def get_ground_height_at(self, player_x, player_y, velocity_y):
        #Return the Y of the nearest ground/platform below the player.
        ground_candidates = []

        for p in self.platforms:
            within_x = p.world_x <= player_x <= p.world_x + p.width
            above_platform = player_y <= p.world_y
            falling = velocity_y >= 0

            if within_x and above_platform and falling:
                ground_candidates.append(p.world_y)

        # Always include main ground as a fallback
        ground_candidates.append(self.ground_level)

        return min(ground_candidates)
