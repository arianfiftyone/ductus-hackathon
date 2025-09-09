import pygame
import sys
from vizualizer import MusicVisualizer, Particle

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ONE BUTTON CHALLENGE!!!!!!!!!!!!!")
clock = pygame.time.Clock()

# CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NOTE_COLOR = (255, 0, 0)
FRETBOARD_COLOR = (104, 132, 124)
HITBOX_COLOR = (0, 00, 0)

# Load button image
button_image = pygame.image.load("screenshot.png").convert_alpha()
button_rect = button_image.get_rect()
button_rect.midbottom = (WIDTH // 2, HEIGHT - 50)

# Fretboard
# fretboard_width = 200
# fretboard_rect = pygame.Rect(WIDTH // 2 - fretboard_width // 2, 0, fretboard_width, HEIGHT // 2 + 100)
fretboard_width = 200
fretboard_height = HEIGHT // 2 + 100
fretboard_image = pygame.image.load("fretboard.png").convert_alpha()
fretboard_image = pygame.transform.scale(fretboard_image, (fretboard_width + 50, fretboard_height))
fretboard_rect = fretboard_image.get_rect()
fretboard_rect.topleft = (WIDTH // 2 - fretboard_width // 2, 0)

# Hitbox
hitbox_height = 20
hitbox_rect = pygame.Rect((WIDTH // 2 - fretboard_width // 2) + 30, button_rect.top - hitbox_height, 140, hitbox_height)

# Note properties
note_width, note_height = 60, 30
note_speed = 5
note_rect = pygame.Rect(WIDTH // 2 - note_width // 2, 0, note_width, note_height)

font = pygame.font.SysFont(None, 48)
score = 0

songs = ["testo.mp3", "testo2.mp3"]
current_song_index = 0

# Init song
try:
    pygame.mixer.music.load(songs[current_song_index])
    pygame.mixer.music.play()
except Exception as e:
    print(f"Failed to play song: {e}")

mouse_held_start = None
holding_threshold = 1000  # milliseconds

# Initialize the background visualizer
visualizer = MusicVisualizer("testo.mp3")

all_particles = []

running = True
while running:
    clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                mouse_held_start = now
                if note_rect.colliderect(hitbox_rect):
                    score += 1
                    note_rect.y = 0
                    note_speed += 1
                    all_particles += Particle.create_particle_explosion(85, 50, 100)
                    all_particles += Particle.create_particle_explosion(WIDTH // 2, 666, 100)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_held_start = None

    # Change song on hold
    if mouse_held_start and (now - mouse_held_start) >= holding_threshold:
        current_song_index = (current_song_index + 1) % len(songs)
        try:
            pygame.mixer.music.load(songs[current_song_index])
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Failed to load new song: {e}")
        score = 0
        note_speed = 5
        note_rect.y = 0
        mouse_held_start = None

    note_rect.y += note_speed

    if note_rect.y > HEIGHT:
        note_rect.y = 0

    # Draw background
    screen.fill(visualizer.get_visual_color())

    # Draw waveform
    visualizer.draw_ripples(screen, WIDTH, HEIGHT)
    visualizer.draw_spiral(screen, WIDTH, HEIGHT, pygame.time.get_ticks())
    visualizer.draw_waveform(screen, WIDTH, HEIGHT)
    visualizer.draw_radial_bars(screen, WIDTH, HEIGHT)
    visualizer.draw_wave_grid(screen, WIDTH, HEIGHT, pygame.time.get_ticks())

    # pygame.draw.rect(screen, FRETBOARD_COLOR, fretboard_rect)

    for particle in all_particles[:]:
        particle.move()
        particle.draw(screen)

        # Remove the particle if it has shrunk completely
        if particle.size <= 0:
            all_particles.remove(particle)

    screen.blit(fretboard_image, fretboard_rect)
    pygame.draw.rect(screen, HITBOX_COLOR, hitbox_rect)
    pygame.draw.rect(screen, NOTE_COLOR, note_rect)
    screen.blit(button_image, button_rect)


    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (40, 40))

    pygame.display.flip()

pygame.quit()
sys.exit()
