from Global import *
import pygame
from pymunk.vec2d import Vec2d
class Animation(object):
    """description of class"""
    def __init__(self, screen, image):
        self.screen = screen
        self.image = image
        self.pos = Vec2d(0,0)
        self.target = Vec2d(0,0)
        self.startTime = 0
        self.onScreen = True
        self.ctr = 0
        self.mvmtTime = 0
        self.duration = 0
        self.diff = Vec2d(0,0)
        self.startPos = Vec2d(0,0)
        self.endPos = Vec2d(0,0)
        self.radius = 5
        self.foreGr = False
        self.xCrop = 0
        self.yCrop = 0
    def rePos(self, newX, newY):
        #self.pos = Vec2d(newX - int(self.get_width()/2), newY - int(self.get_height()/2))
        self.pos = Vec2d(newX, newY)

    def rawRePos(self, newPos):
        self.pos = newPos

    def move(self, newX, newY, mvmtTime):
        self.target = Vec2d(newX, newY)
        self.mvmtTime = mvmtTime

    def reset(self):
        self.ctr = 0
        self.onScreen = True
        self.pos = self.startPos

    def display(self):
        if(self.onScreen):
            
            if self.ctr == 0:
                x = self.target.x - self.pos.x
                y = self.target.y - self.pos.y
                self.diff = Vec2d(x,y)
                self.startPos = self.pos
            if self.ctr < self.mvmtTime * NUM_STEPS:
                self.pos = self.startPos + self.ctr * self.diff / (self.mvmtTime * NUM_STEPS)
                self.pos = Vec2d(int(self.pos.x), int(self.pos.y))
                self.ctr+=1
            elif self.ctr < self.mvmtTime * NUM_STEPS + self.duration * NUM_STEPS:
                self.ctr += 1
            else:
                self.onScreen = False

            if self.image == "line":
                x = self.pos - self.endPos/2
                y = self.endPos/2 + self.pos
                #self.crop()
                pygame.draw.line(self.screen, (255,0,0),self.pos - self.endPos/2, self.endPos/2 + self.pos,5)
            elif self.image == "circle":
                pygame.draw.circle(self.screen, (255,0,0), Vec2d(int(self.pos.x), int(self.pos.y)), int(self.radius), 0)
                
            else:
                self.screen.blit(self.image, self.get_top_left())
                
    def crop(self):
        self.origEndPos = self.endPos
        slope = -self.endPos.y / self.endPos.x
        yInt = slope * (self.xCrop - self.pos.x) + self.pos.y
        xInt = -(self.yCrop-self.pos.y)/slope + self.pos.x
        if xInt>self.endPos.x:
            self.endPos = Vec2d(xInt, self.yCrop)
        if yInt<self.endPos.y:
            self.endPos = Vec2d(self.xCrop, yInt)

    def flip(self, hor, ver):

        self.image = pygame.transform.flip(self.image, hor, ver)

    def scale(self, x, y = 0):
        if self.image == "line":
            self.endPos = self.startPos + Vec2d(x,y)
        elif self.image == "circle":
            self.radius = x
        else:
            self.image = pygame.transform.scale(self.image, (int(x), int(y)))

    def get_width(self):
        if self.image == "line" :
            return abs(self.endPos.x )
        else:
            return self.image.get_width()

    def get_height(self):
        if self.image == "line":
            return abs(self.endPos.y )
        else:
            return self.image.get_height()

    def get_top_left(self):
        return Vec2d(-self.get_width()/2, -self.get_height()/2) + self.pos

    def get_top_right(self):
        return Vec2d(self.get_width()/2, -self.get_height()/2) + self.pos

    def get_bottom_left(self):
        return Vec2d(-self.get_width()/2, self.get_height()/2) + self.pos

    def get_bottom_right(self):
        return Vec2d(self.get_width()/2, self.get_height()/2) + self.pos

    def get_top_left_target(self):
        return Vec2d(-self.get_width()/2, -self.get_height()/2) + self.target

    def get_top_right_target(self):
        return Vec2d(self.get_width()/2, -self.get_height()/2) + self.target

    def get_bottom_left_target(self):
        return Vec2d(-self.get_width()/2, self.get_height()/2) + self.target

    def get_bottom_right_target(self):
        return Vec2d(self.get_width()/2, self.get_height()/2) + self.target
