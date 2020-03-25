import math
import numpy as np
from numpy.random import uniform
import pygame
from girlsday_game.music import music

SCREEN_SIZE_X = 800
SCREEN_SIZE_Y = 600

class Entity:
    def __init__(self, entityKeeper):
        self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = None
        self.X_size = 0
        self.Y_size = 0

    def give_center_XY(self):
        X = self.X - self.X_size / 2
        Y = self.Y - self.Y_size / 2
        return X, Y

    def update(self, event_listener):
        ...


class GridEntity(Entity):
    def __init__(self, entityKeeper):
        self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = None
        self.X_size = 0
        self.Y_size = 0
        self.in_transition = False
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0
        self.transition_timer = 0
        self.transition_timer_stop = 0
        self.transition_function = lambda x : x
        self.transition_time = 1

    def update(self, event_listener):
        if self.in_transition:
            self.transition_timer += event_listener.time_passed
            self.transition(event_listener)
        if self.transition_timer >= self.transition_timer_stop:
            self.in_transition = False
            self.X = self.transition_stop_X
            self.Y = self.transition_stop_Y

    def transition(self, event_listener):
        self.X = self.transition_start_X + (self.transition_stop_X - self.transition_start_X) * self.transition_function(self.transition_timer / self.transition_timer_stop)
        self.Y = self.transition_start_Y + (self.transition_stop_Y - self.transition_start_Y) * self.transition_function(self.transition_timer / self.transition_timer_stop)

    def define_transition(self, transition_goal_X, transition_goal_Y, transition_time):
        self.in_transition = True
        self.transition_start_X = self.X
        self.transition_start_Y = self.Y
        self.transition_stop_X = transition_goal_X
        self.transition_stop_Y = transition_goal_Y
        self.transition_timer = 0
        self.transition_timer_stop = transition_time

class Tile(GridEntity):
    def __init__(self, entityKeeper):
        self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.X_size = 30
        self.Y_size = 30
        self.in_transition = False
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0
        self.transition_timer = 0
        self.transition_timer_stop = 0
        self.transition_function = None
        self.transition_time = 1

    def update(self, event_listener):
        pass

    def transition(self, event_listener):
        pass

    def define_transition(self, transition_goal_X, transition_goal_Y, transition_time):
        pass

class Wall(GridEntity):
    def __init__(self, entityKeeper):
        self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = pygame.Surface((10, 10))
        self.image.fill((100, 100, 0))
        self.X_size = 10
        self.Y_size = 10
        self.in_transition = False
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0
        self.transition_timer = 0
        self.transition_timer_stop = 0
        self.transition_function = None
        self.transition_time = 1

    def update(self, event_listener):
        pass

    def transition(self, event_listener):
        pass

    def define_transition(self, transition_goal_X, transition_goal_Y, transition_time):
        pass

class Player(GridEntity):
    def __init__(self, entityKeeper,  Goal, Score):
        self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = pygame.image.load("../images/sized_turtle.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]
        self.in_transition = False
        self.transition_start_X = 0
        self.transition_start_Y = 0
        self.transition_stop_X = 0
        self.transition_stop_Y = 0
        self.transition_timer = 0
        self.transition_timer_stop = 0
        self.transition_function = lambda x : -np.cos(np.pi * x / 2) + 1
        self.transition_time = 1
        self.score = Score
        self.goal = Goal

    def update(self, event_listener):
        if self.in_transition:
            self.transition_timer += event_listener.time_passed
            self.transition(event_listener)
            if self.transition_timer >= self.transition_timer_stop:
                self.in_transition = False
                self.X = self.transition_stop_X
                self.Y = self.transition_stop_Y
        else:
            X_change = 0
            Y_change = 0
            if not self.in_transition and event_listener.K_LEFT:
                X_change -= 2
            if not self.in_transition and event_listener.K_RIGHT:
                X_change += 2
            if not self.in_transition and event_listener.K_UP:
                Y_change -= 2
            if not self.in_transition and event_listener.K_DOWN:
                Y_change += 2
            if not self.in_transition and any([event_listener.K_LEFT, event_listener.K_RIGHT, event_listener.K_UP, event_listener.K_DOWN]):
                grid_destination_X = self.entityKeeper.grid_X + X_change
                grid_destination_Y = self.entityKeeper.grid_Y + Y_change
                if not self.entityKeeper.entityKeeper.requestMove(grid_destination_X, grid_destination_Y):
                    grid_destination_X = self.entityKeeper.grid_X
                    grid_destination_Y = self.entityKeeper.grid_Y
                self.entityKeeper.entityKeeper.moveGridEntity(self, grid_destination_X, grid_destination_Y)
                destination_X, destination_Y = self.entityKeeper.grid_XY_to_world_XY(grid_destination_X, grid_destination_Y)
                print(grid_destination_X, grid_destination_Y)
                print(self.entityKeeper.grid_X, self.entityKeeper.grid_Y)
                #print(destination_X, destination_Y)
                self.define_transition(destination_X, destination_Y, self.transition_time)

            distance_to_goal = math.sqrt(
                math.pow((self.entityKeeper.grid_X - self.goal.entityKeeper.grid_X), 2) + math.pow((self.entityKeeper.grid_Y - self.goal.entityKeeper.grid_Y), 2))
            if distance_to_goal <= 0.7:
                self.goal.eaten = True
                self.score.score += 1
                music.sound_handler('../sounds/munch.wav', 0)

            #self.input_cooldown_timer = self.input_cooldown
            #self.input_cooldown_timer -= event_listener.time_passed



class Goal(GridEntity):
    def __init__(self, entityKeeper):
        self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.image = pygame.image.load("../images/lettuce.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]
        self.eaten = False


    def update(self, event_listener):
        if self.eaten == True:
            self.eat()
            self.respawn()
            self.eaten = False

    def destroy(self):
        self.entityKeeper.removeEntity(self)

    def eat(self):
        self.destroy()

    def respawn(self):
        grid_X = np.random.randint(0, 7) * 2 + 1
        grid_Y = np.random.randint(0, 5) * 2 + 1
        self.entityKeeper.entityKeeper.addGridEntity(self, grid_X, grid_Y)

class Score(GridEntity):
    def __init__(self, entityKeeper):
        self.entityKeeper = entityKeeper
        self.X = 10
        self.Y = 10
        self.score = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.image = self.font.render("Score : " + str(self.score), True, (0, 0, 0))
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]

    def update(self, event_listener):
        score = self.font.render("Score : " + str(self.score), True, (0, 0, 0))
        self.image = score


class PhysicalEntity(Entity):
    def __init__(self, entityKeeper):
        self.entityKeeper = entityKeeper
        self.X = 0
        self.Y = 0
        self.impulse_X = 0
        self.impulse_Y = 0
        self.speed = 0
        self.mass = 0
        self.image = None
        self.X_size = 0
        self.Y_size = 0
        self.collided = False

    def update(self, event_listener):
        ...

    def collision(self):
        ...

class Projectile(PhysicalEntity):
    def __init__(self, entityKeeper, X, Y, impulse_X, impulse_Y):
        self.entityKeeper = entityKeeper
        self.X = X
        self.Y = Y
        self.impulse_X = impulse_X
        self.impulse_Y = impulse_Y
        self.speed = 40
        self.mass = 1
        self.image = None
        self.X_size = 0
        self.Y_size = 0
        self.collided = False

    def update(self, event_listener):
        if self.collided:
            self.collision()
            self.collided = False
        self.impulse_X += self.speed * event_listener.time_passed

    def destroy(self):
        self.entityKeeper.removeEntity(self)

    def collision(self):
        self.destroy()

class Particle(Projectile):
    def __init__(self, entityKeeper, X, Y, impulse_X, impulse_Y):
        self.entityKeeper = entityKeeper
        self.X = X
        self.Y = Y
        self.impulse_X = impulse_X
        self.impulse_Y = impulse_Y
        self.speed = 0
        self.mass = 0.1
        self.image = pygame.image.load("../images/explosion.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]
        self.collided = False
        self.life_time = 0.25 + uniform(-0.1,0.1)

    def update(self, event_listener):
        if self.collided:
            if self.collided:
                self.destroy()
        self.impulse_X += self.speed * event_listener.time_passed
        self.life_time -= event_listener.time_passed
        if not self.collided and  self.life_time < 0:
            self.destroy()

class Rocket(Projectile):
    def __init__(self, entityKeeper, X, Y, impulse_X, impulse_Y):
        self.entityKeeper = entityKeeper
        self.X = X
        self.Y = Y
        self.impulse_X = impulse_X
        self.impulse_Y = impulse_Y
        self.speed = 40
        self.mass = 1
        self.image = pygame.image.load("../images/pizza-box.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]
        self.collided = False
        self.particle_count = 20
        self.spread = 20
        self.impulse_modifier = 1
        self.impulse_multiplier = 0.1

    def update(self, event_listener):
        if self.collided:
            self.make_particles()
            self.destroy()
            self.collided = False
        self.impulse_X += self.speed * event_listener.time_passed


    def destroy(self):
        self.entityKeeper.removeEntity(self)

    def collision(self):
        self.destroy()

    def make_particles(self):
        for i in range(self.particle_count):
            self.entityKeeper.addEntity(Particle(self.entityKeeper, self.X + uniform(-self.spread,self.spread), self.Y + uniform(-self.spread,self.spread), self.impulse_X * self.impulse_multiplier + uniform(-self.impulse_modifier, self.impulse_modifier), self.impulse_Y * self.impulse_multiplier + uniform(-self.impulse_modifier, self.impulse_modifier)))

class RocketDuck(PhysicalEntity):
    def __init__(self, entityKeeper):
        self.entityKeeper = entityKeeper
        self.X = 370
        self.Y = 480
        self.impulse_X = 0
        self.impulse_Y = 0
        self.speed = 20
        self.mass = 1
        self.image = pygame.image.load("../images/rocket_duck.png")
        self.X_size = self.image.get_size()[1]
        self.Y_size = self.image.get_size()[0]
        self.angle = 3 * np.pi / 2
        self.turn_speed = 50
        self.collided = False

    def update(self, event_listener):
        if self.collided:
            self.collision()
            self.collided = False
        self.angle += (
            self.turn_speed * np.random.uniform(-1, 1) * event_listener.time_passed
        )
        if self.angle < 0:
            self.angle += 2 * np.pi
        if self.angle > 2 * np.pi:
            self.angle -= 2 * np.pi
        self.impulse_X += np.cos(self.angle) * self.speed * event_listener.time_passed
        self.impulse_Y += np.sin(self.angle) * self.speed * event_listener.time_passed


    def collision(self):
        pass