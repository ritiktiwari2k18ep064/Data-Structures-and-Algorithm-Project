import sys
import time
import random

import pygame
from pygame.locals import *
import pyjokes

class Application:

    def __init__(self):
        self.H_color = (255, 0, 0)
        self.T_color = (255, 255, 255)
        self.R_color = (255, 100, 100)

        self.input_text = ''
        self.word = ''

        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '

        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        self.reset = True
        self.active = False
        self.end = False

        self.width = 750
        self.height = 500

        pygame.init()

        self.Home_Page = pygame.image.load('images/logo.jpg')
        self.Home_Page = pygame.transform.scale(self.Home_Page, (self.width, self.height))

        self.background = pygame.image.load('images/background.jpg')
        self.background = pygame.transform.scale(self.background, (750, 550))

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('PRATIK TYPING TEST')

    def show_results(self, screen):
        if(not self.end):

            self.total_time = time.time() - self.time_start

            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100

            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)

            self.results = 'Time:'+str(round(self.total_time)) + " secs   Accuracy:" + str(
                round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            self.time_img = pygame.image.load('images/icon.png')
            self.time_img = pygame.transform.scale(self.time_img, (150, 150))

            screen.blit(self.time_img, (self.width/2-75, self.height-140))
            self.center_allign(screen, "Restart", self.height - 70, 26, (100, 100, 100))

            print(self.results)
            pygame.display.update()

    def center_allign(self, screen, hd, size, fsize, color):

        font = pygame.font.Font(None, fsize)
        text = font.render(hd, 5, color)
        center = text.get_rect(center=(self.width/2, size))
        screen.blit(text, center)
        pygame.display.update()

    def get_sentence(self):

        joke = pyjokes.get_joke()
        if len(joke) <= 75:
            return joke

    def restart(self):
        self.screen.blit(self.Home_Page, (0, 0))
        pygame.display.update()
        time.sleep(1)
        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        self.word = self.get_sentence()
        if (not self.word):
            self.restart()

        self.screen.blit(self.background, (0, 0))
        hd = "PRATIK: Typing Speed Test"
        self.center_allign(self.screen, hd, 60, 60, self.H_color)

        pygame.draw.rect(self.screen, (212, 156, 146), (51, 251, 651, 51))

        self.center_allign(self.screen, self.word, 200, 28, self.T_color)

        pygame.display.update()

    def start(self):
        self.restart()

        self.running = True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.H_color, (50, 250, 650, 50), 3)

            # update the text of user input
            self.center_allign(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if(x >= 50 and x <= 650 and y >= 250 and y <= 300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                     # position of reset box
                    if(x >= 310 and x <= 510 and y >= 390 and self.end):
                        self.restart()
                        x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.center_allign(
                                self.screen, self.results, 350, 28, self.R_color)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()

        clock.tick(60)

Application().start()
