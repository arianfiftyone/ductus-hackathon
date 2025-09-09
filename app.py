import pygame
import sys
from vizualizer import MusicVisualizer

pygame.init()
pygame.mixer.init()

# Initialize the background visualizer
visualizer = MusicVisualizer()

WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ONE BUTTON CHALLENGE!!!!!!!!!!!!!")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NOTE_COLOR = (255, 0, 0)
FRETBOARD_COLOR = (50, 50, 50)  # Dark gray

# Load button image and position it at the bottom center
button_image = pygame.image.load("screenshot.png").convert_alpha()
button_rect = button_image.get_rect()
button_rect.midbottom = (WIDTH // 2, HEIGHT - 50)

# Define fretboard lane (vertical rectangle behind the note)
fretboard_width = 80
fretboard_rect = pygame.Rect(
    WIDTH // 2 - fretboard_width // 2,
    0,
    fretboard_width,
    HEIGHT
)

# Define falling note block properties
note_width, note_height = 60, 30
note_speed = 5
note_rect = pygame.Rect(
    WIDTH // 2 - note_width // 2,
    0,
    note_width,
    note_height
)

# Start music
try:
    pygame.mixer.music.load("testo.mp3")
    pygame.mixer.music.play()
except Exception as e:
    print(f"Failed to play song at start: {e}")

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the note down
    note_rect.y += note_speed

    # Check if it reached the button (bottom zone)
    if note_rect.colliderect(button_rect):
        print("Note hit the fret!")
        note_rect.y = 0  # Reset to top

    # Draw everything
    screen.fill(BLACK)

    # Draw fretboard behind the note
    pygame.draw.rect(screen, FRETBOARD_COLOR, fretboard_rect)

    # Draw note block
    pygame.draw.rect(screen, NOTE_COLOR, note_rect)

    # Get visual color from visualizer
    visual_color = visualizer.get_visual_color()

    # Fill screen with visual color
    screen.fill(visual_color)

    # Draw button image
    screen.blit(button_image, button_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
