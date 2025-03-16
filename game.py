# Copyright (C) 2025  Sarunphat "Gusza" Nimsuntorn
# See C.txt

import pygame
import types
from multiprocessing import Process

class vector:
    """Base class for 2 dimensional position and scale"""

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
        except FileNotFoundError:
            try:
                self.sprite = pygame.image.load(spritedir+".png")
            except FileNotFoundError:
                self.sprite = pygame.image.load("Defaults/MissingTexture.png")
        
        if OnCreate:
            self.Created = types.MethodType(OnCreate,self)
        
        if OnUpdate:
            self.Update = types.MethodType(OnUpdate,self)
    
    def Created(self):
        return
    
    def Update(self):
        return

class nil:
    """A placeholder 'sprite' that replace a deleted sprite and only removed from the list when its the last sprite so other sprite's ID doesnt change"""
    def Update():
        return

class base:
    """Class containing every default pre-made sprite presets"""

    class player(sprite):
        """Player Controlled Characters"""
        def __init__(self, spritedir = "Defaults/DefaultPlayer", x = 0, y = 0):
            super().__init__(spritedir, None, None, x, y)

        def Update(self):
            keypressed = pygame.key.get_pressed()
            if keypressed[pygame.K_a]:
                self.position.x -= 5
            if keypressed[pygame.K_d]:
                self.position.x += 5
            if keypressed[pygame.K_w]:
                self.position.y -= 5
            if keypressed[pygame.K_s]:
                self.position.y += 5
    
    class follower(sprite):
        """Basic Character that can be used for enemy characters but there is no health system in the base game"""
        def __init__(self, spritedir = "Defaults/MissingTexture", OnCreate=None, x = 0, y = 0):
            super().__init__(spritedir, OnCreate, x, y)

        def Update(self):

            try:
                player = next(filter(lambda a: type(a) is base.player,game.active_sprites))
            except StopIteration:
                return
            
            if self.position.x > player.position.x:
                self.position.x -= 2
            else:
                self.position.x += 2
            
            if self.position.y > player.position.y:
                self.position.y -= 2
            else:
                self.position.y += 2

class game:
    """Function and other things related to the main game"""

    active_sprites:list[sprite] = []
    """Sprites currently on the level"""

    def kill(spriteID):
        game.active_sprites[spriteID] = nil

    def update(events):

        for item in game.active_sprites:
            currentsprite = item

            currentsprite.Update()
        
        while game.active_sprites[-1] is nil:
            game.active_sprites.pop()

        return

    def begin():
        game.active_sprites.append(base.player())
        game.active_sprites.append(base.follower())
        game.active_sprites.append(base.follower())
        game.kill(2)

        return
    

class commandterminal:
    def main():
        print(">------------------------<")
        print(">----Command terminal----<")
        print(">Enter command to execute<")
        command = input(">")

class engine:
    """Function and other things not related to the main game"""

    pygame.init()
    screen = pygame.display.set_mode(viewport.size)
    clock = pygame.time.Clock()
    running = True

    def main():

        
        game.begin()

        while engine.running:
            engine.screen.fill(pygame.Color(64,128,200))
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
        for rendersprite in game.active_sprites:
            if rendersprite is nil: continue

            position = rendersprite.position-viewport.position+(viewport.size/vector(2,2))

            engine.screen.blit(rendersprite.sprite,position)
        return


if __name__ == "__main__":
    print('Copyright (C) 2025  Sarunphat "Gusza" Nimsuntorn')
    engine.main()