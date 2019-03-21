import pygame
from pygame.locals import *
from pygame.color import *
from pygame.key import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
from Animation import *
import os
import time
from collections import defaultdict
from Global import *
import random
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
pygame.init()
height = 600
width = 1200
screen = pygame.display.set_mode((width, height))

draw_options = pymunk.pygame_util.DrawOptions(screen)
clock = pygame.time.Clock()
happy = pygame.image.load(os.path.join(os.getcwd(),"HappyCustomer.JPG"))
sad = pygame.image.load(os.path.join(os.getcwd(),"SadMan.JPG"))
poor = pygame.image.load(os.path.join(os.getcwd(), "PoorMan.JPG"))
rich = pygame.image.load(os.path.join(os.getcwd(), "RichGuy.JPG"))
moneySpeech = pygame.image.load(os.path.join(os.getcwd(), "MoneySpeech.png"))
presentSpeech = pygame.image.load(os.path.join(os.getcwd(), "PresentSpeech.JPG"))
blankGraph = pygame.image.load(os.path.join(os.getcwd(), "BlankGraph.JPG"))
blankBottom = pygame.image.load(os.path.join(os.getcwd(), "BlankGraphBottom.JPG"))
PE = pygame.image.load(os.path.join(os.getcwd(), "PE.JPG"))
QE = pygame.image.load(os.path.join(os.getcwd(), "QE.JPG"))
demand = pygame.image.load(os.path.join(os.getcwd(), "D.JPG"))
supply = pygame.image.load(os.path.join(os.getcwd(), "S.JPG"))
pause = True
def MicroSupplyDemand():
    global pause

    running = True
    gameTime = 0
    anims = defaultdict()

    #constants
    dt = 1/NUM_STEPS
    speechDim = 50
    negTime = 7
    padding = 0.1
    stMvTm = 4
    endMvTm = 3

    # define animations
    anims["sad"] = Animation(screen, sad)
    anims["moneySpeech"] = Animation(screen, moneySpeech)
    anims["poor"] = Animation(screen, poor)
    anims["presentSpeech"] = Animation(screen, presentSpeech)
    anims["happy"] = Animation(screen, happy)
    anims["rich"] = Animation(screen, rich)

    # transform and set times
    anims["sad"].flip(True, False)
    anims["sad"].scale(factor * 50, factor * 100)
    anims["sad"].duration = negTime
    
    anims["moneySpeech"].scale(factor * speechDim, factor * speechDim)
    anims["moneySpeech"].duration = negTime
    anims["moneySpeech"].startTime = stMvTm
    
    anims["poor"].scale(factor * 50, factor * 100)
    anims["poor"].duration = negTime

    anims["presentSpeech"].scale(factor * speechDim, factor * speechDim)
    anims["presentSpeech"].duration = negTime
    anims["presentSpeech"].startTime = stMvTm
    anims["presentSpeech"].flip(True, False)

    anims["happy"].scale(factor * 100, factor * 100)
    anims["happy"].startTime = stMvTm + negTime
    anims["happy"].flip(True, False)

    anims["rich"].scale(factor * 100, factor * 100)
    anims["rich"].startTime = stMvTm + negTime
    anims["rich"].flip(True, False)

    #set initial positions
    anims["sad"].rePos(0, height/2)
    anims["moneySpeech"].rePos(width/2 - 0.5 * anims["moneySpeech"].get_width(), height/2 - anims["sad"].get_height()/2)
    anims["presentSpeech"].rePos(width/2 + 0.5 * anims["presentSpeech"].get_width(), height/2 - anims["poor"].get_height()/2)
    anims["poor"].rePos(width, height/2)
    anims["happy"].rePos(width/2 - anims["moneySpeech"].get_width() - anims["sad"].get_width()/2, height/2)
    anims["rich"].rePos(width/2 + anims["presentSpeech"].get_width() + anims["poor"].get_width()/2, height/2)

    #define movements
    anims["sad"].move(width/2 - anims["moneySpeech"].get_width() - anims["sad"].get_width()/2 , height/2, stMvTm)
    anims["poor"].move(width/2 + anims["presentSpeech"].get_width() + anims["poor"].get_width()/2, height/2 , stMvTm)
    anims["happy"].move(0, height/2,endMvTm)
    anims["rich"].move(width, height/2,endMvTm)
    
    # main loop
    while (running):

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_p:
                    pause = not pause
                elif event.type == KEYDOWN and event.key == K_r:
                    for anim in anims.values():
                        anim.reset()
                    gameTime = 0
                elif event.type == KEYDOWN and event.key == K_s:
                    for key, value in anims.items():
                        print(key+ " startPt: " + str(value.startPt) + ", endPt: " + str(value.endPt) + ", startTime: " + str(value.startTime) + "\n" )
            if pause:
                continue
            screen.fill(THECOLORS["white"])
            running = False
            for anim in anims.values():
                if anim.startTime <= gameTime:
                    anim.display()
                if anim.onScreen:
                    running = True
            gameTime += dt
            pygame.display.flip()
            clock.tick_busy_loop(FPS)
            pygame.display.set_caption("fps: " + str(clock.get_fps()))

def FailedTransaction():
    global pause
    running = True
    gameTime = 0
    anims = defaultdict()

    #constants
    dt = 1/NUM_STEPS
    speechDim = 50
    negTime = 3
    padding = 0.1
    stMvTm = 4
    endMvTm = 3

    # define animations
    anims["sad"] = Animation(screen, sad)
    anims["moneySpeech"] = Animation(screen, moneySpeech)
    anims["poor"] = Animation(screen, poor)
    anims["presentSpeech"] = Animation(screen, presentSpeech)
    anims["sad2"] = Animation(screen, sad)
    anims["poor2"] = Animation(screen, poor)
    anims["XMoney"] = Animation(screen, "line")
    anims["XPresent"] = Animation(screen, "line")
    # transform and set times
    anims["sad"].flip(True, False)
    anims["sad"].scale(factor * 50, factor * 100)
    anims["sad"].duration = negTime * 2
    
    anims["moneySpeech"].scale(factor * speechDim, factor * speechDim)
    anims["moneySpeech"].duration = negTime * 2
    anims["moneySpeech"].startTime = stMvTm
    
    anims["poor"].scale(factor * 50, factor * 100)
    anims["poor"].duration = negTime * 2

    anims["presentSpeech"].scale(factor * speechDim, factor * speechDim)
    anims["presentSpeech"].duration = negTime * 2
    anims["presentSpeech"].startTime = stMvTm
    anims["presentSpeech"].flip(True, False)

    anims["sad2"].scale(factor * 50, factor * 100)
    anims["sad2"].startTime = stMvTm + negTime * 2 

    anims["poor2"].scale(factor * 50, factor * 100)
    anims["poor2"].startTime = stMvTm + negTime * 2
    anims["poor2"].flip(True, False)

    anims["XMoney"].startTime = stMvTm
    anims["XMoney"].duration = negTime
    anims["XMoney"].scale(anims["moneySpeech"].get_width(), anims["moneySpeech"].get_height())
    anims["XMoney"].foreGr = True

    anims["XPresent"].startTime = stMvTm + negTime
    anims["XPresent"].duration = negTime
    anims["XPresent"].scale(anims["presentSpeech"].get_width(), anims["presentSpeech"].get_height())
    anims["XPresent"].foreGr = True

    #set initial positions
    anims["sad"].rePos(0, height/2)
    anims["moneySpeech"].rePos(width/2 - 0.5 * anims["moneySpeech"].get_width(), height/2 - anims["sad"].get_height()/2)
    anims["presentSpeech"].rePos(width/2 + 0.5 * anims["presentSpeech"].get_width(), height/2 - anims["poor"].get_height()/2)
    anims["poor"].rePos(width, height/2)
    anims["sad2"].rePos(width/2 - anims["moneySpeech"].get_width() - anims["sad"].get_width()/2, height/2)
    anims["poor2"].rePos(width/2 + anims["presentSpeech"].get_width() + anims["poor"].get_width()/2, height/2)
    anims["XMoney"].rawRePos( anims["moneySpeech"].pos)
    anims["XPresent"].rawRePos(anims["presentSpeech"].pos)

    #define movements
    anims["sad"].move(width/2 - anims["moneySpeech"].get_width() - anims["sad"].get_width()/2 , height/2, stMvTm)
    anims["poor"].move(width/2 + anims["presentSpeech"].get_width() + anims["poor"].get_width()/2, height/2 , stMvTm)
    anims["sad2"].move(0, height/2,endMvTm)
    anims["poor2"].move(width, height/2,endMvTm)
    
    while (running):

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_p:
                    pause = not pause
                elif event.type == KEYDOWN and event.key == K_r:
                    for anim in anims.values():
                        anim.reset()
                    gameTime = 0
            if pause:
                continue
            screen.fill(THECOLORS["white"])
            running = False
            for anim in anims.values():
                if anim.startTime <= gameTime and not anim.foreGr:
                    anim.display()
                if anim.onScreen:
                    running = True
            for anim in anims.values():
                if anim.startTime <= gameTime and anim.foreGr:
                    anim.display()
                if anim.onScreen:
                    running = True
            gameTime += dt
            pygame.display.flip()
            clock.tick_busy_loop(FPS)
            pygame.display.set_caption("fps: " + str(clock.get_fps()))

def SDCurve(demandMv = 0, supplyMv = 0, demandPtQ = False, supplyPtQ = False, shiftTime = 5, dur = 5, eq = False):
    global pause
    running = True
    gameTime = 0
    anims = defaultdict()

    #constants
    dt = 1/NUM_STEPS
    speechDim = 50
    padding = 0.1
    stMvTm = 5
    endMvTm = 5
    graphStart = Vec2d(100,50)#100, 550 in screen coordinates
    graphCenter = Vec2d(width/2 + graphStart.x, height/2 - graphStart.y)
    letterDim = 25
    # define animations
    anims["graph"] = Animation(screen, blankGraph)
    anims["supply"] = Animation(screen, "line")
    anims["supplyPt"] = Animation(screen, "circle")
    anims["demand"] = Animation(screen, "line")
    anims["demandPt"] = Animation(screen, "circle")
    anims["graphBottom"] = Animation(screen, blankBottom)
    anims["PE"] = Animation(screen, PE)
    anims["QE"] = Animation(screen, QE)
    anims["D"] = Animation(screen, demand)
    anims["S"] = Animation(screen, supply)
    # transform and set times
    anims["graph"].scale(width , height)
    anims["demand"].scale(width , height)
    anims["supply"].scale(width, -height)
    anims["demandPt"].scale(15)
    anims["supplyPt"].scale(15)
    anims["graphBottom"].scale(width, graphStart.y)
    anims["graphBottom"].foreGr = True
    anims["PE"].scale(letterDim, letterDim)
    anims["QE"].scale(letterDim, letterDim)
    anims["D"].scale(letterDim, letterDim)
    anims["S"].scale(letterDim, letterDim)
    #set initial positions
    anims["graph"].rePos(width/2, height/2)
    anims["graph"].duration = dur + shiftTime
    anims["supply"].rawRePos(graphCenter)
    anims["supply"].duration = dur
    anims["demand"].rawRePos(graphCenter)
    anims["demand"].duration = dur
    anims["demandPt"].rawRePos(anims["demand"].get_top_left())
    anims["demandPt"].duration = dur * int(demandPtQ)
    anims["supplyPt"].rawRePos(anims["supply"].get_bottom_left())
    anims["supplyPt"].duration  = dur * int(supplyPtQ)
    anims["graphBottom"].rePos(width/2, height - 0.5 * anims["graphBottom"].get_height())
    anims["graphBottom"].duration = dur + shiftTime
    anims["PE"].rePos(graphStart.x + 15, graphCenter.y)
    anims["PE"].duration = dur
    anims["QE"].rePos(graphCenter.x, height - graphStart.y - 15)
    anims["QE"].duration = dur 
    anims["S"].rePos(graphStart.x + 15, height - graphStart.y - 15)
    anims["S"].duration = dur
    anims["D"].rePos(graphStart.x + 75, 15)
    anims["D"].duration = dur
    #define movements
    if(demandMv>0):
        newX = graphCenter.x + demandMv
        anims["demand"].move(newX, graphCenter.y,shiftTime)
    else:
        
        newY = graphCenter.y - demandMv
        anims["demand"].move(graphCenter.x, newY, shiftTime)
        demandMv*=2
    
    if(supplyMv>0):
        anims["supply"].move(graphCenter.x + supplyMv, graphCenter.y, shiftTime )
    else:
        anims["supply"].move(graphCenter.x, graphCenter.y + supplyMv, shiftTime)
        supplyMv*=2
    
    anims["PE"].move(anims["PE"].pos.x, anims["PE"].pos.y - demandMv/4 + supplyMv/4, shiftTime)
    anims["QE"].move(anims["QE"].pos.x + (demandMv + supplyMv)/2, anims["QE"].pos.y, shiftTime)

    if supplyMv > 0:
        anims["S"].move( supplyMv + graphStart.x + 15, anims["S"].pos.y, shiftTime)
    elif supplyMv < 0:
        anims["S"].move( anims["S"].pos.x, supplyMv/2 + (height-graphStart.y) -15, shiftTime)
    else:
        anims["S"].duration += shiftTime
    if(demandMv > 0):
        anims["D"].move(demandMv + graphStart.x + 75, anims["D"].pos.y, shiftTime)
    elif demandMv < 0 :
        anims["D"].move(anims["D"].pos.x, -demandMv/2 +15, shiftTime)
    else:
        anims["D"].duration += shiftTime
    if eq:
        anims["demandPt"].move(anims["QE"].target.x, anims["PE"].target.y,shiftTime)
        anims["supplyPt"].move(anims["QE"].target.x, anims["PE"].target.y,shiftTime)
    else:
        targetSupply = anims["supply"].get_top_right_target()
        anims["supplyPt"].move(targetSupply.x, targetSupply.y,shiftTime * int(supplyPtQ))
        targetDemand = anims["demand"].get_bottom_right_target()
        anims["demandPt"].move(targetDemand.x, targetDemand.y, shiftTime * int(demandPtQ))
    while (running):

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pause = not pause
            elif event.type == KEYDOWN and event.key == K_r:
                for anim in anims.values():
                    anim.reset()
                gameTime = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
        if pause:
            continue
        screen.fill(THECOLORS["white"])
        running = False
        for anim in anims.values():
            if anim.startTime < gameTime:
                anim.display()
            if anim.onScreen:
                    running = True
        #for anim in anims.values():
        #    if anim.startTime <= gameTime and anim.foreGr:
        #        anim.display()
        gameTime += dt
        pygame.display.flip()
        clock.tick_busy_loop(FPS)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))

MicroSupplyDemand()#14
FailedTransaction()#27
SDCurve(supplyPtQ = True,shiftTime = 16, dur = 0)#43
SDCurve(demandPtQ = True, shiftTime = 11, dur = 0)#54
SDCurve(demandPtQ = True, supplyPtQ = True, shiftTime = 19, dur = 0, eq = True)#1 13
SDCurve(demandPtQ = True, supplyPtQ = True, shiftTime = 8, dur = 0)#1 21
SDCurve(supplyPtQ= True, shiftTime = 14, dur = 0)#1:35
SDCurve(supplyMv = 400, shiftTime = 20, dur = 0)#1 55

SDCurve(supplyMv = -400, shiftTime = 20, dur = 0)#2 15
SDCurve(demandPtQ = True, shiftTime = 14, dur = 0)#2:29
SDCurve(demandMv = 400, shiftTime = 20, dur = 0)#2 49
SDCurve(demandMv = -400, shiftTime = 12, dur = 0)#3:01

SDCurve(dur = 7)# 3:08

