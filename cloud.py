import pygame
from random import randint


class Cloud(pygame.sprite.Sprite):
    '''
    A Cloud object contains the behaviour of a cloud in the game

    Attributes:
        image: The current image to be displayed
        rect: A rectangle object to aid in the positioning of the image 
    '''
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('images/cloud.png')

        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_rect(midbottom=(randint(1000, 1200), randint(50, 150)))

    def __remove_cloud(self):
        '''
        Remove cloud objects that are no longer visible on the screen
        '''
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        '''
        Update the state of a cloud
        '''
        self.rect.x -= 3.5
        self.__remove_cloud()
