import random
import sys
from types import TracebackType
from typing import List, Tuple
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

GAME_SCENE_WIDTH = 1280
GAME_SCENE_HEIGHT = 960


def debug(message: str, surface: pygame.Surface):
    font = pygame.font.SysFont("Arial", 15)
    text = font.render(f"{message}", True, "white")
    surface.blit(text, [10, 10])


class Player:
    def __init__(
        self,
        name: str = "P1",
        color: pygame.color.Color = "blue",
        left_key: int = pygame.K_a,
        right_key: int = pygame.K_d,
        up_key: int = pygame.K_w,
        down_key: int = pygame.K_s,
    ):
        # setup
        self.name = name
        self.color = color
        self.speed = 60

        # position
        self.pos = pygame.Vector2(
            random.randint(20, GAME_SCENE_WIDTH - 20),
            random.randint(20, GAME_SCENE_HEIGHT - 20),
        )
        self.direction = pygame.Vector2(0, 0)

        # control
        self.left_key = left_key
        self.right_key = right_key
        self.up_key = up_key
        self.down_key = down_key

    def player_input(self, dt: float):
        keys = pygame.key.get_pressed()
        if keys[self.left_key]:
            self.move_left(dt)
        if keys[self.right_key]:
            self.move_right(dt)
        if keys[self.up_key]:
            self.move_up(dt)
        if keys[self.down_key]:
            self.move_down(dt)

    def move_left(self, dt: float):
        self.direction -= pygame.Vector2(self.speed * dt, 0)

    def move_right(self, dt: float):
        self.direction += pygame.Vector2(self.speed * dt, 0)

    def move_up(self, dt: float):
        self.direction -= pygame.Vector2(0, self.speed * dt)

    def move_down(self, dt: float):
        self.direction += pygame.Vector2(0, self.speed * dt)

    def update(self, dt: float):
        self.player_input(dt)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.pos += self.direction
        self.direction = pygame.Vector2(0, 0)


class GameScene:
    def __init__(self, players: List[Player]):
        self.scene_surface = pygame.Surface((GAME_SCENE_WIDTH, GAME_SCENE_HEIGHT))
        self.players = players

    def update(self, dt: float):
        for player in self.players:
            player.update(dt)


class Scene1(GameScene):
    def __init__(self, players: List[Player]):
        super().__init__(players)

        self.bg = pygame.Surface(self.scene_surface.get_size())

        ar = pygame.PixelArray(self.bg)
        for x in range(self.bg.get_width()):
            c = x / self.bg.get_width() * 255
            r, g, b = c, c, c
            ar[x, :] = (r, g, b)

    def update(self, dt: float):
        super().update(dt)
        self.scene_surface.fill("green")
        self.scene_surface.blit(self.bg, (0, 0))
        for player in self.players:
            pygame.draw.rect(
                self.scene_surface, player.color, (player.pos[0], player.pos[1], 30, 30)
            )


class GameWindow:
    instance = None

    def __new__(cls, *args, **kwds):
        """Return an open Pygame window"""

        if GameWindow.instance is not None:
            return GameWindow.instance
        self = object.__new__(cls)
        pygame.init()
        self.window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player1 = Player()
        self.player2 = Player(
            "P2", "orange", pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k
        )
        self.camera1 = Camera(self.player1, (0, 0))
        self.camera2 = Camera(self.player2, (0, SCREEN_HEIGHT // 2))
        self.set_scene()
        GameWindow.instance = self
        return self

    def __enter__(self):
        return self

    def __exit__(
        self, exc_type: type, exc_value: Exception, exc_traceback: TracebackType
    ):
        self.close()
        return False

    def close(self):
        pygame.quit()
        GameWindow.instance = None

    def set_scene(self):
        self.scene = Scene1([self.player1, self.player2])

    def run(self):
        dt = 0.0
        while True:
            self.window_surface.fill("black")

            for event in pygame.event.get([pygame.QUIT]):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.scene.update(dt)
            self.camera1.update(self.scene.scene_surface)
            self.camera2.update(self.scene.scene_surface)

            pygame.display.update()
            dt = self.clock.tick(60) / 1000


class Camera:
    def __init__(self, player: Player, screen_pos: Tuple[int, int]):
        self.offset = pygame.Vector2()
        self.center_pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 // 2)
        self.player = player
        self.screen_pos = screen_pos
        self.internal_surface = pygame.Surface((SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3))

    def center_target_camera(self):
        self.offset = self.center_pos - self.player.pos

    def update(self, scene_surface: pygame.Surface):
        self.internal_surface.fill("red")
        self.center_target_camera()
        self.internal_surface.blit(scene_surface, self.offset)
        debug(f"{self.player.name} {self.offset}", self.internal_surface)
        GameWindow().window_surface.blit(
            self.internal_surface, (self.screen_pos[0], self.screen_pos[1])
        )


if __name__ == "__main__":
    with GameWindow() as game:
        game.run()
