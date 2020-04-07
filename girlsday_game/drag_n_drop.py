import pygame
import random
import time
from pygame.sprite import Sprite

class Key(Sprite):
    def __init__(self, button):
        Sprite.__init__(self)
        self.image=button[0]
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.y = button[1]
        self.rect.x = button[2]
        self.clicked = False
        self.id = button[3]


pygame.init()

Black = (0,0,0)

size = (800,600)

screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()

key_list = pygame.sprite.Group()

up = [pygame.image.load("../images/buttons/up.png"),100, 10, 0]
down = [pygame.image.load("../images/buttons/down.png"), 200, 10, 1]
left = [pygame.image.load("../images/buttons/left.png"), 300, 10, 1]
right = [pygame.image.load("../images/buttons/right.png"), 400, 10, 1]

key_list.add(Key(up))
key_list.add(Key(down))
key_list.add(Key(left))
key_list.add(Key(right))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]

            if event.button == 1:
                for key in key_list:
                    if key.rect.collidepoint(pos):
                        key.clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            if pos[0] > 100:
                key_list.add(Key(up))

            for key in key_list:
                key.clicked = False
            drag_id = 0

    for number, key in enumerate(key_list):

        # if clicked and no collision you can move the object
        if key.clicked == True and len(pygame.sprite.spritecollide(key,key_list, False)) == 1:
            pos = pygame.mouse.get_pos()

            px = pos[0] - (key.rect.width/2)
            py = pos[1] - (key.rect.height/2)

            key.rect.x = px
            key.rect.y = py

            # if a collision is detected you should not be allowed to place the object
            if len(pygame.sprite.spritecollide(key,key_list, False)) > 1:
                #print(pygame.mouse.get_pressed())
                key.rect.x <= px
                key.rect.y <= py



    screen.fill(Black)
    key_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
