import pyperclip
from random import randint as rdi

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from pygame_layout import Layout

pygame.init()
pygame.display.set_caption("Password Generator")
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((800, 500), pygame.RESIZABLE | pygame.DOUBLEBUF)

Layout.set_font("../data/Ubuntu-Regular.ttf")
layout = Layout('layout.xml', SCREEN.get_size())

execute = True
def exit_handler(layout):
    global execute
    execute = False

def generate_password(layout):
    allowed = [chr(i) for i in range(97, 123)]
    if layout.is_checked('special_checkbox'):
        allowed += [chr(i) for i in range(33, 48)]
    if layout.is_checked('numbers_checkbox'):
        allowed += [chr(i) for i in range(48, 58)]
    if layout.is_checked('uppercase_checkbox'):
        allowed += [chr(i) for i in range(65, 91)]

    length = layout.get_value('length')
    password = ""
    for _ in range(int(length)):
        password += allowed[rdi(0, len(allowed) - 1)]
    layout.set_text('password', password)
    layout.set_text('password_length', str(int(length)))
    
def on_value_changed(layout, value):
    layout.set_text('password_length', str(int(value)))
    generate_password(layout)

def copy_password(layout):
    pyperclip.copy(layout.get_text('password'))

def on_checkbox_changed(layout, checked):
    generate_password(layout)

layout.set_on_click('exit', exit_handler)

layout.set_on_image_click('copy', copy_password)
layout.set_on_image_click('refresh', generate_password)

layout.set_on_value_changed('length', on_value_changed)

layout.set_on_action('special_checkbox', on_checkbox_changed)
layout.set_on_action('numbers_checkbox', on_checkbox_changed)
layout.set_on_action('uppercase_checkbox', on_checkbox_changed)

generate_password(layout)

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
