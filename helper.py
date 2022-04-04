import pygame


def debug(message: str, surface: pygame.Surface):
    font = pygame.font.SysFont("Arial", 15)
    text = font.render(f"{message}", True, "white")
    surface.blit(text, [10, 10])
