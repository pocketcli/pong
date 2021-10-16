# imports pygame, RNGesus libraries, starts pygame
import pygame
from random import randint

pygame.init()

# sets colour names to colour values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# create paddle asset/movement rendering code
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y = 400

# create ball asset/moving rendering code
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = [randint(2, 6), randint(-4, 4)]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)

    def serve(self, paddle):
        if paddle.rect.x == 20:
            self.velocity = [randint(2, 6), randint(-4, 4)]
            self.rect.x = paddle.rect.x + 20
        else:
            self.velocity = [-randint(2, 6), randint(-4, 4)]
            self.rect.x = paddle.rect.x - 20
        self.rect.y = paddle.rect.y

# left paddle dimensions + origin
paddleLeft = Paddle(WHITE, 10, 100)
paddleLeft.rect.x = 20
paddleLeft.rect.y = 200

# right paddle dimensions + origin
paddleRight = Paddle(WHITE, 10, 100)
paddleRight.rect.x = 670
paddleRight.rect.y = 200

# ball dimensions + origin
ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

# define list of game sprites
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(paddleLeft)
all_sprites_list.add(paddleRight)
all_sprites_list.add(ball)

# Create game window
# if you REALLY, REALLY want to change this, you'll need to adjust ALL other sprite positions as well
# don't say I didn't warn you
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

# loop continues until game is quit
carryOn = True

# clock used to control screen update speed
clock = pygame.time.Clock()

# set initial scores
scoreLeft = 0
scoreRight = 0
rallyCount = 0 # AKA how many times the ball has been hit by the paddles without scoring

# main program loop, mostly handles meta controls
firstTime = True

while carryOn:
    font = pygame.font.Font(None, 60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x: # press 'x', game quits
                carryOn = False
            elif event.key == pygame.K_ESCAPE: # press 'esc', game pauses
                text = font.render("[PAUSED]", True, WHITE, BLACK)
                screen.blit(text, (350 - text.get_width() / 2, 220))
                pygame.display.flip()
                paused = True
                while paused:
                    for ev in pygame.event.get():
                        if ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_ESCAPE: # press 'esc' again, game unpauses
                                paused = False
                            elif ev.key == pygame.K_x: # press 'x', game quits
                                paused = False
                                carryOn = False

    # key control mappping
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleLeft.moveUp(8) # movement value in pixels, chose 8 since it worked best for me personally
    if keys[pygame.K_s]:
        paddleLeft.moveDown(8)
    if keys[pygame.K_UP]:
        paddleRight.moveUp(8)
    if keys[pygame.K_DOWN]:
        paddleRight.moveDown(8)

    # stops paddles from going off-screen
    if paddleLeft.rect.y >= ball.rect.y-50:
        paddleLeft.moveUp(5)
    if paddleLeft.rect.y <= ball.rect.y-50:
        paddleLeft.moveDown(5)

    # all of your game logic are belong to us
    all_sprites_list.update()

    if ball.rect.x >= 690: # for when left scores
        scoreLeft += 1
        rallyCount = 0
        ball.serve(paddleRight)

    if ball.rect.x <= 0: # for when right scores
        scoreRight += 1
        rallyCount = 0
        ball.serve(paddleLeft)

    if ball.rect.y > 490: # tennis ball, throw against the wall (AKA ball-wall bounce code)
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    if pygame.sprite.collide_mask(ball, paddleLeft) or pygame.sprite.collide_mask(ball, paddleRight): # paddle-ball bounce code
        ball.bounce()
        rallyCount += 1
        if ball.velocity[0] <= 0:
            ball.velocity[0] -= 1
        if ball.velocity[0] >= 0:
            ball.velocity[0] += 1

    # all drawing code here
    screen.fill(BLACK) # ensures blank slate to draw on
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5) # Draw field of play
    all_sprites_list.draw(screen)

    text = font.render(str(scoreLeft), True, WHITE) # left score text
    screen.blit(text, (250, 10))
    text = font.render(str(scoreRight), True, WHITE) # right score text
    screen.blit(text, (420, 10))
    text = font.render(str(rallyCount), True, GREEN) # rally score text
    screen.blit(text, (10, 10))
    text = font.render(str(ball.velocity), True, RED) # ball velocity text
    screen.blit(text, (550, 10))

    # Update screen every tick
    pygame.display.flip()

    # draw main menu
    if firstTime:
        screen.fill(BLACK)
        text = font.render("[Press ENTER to start the game] ", True, WHITE)
        screen.blit(text, (30, 220))
        pygame.display.flip()

    # StartTheGameAlready.mp3
    while firstTime:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    firstTime = False

    # Limits to 60fps
    clock.tick(60)

# upon exit, stop game engine
pygame.quit()
