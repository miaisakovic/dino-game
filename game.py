import pygame
from random import choice
from sys import exit

from dinosaur import Dinosaur
from obstacles import Obstacles
from cloud import Cloud


class DinoGame:
    '''
    A DinoGame object manages the behaviour of the overall game 

    Attributes:
        screen: Display surface for the game
        play_game: True if the user is currently playing the game, and False otherwise
        score: Track the current score
        overall_time_played: The overall time this program has been running for
        frame_rate: A clock object to help manage the frame rate
        game_font: A font object 
        dino: A single group for the dinosaur object 
        current_obstacles: A group for current obstacles (cactus and pterodactyl objects)
        create_obstacle: Custom event that will trigger obstacle creation
        clouds: A group for current cloud objects
        display_cloud: Custom event that will dictate how often clouds are added
    '''
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dinosaur Game')
        self.screen = pygame.display.set_mode((900, 250))

        self.playing_game = True
        self.score = 0
        self.overall_time_played = 0

        self.frame_rate = pygame.time.Clock()
        self.game_font = pygame.font.Font('font/pixel_font.ttf', 25)

        self.dino = pygame.sprite.GroupSingle()
        self.dino.add(Dinosaur())

        self.current_obstacles = pygame.sprite.Group()

        self.create_obstacle = pygame.USEREVENT + 1
        pygame.time.set_timer(self.create_obstacle, 1500)

        self.clouds = pygame.sprite.Group()

        self.display_cloud = pygame.USEREVENT + 2
        pygame.time.set_timer(self.display_cloud, 1500)

    def run_game(self):
        '''
        A game loop that updates the state of the game 
        '''
        ground_surface = pygame.image.load('images/ground.png')
        ground_surface = pygame.transform.scale_by(ground_surface, 1.25)

        redo_surface = pygame.image.load('images/redo.png')
        redo_surface = pygame.transform.scale_by(redo_surface, 1.5)
        redo_rectangle = redo_surface.get_rect(center=(450, 125))

        game_over_surface = self.game_font.render('GAME OVER', False, (83, 83, 83))
        game_over_rectangle = game_over_surface.get_rect(center=(450, 80))

        while True:
            self.__event_loop()

            if self.playing_game:
                self.screen.fill((255, 255, 255))
                self.screen.blit(ground_surface, (0, 205))
                self.score = self.__get_score()
                self.playing_game = self.__check_collision()

                self.clouds.draw(self.screen)
                self.clouds.update()

                self.dino.draw(self.screen)
                self.dino.update(self.playing_game)

                self.current_obstacles.draw(self.screen)
                self.current_obstacles.update()

            else:
                self.dino.draw(self.screen)
                self.dino.update(self.playing_game)

                self.screen.blit(redo_surface, redo_rectangle)
                self.screen.blit(game_over_surface, game_over_rectangle)

            pygame.display.update()

            # Set a maximum frame rate
            self.frame_rate.tick(60)

    def __event_loop(self):
        '''
        Obtain user input, create obstacles, and add clouds
        '''
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

                if event.type == self.display_cloud:
                    self.clouds.add(Cloud())
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # Delete all current obstacles from the group
                    self.current_obstacles.empty()
                    self.playing_game = True
                    self.overall_time_played = int(pygame.time.get_ticks() / 100)

    def __get_score(self):
        '''
        Obtain and display the current game score

        Returns:
            The time (in 100 milliseconds) the user has played the game for
        '''
        score = int(pygame.time.get_ticks() / 100) - self.overall_time_played
        score_surface = self.game_font.render(str(score).zfill(5), False, (83, 83, 83))
        score_rectangle = score_surface.get_rect(topright=(880, 20))
        self.screen.blit(score_surface, score_rectangle)
        return score

    def __check_collision(self):
        '''
        Check if the dinosaur sprite collided with either a pterodactyl or a cactus

        Returns:
            True if a collision occured, and False otherwise
        '''
        if pygame.sprite.spritecollide(self.dino.sprite, self.current_obstacles, False):
            return False
        else:
            return True
