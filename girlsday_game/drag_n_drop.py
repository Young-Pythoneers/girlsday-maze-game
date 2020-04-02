import pygame
import random

from pygame.sprite import Sprite

class Key(Sprite):
    def __init__(self, image, y, x, id):
        Sprite.__init__(self)
        self.image=image
        self.clicked = False
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.clicked = False
        self.id = id


pygame.init()

Black = (0,0,0)

size = (800,600)

screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()

key_list = pygame.sprite.Group()

up = pygame.image.load("../images/buttons/up.png")
down = pygame.image.load("../images/buttons/down.png")
left = pygame.image.load("../images/buttons/left.png")
right = pygame.image.load("../images/buttons/right.png")
button_list = [[up, 100, 10, 0], [down, 200, 10, 1], [right, 300, 10, 2], [left, 400, 10, 3]]

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[0]
            y = pos[1]
            if event.button == 3:
                for x in button_list:
                    key_list.add(Key(x[0], x[1], x[2], x[3]))
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
