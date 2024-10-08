import sys
import pygame
from time import sleep
from game_stats import Gamestats
from settings import Settings
from ship import Ship
from bullets import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """overall class to manage game assests and behaviour"""

    def __init__(self):
        """initialize the game and its resoursces"""
        pygame.init()

        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = Gamestats(self)
        self.play_button = Button(self , "PLay")
        self.sb = Scoreboard(self)

    def run_game(self):
        self._create_fleet()
        while True:
            self._check_events()
            self._update_screen()
            self.bullets.update()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()


    def _update_bullets(self):
        # Get rid of old bullets to save memory
        #update bullet positions
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # Check for any bullets that have hit aliens
        # If so, get rid of both the alien and the bullet
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets ad create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
        
        # increase score in collsions
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _update_aliens(self):
        """ 
        Check if the alien is at the edge of the screen 
        and thenUpdate postion of all the aliens
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Check for collision between ship and aliens
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """ response to ship hit by aliens"""
        if self.stats.ships_left>0:
        
            #decrement in ships left 
            self.stats.ships_left -= 1
            self.sb.prep_ships()
        
            # Get rid of remining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create new fleet and bullets 
            self._create_fleet()
            self.ship.center_ship()

            # give time to user to calculate using sleep function 
            sleep(0.7)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
        
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #determine the number of aliens that can fit in a row
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3*alien_height) - ship_height
        number_rows = available_space_y//(2*alien_height)
 
        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_dropspeed
        self.settings.fleet_direction *= -1

    def _create_alien(self,alien_number,row_number):    
        """ Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width , alien_height= alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien_height + (2+alien.rect.height*row_number)
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_events(self):
        #watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
               
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_play_button(self, mouse_pos):
        """Check if the postion of mouse cursor overlaps with the play button """
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            #reset game settings when play button is pressed again 
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats

            # put the game in active state
            self.stats.game_active = True

            #Hide mouse cursor 
            pygame.mouse.set_visible(False)

            #GEt rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship 
            self._create_fleet()
            self.ship.center_ship()

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

    def _check_keydown_events(self,event):
         """Respond to key presses"""
         if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
         elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
         elif event.key ==pygame.K_ESCAPE:
             sys.exit()
         elif event.key == pygame.K_SPACE:
             self._fire_bullets()
    
    def _check_keyup_events(self,event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullets(self):
        """Create new bullet and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            

    def _update_screen(self):
        """set the background color"""
        self.screen.fill(self.settings.bg_color)

        """places ship on the screen"""
        self.ship.blit()

        for bullet in self.bullets.sprites():
            bullet.Draw_bullet()
        self.aliens.draw(self.screen)

        # DRaw score board on the screen
        self.sb.show_score()

        # Draw the play button if the game is in inactive state
        if not self.stats.game_active:
            self.play_button.draw_button()

        #make the most recently closed screen to be visible
        pygame.display.flip()
            
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
