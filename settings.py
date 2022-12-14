class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        # Bullet settings
        self.bullet_speed_factor = 2
        self.bullet_width = 5
        self. bullet_height = 15
        self.bullet_color = (70, 80, 60)
        self.bullets_allowed = 10

        # Screen settings
        self.screen_width = 1280
        self.screen_height = 600
        self.bg_color = (255, 255, 255)


        # Alien settings
        self.alien_speed_factor = .5
        self.fleet_drop_speed = .5
        self.fleet_direction = 1
        self.alien_points = 50

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Speed-up rate
        self.speedup_rate = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = .5
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """ Increase speed settings"""
        self.ship_speed_factor *= self.speedup_rate
        self.bullet_speed_factor *= self.speedup_rate
        self.alien_speed_factor *= self.speedup_rate
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)


