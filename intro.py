import pygame
import subprocess  # Use subprocess to open a new Python file

pygame.init()

# Set up display
win = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Intro")

# Load background
bg = pygame.image.load('img/Background/background.png')

# Set up clock for sprite animation
sprite_clock = pygame.time.Clock()

# Set up clock for text animation
text_clock = pygame.time.Clock()

# Character attributes
x = 200
y = 150
width = 250
height = 100

# Load idle sprites (replace with your actual image paths)
idle_sprites = [
    pygame.image.load('img/Bandit/Idle/0.png').convert_alpha(),
    pygame.image.load('img/Bandit/Idle/1.png').convert_alpha(),
    pygame.image.load('img/Bandit/Idle/2.png').convert_alpha(),
    pygame.image.load('img/Bandit/Idle/3.png').convert_alpha(),
    pygame.image.load('img/Bandit/Idle/4.png').convert_alpha(),
    pygame.image.load('img/Bandit/Idle/5.png').convert_alpha(),
    pygame.image.load('img/Bandit/Idle/6.png').convert_alpha(),
    pygame.image.load('img/Bandit/Idle/7.png').convert_alpha(),
]

# New size for the scaled sprites
sprite_scale_width = 100  # Desired width of the sprite
sprite_scale_height = 200  # Desired height of the sprite

# Scale the sprites to the new size
idle_sprites = [pygame.transform.scale(sprite, (sprite_scale_width, sprite_scale_height)) for sprite in idle_sprites]

# Animation variables
current_frame = 0
frame_count = len(idle_sprites)
frame_rate_sprites = 24  # Frame rate for sprite animation
sprite_timer = 0

# Set up font for text
font = pygame.font.Font(None, 36)  # Use None for default font with size 36

# Define multiple texts
texts = [
    "Trying to move?",
    "Great job!",
    "Keep going!",
    "You're doing awesome!",
    "Just kidding...",
    "You're nothing but an NPC.",
    "Your job is not to be great.",
    "All you're supposed to do is feel pain...",
    "Eternal Pain.",
    "Become Pain itself..."
]

# Typing effect variables
text_index = 0  # Current text index
typed_text = ""  # Text that is currently being displayed
show_text = False  # Flag to control text visibility
text_rate = 5  # Frames per character for typing effect
text_timer = 0  # Timer for character typing
change_timer = 0  # Timer for changing text
delay_between_texts = 20  # Delay in frames before changing text
end_timer = 0  # Timer for counting down after the last text is displayed
end_timer_limit = 50  # Frames to wait after the last text
final_wait_time = 300  # Frames to wait after the last text before opening battle.py

def draw_text(text, x, y):
    """Render text on the screen."""
    text_surface = font.render(text, True, (255, 255, 255))  # White color
    win.blit(text_surface, (x, y))

def redrawGameWindow():
    win.blit(bg, (0, 0))
    win.blit(idle_sprites[current_frame], (x, y))  # Draw the current frame

    # Draw the currently typed text if it's visible, shifted 100 pixels right
    if show_text:
        draw_text(typed_text, 50, 350)  # Shift text to the right by 100 pixels

    pygame.display.update()

run = True

while run:
    sprite_clock.tick(100)  # Control the sprite animation frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update sprite animation frame
    sprite_timer += 1
    if sprite_timer >= frame_rate_sprites:
        current_frame = (current_frame + 1) % frame_count
        sprite_timer = 0  # Reset the sprite timer

    keys = pygame.key.get_pressed()

    # Show text and change text when a key is pressed
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]:
        if not show_text:  # Only change text if it's not currently being shown
            typed_text = ""  # Reset typed text for new message
            show_text = True  # Show text
            text_index = 0  # Start from the first text
            change_timer = 0  # Reset the change timer
            end_timer = 0  # Reset the end timer

    # Typing effect logic
    if show_text:
        text_timer += 1
        if text_timer >= text_rate:
            if len(typed_text) < len(texts[text_index]):
                typed_text += texts[text_index][len(typed_text)]  # Add one character at a time
            else:
                # Start the timer to change text after fully typing
                change_timer += 1
                if change_timer >= delay_between_texts:
                    # Move to the next text after the delay
                    text_index += 1  # Move to the next text
                    if text_index >= len(texts):
                        # Start the end timer once the last text is displayed
                        end_timer += 1
                        if end_timer >= final_wait_time:
                            run = False  # Quit the game after the last text is displayed
                    typed_text = ""  # Reset typed text for new message
                    change_timer = 0  # Reset the change timer
                show_text = True  # Keep showing the text

            text_timer = 0  # Reset the timer for typing effect

    redrawGameWindow()

# Open the new Python file using subprocess after a delay
subprocess.Popen(['mp4', 'vid.mp4'])  # Change 'battle.py' to the correct path if necessary

pygame.quit()
