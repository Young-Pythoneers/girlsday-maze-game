import pygame

# initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load("../images/island.png")


# Caption and Icon
pygame.display.set_caption("Treasure quest")
icon = pygame.image.load("../images/ship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("../images/ship.png")
playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
    screen.blit(playerImg, (x,y))

running = True
while running:

    # RGB screen lvl
    screen.fill((0,0,0))

    # Background image
    #screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change =  5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 763:
        playerX = 763
