import random
import sys
import pygame


def debug(message: str):
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont("Arial", 15)
    text = font.render(f"{message}", True, "white")
    screen.blit(text, [10, 10])


class Player:
    def __init__(self, name: str, color: pygame.color.Color):
        super().__init__()
        self.name = name
        self.color = color
        self.speed = 60

        self.pos = pygame.Vector2(random.randint(20, 620), 300)
        self.direction = pygame.Vector2(0, 0)

    def player_input(self, dt: float):
        pass

    def move_left(self, dt: float):
        self.direction -= pygame.Vector2(self.speed * dt, 0)

    def move_right(self, dt: float):
        self.direction += pygame.Vector2(self.speed * dt, 0)

    def move_up(self, dt: float):
        self.direction -= pygame.Vector2(0, self.speed * dt)

    def move_down(self, dt: float):
        self.direction += pygame.Vector2(0, self.speed * dt)

    def update(self, surface: pygame.surface.Surface, dt: float):
        self.player_input(dt)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.pos += self.direction
        pygame.draw.rect(surface, self.color, (self.pos[0], self.pos[1], 30, 30))
        self.direction = pygame.Vector2(0, 0)


class Player1(Player):
    def player_input(self, dt: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move_left(dt)
        if keys[pygame.K_d]:
            self.move_right(dt)
        if keys[pygame.K_w]:
            self.move_up(dt)
        if keys[pygame.K_s]:
            self.move_down(dt)


class Player2(Player):
    def player_input(self, dt: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j]:
            self.move_left(dt)
        if keys[pygame.K_l]:
            self.move_right(dt)
        if keys[pygame.K_i]:
            self.move_up(dt)
        if keys[pygame.K_k]:
            self.move_down(dt)


class GameWindow:
    def __init__(self):
        pygame.init()
        self.window_surface = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        self.player1 = Player1("P1", "blue")
        self.player2 = Player2("P2", "orange")

    def run(self):
        dt = 0.0
        while True:
            self.window_surface.fill("black")

            for event in pygame.event.get([pygame.QUIT]):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player1.update(self.window_surface, dt)
            self.player2.update(self.window_surface, dt)

            pygame.display.flip()
            dt = self.clock.tick(60) / 1000


if __name__ == "__main__":
    game = GameWindow()
    game.run()
