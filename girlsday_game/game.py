import pygame

from girlsday_game.collisions import Collisions
from girlsday_game.display import Display
from girlsday_game.entity import Enemy, Goal, Grid, Player, Score
from girlsday_game.listener import EventListener
from girlsday_game.music import Music
from girlsday_game.physics import Physics
from girlsday_game.timer import TimerContainer


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.display = Display(self, 800, 600)
        self.event_listener = EventListener(self)
        self.timer_container = TimerContainer()
        self.grid = Grid(self.timer_container)
        self.music = Music(self)
        self.collisions = Collisions(self)
        self.physics = Physics(self)
        goal = Goal()
        self.grid.add_grid_entity(goal, 3, 1)

        score = Score()
        self.grid.add_grid_entity(score, 1, 1)
        player = Player()
        self.grid.add_grid_entity(player, 1, 1)
        enemy = Enemy(player)
        self.grid.add_grid_entity(enemy, 7, 5)

    def run(self):

        while True:
            do_we_continue = self.event_listener.listen()
            self.collisions.apply_collisions(self.grid.entities)
            self.physics.apply_physics(
                self.grid.entities, self.event_listener, self.timer_container
            )
            self.grid.update_entities(self.event_listener)
            self.display.draw_screen(self.grid.entities)
            self.timer_container.update_timers()

            if not do_we_continue is None:
                break
