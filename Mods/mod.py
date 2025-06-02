class load:
    @staticmethod
    def sync(data:object,sprite:object,defaults:object,command:object):
        load.data = data
        load.sprite = sprite
        load.defaults = defaults
        load.command = command

class Mod:
    def onLoad(data:object,sprite:object,defaults:object,command:object):
        load.sync(data,sprite,defaults,command)
        print("Mod has been loaded")

        load.command.summon(load.defaults.follower(x=100,y=100))

    def onUpdate():

        return