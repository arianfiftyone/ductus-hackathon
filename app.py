import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ONE BUTTON CHALLENGE!!!!!!!!!!!!!")
clock = pygame.time.Clock()

image = pygame.image.load("Screenshot.png").convert_alpha()
screen_rect = screen.get_rect()
image_rect = image.get_rect(center=screen_rect.center)

BLACK = (0, 0, 0)
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect mouse clicks on the image
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if image_rect.collidepoint(event.pos):
        
                print("Image clicked!")

    screen.fill(BLACK)
    screen.blit(image, image_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()
