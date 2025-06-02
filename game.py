import pygame
import types
import random

from sprite import *
from vector import *
import defaults

class commands:
    """Commands"""
    
    def listSprites():
        "List all sprites"
        for idx, item in enumerate(data.active_sprites):
            print(f"{idx}: {type(item).__name__}")
    
    def id(name:sprite):
        "Return ID of a sprite"
        return data.active_sprites.index(sprite)
    
    def Sprite(id:int):
        "Return a sprite from their ID"
        return  data.active_sprites[id]

    def summon(name:sprite):
        "Creat sprite {name}"

        print(f"{(type(name).__name__)} summoned at {name.position.x},{name.position.y}")

        data.active_sprites.append(name)

        return name
    
    def spawn(name:sprite): "Equivalent to summon(name)"; return commands.summon(name)
    
    def kill(sprite:sprite):
        "Remove a Sprite"
        data.active_sprites.pop(commands.id(sprite))
        print(f"Sprite {type(sprite).__name__} (ID: {commands.id(sprite)}) has been removed")
    
    def getTags(sprite:sprite):
        for tag in sprite.tags:
            print(f"> {tag}")
        return sprite.tags

    def getAttributes(sprite:sprite):
        for attr in sprite.attributes:
            print(f"> {attr} = {sprite.attributes[attr]}")
        return sprite.attributes



class data:
    active_sprites:list[sprite] = []
    """Sprites currently on the level"""

    physicupdate = 0.1
    """Delay between each time physics function is called. 1 means physic updates once every frame"""

    timetilphysic = physicupdate

    cam:physicSprite
    player:sprite

class game:
    """Function and other things related to the main game"""

    def update(viewport:int,events:list[pygame.event.Event]):
        for item in data.active_sprites:
            currentsprite = item
            currentsprite.update()
        
        if data.timetilphysic < 1:
            for _ in range(int(1/(data.physicupdate % 1))):
                game.callphysic()
            data.timetilphysic = data.physicupdate
        else:
            data.timetilphysic -= 1

        return data.cam.position + vector(32,32)
    
    def callphysic():
        for physicobject in data.active_sprites:
            if not isinstance(physicobject,physicSprite): continue

            physicobject.onPhysicCall()
            physicobject.physicCall()
        
        for physicobject in data.active_sprites:
            if not isinstance(physicobject,physicSprite):
                continue
            if not physicobject.collide:
                continue

            physicobject.collision()


        return

    def begin(modlist:list[str]):

        sync.sync(data)

        data.cam = commands.summon(physicSprite(spritedir="Defaults/Cam.png",friction=1))

        commands.summon(physicSprite(x=0,y=150,initvx=1,friction=0))
        commands.summon(physicSprite(x=-100,y=150,friction=0,static=True))
        commands.summon(physicSprite(x=100,y=150,friction=0,static=True))

        commands.summon(physicSprite(x=0,y=-150,friction=1))
        commands.summon(physicSprite(x=-100,y=-150,friction=1))
        commands.summon(physicSprite(x=100,y=-150,friction=1))

        data.player = commands.summon(defaults.physicPlayer())
        data.player.addTag("player")
        data.player.setAttribute("health",100)

        commands.getTags(data.player)
        commands.getAttributes(data.player)

        return