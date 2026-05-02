import math
import random
import pygame

from constants import *

class Player:
    def __init__(self, x, y, hp, weapon):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 5
        self.max_hp = hp
        self.hp = self.max_hp
        
        self.coins = 0
        self.last_dash = 0
        self.dash_cooldown = 2000
        self.last_hit_time = 0
        self.hit_cooldown = 800
        self.color = BLUE
        
        # Додаємо зброю як властивість гравця
        self.weapon = weapon 

    def handle_input(self, shop_open, width, height):
        if shop_open: return # Блокуємо рух, якщо відкритий магазин

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed

        self.rect.x = max(0, min(width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(height - self.rect.height, self.rect.y))

        if keys[pygame.K_SPACE]:
            self.dash()

    def dash(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dash > self.dash_cooldown:
            self.rect.x += random.choice([-150, 150])
            self.rect.y += random.choice([-150, 150])
            self.last_dash = current_time

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.hit_cooldown:
            self.hp -= amount
            self.last_hit_time = current_time
            return True
        return False

    def incrementMaxHP(self):
        self.max_hp += 1
        self.hp = self.max_hp

    # НОВА ФУНКЦІЯ: ЛІХТАРИК
    def draw_flashlight(self, screen, fog_surface, mouse_pos, enemies):
        fog_surface.fill((10, 10, 10, 230)) 

        # Розрахунок променя
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        main_angle = math.atan2(dy, dx)
        dist = 500
        spread = 0.3

        p1 = self.rect.center
        p2 = (int(p1[0] + math.cos(main_angle - spread) * dist), int(p1[1] + math.sin(main_angle - spread) * dist))
        p3 = (int(p1[0] + math.cos(main_angle + spread) * dist), int(p1[1] + math.sin(main_angle + spread) * dist))

        pygame.draw.polygon(fog_surface, (0, 0, 0, 0), [p1, p2, p3])
        pygame.draw.circle(fog_surface, (0, 0, 0, 0), p1, 80)

        # Перевірка ворогів всередині класу гравця
        for en in enemies:
            obj_x, obj_y = en.rect.center
            d = math.hypot(obj_x - p1[0], obj_y - p1[1])
            
            is_lit = False
            if d < 80: 
                is_lit = True
            elif d < dist:
                angle_to_obj = math.atan2(obj_y - p1[1], obj_x - p1[0])
                angle_diff = (angle_to_obj - main_angle + math.pi) % (2 * math.pi) - math.pi
                if abs(angle_diff) < spread:
                    is_lit = True
            
            # Малюємо ворога
            en.draw(screen, is_lit)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)