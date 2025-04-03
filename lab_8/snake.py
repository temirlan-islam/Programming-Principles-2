import pygame
import sys
import random

pygame.init()

# Размеры экрана и ячеек
width, height = 500, 500
cell_size = 10

# Настройка экрана
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Snake')

# Определение цветов для игры
black = (0, 0 , 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Начальная позиция змеи
snake_pos = [100, 100]
snake_body = [[100, 100], [80, 100], [60, 100]]  # Змейка состоит из нескольких сегментов
direction = 'RIGHT'  # Направление движения змеи
change_to = direction  # Направление будет изменяться в ходе игры

# Начальная позиция еды
food_pos = [random.randrange(0, width, cell_size), random.randrange(0, height, cell_size)]
food_spawn = True  # Флаг, определяющий, нужно ли генерировать новую еду

# Переменная для счета
score = 0

# Шрифт для отображения счета
font = pygame.font.Font(None, 36)

# Таймер для контроля скорости игры
clock = pygame.time.Clock()

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка на закрытие окна
            running = False
        elif event.type == pygame.KEYDOWN:  # Обработка нажатий клавиш
            if event.key == pygame.K_UP and direction != 'DOWN':  # Если нажата клавиша "вверх"
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':  # Если нажата клавиша "вниз"
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':  # Если нажата клавиша "вправо"
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':  # Если нажата клавиша "влево"
                change_to = 'LEFT'
    
    # Обновление направления змеи
    direction = change_to

    # Движение змеи в зависимости от направления
    if direction == 'UP':
        snake_pos[1] -= cell_size
    elif direction == 'DOWN':
        snake_pos[1] += cell_size
    elif direction == 'LEFT':
        snake_pos[0] -= cell_size
    elif direction == 'RIGHT':
        snake_pos[0] += cell_size

    # Проверка на выход змеи за границы экрана и перемещение её с другой стороны
    if snake_pos[0] < 0:
        snake_pos[0] = width - cell_size
    elif snake_pos[0] >= width:
        snake_pos[0] = 0
    elif snake_pos[1] < 0:
        snake_pos[1] = height - cell_size
    elif snake_pos[1] >= height:
        snake_pos[1] = 0
    
    # Добавление новой головы змеи
    snake_body.insert(0, list(snake_pos))

    # Проверка, съела ли змея еду
    if snake_pos == food_pos:
        food_spawn = False  # Нужно создать новую еду
        score += 1  # Увеличиваем счет
    else:
        snake_body.pop()  # Удаляем последний сегмент тела змеи, если еда не съедена

    # Если еда съедена, генерируем новое место для еды
    if not food_spawn:
        food_pos = [random.randrange(0, width, cell_size), random.randrange(0, height, cell_size)]
    food_spawn = True

    # Проверка на столкновение с телом змеи (если голова встретила тело)
    if snake_pos in snake_body[1:]:
        running = False  # Игра заканчивается

    # Отрисовка экрана
    screen.fill(black)  # Заливаем экран черным цветом
    for segment in snake_body:  # Отрисовываем все сегменты змеи
        pygame.draw.rect(screen, green, pygame.Rect(segment[0], segment[1], cell_size, cell_size))
    
    # Отрисовываем еду
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], cell_size, cell_size))

    # Отображение счета
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

    # Контроль за скоростью игры
    clock.tick(20)

# Завершение игры
pygame.quit()
sys.exit()
