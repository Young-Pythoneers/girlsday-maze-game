import pygame
import random

from pygame.sprite import Sprite

class Key(Sprite):
    def __init__(self, xpos, ypos, id):
        Sprite.__init__(self)

        self.up = pygame.image.load("../images/buttons/up.png")
        self.down = pygame.image.load("../images/buttons/down.png")
        self.left = pygame.image.load("../images/buttons/left.png")
        self.right = pygame.image.load("../images/buttons/right.png")
        self.button_list = [[self.up, 10, 10, 0], [self.down, 50, 10, 1], [self.right, 90, 10, 2], [self.left, 130, 10, 3]]

        for x in self.button_list:
            self.image= x[0]
            self.clicked = False
            self.rect = self.image.get_rect()
            self.rect.y = x[1]
            self.rect.x = x[2]
            self.clicked = False
            self.id = x[3]



pygame.init()

Black = (0,0,0)

size = (800,600)

screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()

key_list = pygame.sprite.Group()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            if event.button == 3:
                key_list.add(Key(x, y,len(key_list)+1))
            elif event.button == 1:
                for key in key_list:
                    if key.rect.collidepoint(pos):
                        key.clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            for key in key_list:
                key.clicked = False
            drag_id = 0

    for key in key_list:
        if key.clicked == True:
            pos = pygame.mouse.get_pos()
            key.rect.x = pos[0] - (key.rect.width/2)
            key.rect.y = pos[1] - (key.rect.height/2)

    screen.fill(Black)
    key_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
