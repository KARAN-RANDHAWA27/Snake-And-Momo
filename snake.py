import pygame
from pygame.locals import *
import time
import random

size = 40


class Food:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.choclate = pygame.image.load("chocolate.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.choclate, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 19)*size
        self.y = random.randint(1, 14)*size


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.player = pygame.image.load("snake.jpg").convert()
        self.x = [40]*length
        self.y = [40]*length
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= 40
        if self.direction == 'right':
            self.x[0] += 40
        if self.direction == 'up':
            self.y[0] -= 40
        if self.direction == 'down':
            self.y[0] += 40

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.player, (self.x[i], self.y[i]))
        pygame.display.flip()

    def inc_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake 2022")
        pygame.mixer.init()
        self.bg_music()

        self.surface = pygame.display.set_mode((800, 600))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.food = Food(self.surface)
        self.food.draw()

    def bg_music(self):
        pygame.mixer.music.load("bg_music.mp3") 
        pygame.mixer.music.play(-1,0)   

    def play_sound(self,sound_name):
        if sound_name == "eat":
            sound = pygame.mixer.Sound("eat.wav") 
        elif sound_name == "died":
            sound = pygame.mixer.Sound("died.wav")  

        pygame.mixer.Sound.play(sound)
        #pygame.mixer.music.stop()   

    def background(self):
        bg = pygame.image.load("bg.jpg") 
        self.surface.blit(bg,(0,0))
       

    def is_collide(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def play(self):
        self.background()
        self.snake.walk()
        self.food.draw()
        self.show_score()
        pygame.display.flip()

        if self.is_collide(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.play_sound("eat")
            self.food.move()
            self.snake.inc_length()

        for i in range(1, self.snake.length):
            if self.is_collide(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("died")
                raise "Game Over"
        
        if not (0<= self.snake.x[0] <=800 and 0<=self.snake.y[0] <=600):
            self.play_sound("died")
            raise "Snake Hits The Boundary"


    def show_game_over(self):
         self.background()
         font = pygame.font.SysFont('arial', 35)
         line1 = font.render(f"Game Over! You Scored {self.snake.length-1}", "True", (245, 75, 37))
         self.surface.blit(line1, (200, 300))
         line2 = font.render("To Play Again Press Enter Or Esc To Exit", "True", (245, 75, 37))
         self.surface.blit(line2, (200, 350))
         
         pygame.display.flip()

         pygame.mixer.music.pause()

    def show_score(self):
         font = pygame.font.SysFont('arial',35)
         score=font.render(f"Score: {self.snake.length-1}","True",(54, 168, 166))
         self.surface.blit(score,(600,10))
    
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.food = Food(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        # pygame.mixer.self.Sound.play.pause(died)
                        pause = False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
                
            
            time.sleep(0.2)
            


if __name__ == '__main__':
    game = Game()
    game.run()
