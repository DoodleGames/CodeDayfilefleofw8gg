import pygame
import random
import button
import sys
import subprocess
pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

# define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

# define fonts
font = pygame.font.SysFont('Times New Roman', 26)

# define colours
red = (255, 0, 0)
green = (0, 255, 0)

# load images
# background image
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
# panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
# button images
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
# load victory and defeat images
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
# sword image (for cursor)
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()

# create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))

# function for drawing panel
def draw_panel():
    # draw panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
    draw_text(f'{bandit1.name} HP: {bandit1.hp}', font, red, 550, screen_height - bottom_panel + 10)
    draw_text(f'{bandit2.name} HP: {bandit2.hp}', font, red, 550, screen_height - bottom_panel + 70)

# fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load hurt images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        # set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        # run enemy hurt animation
        target.hurt()
        # check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        # set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update with new health
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()

damage_text_group = pygame.sprite.Group()

# Knight (now NPC) on the left side and bandits on the right side
knight = Fighter(150, 260, 'Knight', 30, 10, 3)  # NPC on the left
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)  # Player-controlled bandit on the right
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)  # NPC bandit on the right

bandit_list = [bandit1, bandit2]

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

# Create potion button
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

# Game loop
run = True
while run:

    clock.tick(fps)

    # Draw background
    draw_bg()

    # Draw panel
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    # Update damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # Update fighter actions
    knight.update()
    bandit1.update()
    bandit2.update()

    knight.draw()
    bandit1.draw()
    bandit2.draw()

    # Control player actions (bandit1)
    if bandit1.alive:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # Player attack
                if attack:
                    bandit1.attack(knight)
                    current_fighter += 1
                    action_cooldown = 0

                # Player use potion
                elif potion:
                    if bandit1.potions > 0:
                        if bandit1.hp + potion_effect > bandit1.max_hp:
                            bandit1.hp = bandit1.max_hp
                        else:
                            bandit1.hp += potion_effect
                        bandit1.potions -= 1
                        current_fighter += 1
                        action_cooldown = 0

    # Knight (now NPC) behavior
    if knight.alive:
        if current_fighter == 2:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                knight.attack(bandit1)  # Knight now attacks the player-controlled bandit
                current_fighter += 1
                action_cooldown = 0

    # Bandit2 (NPC) behavior
    if bandit2.alive:
        if current_fighter == 3:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                bandit2.attack(knight)
                current_fighter = 1
                action_cooldown = 0

    # Check if player has won or lost
    if game_over == 0:
        if knight.alive == False:
            game_over = 1
        elif bandit1.alive == False:
            game_over = -1

    # Display victory or defeat images
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        elif game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            pygame.quit()  # Close the Pygame window
            subprocess.Popen(['python', 'final.py'])  # Start the battle.py script
            sys.exit()

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Mouse and button controls
    attack = False
    potion = False
    if bandit1.alive:
        if clicked == False and pygame.mouse.get_pressed()[0] == 1:
            clicked = True
            pos = pygame.mouse.get_pos()
            # Check if sword was clicked
            if knight.rect.collidepoint(pos):
                attack = True
            # Check if potion button was clicked
            if potion_button.draw():
                potion = True
        if pygame.mouse.get_pressed()[0] == 0:
            clicked = False

    # Change cursor to sword when hovering over the knight
    if knight.rect.collidepoint(pygame.mouse.get_pos()) and bandit1.alive:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        screen.blit(sword_img, (pygame.mouse.get_pos()))
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    pygame.display.update()

pygame.quit()
