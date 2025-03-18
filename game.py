# Copyright (C) 2025  Sarunphat "Gusza" Nimsuntorn
# See C.txt

import pygame
import types
import os
import threading


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
    

class commandterminal:
    """Command terminal"""
    def main():
        print(">========================<")
        print(">----Command terminal----<")
        print(">Enter command to execute<")
        print(">========================<")

        while engine.running:
            command = (input(">")).lower()
            try:
                commandfunction = command.split()[0]
            except IndexError:
                continue
            commandarg = command.split()[1:]

            try:
                if commandfunction == "help": 
                    print("quit:\n  Quit the game\nlist:\n  List all active sprite\nkill {sprite ID}:\n Delete a sprite\nsummon {sprite type} [position x] [position y]:\n  Spawn a new sprite in a specific location")
                elif commandfunction == "quit": engine.running = False
                elif commandfunction == "list": commandterminal.listsprites()
                elif commandfunction == "kill": commandterminal.kill(commandarg[0])
                elif commandfunction == "summon": commandterminal.summon(commandarg)
            except Exception as E:
                print(f"Failed to execute command `{command}`")
                print(E)

        return
    
    def listsprites():
        for idx, item in enumerate(game.active_sprites):
            if item is nil: continue
            print(f"{idx}: {type(item).__name__}")
        

    def summon(args:list[str]):
        try:
            name = eval(args[0])
        except NameError as N:
            print("Invalid sprite name: " + args[0])
            return

        try:
            x = int(args[1])
        except IndexError:
            x = 0
        try:
            y = int(args[2])
        except IndexError:
            y = 0

        print(f"{(name.__name__).capitalize()} summoned at {x},{y}")

        game.active_sprites.append(name(x=x,y=x))
    
    def kill(spriteID):
        spriteID = int(spriteID)

        print(f"Sprite {type(game.active_sprites[spriteID]).__name__} (ID: {spriteID}) has been removed")
        game.active_sprites[spriteID] = nil


class engine:
    """Function and other things not related to the main game"""

    screen:pygame.surface
    clock:pygame.time.Clock
    running = False
    font_title:pygame.font.Font
    

    def loop():
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

    def main():
        pygame.init()

        engine.screen = pygame.display.set_mode(viewport.size)
        engine.clock = pygame.time.Clock()
        engine.running = True
        engine.font_title = pygame.font.Font(size=64)

        engine.running = True

        game.begin()

        engine.loop()

        return
    
    def render():
        for rendersprite in game.active_sprites:
            if rendersprite is nil: continue

            position = rendersprite.position-viewport.position+(viewport.size/vector(2,2))

            engine.screen.blit(rendersprite.sprite,position)
        return

class game:
    """Function and other things related to the main game"""

    active_sprites:list[sprite] = []
    """Sprites currently on the level"""

    def update(events):

        for item in game.active_sprites:
            currentsprite = item

            currentsprite.Update()
        
        if len(game.active_sprites) != 0:
            while game.active_sprites[-1] is nil:
                game.active_sprites.pop()

        return

    def begin():
        game.active_sprites.append(base.player())
        game.active_sprites.append(base.follower())

        return


if __name__ == "__main__":
    os.system("cls")

    gameprocess = threading.Thread(target=engine.main,name="Game")
    gameprocess.start()

    while not engine.running:
        pass

    # Debug menu / Command Terminal
    print('Copyright (C) 2025  Sarunphat "Gusza" Nimsuntorn')
    commandterminal.main()