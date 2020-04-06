import pygame
import random
import time
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
for x in button_list:
    key_list.add(Key(x[0], x[1], x[2], x[3]))


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
            for key in key_list:
                key.clicked = False
            drag_id = 0

    for number, key in enumerate(key_list):
        pos = pygame.mouse.get_pos()

        print(number)
        if (key.rect[0] > (button_list[number][2] + 80)):
            key_list.add(
                Key(button_list[number][0], button_list[number][1], button_list[number][2], button_list[number][3]))

        #print(len(pygame.sprite.spritecollide(key,key_list, False)))
        #CAN BE USED FOR COLLISION DETECTION, if len of list > 2
        #maybe generate here the new buttons

        if key.clicked == True:

            key.rect.x = pos[0] - (key.rect.width/2)
            key.rect.y = pos[1] - (key.rect.height/2)


    screen.fill(Black)
    key_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
