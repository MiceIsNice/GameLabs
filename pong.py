import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

enemy_paddle_rect = pygame.Rect((SCREEN_WIDTH-PADDLE_START_X, SCREEN_HEIGHT-PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

paddle_direction = 1
enemy_paddle_direction = 1

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score = 0
enemy_score = 0
# Load the font for displaying the score
font = pygame.font.Font(None, 30)
boop = pygame.mixer.Sound('pong.wav')
gameover = False

# Game loop
while True:

	if score == 11:
		gameover = True
		text =font.render("You win! Press R to play again",True,(255,255,255))
		screen.blit(text, ((SCREEN_WIDTH/2)-160, SCREEN_HEIGHT/2))

	if enemy_score == 11:
		gameover = True
		text =pygame.font.Font(None,24).render("You win! Press R to play again",True,(255,255,255))
		screen.blit(text, ((SCREEN_WIDTH/2)-160, SCREEN_HEIGHT/2))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		if pygame.key.get_pressed()[pygame.K_r] and gameover==True:
			gameover = False
			score = 0
			BALL_SPEED = 10
			enemy_score = 0

	if gameover == False:

		# This test if up or down keys are pressed; if yes, move the paddle
		if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect.top > 0:
			paddle_rect.top -= BALL_SPEED
			paddle_direction = -1
		elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect.bottom < SCREEN_HEIGHT:
			paddle_rect.top += BALL_SPEED
			paddle_direction = 1
		elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
			sys.exit(0)
			pygame.quit()
			
		# Update ball position
		ball_rect.left += ball_speed[0]
		ball_rect.top += ball_speed[1]
	
		# Ball collision with rails
		if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
			ball_speed[1] = -ball_speed[1]
		if ball_rect.right >= SCREEN_WIDTH:
			score+=1
			BALL_SPEED+=.5
			ball_rect.left = SCREEN_WIDTH/2
			ball_rect.top = SCREEN_HEIGHT/2
		if ball_rect.right <= 0:
			BALL_SPEED+=.5
			enemy_score+=1
			ball_rect.left = SCREEN_WIDTH/2
			ball_rect.top = SCREEN_HEIGHT/2
		
		if ball_rect.left > SCREEN_WIDTH/2:
			if ball_rect.top > enemy_paddle_rect.top:
				enemy_paddle_rect.top += BALL_SPEED-1
				enemy_paddle_direction = 1
			if ball_rect.bottom < enemy_paddle_rect.bottom:
				enemy_paddle_rect.top -= BALL_SPEED-1
				enemy_paddle_direction = -1
	
		# Test if the ball is hit by the paddle; if yes reverse speed and add a point
		if paddle_rect.colliderect(ball_rect):
			ball_speed[0] = -ball_speed[0]
			ball_speed[1] = BALL_SPEED*paddle_direction
			pygame.mixer.Sound.play(boop)
	
		if enemy_paddle_rect.colliderect(ball_rect):
			ball_speed[0] = -ball_speed[0]
			ball_speed[1] = BALL_SPEED*enemy_paddle_direction
			pygame.mixer.Sound.play(boop)
	
		# Clear screen
		screen.fill((0, 0, 0))	
	
		# Render the ball, the paddle, and the score
		pygame.draw.rect(screen, (255, 255, 255), paddle_rect) # Your paddle
		pygame.draw.rect(screen, (255, 255, 255), enemy_paddle_rect)
		pygame.draw.circle(screen, (255, 255, 255), ball_rect.center, ball_rect.width / 2) # The ball
		pygame.draw.line(screen, (255,255,255), (SCREEN_WIDTH/2,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT),1)
	
		score_text = pygame.font.Font(None,240).render(str(score), True, (255, 255, 255))
		enemy_score_text = pygame.font.Font(None,240).render(str(enemy_score), True, (255, 255, 255))
		
		screen.blit(score_text, (160, 5)) # The score
		screen.blit(enemy_score_text, (SCREEN_WIDTH-260, 5)) # The score
		
		# Update screen and wait 20 milliseconds
		pygame.display.flip()
		pygame.time.delay(20)
