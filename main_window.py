import pygame
import os
import sys
from artificial_intelligence import GameBot
from backend import (PlayersColony, PeacefulColony, EnemyColony, ActionWithTable)


COLOR_ACTIVE_BUTTON = (231, 238, 255)


class MainWindow:
    def __init__(self, size):
        self.starter_position = (0, 0)
        self.size = size

        self.states = {'starter menu': self.render_starter_menu,
                       'new game': self.render_game_lvl_first,
                       'download game': self.render_menu_download_game,
                       'settings': self.render_settings_menu}
        self.game_lvls = {'1 lvl': self.render_game_lvl_first,
                          '2 lvl': self.render_game_lvl_second,
                          '3 lvl': self.render_game_lvl_third}

        self.InitUI()

    def InitUI(self):
        pygame.init()
        pygame.display.set_caption('Колонизация')
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        self.starter_image = pygame.image.load("images/start_image.png").convert()
        cursor_image = pygame.image.load("images/cursor.png")

        pygame.mouse.set_visible(False)
        
        self.running = True

        clock = pygame.time.Clock()
        global_time = 0

        self.check_state = 'starter menu' # по умолчанию изначально вызываем старт. меню

        self.initialization_buttons()

        while self.running:
            self.states[self.check_state]()
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(cursor_image, mouse_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            global_time += clock.tick()
            pygame.display.flip()
        pygame.quit()

    def initialization_buttons(self):
        self.size_new_game = (200, 50)
        self.positions_new_game = (self.size[0] // 2 - (self.size_new_game[0] // 2),
                                   self.size[1] // 2 - (self.size_new_game[1] // 2) - 75)
        self.new_game = Button(self.positions_new_game, (915, 455),
                               self.size_new_game,
                               (179, 179, 179), (0, 0, 0), 'Trebuchet MS',
                               'Новая игра', self.screen)

        self.size_download_game = (200, 50)
        self.positions_download_game = (self.size[0] // 2 - (self.size_download_game[0] // 2),
                                        self.size[1] // 2 - (self.size_download_game[1] // 2) - 15)
        self.download_game = Button(self.positions_download_game, (895, 515),
                                    self.size_download_game,
                                    (179, 179, 179), (0, 0, 0), 'Trebuchet MS',
                                    'Загрузить игру', self.screen)

        self.size_settings = (200, 50)
        self.positions_settings = (self.size[0] // 2 - (self.size_settings[0] // 2),
                                   self.size[1] // 2 - (self.size_settings[1] // 2) + 45)
        self.settings_button = Button(self.positions_settings, (915, 575),
                                      self.size_settings,
                                      (179, 179, 179), (0, 0, 0), 'Trebuchet MS',
                                      'Настройки', self.screen)

        self.size_exit = (200, 50)
        self.positions_exit = (self.size[0] // 2 - (self.size_exit[0] // 2),
                               self.size[1] // 2 - (self.size_exit[1] // 2) + 105)
        self.exit_button = Button(self.positions_exit, (935, 635),
                                  self.size_exit,
                                  (179, 179, 179), (0, 0, 0), 'Trebuchet MS',
                                  'Выйти', self.screen)

    def render_starter_menu(self):
        self.screen.blit(self.starter_image, self.starter_position)

        self.new_game.draw_button()
        self.download_game.draw_button()
        self.exit_button.draw_button()
        self.settings_button.draw_button()
        
        mouse_position = pygame.mouse.get_pos()
        is_clicked_mouse = pygame.mouse.get_pressed()

        # Длинная проверка нахождения мышки на кнопке "новая игра"
        if (mouse_position[0] >= self.positions_new_game[0] and\
        mouse_position[0] <= self.size_new_game[0] + self.positions_new_game[0]) and\
        (mouse_position[1] >= self.positions_new_game[1] and\
        mouse_position[1] <= self.size_new_game[1] + self.positions_new_game[1]):
            self.new_game.draw_active_button()
            if is_clicked_mouse[0] is True:
                self.check_state = 'new game'

        # Длинная проверка нахождения мышки на кнопке "загрузить игру"
        if (mouse_position[0] >= self.positions_download_game[0] and\
        mouse_position[0] <= self.size_download_game[0] + self.positions_download_game[0]) and\
        (mouse_position[1] >= self.positions_download_game[1] and\
        mouse_position[1] <= self.size_download_game[1] + self.positions_download_game[1]):
            self.download_game.draw_active_button()
            if is_clicked_mouse[0] is True:
                self.check_state = 'download game'

        # Длинная проверка нахождения мышки на кнопке "настройки"
        if (mouse_position[0] >= self.positions_settings[0] and\
        mouse_position[0] <= self.size_settings[0] + self.positions_settings[0]) and\
        (mouse_position[1] >= self.positions_settings[1] and\
        mouse_position[1] <= self.size_settings[1] + self.positions_settings[1]):
            self.settings_button.draw_active_button()
            if is_clicked_mouse[0] is True:
                self.check_state = 'settings'

        # Длинная проверка нахождения мышки на кнопке "выход"
        if (mouse_position[0] >= self.positions_exit[0] and\
        mouse_position[0] <= self.size_exit[0] + self.positions_exit[0]) and\
        (mouse_position[1] >= self.positions_exit[1] and\
        mouse_position[1] <= self.size_exit[1] + self.positions_exit[1]):
            self.exit_button.draw_active_button()
            if is_clicked_mouse[0] is True:
                self.running = False

    def render_menu_download_game(self):
        self.screen.blit(self.starter_image, self.starter_position)
    
    def render_settings_menu(self):
        self.render_starter_menu()

    def render_game_lvl_first(self):
        pass

    def render_game_lvl_second(self):
        pass

    def render_game_lvl_third(self):
        pass


class Button:
    def __init__(self, pos, text_pos, size, color_for_button, color_for_text, font, text, screen):
        self.x, self.y = pos
        self.width, self.height = size
        self.pos_for_text = text_pos

        self.color_for_draw = color_for_button
        self.color_for_text = color_for_text

        self.screen = screen

        self.font = font
        self.text = text
        self.size_text = 18

    def print_text_on_button(self):
        self.screen.blit(pygame.font.SysFont(self.font, self.size_text, bold=True).render(self.text, True,
                         self.color_for_text), self.pos_for_text)

    def draw_button(self):
        pygame.draw.rect(self.screen, self.color_for_draw,
                        (self.x, self.y, self.width, self.height))
        self.print_text_on_button()

    def draw_active_button(self):
        pygame.draw.rect(self.screen, COLOR_ACTIVE_BUTTON,
                        (self.x, self.y, self.width, self.height))
        self.print_text_on_button()


class InputText:
    def __init__(self):
        pass


if __name__ == '__main__':
    size = width, height = 1920, 1080
    mw = MainWindow(size)