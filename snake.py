import pygame
from pygame.math import Vector2
import random

pygame.init()

# Configuración de la pantalla
height = 720
width = 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')

# Clase principal del juego de la serpiente
class SnakeGame:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # Posiciones iniciales
        self.direction = Vector2(1, 0)  # Dirección inicial (derecha)
        self.add_block = False  # Controla el crecimiento de la serpiente

    def draw(self):
        for block in self.body:
            pygame.draw.rect(window, (0, 255, 0), (block.x * 20, block.y * 20, 20, 20))

    def move(self):
        # Crear una nueva lista basada en el cuerpo actual
        new_body = self.body[:]
        # Insertar un nuevo bloque al frente
        new_body.insert(0, new_body[0] + self.direction)

        # Si no se va a agregar un bloque, eliminar el último segmento
        if not self.add_block:
            new_body.pop()

        # Actualizar el cuerpo de la serpiente y restablecer `add_block`
        self.body = new_body
        self.add_block = False

    def move_up(self):
        if self.direction != Vector2(0, 1):  # Impide ir hacia abajo
            self.direction = Vector2(0, -1)

    def move_down(self):
        if self.direction != Vector2(0, -1):  # Impide ir hacia arriba
            self.direction = Vector2(0, 1)

    def move_left(self):
        if self.direction != Vector2(1, 0):  # Impide ir hacia la derecha
            self.direction = Vector2(-1, 0)

    def move_right(self):
        if self.direction != Vector2(-1, 0):  # Impide ir hacia la izquierda
            self.direction = Vector2(1, 0)

    def die(self):
        # Verificar si la serpiente choca contra las paredes
        if (
            self.body[0].x < 0
            or self.body[0].y < 0
            or self.body[0].x >= width / 20
            or self.body[0].y >= height / 20
        ):
            print("Game Over: Snake hit the wall!")
            return True

        # Verificar si la cabeza de la serpiente colisiona con su cuerpo
        for block in self.body[1:]:
            if block == self.body[0]:
                print("Game Over: Snake collided with itself!")
                return True

        return False

# Clase para la manzana
class Apple:
    def __init__(self):
        self.generate()

    def generate(self):
        while True:
            self.x = random.randint(0, width // 20 - 1)
            self.y = random.randint(0, height // 20 - 1)
            self.position = Vector2(self.x, self.y)
            # Evitar que la manzana se genere dentro del cuerpo de la serpiente
            if self.position not in snake.body:
                break

    def draw(self):
        pygame.draw.rect(window, (255, 0, 0), (self.position.x * 20, self.position.y * 20, 20, 20))

    def check_collision(self, snake):
        if snake.body[0] == self.position:
            self.generate()
            snake.add_block = True
            return True
        return False

# Función principal
def main():
    global snake  # Necesario para evitar errores al referenciar 'snake' en Apple
    snake = SnakeGame()
    apple = Apple()
    score = 0
    fps = pygame.time.Clock()

    while True:
        fps.tick(30)  # Velocidad del juego (30 FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.move_up()
                elif event.key == pygame.K_DOWN:
                    snake.move_down()
                elif event.key == pygame.K_LEFT:
                    snake.move_left()
                elif event.key == pygame.K_RIGHT:
                    snake.move_right()

        if snake.die():
            print(f"Final Score: {score}")
            pygame.quit()
            return

        if apple.check_collision(snake):
            score += 1
            print(f"Score: {score}")

        window.fill((0, 0, 0))  # Fondo negro
        snake.move()
        snake.draw()
        apple.draw()
        pygame.display.update()

main()