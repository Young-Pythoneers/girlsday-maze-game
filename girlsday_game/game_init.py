import pygame

from girlsday_game.collisions import Collisions
from girlsday_game.display import Display
from girlsday_game.entity_keeper import Grid
from girlsday_game.entity import Goal, Player, Score
from girlsday_game.listener import EventListener
from girlsday_game.music import music
from girlsday_game.physics import Physics

SCREEN_SIZE_X = 800
SCREEN_SIZE_Y = 600


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()

        # Create screen
        self.screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))

        # Caption and Icon
        pygame.display.set_caption("Turtle VS Achilles")
        icon = pygame.image.load("../images/turtle_icon.png")
        pygame.display.set_icon(icon)
        pygame.mouse.set_visible(0)

        self.event_listener = EventListener()
        self.grid = Grid(7, 5)

        self.music = music()

        goal = Goal(self.grid)
        self.grid.addGridEntity(goal, 4, 4)

        score = Score(self.grid)
        self.grid.addGridEntity(score, -0.4, 0.1)

        player = Player(self.grid, goal, score)
        self.grid.addGridEntity(player, 3, 3)

        self.display = Display()

    def run(self):

        while True:
            do_we_continue = self.event_listener.listen()
            self.grid.updateEntities(self.event_listener)
            self.display.drawScreen(self.grid.entities, self.screen)

            if not do_we_continue is None:
                break
