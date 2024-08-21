import pygame, sys, random
from random import randint, uniform
from os.path import join
from pygame.sprite import Group

music_tracks = [
    '../images/track1.mp3',
    '../images/track2.mp3',
    '../images/track3veridisquo.mp3',
    '../images/track4fragmentsoftime.mp3',
    '../images/track5nocturne.mp3',
    '../images/track6prime.mp3'
]

pygame.init()
WIDTH,HEIGHT = 1280, 720
display_surface=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('KILL CHICKEN') 
clock= pygame.time.Clock() 

current_track = music_tracks [0]
pygame.mixer.music.load(current_track)
pygame.mixer.music.play(-1)

#imports
laser_surf = pygame.image.load('../images/arrow.png').convert_alpha()
asteroid = pygame.image.load('../images/asteroid2.png').convert_alpha()
laser= pygame.image.load('../images/arrow.png').convert_alpha()
font = pygame.font.Font(None, 30)
text_surf = font.render('text', True, 'red')
egg_surf = pygame.image.load('../images/egg1.png').convert_alpha()
open_egg_surf = pygame.image.load('../images/egg2.png').convert_alpha()
present_surf = pygame.image.load('../images/gift.png').convert_alpha()
galinha = pygame.image.load('../images/chickenwater.png').convert_alpha()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = (randint(0,WIDTH),randint(0,HEIGHT)))
class Star2(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = (randint(0,WIDTH),randint(0, HEIGHT)))
class Star3(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = (randint(0,WIDTH),randint(0, HEIGHT)))

class Player(pygame.sprite.Sprite):
    def __init__ (self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../images/spaceship4.png').convert_alpha()
        self.rect = self.image.get_rect(center=(WIDTH/2,HEIGHT/2))
        self.direction = pygame.Vector2(1,1)
        self.speed = 450
    
        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 300

        #mask
        # self.mask = pygame.mask.from_surface(self.image)
        # mask_surf = mask.to_surface()
        # mask_surf.set_colorkey((0,0,0)) #object flashing
        # self.image = mask_surf

        # transform (alguns deles diminuem a qualidade)
        # self.image = pygame.transform.rotate(self.image, graus)
        # self.image = pygame.transform.scale2x(self.image)
        # self.image = pygame.transform.greyscale(self.image)

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
        self.laser_timer()
            
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups ):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom = pos)
        

    def update(self, dt):
        self.rect.centery -= 400* dt
        if self.rect.bottom < 0: 
            self.kill()

        
global_asteroid_speed=300
max_asteroid_speed = 600
speed_increase_rate = 1
present_lifetime = 6000
egg_lifetime = 3500

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups, is_special = False   ):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(global_asteroid_speed, global_asteroid_speed + 100)
        self.is_special = is_special

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class Egg(pygame.sprite.Sprite): 
    def __init__(self, surf, pos, direction, speed, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.direction = direction
        self.speed = speed
        self.is_open = False
        self.creation_time = pygame.time.get_ticks() #tempo em q o presente se formou
        self.open_time = None #to track  when egg opens

        self.is_present = random.randint(1,20) == 1
        if self.is_present:
            self.image = present_surf
        self.lifetime = present_lifetime if self.is_present else egg_lifetime
            
        
    def update(self,dt):
        if not self.is_open:
            self.rect.center += self.direction * self.speed * dt
            if self.rect.bottom >= HEIGHT-24:
        
                if self.is_present:
                    self.rect.bottom = HEIGHT-24
                    self.direction = pygame.Vector2(0,0) 
                    if pygame.time.get_ticks() - self.creation_time >= self.lifetime:
                        self.kill()
                else:
                    self.rect.bottom = HEIGHT
                self.open_egg()
        else:
            if pygame.time.get_ticks()-self.creation_time >= self.lifetime:
                self.kill()
        
    
    def open_egg(self):
        if not self.is_present:
            self.image = open_egg_surf 
            self.rect = self.image.get_rect (center = self.rect.center)
            self.direction = pygame.Vector2(0,0)
            self.is_open = True
            self.open_time = pygame.time.get_ticks()

score = 0
score_increment = 150  
galinha_score_inc = 300

def collisions():
    global running, current_time, score, current_track

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        print('gay loser') 
        if current_time < 100:
            print(f'(´,_>`) esperava melhor:{current_time}')
            running = False
        else:
            print(f'(genocida :`)) MATAS_TE:{current_time}')
            running = False
    
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites,True)
        if collided_sprites:
            laser.kill()
            for collided_sprite in collided_sprites:
                if collided_sprite.is_special:
                    score += galinha_score_inc
                else:
                    score += score_increment
                Egg(egg_surf, collided_sprite.rect.center, collided_sprite.direction, collided_sprite.speed, (all_sprites))

    present_collisions = pygame.sprite.spritecollide(player, all_sprites, False)
    for sprite in present_collisions:
        if isinstance(sprite, Egg) and sprite.is_present:
            sprite.kill()

            new_track = random.choice([track for track in music_tracks if track != current_track])
            current_track = new_track
            pygame.mixer.music.load (current_track)
            pygame.mixer.music.play(-1)
                
            

     
def display_score():
    global current_time, score
    current_time = pygame.time.get_ticks() // 100 + score
    text_surf = font.render(str(current_time), True, 'red')
    text_rect = text_surf.get_rect (midbottom = (WIDTH/2, HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
star_surf = pygame.image.load('../images/star2.png')
star2_surf = pygame.image.load('../images/star4.png')
star3_surf = pygame.image.load('../images/star3.png')

for i in range(18):
    Star (all_sprites,star_surf)
for i in range(18):
    Star2 (all_sprites, star2_surf) 
for i in range(18):
    Star3 (all_sprites, star3_surf)
player = Player(all_sprites)

# plain surface
surf = pygame.Surface((100,200))
surf.fill('lime')

# meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)
running = True

while running: 
    dt = clock.tick(60) / 1000
    #event loop
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_event:
            x, y = randint(0,WIDTH), randint(-200, -100)
            
            if random.randint(1,20) == 1:
                Asteroid(galinha, (x,y), (all_sprites, meteor_sprites), is_special = True)
            else:
                Asteroid(asteroid, (x,y), (all_sprites, meteor_sprites), is_special = False)
            
            if global_asteroid_speed < max_asteroid_speed:
                global_asteroid_speed += speed_increase_rate
    # update
    all_sprites.update(dt)
    collisions()
    
    #draw game
    display_surface.fill('black')
    display_score()
    all_sprites.draw(display_surface)
    display_surface.blit(text_surf, (0,0))
    
# pygame.draw.line(display_surface, 'red', (0,0), player.rect.center ou player.mouse.get_pos(), 10)

    pygame.display.update()