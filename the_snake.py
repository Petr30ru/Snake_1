from random import choice
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_POSITION = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 7


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, position=None, body_color=None) -> None:
        """Метод инициализирует базовые атрибуты объекта,
        такие как его позиция и цвет.
        """
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Метод-заготовка для отрисовки объекта на игровом поле."""
        raise NotImplementedError(
            'Определите draw в %s.' % self.__class__.__name__)

    @staticmethod
    def draw_rect(positions, body_color) -> None:
        """Метод для отрисовки rect"""
        rect = pygame.Rect(positions, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс описывающий яблоко и действия с ним"""

    def __init__(self, position=None, body_color=None) -> None:
        """Метод инициализирует базовые атрибуты объекта"""
        super().__init__(position, body_color)
        if position is None:
            self.position = self.randomize_position(START_POSITION)
        if body_color is None:
            self.body_color = APPLE_COLOR

    def draw(self) -> None:
        """Метод для отрисовки яблока на игровой поверхности"""
        self.draw_rect(self.position, self.body_color)

    @staticmethod
    def randomize_position(snake_positions: list) -> tuple[int, int]:
        """Метод для получения случайного положения яблока на игровом поле"""
        while True:
            x_pos = choice(range(0, SCREEN_WIDTH, GRID_SIZE))
            y_pos = choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
            if (x_pos, y_pos) not in snake_positions:
                break
        return x_pos, y_pos


class Snake(GameObject):
    """Класс описывающий змейку и её поведение"""

    direction = RIGHT
    next_direction = None
    last = None

    def __init__(self, position=None, body_color=None) -> None:
        """Инициализирует начальное состояние змейки"""
        super().__init__(position, body_color)
        if position is None:
            self.position = START_POSITION[0]
        if body_color is None:
            self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = START_POSITION

    def update_direction(self) -> None:
        """Метод обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Отрисовывает змейку на экране, затирая след."""
        for positions in self.positions[:-1]:
            self.draw_rect(positions, SNAKE_COLOR)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)

        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self) -> tuple[int, int]:
        """Возвращает новые координаты головы змейки."""
        x_head, y_head = self.get_head_position()
        if self.direction == RIGHT:
            return x_head + GRID_SIZE, y_head
        if self.direction == LEFT:
            return x_head - GRID_SIZE, y_head
        if self.direction == UP:
            return x_head, y_head - GRID_SIZE
        if self.direction == DOWN:
            return x_head, y_head + GRID_SIZE

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        for positions in self.positions:
            last_rect = pygame.Rect(positions, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object) -> None:
    """Метод для обработки нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


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

        new_head_positions = snake.move()
        if new_head_positions in snake.positions:
            snake.reset()
        snake.positions.insert(0, new_head_positions)
        if new_head_positions == apple.position:
            apple.position = apple.randomize_position(snake.positions)
        else:
            snake.last = snake.positions[-1]
            snake.positions.pop()

        pygame.display.update()
        snake.update_direction()


if __name__ == '__main__':
    main()
