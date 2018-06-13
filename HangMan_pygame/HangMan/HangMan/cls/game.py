import pygame
from pygame.locals import *
from cls.keyword import *
from cls.alphabet import *
from cls.score import *

class Letter(pygame.sprite.Sprite):

    def __init__(self, image_path, letter = ''):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        self.letter = letter.upper()

class Player(pygame.sprite.Sprite):

    def __init__(self, image_path, speed = 0):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        #self.collider = pygame.transform.scale(self.image, (int(0.6 * self.rect.width), int(0.6 * self.rect.height)))
        #self.collider = self.collider.move((int(0.2 * self.rect.width), int(0.2 * self.rect.height)))
        #self.collider_rect = self.collider.get_rect()

        self.speed = speed


    def move(self, screen):

        keystate = pygame.key.get_pressed()
        if keystate[K_RIGHT] and self.rect.x < (screen.get_size()[0] - self.rect.width): self.rect.x += self.speed
        if keystate[K_LEFT] and self.rect.x > 400: self.rect.x += self.speed * (-1)
        if keystate[K_DOWN] and self.rect.y < (screen.get_size()[1] - self.rect.height): self.rect.y += self.speed
        if keystate[K_UP] and self.rect.y > 0: self.rect.y += self.speed * (-1)

        #self.collider_rect.x += self.speed * direction[0]
        #self.collider_rect.y += self.speed * direction[1]


class Game():

    all_letters = None
    all_sprites_group = None
    player = None
    keyword = Keyword()
    alphabet = Alphabet()
    score = Score(3)
    t_shuffle = 0

    game_over = False
    new_level = True
    level = None

    def __init__(self):
        self.level = 1

        Keyword.initialize_list()

        self.all_letters = []
        self.all_sprites_group = pygame.sprite.Group()

        self.player = Player("graphics/1.bmp", speed = 3)
        self.player.rect.x = 400
        self.all_sprites_group.add(self.player)

        self.game_over = False
        self.new_level = True


    def process_events(self):
        if self.game_over:
            return True

        for event in pygame.event.get():
            if event.type in (QUIT, K_n):
                return True
            if event.type == pygame.K_y:
                if self.game_over:
                    self.__init__()

    
    def run_level(self, screen):

        if self.new_level:
            self.keyword.assign_new(self.keyword.keywords_list)
            self.alphabet.reset()
            self.player.rect.x = 400
            self.player.rect.y = 0
            self.new_level = False

        if not self.game_over:

            if pygame.time.get_ticks() > 10000 * self.t_shuffle:
                self.t_shuffle += 1
                self.shuffle_alphabet()

            self.player.move(screen)
            self.check_collision()
            self.check_game_result()

    
    # all_letters list will contain available alphabet letters and will be used in player-letter collision detection 
    def shuffle_alphabet(self):
        
        self.all_sprites_group = pygame.sprite.Group()
        self.all_letters = []
        i = 1; j = 1

        for letter in ''.join(random.sample(string.ascii_uppercase, len(string.ascii_uppercase))):
            letter = Letter("graphics/letter_%s.bmp" %(letter,), letter = letter)
            letter.rect.x = 500 + i * letter.rect.width
            letter.rect.y = 400 + j * letter.rect.height

            i += 2
            if i%19 == 0:   # 9 letters/columns per row, then go to next row
                i = 1; j += 2

            if letter.letter in self.alphabet.available: 
                self.all_letters.append(letter)
                self.all_sprites_group.add(letter)


    def check_collision(self):
        #Check if there is a colision player - letter and if yes then update hidden keyword on screen, update alphabet and scores
        collision_list = pygame.sprite.spritecollide(self.player, self.all_letters, False)

        for letter in collision_list:
            self.alphabet.update(letter.letter)
            #letter.kill()
            self.all_sprites_group.remove(letter)
            self.all_letters.remove(letter)

            if letter.letter.upper() in self.keyword.keyword:
                self.keyword.update(letter.letter); 
            else: 
                self.score.decrease_current()


    def check_game_result(self):
        if self.keyword.hidden == self.keyword.keyword:
            self.score.update()
            self.level += 1
            self.new_level = True
            
        elif self.score.current_score == 0:
            self.game_over = True


    def display_frame(self, screen):

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        
        # clean game area
        screen.fill(WHITE, (400, 0, 1200, 800))

        # draw alphabet letters
        self.all_sprites_group.draw(screen) 

        # Draw keyword on the screen
        self.draw_keyword(screen, self.keyword.hidden.split(), BLACK)


        # Draw scores in right top corner
        self.draw_game_results(screen, self.score, BLACK)

        # update player image in new position
        screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

        pygame.display.update()


    def draw_keyword(self, screen, kw_list, color):
        font = pygame.font.SysFont('Arial', 45)
        a = 30; b = 0
        for word in kw_list:
            word = word + " "
            if len(word) > a: a = 30; b +=1
            for c in word:
                self.draw_text(screen, c, font, color, "L", 550 + (30-a)*35, 100 + b*60)
                a -= 1    


    def draw_game_results(self, screen, score, color):
        font = pygame.font.SysFont('Arial', 20)
        game_results_list = ["Level: {}".format(self.level), 
                             "Total score: {}".format(str(score.total_score)), 
                             "{} mistakes to hang!".format(str(score.current_score))]
        
        n = 0
        for result in game_results_list:
            self.draw_text(screen, result, font, color, "R", 1550, 10 + n*30)
            n += 1


    def draw_text(self, screen, text, font, color, side, side_px, top_px):
        text_screen = font.render(text, False, color)
        text_screen_rect = text_screen.get_rect()
        text_screen_rect.top = top_px
        if side == "R": text_screen_rect.right = side_px
        if side == "L": text_screen_rect.left = side_px

        screen.blit(text_screen, text_screen_rect)