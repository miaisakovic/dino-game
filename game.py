import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import pyautogui
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
        cap: A VideoCapture object for the live stream
        recognizer: A Gesture Recognizer task
        open_palm_gesture: True if an open palm is detected, and False otherwise
        hand_landmarks: If a hand is detected, this is a list of 21 x,y,z coordinates
        screen: Display surface for the game
        play_game: True if the user is currently playing the game, and False otherwise
        score: Track the current score
        high_score: Track the highest score so far
        overall_time_played: The overall time this program has been running for
        frame_rate: A clock object to help manage the frame rate
        game_font: A font object 
        dino: A single group for the dinosaur object 
        current_obstacles: A group for current obstacles (cactus and pterodactyl objects)
        create_obstacle: Custom event that will trigger obstacle creation
        clouds: A group for current cloud objects
        display_cloud: Custom event that will determine how often clouds are added
    '''
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        cv2.namedWindow('LiveStream')

        base_options = mp.tasks.BaseOptions(model_asset_path='gesture_recognizer.task')
        running_mode = mp.tasks.vision.RunningMode.LIVE_STREAM
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=running_mode,
            result_callback=self.__get_results
            )
        self.recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)

        self.open_palm_gesture = False
        self.hand_landmarks = []

        pygame.init()
        pygame.display.set_caption('Dinosaur Game')
        self.screen = pygame.display.set_mode((900, 250))

        self.playing_game = True
        self.score = 0
        self.high_score = 0
        self.overall_time_played = 0

        self.frame_rate = pygame.time.Clock()
        self.game_font = pygame.font.Font('font/pixel_font.ttf', 25)

        self.dino = pygame.sprite.GroupSingle()
        self.dino.add(Dinosaur())

        self.current_obstacles = pygame.sprite.Group()

        self.create_obstacle = pygame.USEREVENT + 1
        pygame.time.set_timer(self.create_obstacle, 2000)

        self.clouds = pygame.sprite.Group()

        self.display_cloud = pygame.USEREVENT + 2
        pygame.time.set_timer(self.display_cloud, 2000)

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

        high_score_surface = self.game_font.render("HI  " + str(self.high_score).zfill(5) + " ",
                                                   False, (115, 115, 115), "white")
        high_score_rectangle = high_score_surface.get_rect(topright=(800, 20))

        timestamp = 0

        while True:
            self.__event_loop(self.cap)

            _,frame = self.cap.read()
            timestamp += 1

            # Perform the Gesture Recognition task every 5 frames 
            if timestamp % 5 == 0:
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                self.recognizer.recognize_async(mp_image, timestamp)

                frame = mp_image.numpy_view().copy()
                frame = self.__visualize_results(frame)
                width = int(frame.shape[0] / 3)
                height = int(frame.shape[1] / 3)
                frame = cv2.resize(frame, (height,width))

                cv2.imshow('LiveStream', frame)

            if self.playing_game:
                self.screen.fill((255, 255, 255))
                self.screen.blit(ground_surface, (0, 205))
                self.score = self.__get_score()
                if self.high_score > 0:
                    self.screen.blit(high_score_surface, high_score_rectangle)
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

                if self.score > self.high_score:
                    self.high_score = self.score
                    high_score_surface = self.game_font.render("HI  " + str(self.high_score).zfill(5) + " ",
                                                               False, (115, 115, 115), "white")
                    self.screen.blit(high_score_surface, high_score_rectangle)

            pygame.display.update()

            # Set a maximum frame rate
            self.frame_rate.tick(60)

    def __event_loop(self, cap):
        '''
        Obtain user input, create obstacles, and add clouds

        Args:
            cap: A VideoCapture object for a live stream
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv2.destroyAllWindows()
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

    def __get_results(self, results, frame, timestamp):
        '''
        Based on the results, update the attributes open_palm_gesture and 
        hand_landmarks, and interact with the space bar

        Args:
            results: Classification results
            frame: An image from the live stream
            timestamp: The timestamp for when the image appeared in the live
        '''
        if results.gestures and results.gestures[0][0].category_name == 'Open_Palm':
            self.open_palm_gesture = True
            pyautogui.keyDown('space')
        else:
            self.open_palm_gesture = False
            pyautogui.keyUp('space')

        if results.hand_landmarks:
            self.hand_landmarks = results.hand_landmarks[0]
        else:
            self.hand_landmarks = []

    def __visualize_results(self, frame):
        '''
        Display text if an open palm is detected and draw the hand landmarks

        Args:
            frame: The image that will be drawn on

        Returns:
            The annotated frame
        '''
        if self.hand_landmarks:
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in self.hand_landmarks
            ])
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks_proto,
                mp.solutions.hands.HAND_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                mp.solutions.drawing_styles.get_default_hand_connections_style())

        if self.open_palm_gesture:
            cv2.rectangle(frame, (20, 20), (700, 135), (255,255,255), -1)
            cv2.putText(frame, "Open Palm Detected",
                        (35, 95), cv2.FONT_HERSHEY_DUPLEX,
                        2, (153,76,0), 2)

        return frame

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
