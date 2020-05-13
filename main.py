import pygame, random
from pygame.locals import *
from sorters import *

class App:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    FPS = 60
    WIDTH, HEIGHT = 700, 400
    LINE_HEIGHT = 20
    FONT_SIZE = 16
    INSTRUCTIONS = [
        "[ R ]-( reshuffle )  [ S ]-( step over )  [ A ]-( toggle auto step over )",
        "[ LEFT ]-( rotate left algorithm )  [ RIGHT ]-( rotate right algorithm )",
        "[ UP ]-( Elements * 10 )  [ DOWN ]-( Elements / 10 )"
    ]
    PADDING = (110, (len(INSTRUCTIONS) + 1) * LINE_HEIGHT)

    def __init__(self):
        self._running = True
        self._display_surface = None
        self._clock = pygame.time.Clock()

        self._data = []

        self._step = None
        self._algorithm = None
        self._latency = None
        self._delay = 0
        self._instructions = None
        self._auto = False
        self._auto_step_over_label = None
        self._element_size_label = None
        self._selection = 0

        self.eventHandlers = {
            pygame.QUIT: self._handle_quit,
            pygame.KEYDOWN: self._handle_key_down
        }
        self.eventKeyHandlers = {
            pygame.K_r: self._reshuffle_handler,
            pygame.K_s: self._step_over_handler,
            pygame.K_a: self._auto_step_over_handler,
            pygame.K_LEFT: self._previous_algorithm_handler,
            pygame.K_RIGHT: self._next_algorithm_handler,
            pygame.K_UP: self._increase_elements_handler,
            pygame.K_DOWN: self._decrease_elements_handler
        }

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode((App.WIDTH, App.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._font = pygame.font.SysFont('arial', App.FONT_SIZE)
        self._instructions = []
        instructions = list(reversed(App.INSTRUCTIONS))
        for i in range(len(instructions)):
            self._instructions.append(self._create_label((0, App.HEIGHT - (i + 1) * App.LINE_HEIGHT), instructions[i], App.WHITE, App.BLACK))

        self._auto_step_over_label = self._create_label((0, 40), "running...", App.WHITE, App.BLACK)
        self._running = True
        self._algorithms = []
        for i in sorting_algorithms:
            glyph = self._create_label((App.WIDTH - 100, 0), i.__name__, App.WHITE, App.BLACK)
            glyph_selected = self._create_label((App.WIDTH - 100, 0), i.__name__, App.GREEN, App.BLACK)
            self._algorithms.append((i, glyph, glyph_selected))

        self._set_algorithm(sorting_algorithms[self._selection])
        self._set_latency(16)
        self._set_number_of_elements(0)

    def on_event(self, event):
        if event.type in self.eventHandlers:
            self.eventHandlers[event.type](event)

        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self, deltaTime):
        self._delay -= deltaTime
        if self._delay < 0 and self._auto:
            self._next_step()
            self._delay = self._latency[0]

    def on_render(self):
        self._display_surface.fill(App.BLACK)
        paddingX = App.PADDING[0]
        paddingY = App.PADDING[1]

        if self._data:
            n = len(self._data)
            incrementX = (App.WIDTH - paddingX * 2) / n
            incrementY = (App.HEIGHT - paddingY * 2) / n
            for i in self._data:
                self._draw_bar(incrementX, incrementY, i, App.GREEN if i == self._data[i] else App.WHITE)

        if self._step:
            for i in self._step:
                color = App.YELLOW if i[2] else App.RED
                for j in [0, 1]:
                    self._draw_bar(incrementX, incrementY, i[j], color)

        if self._algorithm:
            self._draw_label(self._algorithm[2])
        if self._latency:
            self._draw_label(self._latency[1])
        if self._instructions:
            for i in self._instructions:
                self._draw_label(i)
        if self._auto:
            self._draw_label(self._auto_step_over_label)
        if self._algorithms:
            for i in range(len(self._algorithms)):
                x = self._algorithms[i]
                label = x[2 if i == self._selection else 1]
                label[1].y = i * 20
                self._draw_label(label)
        if self._element_size_label:
            self._draw_label(self._element_size_label)

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(self._clock.tick(App.FPS))
            self.on_render()
        self.on_cleanup()

    def _handle_quit(self, event):
        self.running = False

    def _handle_key_down(self, event):
        if event.key in self.eventKeyHandlers:
            self.eventKeyHandlers[event.key](event)

    def _reshuffle_handler(self, event):
        self._set_algorithm(reshuffle)

    def _step_over_handler(self, event):
        self._next_step()

    def _auto_step_over_handler(self, event):
        self._toggle_auto_step_over()

    def _next_algorithm_handler(self, event):
        self._next_algorithm()

    def _previous_algorithm_handler(self, event):
        self._previous_algorithm()

    def _increase_elements_handler(self, event):
        self._increase_elements()

    def _decrease_elements_handler(self, event):
        self._decrease_elements()

    def _next_algorithm(self):
        self._set_selection((self._selection + 1) % len(self._algorithms))

    def _previous_algorithm(self):
        n = len(self._algorithms)
        self._set_selection((self._selection - 1 + n) % n)

    def _increase_elements(self):
        n = len(self._data) * 10 if self._data else 1
        self._set_number_of_elements(n)

    def _decrease_elements(self):
        n = len(self._data) / 10
        self._set_number_of_elements(n if n else 1)

    def _toggle_auto_step_over(self):
        self._auto = not self._auto

    def _next_step(self):
        self._step = next(self._algorithm[1], None) if self._algorithm else None
        self._auto = self._auto and self._step
        if not self._step:
            self._set_selection(self._selection)

    def _set_selection(self, selection):
        self._selection = selection
        self._set_algorithm(sorting_algorithms[self._selection])

    def _set_algorithm(self, algorithm):
        glyph = self._create_label((0, 0), 'Executing: ' + str(algorithm.__name__), App.WHITE, App.BLACK)
        self._algorithm = (algorithm, algorithm(self._data), glyph)
        self._auto = False
        self._step = None

    def _set_latency(self, latency):
        glyph = self._create_label((0, App.LINE_HEIGHT),'Latency: ' + str(latency) + ' ms', App.WHITE, App.BLACK)
        self._latency = (latency, glyph)
        self._delay = 0

    def _set_number_of_elements(self, size):
        size = int(size)
        self._data = [x for x in range(size)]
        self._set_selection(self._selection)
        self._element_size_label = self._create_label((0, App.LINE_HEIGHT * 2), 'Data size: ' + str(size), App.WHITE, App.BLACK)

    def _create_label(self, position, text, color, background):
        glyph = self._font.render(text, True, color, background)
        rect = glyph.get_rect()
        rect.x, rect.y = position
        return (glyph, rect)

    def _draw_label(self, label):
        self._display_surface.blit(label[0], label[1])

    def _draw_bar(self, incrementX, incrementY, index, color):
        bounds = (App.PADDING[0] + incrementX * index, App.HEIGHT - App.PADDING[1], incrementX-1, -incrementY * (self._data[index] + 1) +1)
        pygame.draw.rect(self._display_surface, color, bounds)


if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
