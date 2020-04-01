import pygame
import random

from pygame.sprite import Sprite

class Key(Sprite):
    def __init__(self, xpos, ypos, id):
        Sprite.__init__(self)
        self.image = pygame.image.load("../images/soldier.png").convert()
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.y = ypos
        self.rect.x = xpos
        self.clicked = False
        self.id = id
        self.linkReady = False
        self.links = []


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
            print(event.button)
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
