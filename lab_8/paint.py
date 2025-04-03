import pygame
import sys
import math
pygame.init()

# Инициализация экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple paint')

# Определение цветов
white = (255, 255, 255)
black = (0, 0 , 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

# Класс для кнопок
class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 12, self.rect.y + 12))

    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

# Функции для выбора цвета и инструментов
drawing = False
brush_color = black
shape = 'Draw'  # Изменено на 'Draw' по умолчанию

def set_black():
    global brush_color, shape
    brush_color = black
    shape = 'Draw'  # При выборе цвета, снова активируем рисование

def set_green():
    global brush_color, shape
    brush_color = green
    shape = 'Draw'  # При выборе цвета, снова активируем рисование

def set_red():
    global brush_color, shape
    brush_color = red
    shape = 'Draw'  # При выборе цвета, снова активируем рисование

def set_blue():
    global brush_color, shape
    brush_color = blue
    shape = 'Draw'  # При выборе цвета, снова активируем рисование

def set_eraser():
    global shape
    shape = 'Eraser'  # При выборе ластика, активируем ластик

def clear_screen():
    screen.fill(white)

def exit_app():
    pygame.quit()
    sys.exit()

# Создание кнопок
buttons = [
    Button(10, 10, 60, 30, 'Black', black, set_black),
    Button(80, 10, 60, 30, 'Green', green, set_green),
    Button(150, 10, 60, 30, 'Red', red, set_red),
    Button(220, 10, 60, 30, 'Blue', blue, set_blue),
    Button(290, 10, 60, 30, 'Eraser', gray, set_eraser),
    Button(360, 10, 60, 30, 'Clear', gray, clear_screen),
    Button(430, 10, 60, 30, 'Exit', gray, exit_app)
]

# Очистка экрана при старте
clear_screen()

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False

        # Проверяем действия для каждой кнопки
        for button in buttons:
            button.check_action(event)

    if drawing:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 50:  # Убедимся, что рисуем только ниже панели
            if shape == 'Eraser':  # Если выбран ластик
                pygame.draw.circle(screen, white, (mouse_x, mouse_y), 10)
            else:  # Если рисуем
                pygame.draw.circle(screen, brush_color, (mouse_x, mouse_y), 5)

    # Отображаем панель инструментов
    pygame.draw.rect(screen, gray, (0, 0, width, 50))
    for button in buttons:
        button.draw(screen)  # Отображаем кнопки

    pygame.display.flip()
