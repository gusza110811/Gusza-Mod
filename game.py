import pygame
import os
import importlib

from sprite import *
import sprite as spriteall
from vector import *
import defaults

class data:
    active_sprites:list[sprite] = []
    """Sprites currently on the level"""

    physicupdate = 0.1
    """Delay between each time physics function is called. 1 means physic updates once every frame"""

    timetilphysic = physicupdate

    cam:physicSprite
    player:sprite

    loadedMods = []

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
        "Create sprite {name}"

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

# note from the dev, 2 months later: The game was supposed to be a moddable game but its mostly just a game engine here. too hard to change the namings though, everything is too rock solid
class modLoader:
    "Load and run mods, shocking right"
    @staticmethod
    def load(mods:list=None):
        if not mods:
            mods = os.listdir("Mods")

        for moddir in mods:
            mod = importlib.import_module(f"Mods.{moddir}.main")
            print(f"\n< Output of {mod.__name__} >\n")
            mod.Main.onLoad(data=data,sprite=spriteall,defaults=defaults,commands=commands)
            print(f"\n^ Output of {mod.__name__} ^\n")

            try:
                exec("mod.Main.onUpdate()")
                data.loadedMods.append(mod)
            except NameError:
                pass
            except AttributeError:
                pass

        return
    
    def modUpdate():
        for mod in data.loadedMods:
            print(f"< Output of {mod.__name__} >")
            mod.Mod.onUpdate()
            print(f"^ Output of {mod.__name__} ^")

class game:
    """Function and other things related(?) to the main game"""

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
        
        modLoader.modUpdate()

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

        modLoader.load(modlist)

        sync.sync(data)

        return