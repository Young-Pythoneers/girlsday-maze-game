import pygame

from girlsday_game.collisions import Collisions
from girlsday_game.display import Display
from girlsday_game.entity_keeper import Grid
from girlsday_game.entity import Goal, Player, Score
from girlsday_game.listener import EventListener
from girlsday_game.music import music
from girlsday_game.physics import Physics
from girlsday_game.timer_keeper import TimerKeeper

class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.display = Display(self, 800, 600)
        self.event_listener = EventListener(self)
        self.timer_keeper = TimerKeeper()
        self.grid = Grid(self, self.timer_keeper)
        self.music = music(self)
        self.collisions = Collisions(self)
        self.physics = Physics(self)
        goal = Goal()
        self.grid.addGridEntity(goal, 3, 1)

        score = Score()
        self.grid.addGridEntity(score, 1, 1)
        player = Player(goal, score)
        self.grid.addGridEntity(player, 1, 1)


    def run(self):

        while True:
            do_we_continue = self.event_listener.listen()
            self.collisions.applyCollisions(self.grid.entities)
            self.physics.applyPhysics(self.grid.entities, self.event_listener, self.timer_keeper)
            self.grid.updateEntities(self.event_listener, self.timer_keeper)
            self.display.drawScreen(self.grid.entities)
            self.timer_keeper.updateTimers()

            if not do_we_continue is None:
                break