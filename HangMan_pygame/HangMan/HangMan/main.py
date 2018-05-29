import os 
import string
import pygame
from pygame.locals import *
from cls.keyword import *
from cls.alphabet import *
from cls.score import *
from cls.game import *


#if cls.Keyword.keywords is None:
Keyword.initialize_list()

keywords = Keyword.keywords_list
keyword = Keyword()
alphabet = Alphabet()
score = Score(3)

pygame.init()

background_image = pygame.image.load("graphics/background.bmp")
w = 15
h = 10
unit = 50
size = width, height = unit * w, unit * h
background = [background_image] * w
screen = pygame.display.set_mode(size)

for i in range(w):
    for j in range(h):
        screen.blit(background[i], (i * unit, j * unit))


speed = 1
player = GameObject("graphics/player.bmp", unit, unit, speed)
player.rect.x = 0
player.rect.y = 0


all_letters = []
i = 1
for letter in string.ascii_uppercase:
    if letter in "ABCDERQ":
        letter = GameObject("graphics/letter_%s.bmp" %(letter,), unit/2, unit/2, letter = letter)
        letter.rect.x = i*unit
        letter.rect.y = i*unit

        all_letters.append(letter)

        i += 1

#letter_r = GameObject("graphics/letter_r.bmp", unit, unit, letter = 'r')
#letter_r.rect.x = width - 3*unit
#letter_r.rect.y = 3*unit





all_sprites_group = pygame.sprite.Group()
all_sprites_group.add(player)

for sprite in all_letters:
    all_sprites_group.add(sprite)


clock = pygame.time.Clock()


game_on = True

while game_on:

    keyword.assign_new(keywords)
    alphabet.reset()

    while score.current_score > 0 and keyword.hidden != keyword.keyword:
        print("Total score: " + str(score.total_score))
        print(str(score.current_score) + " mistakes to hang!")
        print(keyword.hidden)
        print(alphabet.available)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type in (QUIT,):
                    sys.exit()


            all_sprites_group.update()
            all_sprites_group.draw(screen)  #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
            pygame.display.flip()           #Refresh 

            keystate = pygame.key.get_pressed()

            x, y = 0, 0
            if keystate[K_RIGHT] and player.rect.x < (width - unit): x = 1
            if keystate[K_LEFT] and player.rect.x > 0: x = -1
            if keystate[K_DOWN] and player.rect.y < (height - unit): y = 1
            if keystate[K_UP] and player.rect.y > 0: y = -1
            direction = (x, y)

            ########screen.blit(background_image, (player.rect.x, player.rect.y))
            screen.blit(pygame.transform.scale(background_image, (20, 20)), (player.rect.x, player.rect.y))
            player.move(direction)
            ########screen.blit(player.image, (player.rect.x, player.rect.y))
            screen.blit(pygame.transform.scale(player.image, (20, 20)), (player.rect.x, player.rect.y))
    
            #Check if there is a colision player - letter
            collision_list = pygame.sprite.spritecollide(player, all_letters, False)
            for letter in collision_list:

                if letter.letter.upper() in keyword.keyword: 
                    keyword.update(letter.letter); 
                    print('Well done!')
                else: 
                    score.decrease_current()
                    print("Wrong!")
                
                running = False
                alphabet.update(letter.letter)

                ########screen.blit(background_image, (letter.rect.x, letter.rect.y))
                screen.blit(pygame.transform.scale(background_image, (20, 20)), (letter.rect.x, letter.rect.y))
                letter.kill()
                all_letters.remove(letter)

            pygame.display.update()

            clock.tick(60)            


    if keyword.hidden == keyword.keyword:
        os.system('cls')
        score.update()

        input(keyword.keyword + "\n\nGood job! Next round!")
        os.system('cls')

    elif score.current_score == 0:
        print("Game over!")
        print("Your total score is " + str(score.total_score))
        game_on = False
