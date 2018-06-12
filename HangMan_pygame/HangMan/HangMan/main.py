import os 
import string
import pygame
from pygame.locals import *
from cls.keyword import *
from cls.alphabet import *
from cls.score import *
from cls.game import *

# Print text and align to the right
def print_text_right(text, font, color, right_px, top_px):
    text_screen = font.render(text, False, color)
    text_screen_rect = text_screen.get_rect()
    text_screen_rect.top = top_px
    text_screen_rect.right = right_px
    
    screen.blit(text_screen, text_screen_rect)

def print_text_left(text, font, color, left_px, top_px):
    text_screen = font.render(text, False, color)
    text_screen_rect = text_screen.get_rect()
    text_screen_rect.top = top_px
    text_screen_rect.left = left_px
    
    screen.blit(text_screen, text_screen_rect)

def print_keywords(kw_list, color):
    a = 30; b = 0
    for word in kw_list:
        word = word + " "
        if len(word) > a: a = 30; b +=1
        for c in word:
            print_text_left(c, keyword_font, color, 550 + (30-a)*35, 100 + b*60)
            a -= 1


def print_shuffled_alphabet(alphabet):
        global all_sprites_group; global all_letters
        all_sprites_group = pygame.sprite.Group()
        all_letters = []
        i = 1; j = 1

        for letter in ''.join(random.sample(string.ascii_uppercase, len(string.ascii_uppercase))):
            letter = Letter("graphics/letter_%s.bmp" %(letter,), letter = letter)
            letter.rect.x = 500 + i * letter.rect.width
            letter.rect.y = 400 + j * letter.rect.height

            i += 2
            if i%19 == 0:   # 9 letters/columns per row, then go to next row
                i = 1; j += 2

            if letter.letter in alphabet.available: 
                all_letters.append(letter)
                all_sprites_group.add(letter)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

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
player = Player("graphics/1.bmp", speed = 3)
player.rect.x = 400
player.rect.y = 0

# Sprites group will be used to render sprites (player and letters) on the screen
all_sprites_group_main = pygame.sprite.Group(); all_sprites_group = pygame.sprite.Group()
all_sprites_group.add(player)

# all_letters list will contain available alphabet letters and will be used in player-letter collision detection 
all_letters_main = []; all_letters = []
i = 1; j = 1
for letter in string.ascii_uppercase:
    letter = Letter("graphics/letter_%s.bmp" %(letter,), letter = letter)
    letter.rect.x = 500 + i * letter.rect.width
    letter.rect.y = 400 + j * letter.rect.height

    # main will be used to refresh alphabet each level, w/o main will be used inside single level loop
    all_letters_main.append(letter); all_letters = list(all_letters_main)
    all_sprites_group_main.add(letter); all_sprites_group = all_sprites_group_main.copy()

    i += 2
    if i%19 == 0:   # 9 letters/columns per row, then go to next row
        i = 1; j += 2


clock = pygame.time.Clock()
game_on = True

t = 0

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
        print_text_right("Total score: " + str(score.total_score), scores_font, BLACK, 1550, 10)
        print_text_right(str(score.current_score) + " mistakes to hang!", scores_font, BLACK, 1550, 50)

        # Start loop to allow user move the player to alphabet tiles
        moving = True
        while moving:
            for event in pygame.event.get():
                if event.type in (QUIT,):
                    sys.exit()
            
            # Draw hidden keyword on the screen
            #screen.blit(keyword_font.render(keyword.hidden, False, (0, 0, 0)),(500,100))
            #print_text_left(keyword.hidden, keyword_font, BLACK, 500, 100)
            print_keywords(keyword.hidden.split(), BLACK)



            if pygame.time.get_ticks() > 10000*t:
                t+=1
                screen.blit(background_image, (550, 450), (550, 450, 850, 250))
                print_shuffled_alphabet(alphabet)


            #all_sprites_group.update()
            all_sprites_group.draw(screen)  
            pygame.display.flip()   # Here refreshing the whole screen - neeed to figure out refreshing only sprite rectangulars
            #pygame.display.update(dirty_sprites_rect_list)

            # Choose direction based on user keyboard control - used in sprite.move method 
            # Limit area of player movement (set borders on screen edges)
            #x, y = 0, 0
            #keystate = pygame.key.get_pressed()
            #if keystate[K_RIGHT] and player.rect.x < (width - player.rect.width): x = 1
            #if keystate[K_LEFT] and player.rect.x > 400: x = -1
            #if keystate[K_DOWN] and player.rect.y < (height - player.rect.height): y = 1
            #if keystate[K_UP] and player.rect.y > 0: y = -1
            #direction = (x, y)

            # List to keep screen areas to refresh - to avoid refreshing the whole screen each frame (this still needs to be sorted out... meh)
            dirty_rect_list = []

            # Draw cropped part of background from under player's old position
            screen.blit(background_image, (player.rect.x, player.rect.y), (player.rect.x, player.rect.y, player.rect.width, player.rect.height))
            dirty_rect_list.append(player.rect)
            player.move(width, height)

            # Draw player in new position and refresh only areas of the previous and current player position
            screen.blit(player.image, (player.rect.x, player.rect.y))
            dirty_rect_list.append(player.rect)
            pygame.display.update(dirty_rect_list)
    
            #Check if there is a colision player - letter and if yes then update hidden keyword on screen, update alphabet and scores
            collision_list = pygame.sprite.spritecollide(player, all_letters, False)

            for letter in collision_list:
                if letter.letter.upper() in keyword.keyword: 
                    print('Well done!')
                    #print_text_left(keyword.hidden, keyword_font, WHITE, 500, 100)
                    print_keywords(keyword.hidden.split(), WHITE)
                    keyword.update(letter.letter); 
                    #screen.blit(keyword_hidden_wipe,(500,100))  # Draw previous hidden keyword state in white to wipe out the screen
                else: 
                    print("Wrong!")
                    print_text_right(str(score.current_score) + " mistakes to hang!", scores_font, WHITE, 1550, 50)
                    score.decrease_current()

                alphabet.update(letter.letter)
                #letter.kill()
                all_sprites_group.remove(letter)
                all_letters.remove(letter)

                screen.blit(background_image, (letter.rect.x, letter.rect.y), (letter.rect.x, letter.rect.y, letter.rect.width, letter.rect.height))
                #pygame.display.update(letter.rect)

                # Trigger new loop
                moving = False

            clock.tick(60)
        
        print_text_right(str(score.current_score) + " mistakes to hang!", scores_font, WHITE, 1550, 50)
        print_text_right("Total score: " + str(score.total_score), scores_font, WHITE, 1550, 10)

        # Finish level if whole keyword is uncovered
        if keyword.hidden == keyword.keyword:
            os.system('cls')
            screen.blit(background_image, (player.rect.x, player.rect.y), (player.rect.x, player.rect.y, player.rect.width, player.rect.height))
            pygame.display.update([player.rect])
            player.rect.x = 400
            player.rect.y = 0

            score.update()
            print_keywords(keyword.keyword.split(), BLACK)
            pygame.display.update()
            all_letters = list(all_letters_main)
            all_sprites_group = all_sprites_group_main.copy()

            clock.tick(60)
            pygame.time.wait(3000)
            print_keywords(keyword.keyword.split(), WHITE)

        # Finish game if player lost
        elif score.current_score == 0:
            print_keywords(keyword.hidden.split(), WHITE)
            print_keywords(keyword.keyword.split(), RED)
            screen.blit(background_image, (500, 400), (500, 400, 1100, 400))
            print_text_left("Total score: " + str(score.total_score), keyword_font, BLACK, 500, 400)
            print_text_left("Wanna play again? Y/N", keyword_font, BLACK, 500, 500)
            pygame.display.update()
            
            # ok this is not working but why? meh
            # maybe I'll figure it out tmrw, time to sleep zzzzzzzzzzzz...
            game_over = True
            while game_over:
                print(pygame.key.get_pressed()[K_UP], pygame.key.get_pressed()[K_DOWN])
                keystate2 = pygame.key.get_pressed()

                if keystate2[K_y]: 
                    screen.blit(background_image, (player.rect.x, player.rect.y), (player.rect.x, player.rect.y, player.rect.width, player.rect.height))
                    print_keywords(keyword.keyword.split(), WHITE)
                    print_text_left("Total score: " + str(score.total_score), keyword_font, WHITE, 500, 400)
                    print_text_left("Wanna play again? Y/N", keyword_font, WHITE, 500, 500)
                    pygame.display.update([player.rect])
                    player.rect.x = 400
                    player.rect.y = 0
                    score.reset()
                    all_letters = list(all_letters_main)
                    all_sprites_group = all_sprites_group_main.copy()
                    game_over = False
                elif keystate2[K_n]:
                    game_on = False
                    game_over = False
                    