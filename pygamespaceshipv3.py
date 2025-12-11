import pygame
import random
import os

# =========================
# CONFIG
# =========================
WIDTH = 600
HEIGHT = 700
PLAYER_SPEED = 8
ENEMY_SPEED = 4
BULLET_SPEED = 10
SPAWN_RATE = 1500  # milliseconds
TOTAL_LIVES = 3
FPS = 165

HIGHSCORE_FILE = "highscore.txt"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (255, 0, 0)
CYAN = (0, 206, 209)


# =========================
# LOAD / SAVE HIGH SCORE
# =========================
def load_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, "r") as f:
        return int(f.read().strip() or 0)

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))


# =========================
# SPACESHIP CLASS
# =========================
class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pixel_size = 4
        
        # Spaceship design
        self.design = [
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
        
        self.colors = {
            0: None,
            1: (255, 140, 0),   # Orange
            2: (255, 215, 0),   # Yellow/Gold
            3: (255, 69, 0),    # Red-Orange
            4: (0, 206, 209),   # Cyan
            5: (30, 144, 255),  # Blue
            6: (245, 245, 245), # White
            7: (34, 139, 34)    # Green
        }
        
        self.width = len(self.design[0]) * self.pixel_size
        self.height = len(self.design) * self.pixel_size
    
    def draw(self, surface):
        start_x = self.x - self.width // 2
        start_y = self.y
        
        for row_idx, row in enumerate(self.design):
            for col_idx, color_code in enumerate(row):
                if color_code != 0:
                    px = start_x + col_idx * self.pixel_size
                    py = start_y + row_idx * self.pixel_size
                    pygame.draw.rect(surface, self.colors[color_code],
                                   (px, py, self.pixel_size, self.pixel_size))
    
    def get_rect(self):
        start_x = self.x - self.width // 2
        return pygame.Rect(start_x, self.y, self.width, self.height)
    
    def move(self, dx):
        self.x += dx
        self.x = max(self.width // 2, min(WIDTH - self.width // 2, self.x))


# =========================
# ASTEROID CLASS
# =========================
class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pixel_size = 3
        
        # Asteroid design
        self.design = [
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
        
        self.colors = {
            0: None,
            1: (74, 74, 74),    # Dark gray
            2: (128, 128, 128), # Medium gray
            3: (169, 169, 169)  # Light gray
        }
        
        self.width = len(self.design[0]) * self.pixel_size
        self.height = len(self.design) * self.pixel_size
    
    def draw(self, surface):
        start_x = self.x - self.width // 2
        start_y = self.y
        
        for row_idx, row in enumerate(self.design):
            for col_idx, color_code in enumerate(row):
                if color_code != 0:
                    px = start_x + col_idx * self.pixel_size
                    py = start_y + row_idx * self.pixel_size
                    pygame.draw.rect(surface, self.colors[color_code],
                                   (px, py, self.pixel_size, self.pixel_size))
    
    def get_rect(self):
        start_x = self.x - self.width // 2
        return pygame.Rect(start_x, self.y, self.width, self.height)
    
    def move(self):
        self.y += ENEMY_SPEED


# =========================
# BULLET CLASS
# =========================
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 6
        self.height = 10
    
    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, 
                        (self.x - self.width // 2, self.y, self.width, self.height))
    
    def move(self):
        self.y -= BULLET_SPEED
    
    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)


# =========================
# GAME CLASS
# =========================
class ShootingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Simple Shooting Game - Pygame")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        
        # Confine cursor to window
        pygame.event.set_grab(True)
        
        # Game objects
        self.player = Spaceship(WIDTH // 2, HEIGHT - 60)
        self.bullets = []
        self.enemies = []
        
        # Game state
        self.score = 0
        self.lives = TOTAL_LIVES
        self.highscore = load_highscore()
        self.game_over = False
        
        # Timing
        self.last_spawn = pygame.time.get_ticks()
        
        # Create star background
        self.stars = []
        for _ in range(120):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            self.stars.append((x, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.shoot()
                
                # Add ESC key handling
                if event.key == pygame.K_ESCAPE:
                    return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                self.shoot()
        
        # Continuous movement
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-PLAYER_SPEED)
            if keys[pygame.K_RIGHT]:
                self.player.move(PLAYER_SPEED)
            
            # Mouse movement
            mouse_x, _ = pygame.mouse.get_pos()
            if pygame.mouse.get_focused():
                # Clamp mouse position to window bounds
                self.player.x = max(self.player.width // 2, 
                                   min(WIDTH - self.player.width // 2, mouse_x))
        
        return True
    
    def shoot(self):
        bullet = Bullet(self.player.x, self.player.y)
        self.bullets.append(bullet)
    
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn > SPAWN_RATE:
            x = random.randint(30, WIDTH - 30)
            enemy = Asteroid(x, 20)
            self.enemies.append(enemy)
            self.last_spawn = current_time
    
    def update(self):
        if self.game_over:
            return
        
        # Spawn enemies
        self.spawn_enemy()
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.move()
            
            # Check if enemy passed player
            if enemy.y > self.player.y:
                self.enemies.remove(enemy)
                self.lose_life()
                continue
            
            # Check collision with bullets
            enemy_rect = enemy.get_rect()
            for bullet in self.bullets[:]:
                bullet_rect = bullet.get_rect()
                if enemy_rect.colliderect(bullet_rect):
                    self.score += 1
                    if self.score > self.highscore:
                        self.highscore = self.score
                        save_highscore(self.highscore)
                    
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break
    
    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
    
    def draw(self):
        # Background
        self.screen.fill(BLACK)
        
        # Draw stars
        for star in self.stars:
            pygame.draw.circle(self.screen, WHITE, star, 1)
        
        # Draw game objects
        if not self.game_over:
            self.player.draw(self.screen)
            
            for bullet in self.bullets:
                bullet.draw(self.screen)
            
            for enemy in self.enemies:
                enemy.draw(self.screen)
        
        # Draw UI
        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        highscore_text = self.small_font.render(f"High Score: {self.highscore}", True, YELLOW)
        self.screen.blit(highscore_text, (10, 40))
        
        lives_text = self.small_font.render(f"Lives: {self.lives}", True, RED)
        lives_rect = lives_text.get_rect(topright=(WIDTH - 10, 10))
        self.screen.blit(lives_text, lives_rect)
        
        # Game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(game_over_text, game_over_rect)
            
            restart_text = self.small_font.render("Press ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


# =========================
# RUN THE GAME
# =========================
if __name__ == "__main__":
    game = ShootingGame()
    game.run()
