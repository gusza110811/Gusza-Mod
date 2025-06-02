class load:
    @staticmethod
    def sync(data:object,sprite:object,defaults:object,commands:object):
        load.data = data
        load.sprite = sprite
        load.defaults = defaults
        load.command = commands

class Mod:
    def onLoad(data:object, sprite:object, defaults:object, commands:object, **kwargs):
        load.sync(data,sprite,defaults,commands)
        print("Mod has been loaded")

        load.command.summon(load.defaults.follower(x=150,y=0))