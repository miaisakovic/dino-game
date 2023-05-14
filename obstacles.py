import pygame
from random import randint

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, obstacle):
        super().__init__()

        self.type = obstacle

        if obstacle == 'pterodactyl':
            pterodactyl_1 = pygame.image.load('images/pterodactyl/pterodactyl_1.png')
            pterodactyl_2 = pygame.image.load('images/pterodactyl/pterodactyl_2.png')
            self.pterodactyls = [pterodactyl_1, pterodactyl_2]
            self.index = 0
            self.image = self.pterodactyls[self.index]
            y_pos = 110
        else:
            self.image = pygame.image.load(f'images/cactus/{obstacle}.png')
            y_pos = 223
        
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_rect(midbottom = (randint(1000, 1200), y_pos))
    
    def animate_pterodactyl(self):
        if self.type == 'pterodactyl':
            self.index += 0.1
            if self.index >= len(self.pterodactyls): 
                self.index = 0
            self.image = self.pterodactyls[int(self.index)]
            self.image = pygame.transform.scale_by(self.image, 1.5)

    def remove_obstacle(self):
        # If the obstacle is no longer visible, remove it
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animate_pterodactyl()
        self.rect.x -= 6.5
        self.remove_obstacle()
