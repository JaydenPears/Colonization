import pygame
import os
import sys
from artificial_intelligence import EnemyBot
from backend import ActionWithColony


class MainWindow:
    def __init__(self, size):
        self.fps = 60
        self.size = size
        self.states = {''}
        self.InitUI()

    def InitUI(self):
        pygame.init()
        pygame.display.set_caption('Колонизация')
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        
        running = True

        clock = pygame.time.Clock()
        global_time = 0

        check_starter_menu = True
        self.array_buttons = []

        self.check_state = 'starter menu'

        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if check_starter_menu:
                pass
            global_time += clock.tick()
            pygame.display.flip()
        pygame.quit()

    def render_starter_menu(self):
        pass

    def render_create_account_menu(self):
        pass

    def render_enter_account(self):
        pass

    def render_game_lvl_first(self):
        pass

    def render_game_lvl_second(self):
        pass

    def render_game_lvl_third(self):
        pass


class Button:
    def __init__(self, x, y, width, height, color_for_button):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color_for_draw = color_for_button

    def draw_button(self):
        pass

    def hide_button(self):
        pass


if __name__ == '__main__':
    size = width, height = 1920, 1080
    mw = MainWindow(size)