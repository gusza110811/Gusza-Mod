import pygame
import types
import random

from sprite import *
from vector import *
import defaults

class commands:
    """Commands"""
    
    def listsprites():
        for idx, item in enumerate(game.active_sprites):
            if item is nil: continue
            print(f"{idx}: {type(item).__name__}")

    def summon(name):

        print(f"{(type(name).__name__)} summoned at {name.position.x},{name.position.y}")

        game.active_sprites.append(name)
    
    def kill(spriteID):
        spriteID = int(spriteID)

        print(f"Sprite {type(game.active_sprites[spriteID]).__name__} (ID: {spriteID}) has been removed")
        game.active_sprites[spriteID] = nil



class game:
    """Function and other things related to the main game"""

    active_sprites:list[sprite] = []
    """Sprites currently on the level"""

    physicupdate = 0
    """Delay between each time physics function is called. 0 means physic updates every frame"""

    timetilphysic = physicupdate

    def update(viewport:int,events:list[pygame.event.Event]):

        for item in game.active_sprites:
            currentsprite = item

            currentsprite.update()
        data.active_sprites = game.active_sprites
        
        if len(game.active_sprites) != 0:
            while game.active_sprites[-1] is nil:
                game.active_sprites.pop()
        
        if game.timetilphysic <= 0:
            game.callphysic()
            game.timetilphysic = game.physicupdate
        else:
            game.timetilphysic -= 1

        return viewport
    
    def callphysic():
        physicqueue:list[physicSprite] = filter(lambda a: issubclass(type(a),physicSprite),game.active_sprites)
        
        for physicobject in physicqueue:
            physicobject.physicCall()

        return

    def begin():
        commands.summon(defaults.physicPlayer())

        commands.summon(physicSprite(x=0,y=100,initvx=1,friction=0))
        commands.summon(physicSprite(x=-100,y=100,friction=0,static=True))
        commands.summon(physicSprite(x=100,y=100,friction=0,static=True))

        commands.summon(physicSprite(x=0,y=-100,initvx=1,friction=0))
        commands.summon(physicSprite(x=-100,y=-100,friction=0,static=True))
        commands.summon(physicSprite(x=100,y=-100,friction=0,static=True))

        return