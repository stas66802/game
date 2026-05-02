import pygame 
import random
import math

from enemy import *
from weapons import *
from constants import *
from player import Player # Переконайся, що клас Player у файлі player.py

pygame.init()

cur_width = DEF_WIDTH
cur_height = DEF_HEIGHT

screen = pygame.display.set_mode((cur_width, cur_height)) 

load_all_assets()

pygame.display.set_caption("Shadow Escape ULTIMATE")

# Завантаження текстури фону
texture = assets["background"]
tile_width = texture.get_width()
tile_height = texture.get_height()

def draw_background(width, height):
    for x in range(0, width + tile_width, tile_width):
        for y in range(0, height + tile_height, tile_height):
            screen.blit(texture, (x, y))

# Поверхня туману
fog = pygame.Surface((cur_width, cur_height), pygame.SRCALPHA)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Доступна зброя
weapons = {
    "normal": Weapon("Волина", 1, BLUE, 10),
    "shotgun": Shotgun("Дробовуха", 2, PURPLE, 12),
    "laser": Laser("Вжух", 10, RED, 25),
}

# Ініціалізація гравця
player = Player(
    x=cur_width//2, 
    y=cur_height//2, 
    hp=10, 
    weapon=weapons["normal"]
    )

# State
shop_open = False
score = 0 
level = 1 
next_level_score = 700

# Enemies & Bullets
enemies = []
bullets = []

# Spawn Timer - подія на створення ворогів 
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 2000)

# на повний екран через клавішу F
is_fullscreen = False

running = True
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    # --- ОБРОБКА ПОДІЙ ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_EVENT and not shop_open:
            num_to_spawn = 1 + (level // 2)
            for _ in range(num_to_spawn):
                spawn_enemy(enemies, level, cur_width, cur_height)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                shop_open = not shop_open

            if event.key == pygame.K_f:  # Натискання клавіші 'F'
                is_fullscreen = not is_fullscreen  # Змінюємо стан
            
                if is_fullscreen:
                    # Перехід у повний екран
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    cur_width, cur_height = screen.get_size()
                else:
                    # Повернення у віконний режим
                    screen = pygame.display.set_mode((DEF_WIDTH, DEF_HEIGHT))
                    cur_width, cur_height = DEF_WIDTH, DEF_HEIGHT

                fog = pygame.Surface((cur_width, cur_height), pygame.SRCALPHA)

            if shop_open:
                if event.key == pygame.K_1 and player.coins >= 5:
                    player.speed += 1
                    player.coins -= 5
                if event.key == pygame.K_2 and player.coins >= 5:
                    player.weapon.bullet_speed += 2
                    player.coins -= 5
                if event.key == pygame.K_3 and player.coins >= 10:
                    player.max_hp += 1
                    player.hp = player.max_hp # Повне лікування при апгрейді
                    player.coins -= 10
                if event.key == pygame.K_4 and player.coins >= 15:
                    player.weapon = weapons["shotgun"]
                    player.coins -= 15
                if event.key == pygame.K_5 and player.coins >= 20:
                    player.weapon = weapons["laser"]
                    player.coins -= 20

        if event.type == pygame.MOUSEBUTTONDOWN and not shop_open:
            mx, my = mouse_pos
            dx = mx - player.rect.centerx
            dy = my - player.rect.centery
            dist = max(1, math.hypot(dx, dy))
            player.weapon.shoot(player.rect.centerx, player.rect.centery, dx/dist, dy/dist, bullets)

    # --- ЛОГІКА ГРИ ---
    if not shop_open:
        # Рух та Dash обробляються всередині класу
        player.handle_input(shop_open, cur_width, cur_height)

        # Перевірка рівня
        if score >= next_level_score:
            level += 1
            next_level_score += 1000

        # Оновлення ворогів
        for en in enemies[:]:
            en.move(player.rect)
            
            # Колізія ворога з гравцем через метод take_damage
            if player.rect.colliderect(en.rect):
                if player.take_damage(en.damage):
                    if en.name != "Boss": 
                        enemies.remove(en)

        # Оновлення куль
        for b in bullets[:]:
            b.update(cur_width, cur_height)
            if not b.alive:
                bullets.remove(b)
                continue
                
            b_rect = b.get_rect()
            for en in enemies[:]:
                if b_rect.colliderect(en.rect):
                    en.hp -= player.weapon.getDamage()
                    
                    if b.type != "laser":
                        if b in bullets: 
                            bullets.remove(b)
                    
                    if en.hp <= 0:
                        # переробити , встановити винагороду за вбивство як значення обєкта ворога
                        player.coins += (15 if en.name == "Boss" else (2 if en.name == "Stalker" else 1))
                        enemies.remove(en)
                    break 

        score += 1

    # --- МАЛЮВАННЯ ---
    draw_background(cur_width, cur_height)
    
    # 1. Гравець
    player.draw(screen)
    
    # 2. Ліхтарик та Вороги (вороги малюються всередині методу гравця)
    player.draw_flashlight(screen, fog, mouse_pos, enemies)
    
    # 3. Накладаємо туман
    screen.blit(fog, (0, 0))

    # 4. Кулі (поверх туману)
    for b in bullets:
        b.draw(screen)

    # --- UI ---
    screen.blit(font.render(f"HP: {player.hp}/{player.max_hp}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Coins: {player.coins}", True, WHITE), (10, 40))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 70))
    screen.blit(font.render(f"Weapon: {player.weapon.getName()}", True, WHITE), (10, 100))

    if shop_open:
        overlay = pygame.Surface((cur_width, cur_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0, 0))
        x = cur_width//2-250
        pygame.draw.rect(screen, BLACK, (x, 150, 500, 350))
        pygame.draw.rect(screen, WHITE, (x, 150, 500, 350), 2)
        screen.blit(font.render("SHOP (E to close)", True, WHITE), (x+150, 170))
        screen.blit(font.render(f"1 - Speed +1 (5 coins) | Now: {player.speed}", True, WHITE), (x+20, 210))
        screen.blit(font.render("2 - Bullet speed +2 (5 coins)", True, WHITE), (x+20, 240))
        screen.blit(font.render("3 - Max HP +1 (10 coins)", True, WHITE), (x+20, 270))
        screen.blit(font.render("4 - Shotgun (15 coins)", True, WHITE), (x+20, 300))
        screen.blit(font.render("5 - Laser (20 coins)", True, WHITE), (x+20, 330))

    if player.hp <= 0:
        screen.fill(BLACK)
        over_txt = font.render("GAME OVER", True, RED)
        screen.blit(over_txt, (cur_width//2 - over_txt.get_width()//2, cur_height//2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    pygame.display.flip()

pygame.quit()