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
                        # for x in button_list:
                        #     if key.rect[1] == x[1]:
                        #         key_list.add(Key(x[0], x[1], x[2], x[3]))

                        key.clicked = True

        if event.type == pygame.MOUSEBUTTONUP:
            if pos[0] > 100:
                key_list.add(Key(up))

            for key in key_list:
                key.clicked = False
            drag_id = 0

    for number, key in enumerate(key_list):
        pos = pygame.mouse.get_pos()

        # if clicked and no collision you can move the object
        if key.clicked == True and len(pygame.sprite.spritecollide(key,key_list, False)) == 1:
            key.rect.x = pos[0] - (key.rect.width/2)
            key.rect.y = pos[1] - (key.rect.height/2)

        elif key.clicked == True and len(pygame.sprite.spritecollide(key, key_list, False)) > 1:
            key.rect.x = key.rect.x - 200
            key.rect.y = key.rect.x - 200

        # else:
        #     key.rect.x = pos[0] - (key.rect.width / 2)
        #     key.rect.y = pos[1] - (key.rect.height / 2)


    screen.fill(Black)
    key_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
