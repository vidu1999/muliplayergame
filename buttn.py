import pygame

from main import intface


class Buttn:
    def mdown(self):
        if pygame.mouse.get_pressed():
            print(pygame.mouse.get_pos()[0] // 60, pygame.mouse.get_pos()[1] // 60)
            img = pygame.image.load('E:/vkj/multigame/tank.png')
            position = (pygame.mouse.get_pos()[0] // 60 * 60, pygame.mouse.get_pos()[1] // 60 * 60)
            print(position)
            intface.blit(img, position)
            pygame.display.update()