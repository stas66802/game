import os
import pygame

# Window size
DEF_WIDTH, DEF_HEIGHT = 900, 650 

# Colors

WHITE = (255,255,255) 
BLACK = (0,0,0) 
RED = (200,0,0) 
BLUE = (0,150,255) 
PURPLE = (150,0,200) 
YELLOW = (255,255,0) 
GREEN = (0,200,0) 
ORANGE = (255,140,0)
GRAY = (50, 50, 50)


assets = {
    "ghost": None,
    "ghost2": None,
    "background": None,
    "player": None,
    "font": None
}

def load_all_assets():
    """Цю функцію викликаємо ОДИН РАЗ у main.py після set_mode"""
    global assets
    
    try:
        # Завантаження ворога
        assets["ghost"] = pygame.image.load(os.path.join("resources", "ghost.png")).convert_alpha()
        assets["ghost2"] = pygame.image.load(os.path.join("resources", "ghost2.png")).convert_alpha()
        # Завантаження фону
        assets["background"] = pygame.image.load(os.path.join("resources", "bg_3.jpg")).convert()

        # Завантаження фону
        #assets["player"] = pygame.image.load(os.path.join("resources", "player.png")).convert()
        
        print("Всі ресурси завантажено успішно!")
    except pygame.error as e:
        print(f"Помилка завантаження файлів: {e}")
        # Створюємо заглушки, щоб гра не вилітала, якщо файлів немає
        assets["ghost"] = pygame.Surface((40, 40), pygame.SRCALPHA)
        assets["background"] = pygame.Surface((WIDTH, HEIGHT))