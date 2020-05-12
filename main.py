import pygame
import random
from pygame.locals import *


def bubble_sort(array):
    if array:
        n = len(array)
        for i in range(n-1, -1, -1):
            for j in range(0, i):
                yield (i, j, False)

                if (array[i] < array[j]):
                    array[i], array[j] = array[j], array[i]
                    yield(i, j, True)

class App:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    PADDING = (50, 50)
    FPS = 60
    WIDTH, HEIGHT = 640, 400
    DELAY = 16

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.clock = pygame.time.Clock()

        self.data = [x for x in range(100)]
        self.algorithm = bubble_sort(self.data)
        self.step = None
        self.cooldown = 0

        random.shuffle(self.data)
        print(self.data)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((App.WIDTH, App.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.nextStep()

    def on_loop(self, deltaTime):
        self.cooldown -= deltaTime
        if self.cooldown < 0:
            self.nextStep()
            self.cooldown = App.DELAY

    def nextStep(self):
        self.step = next(self.algorithm, None)

    def on_render(self):
        self._display_surf.fill(App.BLACK)
        paddingX = App.PADDING[0]
        paddingY = App.PADDING[1]

        if self.data:
            n = len(self.data)
            incrementX = (App.WIDTH - paddingX * 2) / n
            incrementY = (App.HEIGHT - paddingY * 2) / n
            for i in self.data:
                self.draw_bar(incrementX, incrementY, i, App.WHITE)

        if self.step:
            color = App.GREEN if self.step[2] else App.RED
            for i in [0, 1]:
                self.draw_bar(incrementX, incrementY, self.step[i], color)

        pygame.display.update()

    def draw_bar(self, incrementX, incrementY, index, color):
        bounds = (App.PADDING[0] + incrementX * index, App.HEIGHT - App.PADDING[1], incrementX-1, -incrementY * (self.data[index] + 1) +1)
        pygame.draw.rect(self._display_surf, color, bounds)

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(self.clock.tick(App.FPS))
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
