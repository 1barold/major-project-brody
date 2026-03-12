import pygame
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)


# Game States
class GameState(Enum):
    START_SCREEN = 1
    HUB = 2
    DUNGEON = 3
    PAUSED = 4


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.vel_x = 0
        self.vel_y = 0

    def handle_input(self, keys):
        self.vel_x = 0
        self.vel_y = 0

        # Arrow keys or WASD
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel_y = self.speed

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Hub Area Class
class Hub:
    def __init__(self):
        self.player = Player(500, 350)
        self.platforms = self.create_platforms()

    def create_platforms(self):
        # Create some simple platforms/walls for the hub
        platforms = [
            pygame.Rect(100, 100, 800, 50),  # Top wall
            pygame.Rect(100, 550, 800, 50),  # Bottom wall
            pygame.Rect(100, 100, 50, 500),  # Left wall
            pygame.Rect(850, 100, 50, 500),  # Right wall
            pygame.Rect(300, 300, 400, 30),  # Middle obstacle
        ]
        return platforms

    def update(self, keys):
        self.player.handle_input(keys)
        self.player.update()

    def draw(self, surface):
        surface.fill(DARK_GREEN)

        # Draw platforms
        for platform in self.platforms:
            pygame.draw.rect(surface, GREEN, platform)

        # Draw player
        self.player.draw(surface)

        # Draw text
        font = pygame.font.Font(None, 24)
        text = font.render("HUB AREA - Use Arrow Keys or WASD to move", True, WHITE)
        surface.blit(text, (10, 10))


# Game Class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Game")
        self.clock = pygame.time.Clock()
        self.state = GameState.START_SCREEN
        self.hub = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.START_SCREEN:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                elif self.state == GameState.HUB:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.START_SCREEN
        return True

    def start_game(self):
        self.state = GameState.HUB
        self.hub = Hub()

    def update(self):
        if self.state == GameState.HUB:
            keys = pygame.key.get_pressed()
            self.hub.update(keys)

    def draw(self):
        if self.state == GameState.START_SCREEN:
            self.draw_start_screen()
        elif self.state == GameState.HUB:
            self.hub.draw(self.screen)

        pygame.display.flip()

    def draw_start_screen(self):
        self.screen.fill(BLACK)

        # Title
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("DUNGEON CRAWLER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Instructions
        inst_font = pygame.font.Font(None, 36)
        inst = inst_font.render("Press SPACE to Start", True, WHITE)
        inst_rect = inst.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(inst, inst_rect)

        # Hint
        hint_font = pygame.font.Font(None, 24)
        hint = hint_font.render("Use Arrow Keys or WASD to move | ESC to return to menu", True, GRAY)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 550))
        self.screen.blit(hint, hint_rect)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


# Main
if __name__ == "__main__":
    game = Game()
    game.run()