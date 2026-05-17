
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.side = "left"

    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(sprite.Sprite):
    def __init__(self, c1, c2, c3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.image = Surface((wall_width, wall_height))
        self.image.fill((c1, c2, c3,))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class KeySprite(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((30, 30))
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"),
                             (win_width, win_height))

player = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)
key_sprite = KeySprite(320, 230)

w1 = Wall(154, 205, 50, 300, 89, 67, 19)
w2 = Wall(154, 205, 50, 240, 260, 260, 20)
w3 = Wall(154, 205, 50, 100, 10, 15, 50)
w4 = Wall(154, 205, 50, 100, 30, 10, 230)
w5 = Wall(154, 205, 50, 260, 50, 13, 360)
walls = [w1, w2, w3, w4, w5]

game = True
finish = False
lives = 3
has_key = False
result = ""
clock = time.Clock()
FPS = 60

font.init()
big_font = font.Font(None, 70)
small_font = font.Font(None, 35)
win_text = big_font.render('YOU WIN!', True, (255, 215, 0))
lose_text = big_font.render('YOU LOSE!', True, (180, 0, 0))
need_key_text = small_font.render('Сначала возьми ключ!', True, (255, 255, 255))
restart_text = small_font.render('Нажми R, чтобы начать заново', True, (255, 255, 255))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

def restart_game():
    global finish, lives, has_key, result
    finish = False
    lives = 3
    has_key = False
    result = ""
    player.rect.x = 5
    player.rect.y = win_height - 80
    monster.rect.x = win_width - 80
    monster.rect.y = 280
    monster.side = "left"
    key_sprite.rect.x = 320
    key_sprite.rect.y = 230

def damage_player():
    global lives, finish, result
    lives -= 1
    kick.play()
    if lives <= 0:
        finish = True
        result = "lose"
    else:
        player.rect.x = 5
        player.rect.y = win_height - 80

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_r:
            restart_game()

    window.blit(background, (0, 0))

    if not finish:
        player.update()
        monster.update()
        player.reset()
        monster.reset()
        final.reset()
        for wall in walls:
            wall.draw_wall()
        if not has_key:
            key_sprite.reset()
        if sprite.collide_rect(player, key_sprite) and not has_key:
            has_key = True
        if sprite.collide_rect(player, monster):
            damage_player()
        for wall in walls:
            if sprite.collide_rect(player, wall):
                damage_player()
                break
        if sprite.collide_rect(player, final):
            if has_key:
                finish = True
                result = "win"
                money.play()
            else:
                window.blit(need_key_text, (220, 150))

        lives_text = small_font.render("Жизни: " + str(lives), True, (255, 255, 255))
        key_text = small_font.render("Ключ: " + ("есть" if has_key else "нет"), True, (255, 255, 255))
        window.blit(lives_text, (10, 10))
        window.blit(key_text, (10, 40))
    else:
        player.reset()
        monster.reset()
        final.reset()
        for wall in walls:
            wall.draw_wall()
        if result == "win":
            window.blit(win_text, (200, 200))
        if result == "lose":
            window.blit(lose_text, (200, 200))
        window.blit(restart_text, (170, 280))

    display.update()
    clock.tick(FPS)

