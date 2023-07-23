import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from pygame_layout import Layout
from random import randint as rdi

pygame.init()
pygame.display.set_caption("Layout Test")
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((1000, 800), pygame.RESIZABLE | pygame.DOUBLEBUF)

Layout.set_font("../data/Ubuntu-Regular.ttf")
layout = Layout('menu.xml', SCREEN.get_size())

execute = True
def exit_handler(layout):
    global execute
    execute = False

def fill_randomly(surface):
    for x in range(0, surface.get_width(), 50):
        for y in range(0, surface.get_height(), 50):
            pygame.draw.rect(surface, (rdi(100, 255), rdi(100, 255), rdi(100, 255)), (x, y, 50, 50))

def setup_text_container(layout):
    layout.set_source('text_container.xml')
    layout.set_on_click('close', setup_main_menu)

def setup_percentage(layout):
    layout.set_source('percentage.xml')
    layout.set_on_click('close', setup_main_menu)

def setup_ui_components(layout):
    layout.set_source('ui_components.xml')
    layout.set_on_click('close', setup_main_menu)
    layout.set_on_view_update('view', fill_randomly)

def setup_main_menu(layout):
    layout.set_source('menu.xml')
    layout.set_on_click('exit', exit_handler)
    layout.set_on_click('text_container', setup_text_container)
    layout.set_on_click('percentage', setup_percentage)
    layout.set_on_click('ui_components', setup_ui_components)

setup_main_menu(layout)

while execute:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            execute = False
        elif event.type == pygame.VIDEORESIZE:
            layout.resize(event.size)
    
    layout.set_text('fps', f"FPS: {int(clock.get_fps())}")
    layout.update(SCREEN)
    
    pygame.display.update()
    clock.tick(0)

pygame.quit()
