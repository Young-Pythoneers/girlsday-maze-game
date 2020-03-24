import pygame


class Display:
    def __init__(self):
        self.background = pygame.image.load("../images/drs_p.jpg").convert()

    def drawScreen(self, entities, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.background, [0, 0])
        for ent in entities:
            X, Y = ent.give_center_XY()
            screen.blit(ent.image, [X, Y])
        # pygame.display.flip()
        pygame.display.update()
