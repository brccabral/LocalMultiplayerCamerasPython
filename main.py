import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from camera import Camera
from game import Scene1


class GameWindow:
    def __init__(self):
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

            self.window_surface.blit(
                self.camera1.camera_surface, self.camera1.screen_pos
            )
            self.window_surface.blit(
                self.camera2.camera_surface, self.camera2.screen_pos
            )

            pygame.display.update()
            dt = self.clock.tick(60) / 1000


if __name__ == "__main__":
    game = GameWindow()
    game.run()
