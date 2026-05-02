import random
import math
import pygame

from constants import *

class Enemy:
    def __init__(self, name, hp, speed, damage, color, size, x, y):
        self.name = name
        self.max_hp = hp
        self.hp = self.max_hp
        self.speed = speed
        self.damage = damage
        self.color = color
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size

        # Масштабуємо картинку під розмір конкретного ворога (Бос буде великим)
        if assets["ghost"] is not None:
            if self.name == "Boss":
                self.image = pygame.transform.scale(assets["ghost"], (size, size))
            else:
                self.image = pygame.transform.scale(assets["ghost2"], (size, size))
        else:
            # Якщо картинка не завантажена, створюємо кольоровий квадрат
            self.image = pygame.Surface((size, size))
            self.image.fill(color)

    def move(self, player_rect):
        # Рух у бік гравця
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        
        if dist != 0:
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed

    def draw(self, surface, is_lit):
        # Якщо ворог у світлі — малюємо справжнім кольором, якщо ні — сірим
        draw_color = self.color if is_lit else WHITE
        # pygame.draw.rect(surface, draw_color, self.rect)

        temp_image = self.image.copy()
        temp_image.fill(draw_color, special_flags=pygame.BLEND_RGBA_MULT)

        surface.blit(temp_image, self.rect)
        
        # Якщо це Босс, можна додати полоску ХП над ним
        if self.name == "Boss" and is_lit:
            health_bar_width = self.size
            current_health = (self.hp / self.max_hp) * health_bar_width
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, current_health, 5))


def create_shadow(x, y):
    return Enemy("Shadow", 3, 2, 1, PURPLE, 60, x, y)

def create_stalker(x, y):
    return Enemy("Stalker", 1, 3, 2, ORANGE, 40, x, y)

def create_boss(x, y, level=1):
    # Більше ХП, великий розмір, але повільніший
    return Enemy(name="Boss", hp=20*level, speed=1.5, damage=5, color=YELLOW, size=100, x=x, y=y)


def spawn_enemy(enemies_list, level, WIDTH, HEIGHT):
    # Визначаємо, з якого боку з'явиться ворог
    side = random.choice(['top', 'bottom', 'left', 'right'])
    
    if side == 'top':
        x = random.randint(0, WIDTH)
        y = -50
    elif side == 'bottom':
        x = random.randint(0, WIDTH)
        y = HEIGHT + 50
    elif side == 'left':
        x = -50
        y = random.randint(0, HEIGHT)
    else: # right
        x = WIDTH + 50
        y = random.randint(0, HEIGHT)

    # Логіка вибору типу ворога
    # Використовуємо випадкове число від 1 до 10 для визначення шансу
    chance = random.randint(1, 10)
    
    # Шанс на Боса (наприклад, якщо рівень кратний 3 і боса ще немає)
    boss_exists = any(e.name == "Boss" for e in enemies_list)
    if level % 3 == 0 and not boss_exists:
        enemies_list.append(create_boss(x, y, level))
        return # Виходимо, щоб не спавнити нікого більше в цей момент

    if boss_exists:
        return

    # Правило: на 3 Shadow -> 1 Stalker (шанс 25% на сталкера, 75% на shadow)
    if chance <= 7: 
        enemies_list.append(create_shadow(x, y))
    else:
        enemies_list.append(create_stalker(x, y))
