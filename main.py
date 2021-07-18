import pygame
from sys import exit

pygame.init()

height = 600
width = 400

# display surface
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()

# other surfaces

bird_image = pygame.image.load("59894 (1).png")
back_ground = pygame.image.load("bg.png")
pipe_image1 = pygame.image.load("pipe1.png")
pipe_image2 = pygame.image.load("pipe2.png")
game_over = pygame.image.load("gameOver.png")
play_image = pygame.image.load("play.png")
logo = pygame.image.load("logo.png")
ins = pygame.image.load("instruction.png")
youwon = pygame.image.load("youwon.png")

start = True
run = False
reset = False
won = False

# class definitions

class Pipe:
	def __init__(self, pos, gap_height):
		self.pos = pos
		self.gap_height = gap_height

	def draw(self, surface):
		# pygame.draw.rect(surface, (0,255,0), pygame.Rect(self.pos, 0, 100, self.gap_height))
		surface.blit(pipe_image1, (self.pos, -self.gap_height))
		#pygame.draw.rect(surface, (0,255,0), pygame.Rect(self.pos, self.gap_height+100, 100, 600-self.gap_height-100))
		surface.blit(pipe_image2, (self.pos, 600-self.gap_height))

	def check_for_collision(self, bird):
		r1 = pipe_image1.get_rect()
		r1.left = self.pos
		r1.top = -self.gap_height

		r2 = pipe_image2.get_rect()
		r2.left = self.pos
		r2.top = 600-self.gap_height

		return bird.rectangle.colliderect(r1) or bird.rectangle.colliderect(r2)

class Bird:
	def __init__(self, image, pos):
		self.image = image
		self.rectangle = image.get_rect()
		self.rectangle.left = pos[0]
		self.rectangle.top = pos[1]

	def draw(self, surface):
		surface.blit(self.image, (self.rectangle.left, self.rectangle.top))

	def score(self, pipes):
		s=0
		for p in pipes:
			if self.rectangle.left > p.pos + 100:
				s+=1
		return s

pipe = Pipe(200, 250)
bird = Bird(bird_image, [20,150])

gravity = 1
angle = 0

pipes = [pipe, Pipe(450, 150), Pipe(700, 200)]

font = pygame.font.Font("LCD Light.ttf", 50)
text_surface = font.render(f"{bird.score(pipes)}", "LCD Light.ttf", "red")

# main game loop
while True:
	text_surface = font.render(f"{bird.score(pipes)}", "LCD Light.ttf", "red")
	if bird.score(pipes) == 3:
		run = False
		won = True
	if start:
		if pygame.mouse.get_pressed()[0]:
			run = True
			start = False
	elif run:
		copy = bird_image.copy()
		copy = pygame.transform.rotate(copy, -2 * gravity)
		bird.image = copy
		bird.rectangle.top += gravity
		gravity += 1



		for p in pipes:
			p.pos -= 5
			if p.check_for_collision(bird):
				run = False

		if run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

				if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or pygame.mouse.get_pressed()[0]:
						gravity = -15
						pygame.mixer.music.load("wing.mp3")
						pygame.mixer.music.play()
	else:
		mouse_pos = pygame.mouse.get_pos()
		if 170 < mouse_pos[0] <= 220 and  300 <= mouse_pos[1] <= 330:
			if pygame.mouse.get_pressed()[0]:
				reset = True
				print("reset")

	if reset:
		pipe = Pipe(200, 250)
		bird = Bird(bird_image, [20,150])

		gravity = 1
		angle = 0

		pipes = [pipe, Pipe(450, 150), Pipe(700, 200)]

		run = True
		reset = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	screen.blit(back_ground, (0,0))
	if not start:
		for p in pipes:
			p.draw(screen)
		bird.draw(screen)
		if not run:
			if not won:
				screen.blit(game_over, (5, 200))
			else:
				screen.blit(youwon, (140,200))
			screen.blit(play_image, (170,300))
		screen.blit(text_surface, (0,0))
	else:
		screen.blit(logo, (0,200))
		screen.blit(ins, (150,300))
	
	pygame.display.update()
	clock.tick(20)