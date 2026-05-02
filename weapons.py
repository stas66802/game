import random
from bullets import *

class Weapon:
    TYPE = "normal"
    def __init__(self, name, damage, bullet_color, bullet_speed):
        self.name = name
        self.damage = damage
        self.bullet_color = bullet_color
        self.bullet_speed = bullet_speed

    def shoot(self, x, y, dx, dy, bullets_list):
        # Логіка за замовчуванням (normal)
        new_bullet = Bullet(x, y, dx, dy, self.bullet_speed, self.bullet_color, self.damage, self.TYPE)
        bullets_list.append(new_bullet)

    def getName(self):
        return self.name
    def getDamage(self):
        return self.damage
    def getBulletColor(self):
        return self.bullet_color
    def getBulletSpeed(self):
        return self.bullet_speed


class Shotgun(Weapon):
    TYPE = "shotgun"
    def shoot(self, x, y, dx, dy, bullets_list):
        for _ in range(5):
            sx = dx + random.uniform(-0.2, 0.2)
            sy = dy + random.uniform(-0.2, 0.2)
            bullets_list.append(Bullet(x, y, sx, sy, self.bullet_speed, self.bullet_color, self.damage, self.TYPE))

class Laser(Weapon):
    TYPE = "laser"
    def shoot(self, x, y, dx, dy, bullets_list):
        bullets_list.append(Bullet(x, y, dx, dy, self.bullet_speed, self.bullet_color, self.damage, self.TYPE))

