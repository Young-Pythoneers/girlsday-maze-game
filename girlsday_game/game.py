import pygame

from girlsday_game.collisions import Collisions
from girlsday_game.display import Display
from girlsday_game.entity_keeper import Grid
from girlsday_game.entity import Goal, Player, Score, Enemy
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
        self.grid = Grid(self.timer_keeper)
        self.music = music(self)
        self.collisions = Collisions(self)
        self.physics = Physics(self)
        goal = Goal()
        self.grid.add_grid_entity(goal, 3, 1)

        score = Score()
        self.grid.add_grid_entity(score, 1, 1)
        player = Player(goal, score)
        self.grid.add_grid_entity(player, 1, 1)
        enemy= Enemy(player)
        self.grid.add_grid_entity(enemy, 7,5)


    def run(self):

        while True:
            do_we_continue = self.event_listener.listen()
            self.collisions.apply_collisions(self.grid.entities)
            self.physics.apply_physics(self.grid.entities, self.event_listener, self.timer_keeper)
            self.grid.update_entities(self.event_listener, self.timer_keeper)
            self.display.draw_screen(self.grid.entities)
            self.timer_keeper.update_timers()

            if not do_we_continue is None:
                break