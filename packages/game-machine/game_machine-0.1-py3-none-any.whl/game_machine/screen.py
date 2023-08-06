import pygame
from pygame.locals import QUIT

from .container import Container
from .eventobject import EventObject


class Screen (Container, EventObject) :
    """
    Screen is the central class for Game Machine.

    Screen wraps pygame.display and sets up and initialises pygame. An
    application developed using Game Machine should create a Screen instance
    first, and then place all visual or interactive elements onto that
    instance.

    """
    
    def __init__ (self,
                  size = (0, 0),
                  colour = (255, 255, 255),
                  title = "Game machine window",
                  centre = None,
                  cartesian = True) :
        super(Screen, self).__init__()
        self.size = size
        self.colour = colour
        self.cartesian = cartesian
        pygame.init()
        self.reset = 0
        self.pygame_screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self.pygame_screen.fill(self.colour)
        self.clock = pygame.time.Clock()
        self.timer = pygame.time.Clock()
        self.centre = (size[0] / 2, size[1] / 2) if (centre == None) else centre
        self.pygame_events = None


    def is_open(self) :
        """
        is_open checks to see if the user has closed the window that the
        current Screen instance is housed in.

        Returns
        -------
        Boolean
            True if the window is open, False if it has been closed.
        """
        if self.pygame_events == None :
            return True
        for event in self.pygame_events :
            if event.type == QUIT :
                return False
        return True

    def get_coords(self, coords) :

        if not self.cartesian :
            return coords
        else :
            return (coords[0] - self.centre[0], -coords[1] + self.centre[1])
        
    def to_pygame_coords(self, coords, bounds = (0, 0), margin = 0, size_ovr = None) :

        centre = self.centre if size_ovr == None else (size_ovr[0] / 2, size_ovr[1] / 2)
        if not self.cartesian :
            return (coords[0] - margin, coords[1] - margin)
        else :
            return (coords[0] + centre[0] - (bounds[0] / 2),
                    -coords[1] + centre[1] - (bounds[1] / 2))
        
    def get_mouse_coords(self) :
        if pygame.mouse.get_focused() :
            return self.get_coords(pygame.mouse.get_pos())
        else :
            return None

    def draw(self, update = False, fps = 12) :
        """
        update calls update on all the child sprites and then draws all the
        child sprites on the screen. It then waits according the fps (frames
        per second) argument
        """
        self.pygame_events = pygame.event.get()
        if self.pygame_events != None :
            for ev in self.pygame_events :
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    self.trigger('click', self.mouse_coords)
                elif ev.type == pygame.KEYDOWN :
                    self.trigger('keydown', ev.key)
                elif ev.type == pygame.KEYUP :
                    self.trigger('keyup', ev.key)
        self.pygame_screen.fill(self.colour)
        for child in self.children :
            child.draw()
            if update:
                child.update()
        pygame.display.update()
        self.clock.tick(fps)

    
    def close( self ) :
        """
        close closes the screen and shuts down pygame
        """
        pygame.quit( )

    def add(self, child) :
        super(Screen, self).add(child)
        child._screen = self

    def bounds(self) :
        if self.cartesian :
            return ((-self.width / 2, self.height / 2),
                    (self.width / 2, -self.height / 2))
        else :
            return ((0, 0), (self.width, self.height))

    def reset_timer(self) :
        self.reset = pygame.time.get_ticks()

    @property
    def width(self):
        return self.size[0]
    @property
    def height(self):
        return self.size[1]

    @property
    def mouse_coords(self):
        if pygame.mouse.get_focused() :
            return self.get_coords(pygame.mouse.get_pos())
        else :
            return None

    @property
    def time(self) :
        return pygame.time.get_ticks() - self.reset
