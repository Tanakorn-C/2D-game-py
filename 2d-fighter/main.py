import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#define figther variable
KNIGHT_SIZE = 162
KNIGHT_SCALE = 3
KNIGHT_OFFSET = [62, 45]
KNIGHT_DATA = [KNIGHT_SIZE, KNIGHT_SCALE,  KNIGHT_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [110, 110]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D-Fighting")

#set framrate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (170, 183, 184)
BLACK = (0, 0, 0)
DARK_GREEN = (15, 113, 73)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1,P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#load music and sounds
pygame.mixer.music.load("assets/audio/war-behind-the-hills.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/whoosh.flac")
sword_fx.set_volume(0.5)
#sword2_fx = pygame.mixer.Sound("assets/audio/sword-thunder01.wav")
#sword2_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/fire-magic.wav")
magic_fx.set_volume(0.5)

#load background image
bg_image = pygame.image.load("assets/images/background/background.png").convert_alpha()

#load spritesheets
knight_sheet = pygame.image.load("assets/images/knight/Sprites/com_knight.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/com_wizard.png").convert_alpha()

#load victory igmae
victyory_image = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#define number of steps in each animation
KNIGHT_ANIMATIONS_STEPS = [10, 8, 1, 6, 7, 4, 9]
WIZARD_ANIMATIONS_STEPS = [8, 8, 2, 8, 8, 4, 6]

#define font
count_font = pygame.font.Font("assets/fonts/DTNightingale.otf", 80)
score_font = pygame.font.Font("assets/fonts/DTNightingale.otf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
	scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
	screen.blit(scaled_bg, (0, 0))

#function for drawing health bars
def draw_health_bar(health, x, y):
	ratio = health / 100
	pygame.draw.rect(screen, BLACK, (x - 5, y - 5, 410, 40))
	pygame.draw.rect(screen, RED, (x, y, 400, 30))
	pygame.draw.rect(screen, DARK_GREEN, (x, y, 400 * ratio, 30))


#create twon instances of fighters
fighter_1 = Fighter(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATIONS_STEPS, sword_fx)
fighter_2 = Fighter(2, 770, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATIONS_STEPS, magic_fx) 


#game loop
run = True
while run:

	clock.tick(FPS)

	#draw background 
	draw_bg()

	#show player stats
	draw_health_bar(fighter_1.health, 20, 20)
	draw_health_bar(fighter_2.health, 580, 20)
	draw_text("Score: " + str(score[0]), score_font, RED, 20,60)
	draw_text("Score: " + str(score[1]), score_font, RED, 580,60)

	#update countdown
	if intro_count <= 0:
		#move fighters
		fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
		fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
	else:
		#display count timer
		draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_WIDTH / 4)
		#update count timer
		if (pygame.time.get_ticks() - last_count_update) >= 1000:
			intro_count -= 1
			last_count_update = pygame.time.get_ticks()
			


	#update fighters
	fighter_1.update()
	fighter_2.update()

	#draw fighters
	fighter_1.draw(screen)
	fighter_2.draw(screen)


	#check for player defeat
	if round_over == False:
	 if fighter_1.alive == False:
			score[1] += 1
			round_over = True
			round_over_time = pygame.time.get_ticks()
	elif fighter_2.alive == False:
			score[0] += 1
			round_over = True
			round_over_time = pygame.time.get_ticks()
	else:
		#display victory image
		screen.blit(victyory_image, (200, 160))
		if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
			round_over = False
			intro_count = 3
			#create twon instances of fighters
			fighter_1 = Fighter(1, 200, 310, False, KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATIONS_STEPS, sword_fx)
			fighter_2 = Fighter(2, 770, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATIONS_STEPS, magic_fx) 

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	#update display
	pygame.display.update()

#exit pygame
pygame.quit()