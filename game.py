import pygame
from random import choice
from sys import exit

from dinosaur import Dinosaur
from obstacles import Obstacles

class DinoGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dinosaur Game')
        self.screen = pygame.display.set_mode((900,250))

        self.playing_game = True
        self.score = 0
        self.overall_time_played = 0

        self.frame_rate = pygame.time.Clock()
        self.game_font = pygame.font.Font('font/pixel_font.ttf', 25)

        self.dino = pygame.sprite.GroupSingle()
        self.dino.add(Dinosaur())

        self.current_obstacles = pygame.sprite.Group()

        # Custom event that will trigger obstacle creation
        self.create_obstacle = pygame.USEREVENT + 1
        pygame.time.set_timer(self.create_obstacle, 1500)

        self.ground_surface = pygame.image.load('images/ground.png')
        self.ground_surface = pygame.transform.scale_by(self.ground_surface, 1.25)
        self.redo_surface = pygame.image.load('images/redo.png')

    def run_game(self):
        while True:
            self.event_loop()
            
            if self.playing_game:
                self.screen.fill((255,255,255))
                self.screen.blit(self.ground_surface,(0,205))
                self.score = self.get_score()
                self.playing_game = self.check_collision()

                self.dino.draw(self.screen)
                self.dino.update(self.playing_game)

                self.current_obstacles.draw(self.screen)
                self.current_obstacles.update()

            else:
                self.dino.draw(self.screen)
                self.dino.update(self.playing_game)

            pygame.display.update()

            # Set a maximum frame rate
            self.frame_rate.tick(60)
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            if self.playing_game:
                if event.type == self.create_obstacle:
                    available_obstacles = ["pterodactyl", "cactus_1", 
                                           "cactus_2", "cactus_3", 
                                           "cactus_5"]
                    self.current_obstacles.add(Obstacles(choice(available_obstacles)))
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Delete all current obstacles from the group
                    self.current_obstacles.empty()
                    self.playing_game = True
                    self.overall_time_played = int(pygame.time.get_ticks() / 100)

    def get_score(self):
        score = int(pygame.time.get_ticks() / 100) - self.overall_time_played
        score_surface = self.game_font.render(str(score).zfill(5), False, (83,83,83))
        score_rectangle = score_surface.get_rect(topright = (880, 20))
        self.screen.blit(score_surface, score_rectangle)
        return score

    def check_collision(self):
        if pygame.sprite.spritecollide(self.dino.sprite, self.current_obstacles, False):
            return False
        else:
            return True

