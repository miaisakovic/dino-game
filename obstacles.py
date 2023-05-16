import pygame
from random import randint


class Obstacles(pygame.sprite.Sprite):
    '''
    An Obstacles object contains the behaviour of a cactus or pterodactyl in the game

    Args:
        obstacle: A string that specifies whether the object is a pterodactyl 
            or a cactus

    Attributes:
        type: Stores the provided obstacle argument 
        pterodactyls: A list of two pterodactyl image surfaces 
            (only available when the argument 'pterodactyl' has been passed)
        index: An integer that specifies which element to display in the pterodactyls list
            (only available when the argument 'pterodactyl' has been passed)
        image: The current image to be displayed
        rect: A rectangle object to aid in the positioning of the image 
    '''
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
        self.rect = self.image.get_rect(midbottom=(randint(1000, 1200), y_pos))

    def __animate_pterodactyl(self):
        '''
        Update the pterodactyl's image surface so that it appears to fly
        '''
        if self.type == 'pterodactyl':
            self.index += 0.1
            if self.index >= len(self.pterodactyls):
                self.index = 0
            self.image = self.pterodactyls[int(self.index)]
            self.image = pygame.transform.scale_by(self.image, 1.5)

    def __remove_obstacle(self):
        '''
        Remove pterodactyl and cactus objects that are no longer visible on the screen
        '''
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        '''
        Update the state of an obstacle 
        '''
        self.__animate_pterodactyl()
        self.rect.x -= 6.5
        self.__remove_obstacle()
