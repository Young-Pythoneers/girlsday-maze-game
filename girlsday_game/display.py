import pygame


class Display:
    def __init__(self, game, screen_size_X, screen_size_Y):
        self.game = game
        self.screen_size_X = screen_size_X
        self.screen_size_Y = screen_size_Y
        # Create screen
        self.screen = pygame.display.set_mode((self.screen_size_X, self.screen_size_Y))

        # Caption and Icon
        pygame.display.set_caption("Turtle VS Achilles")
        icon = pygame.image.load("../images/turtle_icon.png")
        pygame.display.set_icon(icon)
        pygame.mouse.set_visible(1)

        self.background = pygame.image.load("../images/drs_p.jpg").convert()

    def drawScreen(self, entities):
        #Fill the screen with a solid RGB color
        self.screen.fill((0, 0, 0))
        #Draw the background
        self.screen.blit(self.background, [0, 0])
        for ent in entities:
            #Translate the image so it is centered on the center of the Entity
            X, Y = ent.give_center_XY()
            #Then draw it
            self.screen.blit(ent.image, [X, Y])
        pygame.display.update()
