import pygame
import types
import random

from vector import *

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

class sprite:
    """Base Sprite for every objects in the game"""
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
            self.created = types.MethodType(OnCreate,self)
        
        if OnUpdate:
            self.update = types.MethodType(OnUpdate,self)
    
    def created(self):
        return
    
    def update(self):
        return

class physicSprite(sprite):
    """Base sprite for physic-based objects in the game"""
    def __init__(self, spritedir = "Defaults/MissingTexture", OnCreate=None, OnUpdate=None, x = 0, y = 0, OnPhysic=None, collide=True, xgravity=0, ygravity=0, initvx=0,initvy=0, friction=0.1, clipstrength=0.0001):
        super().__init__(spritedir, OnCreate, OnUpdate, x, y)

        if OnPhysic:
            self.onPhysicCall = types.MethodType(OnPhysic,self)

        self.collide = collide
        self.gravity = vector(xgravity,ygravity)
        self.velocity = vector(initvx,initvy)
        self.friction = vector(friction,friction)
        self.hitdetector = self.sprite.get_rect(topleft=(x, y))
        self.cliptime = 0
        self.tolerance = 10**-4 # not intended for modders use
        self.clipstrength = clipstrength
    
    def isClipping(self):
        def getrand(): return (random.choice([-self.cliptime,self.cliptime]))
        self.position += vector(getrand(),getrand())
        self.cliptime += self.clipstrength
        return

    def collide_with(self, other):
        """Check collision with another sprite"""
        return self.hitdetector.colliderect(other.hitdetector)

    def onPhysicCall(self):
        return

    def physicCall(self):

        self.onPhysicCall()

        # Handle Collision with other physics objects
        if self.collide:
            self.collision()

        # Apply physics updates
        self.position += self.velocity
        self.velocity += self.gravity
        self.velocity -= self.velocity * self.friction

        # Update hitbox position
        self.hitdetector.topleft = (self.position.x, self.position.y)
    
    def isColliding(self):
        objs = []
        for obj in game.active_sprites:
            if (obj is self) or (not isinstance(obj, physicSprite)) or (not obj.collide):
                continue
            
            if self.collide_with(obj):
                objs.append(obj)
        return objs

    def collision(self):
        for obj in game.active_sprites:
            if (obj is self) or (not isinstance(obj, physicSprite)) or (not obj.collide):
                continue
            
            if self.collide_with(obj):
                # Bounce back
                self.position -= self.velocity

                if (abs(self.velocity.x) <= self.tolerance) and (abs(self.velocity.y) <= self.tolerance):
                    self.isClipping()
                    self.hitdetector.topleft = (self.position.x, self.position.y)  # Reset hitbox position
                    continue
                elif self.cliptime > 0:
                    self.cliptime -= self.clipstrength/2

                if self.hitdetector.midtop[1] > obj.hitdetector.midtop[1]:
                    self.velocity.y *= -1
                elif self.hitdetector.midleft[0] > obj.hitdetector.midleft[0]:
                    self.velocity.x *= -1
                elif self.hitdetector.midright[0] < obj.hitdetector.midright[0]:
                    self.velocity.x *= -1
                elif self.hitdetector.midbottom[1] > obj.hitdetector.midbottom[1]:
                    self.velocity.y *= -1
                else:
                    self.velocity *= vector(-1,-1)

                self.hitdetector.topleft = (self.position.x, self.position.y)  # Reset hitbox position

class nil:
    """A placeholder 'sprite' that replace a deleted sprite and only removed from the list when its the last sprite so other sprite's ID doesnt change"""
    def update():
        return

class base:
    """Class containing default sprites"""

    class player(sprite):
        def __init__(self, spritedir="Defaults/DefaultPlayer", OnCreate=None, OnUpdate=None, x=0, y=0, OnPhysic=None, collide=True, xgravity=0, ygravity=0, initvx=0, initvy=0, friction=0.5):

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
        def __init__(self, spritedir="Defaults/DefaultPlayer", OnCreate=None, OnUpdate=None, x=0, y=0, OnPhysic=None, collide=True, xgravity=0, ygravity=0, initvx=0, initvy=0, friction=0.5,clipstrength=1):

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

            super().__init__(spritedir, OnCreate, OnUpdate, x, y, movement, collide, xgravity, ygravity, initvx, initvy, friction,clipstrength)

    class follower(sprite):
        """Basic Character that can be used for enemy characters but there is no health system in the base game"""
        def __init__(self, spritedir = "Defaults/MissingTexture", OnCreate=None, x = 0, y = 0):
            super().__init__(spritedir, OnCreate, x, y)

        def update(self):

            try:
                player = next(filter(lambda a: (type(a) is base.physicPlayer) or (type(a) is base.player),game.active_sprites))
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

    physicupdate = 0
    """Delay between each time physics function is called. 0means physic updates every frame"""

    timetilphysic = physicupdate

    def update(viewport:int,events:list[pygame.event.Event]):

        for item in game.active_sprites:
            currentsprite = item

            currentsprite.update()
        
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
        commands.summon(base.physicPlayer())

        commands.summon(physicSprite(x=0,y=100,initvx=1,friction=0))
        commands.summon(physicSprite(x=100,y=100,friction=0))

        commands.summon(physicSprite(x=0,y=-100,initvx=1,friction=0))
        commands.summon(physicSprite(x=100,y=-100,friction=0))

        return