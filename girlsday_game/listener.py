import pygame


class EventListener:
    def __init__(self, game):
        self.game = game
        self.K_LEFT = 0
        self.K_RIGHT = 0
        self.K_UP = 0
        self.K_DOWN = 0
        self.K_SPACE = 0
        self.MOUSEBUTTONUP = 0
        self.MOUSEBUTTONDOWN = 0
        self.up_button = 0
        self.down_button = 0

    def listen(self):
        self.MOUSEBUTTONUP = 0
        self.MOUSEBUTTONDOWN = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONUP:
                self.MOUSEBUTTONUP = 1
                self.up_button = event.button

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.MOUSEBUTTONDOWN = 1
                self.down_button = event.button

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.K_LEFT = 0
                if event.key == pygame.K_RIGHT:
                    self.K_RIGHT = 0
                if event.key == pygame.K_UP:
                    self.K_UP = 0
                if event.key == pygame.K_DOWN:
                    self.K_DOWN = 0
                if event.key == pygame.K_SPACE:
                    self.K_SPACE = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.K_LEFT = 1
                if event.key == pygame.K_RIGHT:
                    self.K_RIGHT = 1
                if event.key == pygame.K_UP:
                    self.K_UP = 1
                if event.key == pygame.K_DOWN:
                    self.K_DOWN = 1
                if event.key == pygame.K_SPACE:
                    self.K_SPACE = 1
