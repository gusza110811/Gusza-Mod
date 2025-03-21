import pygame

from game import *
from vector import *

class viewport:
    position = vector(0,0)
    size = vector(640,480)

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