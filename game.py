import pygame
import sys
import subprocess
from PIL import Image

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 578
WHITE = (255, 255, 255)
FONT_COLOR = (255, 165, 0)
FPS = 30

# Load GIF and extract frames
def load_gif(filename):
    frames = []
    try:
        with Image.open(filename) as img:
            for frame in range(img.n_frames):
                img.seek(frame)
                frame_image = img.convert("RGBA")  
                pygame_image = pygame.image.fromstring(frame_image.tobytes(), frame_image.size, frame_image.mode)
                frames.append(pygame_image)
    except Exception as e:
        print(f"Error loading GIF: {e}")
        sys.exit()
    return frames

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Main Menu')

# Load pixel font
font = pygame.font.Font('VCR_OSD_MONO_1.001.ttf', 80)
small_font = pygame.font.Font('VCR_OSD_MONO_1.001.ttf', 40)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    
    is_hovered = x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height

    if is_hovered:
        gradient_color = (
            (255, 165, 0),
            (255, 140, 0),
            (255, 100, 0),
        )
        current_color = gradient_color[(pygame.time.get_ticks() // 100) % len(gradient_color)]
    else:
        current_color = FONT_COLOR
    
    draw_text(text, small_font, current_color, screen, x + width // 2, y + height // 2)

    return is_hovered and mouse_click[0]

def main_menu():
    frames = load_gif('ezgif-2-731383aecb.gif')  # Your GIF file name
    clock = pygame.time.Clock()
    frame_index = 0

    while True:
        screen.fill(WHITE)

        # Display the current frame
        screen.blit(frames[frame_index], (0, 0))

        draw_text('Main Menu', font, FONT_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # Create buttons
        if button('Start Game', SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50):
            start_game('intro.py')  

        if button('Quit', SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 25, 200, 50):
            pygame.quit()
            sys.exit()

        pygame.display.flip()

        # Cycle through frames
        frame_index = (frame_index + 1) % len(frames)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def start_game(script_name):
    pygame.quit()  # Close the Pygame window
    subprocess.Popen(['python', script_name])  # Start the battle.py script
    sys.exit()

if __name__ == '__main__':
    try:
        main_menu()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()
