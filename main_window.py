import pygame
from artificial_intelligence import GameBot
from backend import (PlayersColony, PeacefulColony, EnemyColony, ActionWithTable,
                     get_right_and_left_pos)

COLOR_ACTIVE_BUTTON = (231, 238, 255)


class MainWindow:
    def __init__(self, size):
        self.starter_position = (0, 0)
        self.size = size

        self.font = 'Trebuchet MS'
        self.color_for_text = (0, 0, 0)

        self.states = {'starter menu': self.render_starter_menu,
                       'new game': self.render_rules,
                       'download game': self.render_menu_download_game,
                       'settings': self.render_settings_menu}

        self.InitUI()

    def InitUI(self):
        pygame.init()
        pygame.display.set_caption('Колонизация')
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        self.starter_image = pygame.image.load("images/start_image.png").convert()
        cursor_image = pygame.image.load("images/cursor.png")

        pygame.mouse.set_visible(False)

        self.running = True

        self.saves = ActionWithTable('saves.csv').get_dict()

        clock = pygame.time.Clock()
        global_time = 0

        self.check_state = 'starter menu'  # по умолчанию изначально вызываем старт. меню

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

    def check_pos_on_button(self, mouse_pos, button_xy, button_size):
        if (mouse_pos[0] >= button_xy[0] and mouse_pos[0] <= button_size[0] + button_xy[0]) \
                and (mouse_pos[1] >= button_xy[1] and mouse_pos[1] <= button_size[1] + button_xy[1]):
            return True
        return False

    def initialization_buttons(self):
        self.size_new_game = (200, 50)
        self.positions_new_game = (self.size[0] // 2 - (self.size_new_game[0] // 2),
                                   self.size[1] // 2 - (self.size_new_game[1] // 2) - 75)
        self.new_game = Button(self.positions_new_game, (915, 455),
                               self.size_new_game,
                               (179, 179, 179), self.color_for_text, self.font,
                               'Новая игра', self.screen)

        self.size_download_game = (200, 50)
        self.positions_download_game = (self.size[0] // 2 - (self.size_download_game[0] // 2),
                                        self.size[1] // 2 - (self.size_download_game[1] // 2) - 15)
        self.download_game = Button(self.positions_download_game, (895, 515),
                                    self.size_download_game,
                                    (179, 179, 179), self.color_for_text, self.font,
                                    'Загрузить игру', self.screen)

        self.size_settings = (200, 50)
        self.positions_settings = (self.size[0] // 2 - (self.size_settings[0] // 2),
                                   self.size[1] // 2 - (self.size_settings[1] // 2) + 45)
        self.settings_button = Button(self.positions_settings, (915, 575),
                                      self.size_settings,
                                      (179, 179, 179), self.color_for_text, self.font,
                                      'Настройки', self.screen)

        self.size_exit = (200, 50)
        self.positions_exit = (self.size[0] // 2 - (self.size_exit[0] // 2),
                               self.size[1] // 2 - (self.size_exit[1] // 2) + 105)
        self.exit_button = Button(self.positions_exit, (935, 635),
                                  self.size_exit,
                                  (179, 179, 179), self.color_for_text, self.font,
                                  'Выйти', self.screen)

    def render_starter_menu(self):
        self.screen.blit(self.starter_image, self.starter_position)

        self.new_game.draw_button()
        self.download_game.draw_button()
        self.exit_button.draw_button()
        self.settings_button.draw_button()

        mouse_position = pygame.mouse.get_pos()
        is_clicked_mouse = pygame.mouse.get_pressed()

        if self.check_pos_on_button(mouse_position, self.positions_new_game,
                                    self.size_new_game):
            self.new_game.draw_active_button()
            if is_clicked_mouse[0] is True:
                pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                self.check_state = 'new game'

        if self.check_pos_on_button(mouse_position, self.positions_download_game,
                                    self.size_download_game):
            self.download_game.draw_active_button()
            if is_clicked_mouse[0] is True:
                pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                self.check_state = 'download game'

        if self.check_pos_on_button(mouse_position, self.positions_settings,
                                    self.size_settings):
            self.settings_button.draw_active_button()
            if is_clicked_mouse[0] is True:
                pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                self.check_state = 'settings'

        if self.check_pos_on_button(mouse_position, self.positions_exit,
                                    self.size_exit):
            self.exit_button.draw_active_button()
            if is_clicked_mouse[0] is True:
                pygame.mixer.Sound.play(pygame.mixer.Sound(r'sounds\click_on_button.mp3'))
                pygame.time.delay(275)
                self.running = False

    def render_menu_download_game(self):
        self.screen.blit(self.starter_image, self.starter_position)

        board = DrawBoard(r'GameLevels\Board1.txt', self.screen)
        board.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.check_state = 'starter menu'

    def render_settings_menu(self):
        self.screen.blit(self.starter_image, self.starter_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.check_state = 'starter menu'

    def render_rules(self):
        color_for_draw = (231, 238, 255)
        pos_for_rect = (50, 50)
        size = (1820, 980)
        alpha_level = 100

        rect = pygame.Surface(size)
        rect.set_alpha(alpha_level)
        rect.fill(color_for_draw)

        self.screen.blit(self.starter_image, self.starter_position)
        self.screen.blit(rect, pos_for_rect)

        pos_for_text = [55, 50]
        size_text = 29
        text = ['Суть игры:', '', 'Уважаемый игрок, приветствуем Вас в игре "Колонизация"',
                'В ходе игры Вам предстоит решать различного рода стратегические головоломки, совершая некоторые логические',
                'умозаключения, чтобы победить соперников и ' +
                'расширить свое превосходство над своими оппонентами.',
                'Вы можете сражаться за территории (колонии), уничтожать злостных врагов ' +
                'и защищать границы своих земель.',
                'Требуется захватывать колонии, которые предстают ' +
                'прямоугольниками некоторого размера на игровом поле.',
                'В дальнейшем же, чтобы победить, требуется захвать все имеющиеся ' +
                'на поле колонии.']

        for i in range(len(text)):
            self.screen.blit(pygame.font.SysFont(self.font, size_text, bold=True).render(text[i], True,
                                                                                         self.color_for_text),
                             tuple(pos_for_text))
            pos_for_text[1] += 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.check_state = 'starter menu'

    def render_endgame(self):
        # Реализовать бег спрайтов в титрах с учётом коллайда и анимаций
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
                                                                                          self.color_for_text),
                         self.pos_for_text)

    def draw_button(self):
        pygame.draw.rect(self.screen, self.color_for_draw,
                         (self.x, self.y, self.width, self.height))
        self.print_text_on_button()

    def draw_active_button(self):
        pygame.draw.rect(self.screen, COLOR_ACTIVE_BUTTON,
                         (self.x, self.y, self.width, self.height))
        self.print_text_on_button()


class DrawBoard:
    def __init__(self, filename, screen):
        self.filename = filename
        self.screen = screen

        self.nums_from_matrix = ActionWithTable(self.filename).get_nums_from_matrix()
        self.matrix = ActionWithTable(self.filename).get_matrix()

        self.color_rect = (0, 0, 0)

    def draw(self):
        for i in self.nums_from_matrix:
            pos = get_right_and_left_pos(self.matrix, i)

            x = 50 + pos[0][0] * 50
            y = 50 + pos[0][1] * 50

            width = (pos[1][0] - pos[0][0]) * 50
            height = (pos[1][1] - pos[0][1]) * 50

            pygame.draw.rect(self.screen, self.color_rect,
                            (x, y, width, height))


if __name__ == '__main__':
    size = width, height = 1920, 1080
    mw = MainWindow(size)