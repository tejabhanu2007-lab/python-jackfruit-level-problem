import pygame
import random
import sys


WIDTH, HEIGHT = 600, 700
PLAYER_SPEED = 7
BULLET_SPEED = 8
ASTEROID_SPEED = 4
SPAWN_RATE = 1200  
FPS = 30

pygame.init()
pygame.display.set_caption("Asteroid Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.pixel_size = 4

        design = [
            [0,0,0,0,0,6,6,0,0,0,0,0],
            [0,0,0,0,6,1,1,6,0,0,0,0],
            [0,0,0,0,6,6,6,6,0,0,0,0],
            [0,0,0,3,6,5,4,6,3,0,0,0],
            [0,0,3,2,2,4,4,2,2,3,0,0],
            [0,3,2,2,1,4,4,1,2,2,3,0],
            [3,2,2,1,1,3,3,1,1,2,2,3],
            [2,1,1,3,3,7,7,3,3,1,1,2],
            [0,3,3,7,7,7,7,7,7,3,3,0],
            [0,0,0,7,7,0,0,7,7,0,0,0]
        ]

        colors = {
            0: None,
            1: (255, 140, 0),   
            2: (255, 215, 0),    
            3: (255, 69, 0),     
            4: (0, 206, 209),    
            5: (30, 144, 255),   
            6: (245, 245, 245),  
            7: (34, 139, 34)     
        }


        width = len(design[0]) * self.pixel_size
        height = len(design) * self.pixel_size

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        for r, row in enumerate(design):
            for c, code in enumerate(row):
                if code != 0:
                    color = colors[code]
                    x = c * self.pixel_size
                    y = r * self.pixel_size
                    pygame.draw.rect(self.image, color, (x, y, self.pixel_size, self.pixel_size))

 
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 80))

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

 
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.y < -20:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pixel_size = 3

        
        design = [
            [0,0,0,2,2,3,3,2,0,0,0],
            [0,0,2,2,3,3,3,2,1,0,0],
            [0,2,2,3,3,1,3,3,2,1,0],
            [2,2,3,3,1,1,1,3,2,1,1],
            [2,3,3,1,1,2,1,3,3,2,1],
            [3,3,1,1,2,2,2,1,3,2,1],
            [2,3,1,2,2,3,2,1,3,2,0],
            [2,2,1,1,3,3,1,1,2,1,0],
            [0,2,2,1,1,1,1,2,2,0,0],
            [0,0,1,2,2,2,2,1,0,0,0]
        ]

        colors = {
            0: None,
            1: (74, 74, 74),     
            2: (128, 128, 128),  
            3: (169, 169, 169) 
        }


        width = len(design[0]) * self.pixel_size
        height = len(design) * self.pixel_size

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        for r, row in enumerate(design):
            for c, code in enumerate(row):
                if code != 0:
                    color = colors[code]
                    x = c * self.pixel_size
                    y = r * self.pixel_size
                    pygame.draw.rect(self.image, color, (x, y, self.pixel_size, self.pixel_size))

        self.rect = self.image.get_rect(center=(random.randint(30, WIDTH - 30), -20))

        self.speed = ASTEROID_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT + 20:
            self.kill()


class Game:
    def __init__(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.lives = 3
        pygame.time.set_timer(pygame.USEREVENT, SPAWN_RATE)

    def spawn_asteroid(self):
        asteroid = Asteroid()
        self.asteroids.add(asteroid)
        self.all_sprites.add(asteroid)

    def run(self):
        while True:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    self.spawn_asteroid()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)

            self.player.update(keys)
            self.bullets.update()
            self.asteroids.update()
                        # UPDATE
            self.player.update(keys)
            self.bullets.update()
            self.asteroids.update()

          
            for a in list(self.asteroids):   
                
                if a.rect.top > self.player.rect.bottom:
                    a.kill()              
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over()
                    
            for bullet in pygame.sprite.groupcollide(self.bullets, self.asteroids, True, True):
                self.score = getattr(self, "score", 0) + 1   


            
            for bullet in pygame.sprite.groupcollide(self.bullets, self.asteroids, True, True):
                pass

            
            if pygame.sprite.spritecollide(self.player, self.asteroids, True):
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()

            
            screen.fill((0, 0, 0))
            self.all_sprites.draw(screen)
            self.draw_text(f"Lives: {self.lives}", 30, 10, 10)
            pygame.display.update()
            clock.tick(FPS)

    def game_over(self):
        screen.fill((0, 0, 0))
        self.draw_text("GAME OVER", 70, WIDTH//2 - 160, HEIGHT//2 - 40)
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    def draw_text(self, text, size, x, y):
        font = pygame.font.SysFont("arial", size)
        img = font.render(text, True, (255, 255, 255))
        screen.blit(img, (x, y))




Game().run()