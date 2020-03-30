import pygame


class Display:
    def __init__(self, game, screen_size_x, screen_size_y):
        self.game = game
        self.screen_size_x = screen_size_x
        self.screen_size_y = screen_size_y
        # Create screen
        self.screen = pygame.display.set_mode((self.screen_size_x, self.screen_size_y))

        # Caption and Icon
        pygame.display.set_caption("Turtle VS Achilles")
        icon = pygame.image.load("../images/turtle_icon.png")
        pygame.display.set_icon(icon)
        pygame.mouse.set_visible(1)

        self.background = pygame.image.load("../images/drs_p.jpg").convert()

    def draw_screen(self, entities):
        #Fill the screen with a solid RGB color
        self.screen.fill((0, 0, 0))
        #Draw the background
        self.screen.blit(self.background, [0, 0])
        for ent in entities:
            #Translate the image so it is centered on the center of the Entity
            x, y = ent.give_center_xy()
            #Then draw it
            self.screen.blit(ent.image, [x, y])
        pygame.display.update()
