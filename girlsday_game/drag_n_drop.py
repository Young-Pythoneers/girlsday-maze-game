import random
import time

import pygame
from pygame.sprite import Sprite


class Key(Sprite):  # TODO should also inherit from Updateable
    def __init__(self, button, key_list):
        Sprite.__init__(self)
        self.key_list = key_list
        self.image = button[0]
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.x = button[1]
        self.rect.y = button[2]
        self.clicked = False
        self.id = button[3]

    def update(self):
        if self.clicked:
            pos = pygame.mouse.get_pos()
            px = pos[0] - (key.rect.width / 2)
            py = pos[1] - (key.rect.height / 2)
            self.rect.x = px
            self.rect.y = py

    def draw(self, screen):
        screen.blit(key.image, [key.rect[0], key.rect[1]])


class KeyFactory(Key):
    def __init__(self, button, key_list, max_keys):
        Key.__init__(self, button, key_list)
        self.max_keys = max_keys

        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.text = self.font.render(str(self.max_keys), True, (200, 255, 255))

    def update(self):
        if self.clicked and self.max_keys > 0:
            key = Key([self.image, self.rect.x, self.rect.y, self.id], self.key_list)
            key.clicked = True
            self.clicked = False
            self.key_list.append(key)
            self.max_keys -= 1
            self.text = self.font.render(str(self.max_keys), True, (200, 255, 255))

    def draw(self, screen):
        screen.blit(key.image, [key.rect[0], key.rect[1]])
        screen.blit(key.text, [key.rect[0], key.rect[1]])


pygame.init()

Black = (0, 0, 0)

size = (800, 600)

screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()

key_list = []


up = [pygame.image.load("../images/buttons/up.png"), 10, 100, 0]
down = [pygame.image.load("../images/buttons/down.png"), 10, 200, 1]
left = [pygame.image.load("../images/buttons/left.png"), 10, 300, 2]
right = [pygame.image.load("../images/buttons/right.png"), 10, 400, 3]

key_list.append(KeyFactory(up, key_list, 2))
key_list.append(KeyFactory(down, key_list, 1))
key_list.append(KeyFactory(left, key_list, 3))
key_list.append(KeyFactory(right, key_list, 4))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            for key in key_list:
                key.clicked = False
            # drag_id = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.button == 1:
                for key in key_list[::-1]:
                    if key.rect.collidepoint((mouse_x, mouse_y)):
                        key.clicked = True
                        key_list.remove(key)
                        key_list.append(key)
                        break
    for key in key_list:
        key.update()
    screen.fill(Black)
    for key in key_list:
        key.draw(screen)
    pygame.display.update()
pygame.quit()
