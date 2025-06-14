class load:
    @staticmethod
    def sync(data:object,sprite:object,defaults:object,commands:object):
        load.data = data
        load.sprite = sprite
        load.defaults = defaults
        load.commands = commands

class Main:
    def onLoad(data:object, sprite:object, defaults:object, commands:object, **kwargs):
        load.sync(data,sprite,defaults,commands)

        load.data.cam = commands.summon(load.sprite.physicSprite(spritedir="Defaults/Cam.png",friction=1))

        load.commands.summon(load.sprite.physicSprite(x=0,y=150,initvx=1,friction=0))
        load.commands.summon(load.sprite.physicSprite(x=-100,y=150,friction=0,static=True))
        load.commands.summon(load.sprite.physicSprite(x=100,y=150,friction=0,static=True))

        load.commands.summon(load.sprite.physicSprite(x=0,y=-150,friction=1))
        load.commands.summon(load.sprite.physicSprite(x=-100,y=-150,friction=1))
        load.commands.summon(load.sprite.physicSprite(x=100,y=-150,friction=1))

        load.data.player = commands.summon(defaults.physicPlayer())
        load.data.player.addTag("player")
        load.data.player.setAttribute("health",100)

        load.commands.getTags(data.player)
        load.commands.getAttributes(data.player)

        print("Main script has been loaded")