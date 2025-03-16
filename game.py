# Copyright (C) 2025  Sarunphat "Gusza" Nimsuntorn
# See C.txt

import pygame
import types

class vector:
    """Base class for 2 dimensional position and scale unit"""

    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __add__(self, number):
        return vector(self.x + number[0], self.y + number[1])
    def __sub__(self, number):
        return vector(self.x - number[0], self.y - number[1])
    def __mul__(self, number):
        return vector(self.x * number[0], self.y * number[1])
    def __truediv__(self, number):
        return vector(self.x / number[0], self.y / number[1])
    
    def __len__(s):
        return 2
   
    def __getitem__(s, i):
        return [s.x, s.y][i]
    

ZERO = vector(0,0)

class viewport:
    position = vector(0,0)
    size = vector(640,480)

class sprite:
    """Base Sprite for every object in the game"""
    def __init__(self,spritedir:str="Defaults/MissingTexture",OnCreate = None, OnUpdate = None, x:int=0,y:int=0):
        self.position = vector(x,y)
        try:
            self.sprite = pygame.image.load(spritedir)
        except:
            self.sprite = pygame.image.load("Defaults/MissingTexture")
        
        if OnCreate:
            self.Created = types.MethodType(OnCreate,self)
        
        if OnUpdate:
            self.Update = types.MethodType(OnUpdate,self)
    
    def Created(self):
        return
    
    def Update(self):
        return

class game:
    """Function and other things related to the main game"""

    active_sprites = {}
    """Sprites currently on the level"""

    def update(events):
        for name in game.active_sprites:
            currentsprite = game.active_sprites[name]

            currentsprite.Update()

        return

    def begin():
        def playermovement(self):
            keypressed = pygame.key.get_pressed()
            if keypressed[pygame.K_a]:
                self.position.x -= 5
            if keypressed[pygame.K_d]:
                self.position.x += 5

            return
        game.active_sprites["player"] = sprite(spritedir="Defaults/DefaultPlayer.png",x=20,y=20, OnUpdate=playermovement)

        return
    

class engine:
    """Function and other things not related to the main game"""

    pygame.init()
    screen = pygame.display.set_mode(viewport.size)
    clock = pygame.time.Clock()
    running = True

    def main():

        
        game.begin()

        while engine.running:
            engine.screen.fill(pygame.Color(100,100,128))
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    engine.running = False
            
            game.update(events)

            engine.render()

            pygame.display.flip()
            engine.clock.tick(30)

        return
    
    def render():
        for name in game.active_sprites:
            rendersprite:sprite=game.active_sprites[name]
            
            position = rendersprite.position-viewport.position+(viewport.size/vector(2,2))

            engine.screen.blit(rendersprite.sprite,position)
        return


if __name__ == "__main__":
    print('Copyright (C) 2025  Sarunphat "Gusza" Nimsuntorn')
    engine.main()