#This is Pong in pink hence pink pong 
#sys is a module access some more functinality on your system, we're only using it to close the game 
#random is to give the ball a random restart after it collides with either the left or the right ball 

#We're using sprites in this set of code. putting everything in classes and reducing number of global variables 
#In earlier days, objects with a specific look in a game were called sprites and now that name is kinda stuck
#In python Sprite is a class in pygame
#We'll also write this code in such a way that we are able to add more functionality later

import pygame ,sys, random

#Classes that we'll use 

    #This class is something that all the other classes will inherit.
    #This will create a rectangle for them and use images to show them
class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos) : 
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

    #To define player paddle actions
class Player(Block) : 
    def __init__(self,path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0
    
    def screen_constraints(self) :
        if self.rect.top <= 0 : 
            self.rect.top = 0
        if self.rect.bottom >= screen_height : 
            self.rect.bottom = screen_height

    def update(self, ball_group) : 
        self.rect.y += self.movement
        self.screen_constraints()

    #To define Ball animations and colissions
class Ball(Block) : 
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles) : 
        super().__init__(path, x_pos,y_pos) 
        self.speed_x = speed_x * random.choice((1, -1))
        self.speed_y = speed_y * random.choice((1, -1))
        self.paddles = paddles
        self.active = False 
        self.score_time = 0 

    def update(self) : 
        if self.active : 
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else  :
            self.restart_counter()
    
    def collisions(self) : 
        
        #To manage collisions with the wall
        if self.rect.top <= 0 or self.rect.bottom >= screen_height :
            pygame.mixer.Sound.play(pong_sound)
            self.speed_y *= -1
        
        #To manage collisions with paddles 
        if pygame.sprite.spritecollide(self, self.paddles, False) : 
            pygame.mixer.Sound.play(bounce_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1 
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1   
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1  
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1  
    
    def reset_ball(self) : 
        self.active = False
        self.speed_x *= random.choice((1, -1))
        self.speed_y *= random.choice((1, -1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2 , screen_height/2 )
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self) : 

        current_time  = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700 : 
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400 : 
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100 :
            countdown_number = 1
        if current_time - self.score_time > 2100 : 
            self.active = True 
        
        time_counter = game_font.render(str(countdown_number), True, hot_pink)
        time_counter_rect = time_counter.get_rect(center = (screen_width/2, screen_height /2 + 40))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect )

    #To define Opponent AI
class Opponent(Block)  :
    def __init__(self, path,  x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
    
    def update(self, ball_group) :
        if self.rect.top <= ball_group.sprite.rect.y : 
            self.rect.top += self.speed
        if self.rect.bottom >= ball_group.sprite.rect.y : 
            self.rect.bottom -= self.speed
        self.constraints()

    def constraints(self) : 
        if self.rect.top <= 0 : 
            self.rect.top = 0

        if self.rect.bottom >= screen_height : 
            self.rect.bottom = screen_height
  
    #Time for the final showdown, The gamemanager, where the classes come together and we make a game 
class GameManager:
    def __init__(self, ball_group, paddle_group) : 
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self) : 
        #Drawing the game objects 
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        #updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()
    
    def reset_ball(self) : 
        if self.ball_group.sprite.rect.right >= screen_width : 
            self.opponent_score += 1 
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0 :
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self)  :
        player_score = game_font.render(str(self.player_score) , True, hot_pink)
        opponent_score = game_font.render(str(self.opponent_score) , True, hot_pink)

        player_score_rect = player_score.get_rect(midleft = (screen_width/2 + 40, screen_height/2 ))
        opponent_score_rect = opponent_score.get_rect(midleft = (screen_width/2 - 40, screen_height/2 ))
        
        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

#General Setup
pygame.mixer.pre_init(4410, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

#Setting up the main window 
screen_width  = 1280
screen_height = 700
screen  = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Pink Pong')

#picking colors
bg_color = pygame.Color('pink')
hot_pink = pygame.Color('hotpink')

#Setting up the middle Strip
middle_strip = pygame.Rect(screen_width/2 -2, 0 , 4, screen_height)

#Game Sounds
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
bounce_sound = pygame.mixer.Sound("Ball_bounce.wav")

#Background Music
pygame.mixer.init(500000)
pygame.mixer.music.load("The-Pink-Panther-Theme-Song.mp3")
pygame.mixer.music.play(-1)

#Text variable 
game_font = pygame.font.Font("pink_panther.ttf", 26)


#Game Objects 
player = Player('Paddle.png', screen_width - 20, screen_height/2, 5 )
opponent = Opponent('Paddle.png', 20, screen_height/2, 6 )
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

ball = Ball('Ball.png', screen_width/2, screen_height/2, 4, 4, paddle_group )
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)

#This is the Loop of the whole Game
while True: 

    #Handeling input 
    for event in pygame.event.get():

        #to exit the game
        if event.type == pygame.QUIT :
            pygame.mixer.fadeout() 
            pygame.quit()
            sys.exit()

        #to move the player up or down using input         
        if event.type == pygame.KEYDOWN : 
            if event.key == pygame.K_DOWN : 
                player.movement += player.speed
            if event.key == pygame.K_UP : 
                player.movement -= player.speed
        
        if event.type == pygame.KEYUP : 
            if event.key == pygame.K_DOWN : 
                player.movement -= player.speed
            if event.key == pygame.K_UP : 
                player.movement += player.speed

    #Background things 
    screen.fill(bg_color) 
    pygame.draw.rect(screen, hot_pink, middle_strip)

    #Running the Game
    game_manager.run_game()
    
    #updating the window 
    pygame.display.flip()
    clock.tick(120)

