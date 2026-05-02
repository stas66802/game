import pygame

class Bullet:
    def __init__(self, x, y, dx, dy, speed, color, damage, b_type="normal"):
        self.pos = pygame.Vector2(x, y)
        self.dir = pygame.Vector2(dx, dy)
        self.speed = speed
        self.color = color
        self.damage = damage
        self.type = b_type
        self.alive = True

    def update(self, w_width,w_height):
        # Рух
        self.pos += self.dir * self.speed
        # Перевірка виходу за межі
        if self.pos.x < 0 or self.pos.x > w_width or self.pos.y < 0 or self.pos.y > w_height:
            self.alive = False

    def draw(self, screen):
        if self.type == "laser":
            # Малюємо смужку
            end_pos = self.pos - self.dir * 30
            pygame.draw.line(screen, self.color, self.pos, end_pos, 4)
        elif self.type == "shotgun":
            # Малюємо кружок
            pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), 4)
        else:
            # Звичайний квадратик
            pygame.draw.rect(screen, self.color, (int(self.pos.x)-2, int(self.pos.y)-2, 5, 5))

    def get_rect(self):
        # Потрібно для колізій
        return pygame.Rect(int(self.pos.x)-3, int(self.pos.y)-3, 6, 6)
