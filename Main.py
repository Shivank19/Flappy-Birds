import random
import sys
import pygame
from pygame.locals import *

#************************************************************************************************************************************
#GLOBAL VARIABLES
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'sprites/redbird-upflap.png'
BACKGROUND = 'sprites/background-day.png'
PIPE = 'sprites/pipe-green.png'

#************************************************************************************************************************************
#WELCOME SCREEN
def welcome():
    player_x = int(SCREENWIDTH/5)
    player_y = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    message_x = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    message_y = int(SCREENHEIGHT*0.13)
 
    base_x = 0
    for event in pygame.event.get():
        #GAME CLOSE EVENT
        if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        #GAME START EVENT
        elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            return
        else:
            SCREEN.blit(GAME_SPRITES['background'], (0, 0))
            SCREEN.blit(GAME_SPRITES['player'], (player_x ,player_y ))
            SCREEN.blit(GAME_SPRITES['message'], (message_x ,message_y))
            SCREEN.blit(GAME_SPRITES['base'], (base_x , GROUNDY))
            pygame.display.update()
            fpsClock.tick(FPS) 

def mainGame():
    score = 0
    player_x = int(SCREENWIDTH / 5)
    player_y = int(SCREENWIDTH / 2)
    base_x = 0

    pipe1 = getRandomPipe()
    pipe2 = getRandomPipe()

    upperPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : pipe1[0]['y']},
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y' : pipe2[0]['y']}
    ]

    lowerPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : pipe1[1]['y']},
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y' : pipe2[1]['y']}
    ]

    PipeVelX = -4
    PlayerVelY = -9
    PlayerMaxY = 10
    PlayerMinY = -8
    PlayerAccY = 1
    playerFlapVel = -8
    PlayerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE ):
                pygame.quit
                sys.exit
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    PlayerVelY = playerFlapVel
                    PlayerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(player_x, player_y, upperPipes, lowerPipes)
        
        if crashTest:
            return            

        #score 
        playerMidPos = player_x + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos <= pipeMidPos + 4:
                score += 1
                print(f'Score is {score}')
                GAME_SOUNDS['point'].play()

        if PlayerVelY < PlayerMaxY and not PlayerFlapped:
            PlayerVelY += PlayerAccY
        
        if PlayerFlapped:
            PlayerFlapped = False
        
        playerHeight = GAME_SPRITES['player'].get_height()
        player_y = player_y + min(PlayerVelY, GROUNDY - player_y - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += PipeVelX
            lowerPipe['x'] += PipeVelX
        
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (base_x, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (player_x, player_y))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        fpsClock.tick(FPS)

def isCollide(player_x, player_y, upperPipes, lowerPipes):
    if player_y> GROUNDY - 25  or player_y<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (player_y < pipeHeight + pipe['y'] and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (player_y + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False
def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x' : pipex, 'y' : -y1},
        {'x' : pipex, 'y' : y2}
    ]
    return pipe

#************************************************************************************************************************************
#MAIN
if __name__ == '__main__':
    pygame.init()
    fpsClock = pygame.time.Clock()
    pygame.display.set_caption('FLAPPY BIRD')
    GAME_SPRITES['numbers'] = (
        pygame.image.load ('sprites/0.png').convert_alpha(),
        pygame.image.load ('sprites/1.png').convert_alpha(),
        pygame.image.load ('sprites/2.png').convert_alpha(),
        pygame.image.load ('sprites/3.png').convert_alpha(),
        pygame.image.load ('sprites/4.png').convert_alpha(),
        pygame.image.load ('sprites/5.png').convert_alpha(),
        pygame.image.load ('sprites/6.png').convert_alpha(),
        pygame.image.load ('sprites/7.png').convert_alpha(),
        pygame.image.load ('sprites/8.png').convert_alpha(),
        pygame.image.load ('sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load ('sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load ('sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load (PIPE).convert_alpha(), 180),
        pygame.image.load (PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load (BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load (PLAYER).convert_alpha()
     

    #GAME SOUNDS
    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav')
    
    while True:
        welcome()
        mainGame()         