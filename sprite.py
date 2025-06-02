import types
from vector import vector
import pygame
import random

class sync:
    localdata:object
    @staticmethod
    def sync(data):
        sync.localdata = data

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

        self.tags = []
        self.attributes = {}
    
    def hasTag(self,tag):
        "Return True if this sprite as {tag}"
        return tag in self.tags
    
    def addTag(self,tag):
        "Add {tag} to this sprite"
        self.tags.append(tag)
    
    def getAttribute(self,attr):
        "Get value of {attr}, return None if {attr} does not exist"
        try:
            return self.attributes[attr]
        except KeyError:
            return None

    def setAttribute(self,attr,value):
        "Set {attr} to {value}"
        self.attributes[attr] = value
    def addAttribute(self,attr): "Equivalent to setAttribute({attr},None)"

    def created(self):
        return
    
    def update(self):
        return


class physicSprite(sprite):
    """Base sprite for physic-based objects in the game"""
    def __init__(self, spritedir = "Defaults/MissingTexture", OnCreate=None, OnUpdate=None, x = 0, y = 0, OnPhysic=None, OnCollide=None, collide=True, xgravity=0, ygravity=0, initvx=0,initvy=0, friction=0.1, clipstrength=0.0001, static=False):
        super().__init__(spritedir, OnCreate, OnUpdate, x, y)

        if OnPhysic:
            self.onPhysicCall = types.MethodType(OnPhysic,self)
        if OnCollide:
            self.onCollide = types.MethodType(OnCollide,self)

        self.collide = collide
        self.gravity = vector(xgravity,ygravity)
        self.velocity = vector(initvx,initvy)
        self.friction = vector(friction,friction)
        self.hitdetector = self.sprite.get_rect(topleft=(x, y))
        self.cliptime = 0
        self.tolerance = 0 # not intended for modders use
        self.clipstrength = clipstrength
        self.static = static
    
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
    
    def onCollide(self,sprite):
        return

    def physicCall(self):

        # Apply physics updates
        self.position += self.velocity
        self.velocity += self.gravity
        self.velocity *= vector(1,1)-self.friction

        # Update hitbox position
        self.hitdetector.topleft = (self.position.x, self.position.y)
    
    def isColliding(self):
        objs = []
        for obj in sync.localdata.active_sprites:
            if (obj is self) or (not isinstance(obj, physicSprite)) or (not obj.collide):
                continue
            
            if self.collide_with(obj):
                objs.append(obj)
        return objs

    def collision(self):
        # Skip the entire thing if sprite is static
        if self.static: return

        collided = False
        for obj in sync.localdata.active_sprites:

            if obj is self or not isinstance(obj, physicSprite) or not obj.collide:
                continue

            if not self.collide_with(obj):
                continue

            collided = True

            # Calculate overlap (MTV method)
            dx = self.hitdetector.centerx - obj.hitdetector.centerx
            px = (self.hitdetector.width + obj.hitdetector.width) / 2 - abs(dx)

            dy = self.hitdetector.centery - obj.hitdetector.centery
            py = (self.hitdetector.height + obj.hitdetector.height) / 2 - abs(dy)

            # Against non-static objects
            if not obj.static:
                if px < py:
                    # Resolve horizontally
                    if dx > 0:
                        self.position.x += px
                    else:
                        self.position.x -= px
                else:
                    # Resolve vertically
                    if dy > 0:
                        self.position.y += py
                    else:
                        self.position.y -= py
            else:
                if px < py:
                    self.velocity.x *= -1
                    self.position.x += self.velocity.x
                else:
                    self.velocity.y *= -1
                    self.position.y += self.velocity.y

            # Update hitbox position after resolution
            self.hitdetector.topleft = (self.position.x, self.position.y)
            self.onCollide(obj)

        return collided