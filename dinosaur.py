import pygame


class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        dino_1 = pygame.image.load('images/dino/dino_walk_1.png')
        dino_2 = pygame.image.load('images/dino/dino_walk_2.png')
        self.index = 0
        self.walking_dino = [dino_1, dino_2]

        self.dino_jump = pygame.image.load('images/dino/dino_jump.png')
        self.dino_collide = pygame.image.load('images/dino/dino_collide.png')

        self.image = self.walking_dino[self.index]
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.rect = self.image.get_rect(midbottom=(75, 220))
        self.gravity = 0

    def get_input(self):
        keys_pressed = pygame.key.get_pressed()
        # The dino will not jump if it is already jumping
        if keys_pressed[pygame.K_SPACE] and self.rect.bottom >= 220:
            self.gravity = -17.5
            self.rect.y += self.gravity

    def animate_dino(self):
        if self.rect.bottom < 220:
            self.gravity += 1
            self.rect.y += self.gravity
            self.image = self.dino_jump
        else:
            # Reset the position and gravity in case the dino had just jumped
            self.gravity = 0
            self.rect.bottom = 220

            self.index += 0.1
            if self.index >= len(self.walking_dino):
                self.index = 0
            self.image = self.walking_dino[int(self.index)]

        self.image = pygame.transform.scale_by(self.image, 1.75)

    def update(self, playing_game):
        if playing_game:
            self.get_input()
            self.animate_dino()
        else:
            self.image = self.dino_collide
            self.image = pygame.transform.scale_by(self.image, 1.75)
