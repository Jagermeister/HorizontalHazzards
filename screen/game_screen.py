import sys
from screen.screen import *
from weapon.weapon import *
from ship.gameobject import *
from ship.ship import *
from ship.baddie import *
from ship.spawner import *
from level.level import *

class Game_Screen(Screen):
    ship = None
    level = None

    def __init__(self, screen_manager, ship_class):
        super().__init__(screen_manager)
        self.level = Level()
        self.ship = ship_class(self.level.on_weapon_update_callback, self.level.on_status_effect_callback, 100, 360, BasicPew())
        self.level.on_start(self.ship)
        self.level.spawner_add(
            Spawner(
                self,
                self.level.baddie_add_callback,
                1.0,
                3.0,
                900,
                500,
                5,
                lambda xy: Baddie(
                    self.level.on_weapon_update_callback,
                    self.level.on_status_effect_callback,
                    self.level.baddie_bullet_add_callback,
                    self.level.baddie_on_death_callback,
                    xy[0],
                    xy[1],
                    [(700,400), (500,300), (200, 600)],
                    weapon=BasicPew4())))
        self.level.spawner_add(
            Spawner(
                self,
                self.level.baddie_add_callback,
                18.0,
                3.0,
                900,
                300,
                5,
                lambda xy: Baddie(
                    self.level.on_weapon_update_callback,
                    self.level.on_status_effect_callback,
                    self.level.baddie_bullet_add_callback,
                    self.level.baddie_on_death_callback,
                    xy[0],
                    xy[1],
                    weapon=BasicPew4()),
                x_offset = 0,
                y_offset = 25))
        self.level.spawner_add(
            Spawner(
                self,
                self.level.baddie_add_callback,
                35.0,
                1.0,
                900,
                100,
                6,
                lambda xy: Baddie(
                    self.level.on_weapon_update_callback,
                    self.level.on_status_effect_callback,
                    self.level.baddie_bullet_add_callback,
                    self.level.baddie_on_death_callback,
                    xy[0],
                    xy[1],
                    weapon=BasicPew4()),
                x_offset = 0,
                y_offset = 100))

    def handle_event(self, event):
        """Translate user input to model actions"""
        self.level.handle_event(event)

    def update(self, delta):
        if self.level:
            self.level.update(delta)

    def display(self):
        """Blit everything to the screen"""
        super().display()
        self.level.display()
        pygame.display.update()

    def quit(self):
        """Clean up assets and unload graphic objects"""
        pygame.quit()
        sys.exit()