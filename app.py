import pygame
import sys

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ONE BUTTON CHALLENGE!!!!!!!!!!!!!")
clock = pygame.time.Clock()

image1 = pygame.image.load("screenshot.png").convert_alpha()
image2 = pygame.image.load("screenshot2.png").convert_alpha()

song1 = "testo.mp3"
song2 = "testo2.mp3" 

current_image = image1
current_song = song1
using_first = True  # current song/image

# init song
pygame.mixer.music.load(current_song)

screen_rect = screen.get_rect()
image_rect = current_image.get_rect(center=screen_rect.center)

BLACK = (0, 0, 0)
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if image_rect.collidepoint(event.pos):
                print("Image clicked!")

                # Toggle image and song
                using_first = not using_first
                if using_first:
                    current_image = image1
                    current_song = song1
                else:
                    current_image = image2
                    current_song = song2

                # Reload the new music
                try:
                    pygame.mixer.music.load(current_song)
                    pygame.mixer.music.play()
                except Exception as e:
                    print(f"Failed to play music: {e}")

    screen.fill(BLACK)
    screen.blit(current_image, image_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()
