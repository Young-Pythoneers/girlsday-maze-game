import pygame


class Display:
    def __init__(self):
        self.background = pygame.image.load("../images/drs_p.jpg").convert()

    def drawScreen(self, entities, screen):
        #Fill the screen with a solid RGB color
        screen.fill((0, 0, 0))
        #Draw the background
        screen.blit(self.background, [0, 0])
        for ent in entities:
            #Translate the image so it is centered on the center of the Entity
            X, Y = ent.give_center_XY()
            #Then draw it
            screen.blit(ent.image, [X, Y])
        pygame.display.update()
