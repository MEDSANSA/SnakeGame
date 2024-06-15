from pygame.locals import *
import pygame
import time
from random import randint

class Player:
    x = 0
    y = 0
    d = 0
    positions = []
    length = 3
    
class Apple:
    x = 0
    y = 0

class Game:
    game_width = 10
    game_height = 10
    grid_size = 44
    score = 0
    
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False
    
    def __init__(self):
        self._running = True
        self.player = Player()
        self.apple = Apple()
        
        self.apple.x = randint(0, self.game_width) * self.grid_size
        self.apple.y = randint(0, self.game_height) * self.grid_size

    # Initialisation de l'interface
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((640, 480), pygame.HWSURFACE) # Set the screen size
        pygame.display.set_caption('pygame snake') # Set the screen title
        self._snake = pygame.image.load("snake.png").convert() # Load an image
        self._apple = pygame.image.load("apple.png").convert()
        self.font = pygame.font.Font(None, 36)  # Initialize font for score display

    # Rendre une interface noire
    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        
        for pos in self.player.positions:
            self._display_surf.blit(self._snake, (pos[0], pos[1]))
        
        self._display_surf.blit(self._apple, (self.apple.x, self.apple.y))
        
        # Display the score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self._display_surf.blit(score_text, (10, 10))
        
        pygame.display.flip()

    # Quitter le jeu
    def on_cleanup(self):
        pygame.quit()

    def game_logic(self):
        if self.player.d == 0:
            self.player.x += 44
        elif self.player.d == 1:
            self.player.x -= 44
        elif self.player.d == 2:
            self.player.y -= 44
        elif self.player.d == 3:
            self.player.y += 44
        
        if len(self.player.positions) < self.player.length:
            self.player.positions.append((self.player.x, self.player.y))
        else:
            self.player.positions.pop(0)
            self.player.positions.append((self.player.x, self.player.y))
        
        if self.isCollision(self.player.x, self.player.y, self.apple.x, self.apple.y, 44):
            self.player.length += 1
            self.score += 1
            self.apple.x = randint(0, self.game_width) * self.grid_size
            self.apple.y = randint(0, self.game_height) * self.grid_size
        
        if len(self.player.positions) > self.player.length - 1:
            for i in range(0, self.player.length - 1):
                if self.isCollision(self.player.x, self.player.y, self.player.positions[i][0], self.player.positions[i][1], 40):
                    print("GAME OVER")
                    self._running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
        
        keys = pygame.key.get_pressed()

        if keys[K_d]:
            self.player.d = 0

        if keys[K_q]:
            self.player.d = 1

        if keys[K_z]:
            self.player.d = 2

        if keys[K_s]:
            self.player.d = 3
    
    def on_execute(self):
        if self.on_init() == False:
            self._running == False

        while self._running:
            self.handle_events()
            self.game_logic()
            self.on_render()
            time.sleep(0.1) # Delay

        self.on_cleanup()

if __name__ == "__main__":
    game = Game() # Create an object of type Game class
    game.on_execute() # Execute it
