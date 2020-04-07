import random
import time

import pygame
from pygame.sprite import Sprite


class Key(Sprite):
    def __init__(self, button):
        Sprite.__init__(self)

        self.image = button[0]
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.y = button[1]
        self.rect.x = button[2]
        self.clicked = False
        self.id = button[3]


pygame.init()

Black = (0, 0, 0)

size = (800, 600)

screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()

key_list = []


up = [pygame.image.load("../images/buttons/up.png"), 100, 10, 0]
down = [pygame.image.load("../images/buttons/down.png"), 200, 10, 1]
left = [pygame.image.load("../images/buttons/left.png"), 300, 10, 2]
right = [pygame.image.load("../images/buttons/right.png"), 400, 10, 3]

key_list.append(Key(up))
key_list.append(Key(down))
key_list.append(Key(left))
key_list.append(Key(right))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            for key in key_list:
                key.clicked = False
            # drag_id = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            if event.button == 1:
                for key in key_list[::-1]:
                    if key.rect.collidepoint(pos):
                        key.clicked = True
                        key_list.remove(key)
                        key_list.append(key)
                        break
    for number, key in enumerate(key_list):
        # if clicked and no collision you can move the object
        if key.clicked:
            pos = pygame.mouse.get_pos()

            px = pos[0] - (key.rect.width / 2)
            py = pos[1] - (key.rect.height / 2)

            key.rect.x = px
            key.rect.y = py
    screen.fill(Black)
    for key in key_list:
        screen.blit(key.image, [key.rect[0], key.rect[1]])
    pygame.display.update()
    # clock.tick(60)
pygame.quit()
