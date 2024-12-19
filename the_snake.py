from random import choice
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, DIR_MOVE
from config import APPLE_COLOR, SNAKE_COLOR, BORDER_COLOR, BOARD_BACKGROUND_COLOR, SPEED

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self) -> None:
        """Метод инициализирует базовые атрибуты объекта,
        такие как его позиция и цвет.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self) -> None:
        """Метод-заготовка для отрисовки объекта на игровом поле."""
        pass


class Apple(GameObject):
    """Класс описывающий яблоко и действия с ним"""

    def __init__(self) -> None:
        """Метод инициализирует базовые атрибуты объекта"""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = Apple.randomize_position()

    def draw(self) -> None:
        """Метод для отрисовки яблока на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @staticmethod
    def randomize_position() -> tuple[int, int]:
        """Метод для получения случайного положения яблока на игровом поле"""
        x_pos = choice(range(0, SCREEN_WIDTH, GRID_SIZE))
        y_pos = choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
        return x_pos, y_pos


class Snake(GameObject):
    """Класс описывающий змейку и её поведение"""

    positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    direction = DIR_MOVE['RIGHT']
    next_direction = None

    def __init__(self) -> None:
        """Инициализирует начальное состояние змейки"""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.last = None
        self.length = 1

    def update_direction(self) -> None:
        """Метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple, new_head_snake) -> None:
        """Обновляет позицию змейки (координаты каждой
        секции), добавляя новую голову в начало списка positions и
        удаляя последний элемент, если длина змейки не
        увеличилась.
        """
        self.positions.insert(0, new_head_snake)
        if self.check_eat_apple(apple):
            apple.position = apple.randomize_position()
        else:
            self.last = self.positions[-1]
            self.positions.pop()

    def check_move(self, apple) -> None:
        """Метод для проверки того не врезалась ли змейка в себя."""
        new_head_snake = self.get_new_head_position()
        if new_head_snake in self.positions:
            self.reset()
        else:
            self.move(apple, new_head_snake)

    def draw(self) -> None:
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)

        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_new_head_position(self) -> tuple[int, int]:
        """Возвращает новые координаты головы змейки."""
        x_head, y_head = self.get_head_position()
        if self.direction == DIR_MOVE['RIGHT']:
            return x_head + 20, y_head
        if self.direction == DIR_MOVE['LEFT']:
            return x_head - 20, y_head
        if self.direction == DIR_MOVE['UP']:
            return x_head, y_head - 20
        if self.direction == DIR_MOVE['DOWN']:
            return x_head, y_head + 20

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def check_eat_apple(self, apple) -> bool:
        """Проверка на поедание яблока"""
        if apple.position == self.get_head_position():
            return True
        return False

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        for position in self.positions:
            last_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = DIR_MOVE['RIGHT']
        self.next_direction = None


def handle_keys(game_object) -> None:
    """Метод для обработки нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DIR_MOVE['DOWN']:
                game_object.next_direction = DIR_MOVE['UP']
            elif event.key == pygame.K_DOWN and game_object.direction != DIR_MOVE['UP']:
                game_object.next_direction = DIR_MOVE['DOWN']
            elif event.key == pygame.K_LEFT and game_object.direction != DIR_MOVE['RIGHT']:
                game_object.next_direction = DIR_MOVE['LEFT']
            elif event.key == pygame.K_RIGHT and game_object.direction != DIR_MOVE['LEFT']:
                game_object.next_direction = DIR_MOVE['RIGHT']


def main():
    """Главный класс."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.check_move(apple)
        pygame.display.update()
        snake.update_direction()


if __name__ == '__main__':
    main()
