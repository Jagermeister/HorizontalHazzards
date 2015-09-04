from .screen import *
from weapon.weapon import *
from ship.gameobject import *
from ship.direction import *
from ship.shared import *
from ship.ship import *
from ship.baddie import *
from .game_screen import *

class Selector(pygame.sprite.Sprite):
    positions = []
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([200,200])
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        pygame.draw.rect(
            self.image,
            (0,255,0),
            (0,0,200,200),
            2)
        self.x = x
        self.y = y
        self.index = 1

    def move(self, direction):
        if direction == 1 and self.x < 900:
            self.x += 300
            self.index += 1
        elif direction == -1 and self.x > 300:
            self.x -= 300
            self.index -= 1

    def update(self, delta):
        self.rect.center = (self.x, self.y)

class Ship_Selection_Screen(Screen):
    clock = None
    screen = None
    background = None
    mouse_x, mouse_y = None, None
    all_sprites_group = None
    selector = None
    selectected_ship = None
    ships = []

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))
        self.all_sprites_group = pygame.sprite.Group()
        self.ships = [AverageShip, Tank, GlassCannon]

        for i, ship in enumerate(self.ships):
            ship = ship(None, (i+1)*300, 360, BasicPew())
            ship.add(self.all_sprites_group)

        self.selector = Selector(600,360)
        self.selector.add(self.all_sprites_group)

    def handle_events(self):
        """Translate user input to model actions"""
        clicked = False
        released = False
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                self.mouse_x, self.mouse_y = event.pos
                if event.button == 1:
                    clicked = True
                elif event.button == 3:
                    released = True
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.selector.move(-1)
                elif event.key == K_RIGHT:
                    self.selector.move(1)
                elif event.key == K_RETURN:
                    self.selectected_ship = self.ships[self.selector.index]
                    self.screen_manager.screen_remove(self)
                    self.screen_manager.screen_add(Game_Screen(self.screen_manager, self.selectected_ship))
            elif event.type == QUIT:
                self.quit()

    def update(self, delta):
        for sprite in self.all_sprites_group:
            sprite.update(delta)

    def display(self):
        """Blit everything to the screen"""
        self.screen.blit(self.background, (0, 0))

        #Frames per second
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.clock.get_fps()), 1, (10, 10, 255))
        textpos = text.get_rect()
        textpos.centerx = self.screen.get_rect().topright[0]-textpos.w
        self.screen.blit(text, textpos)

        self.all_sprites_group.draw(self.screen)
        pygame.display.update()

    def quit(self):
        """Clean up assets and unload graphic objects"""
        pygame.quit()
        sys.exit()