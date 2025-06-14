import pygame
import enum

from game import *
from vector import *

class page(enum.Enum):
    EXIT = -1
    MENU = 0
    SETTING = 1
    GAME = 2

class viewport:
    position = vector(0,0)
    size = vector(640,480)

class menu:
    page = page.MENU

    def menu():
        pygame.display.set_caption("Gusza Engine")

        Title:pygame.Surface = fonts.large.render("Gusza Engine",True,pygame.Color(255,255,255))
        titleRect = Title.get_rect()
        titleRect.center = (320,80)

        copy:pygame.Surface = fonts.tiny.render("© 2025 Sarunphat \"Gusza\" Nimsuntorn",True,pygame.Color(200,200,200))
        copyRect = copy.get_rect()
        copyRect.bottomright = (640,480)

        play:pygame.Surface = fonts.midlarge.render("Play",True,pygame.Color(255,255,255),pygame.Color(24,255,40))
        playRect = play.get_rect()
        playRect.center = (320,240)

        while menu.page == page.MENU:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    menu.page = page.EXIT
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    if playRect.collidepoint(mousepos):
                        menu.page = page.GAME

            engine.screen.fill(pygame.Color(140,150,145))
            engine.screen.blit(Title,titleRect)
            engine.screen.blit(copy,copyRect)
            engine.screen.blit(play,playRect)
            pygame.display.flip()

            engine.clock.tick(30)

        return

    def main():
        pygame.init()
        fonts.large = pygame.font.Font(size=128)
        fonts.midlarge = pygame.font.Font(size=80)
        fonts.medium = pygame.font.Font(size=64)
        fonts.small = pygame.font.Font(size=32)
        fonts.tiny = pygame.font.Font(size=16)

        engine.screen = pygame.display.set_mode(viewport.size)
        engine.clock = pygame.time.Clock()
        engine.font_title = pygame.font.Font(size=64)

        while 1:
            if menu.page == page.EXIT:
                pygame.quit()
                return
            if menu.page == page.MENU:
                menu.menu()
            if menu.page == page.GAME:
                engine.main()

        return

class fonts:
    large:pygame.font.Font
    midlarge:pygame.font.Font
    medium:pygame.font.Font
    small:pygame.font.Font
    tiny:pygame.font.Font

class engine:
    """Function and other things not related to the main game"""

    screen:pygame.Surface
    clock:pygame.time.Clock
    running = False
    font_title:pygame.font.Font
    modlist = []


    def loop():
        while engine.running:
            engine.screen.fill(pygame.Color(64,128,200))
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    engine.running = False
            
            viewport.position = game.update(viewport.position,events)

            engine.render()

            pygame.display.flip()
            engine.clock.tick(30)

    def main():
        pygame.display.set_caption("Game")
        engine.running = True

        game.begin(engine.modlist)

        engine.loop()

        menu.page = page.EXIT

        return
    
    def render():
        for rendersprite in data.active_sprites:

            position = rendersprite.position-viewport.position+(viewport.size/vector(2,2))

            engine.screen.blit(rendersprite.sprite,position)
        return