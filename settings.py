class Settings:
    """Initialize game's static settings"""

    def __init__(self):
        self.bg_color = (10,10,10)
        self.screen_width = 1200
        self.screen_height = 800


        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 3

        # Alien Settings
        self.fleet_dropspeed = 10
        self.ship_limit = 3

        #how quickly the game speed's up 
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.bullet_speed = 1.5
        self.ship_speed = 15
        self.alien_speed = 1.0
        # fleet direct of 1 represents right; while -1 represents left
        self.fleet_direction = 1

        #Scoring 
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)