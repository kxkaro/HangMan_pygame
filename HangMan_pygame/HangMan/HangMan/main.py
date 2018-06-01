import os 
import string
import pygame
from pygame.locals import *
from cls.keyword import *
from cls.alphabet import *
from cls.score import *
from cls.game import *


# Initialize list with available keywords
Keyword.initialize_list()
keywords, keyword, alphabet, score = Keyword.keywords_list, Keyword(), Alphabet(), Score(3)

# Set fonts for drawing 
pygame.init()
pygame.font.init() 
keyword_font = pygame.font.SysFont('Arial', 45)
scores_font = pygame.font.SysFont('Arial', 20)

# Set game window frame, background amd fonts for printing
background_image = pygame.image.load("graphics/7.bmp")
size = width, height = background_image.get_rect().width, background_image.get_rect().height
screen = pygame.display.set_mode(size)
screen.blit(background_image, (0, 0))

# Create sprites and set their positions - player and tiles with alphabet letters
player = GameObject("graphics/1.bmp", speed = 3)
player.rect.x = 400
player.rect.y = 0

# Sprites group will be used to render sprites (player and letters) on the screen
all_sprites_group = pygame.sprite.Group()
all_sprites_group.add(player)

# all_letters list will contain available alphabet letters and will be used in player-letter collision detection 
all_letters = []
i = 1; j = 1
for letter in string.ascii_uppercase:
    letter = GameObject("graphics/letter_%s.bmp" %(letter,), letter = letter)
    letter.rect.x = 500 + i * letter.rect.width
    letter.rect.y = 400 + j * letter.rect.height

    all_letters.append(letter)
    all_sprites_group.add(letter)

    i += 2
    if i%19 == 0:   # 9 letters/columns per row, then go to next row
        i = 1; j += 2


clock = pygame.time.Clock()
game_on = True


while game_on:

    # Level N begins
    # Choose a keyword for current level and reset alphabet to include all letters
    keyword.assign_new(keywords)
    alphabet.reset()

    # Start level loop
    while score.current_score > 0 and keyword.hidden != keyword.keyword:
        print("Total score: " + str(score.total_score))
        print(str(score.current_score) + " mistakes to hang!")
        print(keyword.hidden)
        print(alphabet.available)

        # Prepare drawing hidden keyword on the screen 
        # (black for displaying on screen, white for erasing when player guesses a letter)
        keyword_hidden_screen = keyword_font.render(keyword.hidden, False, (0, 0, 0))
        keyword_hidden_wipe = keyword_font.render(keyword.hidden, False, (255, 255, 255))

        score_total_screen = scores_font.render("Total score: " + str(score.total_score), False, (0, 0, 0))
        score_total_wipe = scores_font.render("Total score: " + str(score.total_score), False, (255, 255, 255))
        score_current_screen = scores_font.render(str(score.current_score) + " mistakes to hang!", False, (0, 0, 0))
        score_current_wipe = scores_font.render(str(score.current_score) + " mistakes to hang!", False, (255, 255, 255))

        score_total_screen_rect = score_total_screen.get_rect()
        score_total_screen_rect.top = 10
        score_total_screen_rect.right = 1550

        score_current_screen_rect = score_current_screen.get_rect()
        score_current_screen_rect.top = 50
        score_current_screen_rect.right = 1550

        screen.blit(score_total_screen, score_total_screen_rect)
        screen.blit(score_current_screen, score_current_screen_rect)

        # Start loop to allow user move the player to alphabet tiles
        moving = True
        while moving:
            for event in pygame.event.get():
                if event.type in (QUIT,):
                    sys.exit()
            
            # Draw hidden keyword on the screen
            screen.blit(keyword_font.render(keyword.hidden, False, (0, 0, 0)),(500,100))


            all_sprites_group.update()
            all_sprites_group.draw(screen)  
            pygame.display.flip()   # Here refreshing the whole screen - neeed to figure out refreshing only sprite rectangulars
            #pygame.display.update(dirty_sprites_rect_list)

            # Choose direction based on user keyboard control - used in sprite.move method 
            # Limit area of player movement (set borders on screen edges)
            x, y = 0, 0
            keystate = pygame.key.get_pressed()
            if keystate[K_RIGHT] and player.rect.x < (width - player.rect.width): x = 1
            if keystate[K_LEFT] and player.rect.x > 400: x = -1
            if keystate[K_DOWN] and player.rect.y < (height - player.rect.height): y = 1
            if keystate[K_UP] and player.rect.y > 0: y = -1
            direction = (x, y)

            # List to keep screen areas to refresh - to avoid refreshing the whole screen each frame (this still needs to be sorted out... meh)
            dirty_rect_list = []

            # Draw cropped part of background from under player's old position
            screen.blit(background_image, (player.rect.x, player.rect.y), (player.rect.x, player.rect.y, player.rect.width, player.rect.height))
            dirty_rect_list.append(player.rect)
            player.move(direction)

            # Draw player in new position and refresh only areas of the previous and current player position
            screen.blit(player.image, (player.rect.x, player.rect.y))
            dirty_rect_list.append(player.rect)
            pygame.display.update(dirty_rect_list)
    
            #Check if there is a colision player - letter and if yes then update hidden keyword on screen, update alphabet and scores
            collision_list = pygame.sprite.spritecollide(player, all_letters, False)

            for letter in collision_list:
                if letter.letter.upper() in keyword.keyword: 
                    print('Well done!')
                    keyword.update(letter.letter); 
                    screen.blit(keyword_hidden_wipe,(500,100))  # Draw previous hidden keyword state in white to wipe out the screen
                else: 
                    print("Wrong!")
                    score.decrease_current()

                alphabet.update(letter.letter)
                letter.kill()
                all_letters.remove(letter)

                screen.blit(background_image, (letter.rect.x, letter.rect.y), (letter.rect.x, letter.rect.y, letter.rect.width, letter.rect.height))
                pygame.display.update(letter.rect)

                # Trigger new loop
                moving = False

            clock.tick(60)            


        # Finish level if whole keyword is uncovered
        if keyword.hidden == keyword.keyword:
            os.system('cls')
            score.update()

            input(keyword.keyword + "\n\nGood job! Next round!")
            os.system('cls')

        # Finish game if player lost
        elif score.current_score == 0:
            print("Game over!")
            print("Your total score is " + str(score.total_score))
            game_on = False
