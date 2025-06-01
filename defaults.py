import types
from vector import vector
import pygame
import random

from sprite import *
class data:
    active_sprites = []

class player(sprite):
    def __init__(self, spritedir="Defaults/DefaultPlayer", OnCreate=None, OnUpdate=None, x=0, y=0):

        def movement(self):
            keypressed = pygame.key.get_pressed()
            if keypressed[pygame.K_a]:
                self.position.x -=5
            if keypressed[pygame.K_d]:
                self.position.x +=5
            if keypressed[pygame.K_w]:
                self.position.y -=5
            if keypressed[pygame.K_s]:
                self.position.y +=5

        super().__init__(spritedir, OnCreate, movement, x, y)


class physicPlayer(physicSprite):
    def __init__(self, spritedir="Defaults/DefaultPlayer", OnCreate=None, OnUpdate=None, x=0, y=0, OnPhysic=None, collide=True, xgravity=0, ygravity=0, initvx=0, initvy=0, friction=0.5, clipstrength=0.1, static=False):

        def movement(self:physicSprite):
            keypressed = pygame.key.get_pressed()
            if len(self.isColliding()) == 0:
                if keypressed[pygame.K_a]:
                    self.velocity.x -=5
                if keypressed[pygame.K_d]:
                    self.velocity.x +=5
                if keypressed[pygame.K_w]:
                    self.velocity.y -=5
                if keypressed[pygame.K_s]:
                    self.velocity.y +=5

        super().__init__(spritedir, OnCreate, OnUpdate, x, y, movement, collide, xgravity, ygravity, initvx, initvy, friction, clipstrength, static)

class follower(sprite):
    """Basic Character that can be used for enemy characters but there is no health system in the base game"""
    def __init__(self, spritedir = "Defaults/MissingTexture", OnCreate=None, x = 0, y = 0):
        super().__init__(spritedir, OnCreate, x, y)

    def update(self):

        try:
            Player = next(filter(lambda a: (type(a) is physicPlayer) or (type(a) is player),data.active_sprites))
        except StopIteration:
            return
        
        if self.position.x > Player.position.x:
            self.position.x -= 2
        else:
            self.position.x += 2
        
        if self.position.y > Player.position.y:
            self.position.y -= 2
        else:
            self.position.y += 2