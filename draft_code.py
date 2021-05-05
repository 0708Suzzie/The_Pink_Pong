#This is Pong in pink hence pink pong 
#sys is a module access some more functinality on your system, we're only using it to close the game 
#random is to give the ball a random restart after it collides with either the left or the right ball 

import pygame ,sys, random

def ball_animation(): 
    global ball_speed_x , ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #To manage collisions with the wall
    if ball.top <= 0 or ball.bottom >= screen_height :
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    
    #Player Score 
    if ball.left <= 0 :
        pygame.mixer.Sound.play(pong_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()
    
    #Opponent Score
    if ball.right >= screen_width :
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1  
        score_time = pygame.time.get_ticks()
        
    #To manage collisions with the opponent or the player 
    if ball.colliderect(player) and ball_speed_x > 0 :  #for player
        pygame.mixer.Sound.play(bounce_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1  
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1  
        elif abs(ball.top- player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1  

    if  ball.colliderect(opponent) and ball_speed_x < 0: #for opponent
        pygame.mixer.Sound.play(bounce_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1  
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1  
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

#to bring the ball back at the centre after it touches left or right wall
def ball_restart() :
    global ball_speed_y, ball_speed_x, score_time
    
    ball.center = (screen_width/2 , screen_height/2) #puts it in the center 

    current_time  = pygame.time.get_ticks()
    pygame.mixer.Sound.play(score_sound)
        
   # the first three ifs are to give text on how many seconds are left 
    if current_time - score_time < 700 : 
        three = game_font.render("3", False, hot_pink)
        screen.blit(three,(screen_width /2 - 5 , screen_height/2 + 30 ) )
    
    if 700 < current_time - score_time < 1400 : 
        two = game_font.render("2", False, hot_pink)
        screen.blit(two,(screen_width /2 - 5, screen_height/2 + 30 ) )
    
    if 1400 < current_time - score_time < 2100 : 
        one = game_font.render("1", False, hot_pink)
        screen.blit(one,(screen_width /2 - 5, screen_height/2 + 30 ) )


   #this is to give a delay of three seconds before it begins bouncing again

    if current_time - score_time < 2100 : 
        ball_speed_x, ball_speed_y = 0,0 
    else : 
        ball_speed_y = 4 * random.choice((1, -1))
        ball_speed_x = 4 * random.choice((1, -1))
        score_time = None


def player_animation() : 
    
    #to move the player 
    player.y += player_speed
    if player.top <= 0 : 
        player.top = 0
    if player.bottom >= screen_height : 
        player.bottom = screen_height

def opponent_ai(): 

    if opponent.top <= ball.y : 
        opponent.top += opponent_speed
    if opponent.bottom >= ball.y : 
        opponent.bottom -= opponent_speed
    if opponent.top <= 0 : 
        opponent.top = 0
    if opponent.bottom >= screen_height : 
        opponent.bottom = screen_height

#General Setup
pygame.mixer.pre_init(4410, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

#Setting up the main window 
screen_width  = 1280
screen_height = 700
screen  = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Pink Pong')

#Game Rectangles 
ball = pygame.Rect(screen_width/2 -10, screen_height/ 2  - 10 , 20,20)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

#picking colors
bg_color = pygame.Color('pink')
hot_pink = pygame.Color('hotpink')

#Game variables
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = 4 * random.choice((1, -1))
player_speed = 0
opponent_speed = 6

#Text variable 
player_score  = 0 
opponent_score  = 0 
game_font = pygame.font.Font("pink_panther.ttf", 26)

#time variables 
score_time = True 

#Sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
bounce_sound = pygame.mixer.Sound("Ball_bounce.wav")
pygame.mixer.init(500000)
pygame.mixer.music.load("The-Pink-Panther-Theme-Song.mp3")
pygame.mixer.music.play(-1)


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
                player_speed += 6
            if event.key == pygame.K_UP : 
                player_speed -= 6
        
        if event.type == pygame.KEYUP : 
            if event.key == pygame.K_DOWN : 
                player_speed -= 6
            if event.key == pygame.K_UP : 
                player_speed += 6

    #Game logic
    ball_animation()
    player_animation()
    opponent_ai()

    #Visuals
    screen.fill(bg_color) 
    pygame.draw.rect(screen, hot_pink, player)
    pygame.draw.rect(screen, hot_pink, opponent)
    pygame.draw.ellipse(screen, hot_pink, ball)
    pygame.draw.aaline(screen, hot_pink, (screen_width/2, 0), (screen_width/2, screen_height))


    if score_time : 
        ball_restart()

    #text
    #putting the text on screen 
    #blit puts one layer of screen on another 
    
    player_text = game_font.render(f"{player_score}", False, hot_pink)
    screen.blit(player_text,(screen_width/2 + 10, screen_height/2 -15 )) 
    
    opponent_text = game_font.render(f"{opponent_score}", False, hot_pink)
    screen.blit(opponent_text,(screen_width/2 - 23, screen_height/2 -15 )) 


    #updating the window 
    pygame.display.flip()
    clock.tick(60)
