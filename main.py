import os
os.environ["SDL_VIDEO_CENTERED"] = "1"

import pgzrun
import math
from pygame import Rect

mouse_x = mouse_y = 0

WIDTH = 800
HEIGHT = 600
TITLE = "Python Platformer"
FPS = 60

GAME_STATES = {"MENU": 0, "PLAYING": 1, "GAME_OVER": 2, "WIN": 3}

current_state, music_on, sounds_on, score, ui_tick = GAME_STATES["MENU"], True, True, 0, 0

def draw_platforms(platforms):
    gt, cl, cm, cr = images.terrain_grass_block_top, images.terrain_grass_cloud_left, images.terrain_grass_cloud_middle, images.terrain_grass_cloud_right
    gw, cw = gt.get_width(), cm.get_width()
    for x,y,w,h in platforms:
        is_ground = (x==0 and y==HEIGHT-50 and w==WIDTH and h==50)
        if is_ground:
            for tx in range(x, x+w, gw): screen.blit(gt,(tx,y))
        else:
            t = max(1, math.ceil(w/cw))
            screen.blit(cl,(x,y))
            for i in range(1, t-1): screen.blit(cm,(x+i*cw,y))
            if t>1: screen.blit(cr,(x+(t-1)*cw,y))

class Player:
    def __init__(self):
        base_img = images.player_idle1
        self.width = base_img.get_width()
        self.height = base_img.get_height()
        self.x = 100
        self.y = (HEIGHT - 50) - self.height
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 17
        self.is_jumping = False
        self.facing_right = True
        self.frame = 0
        self.frame_delay = 0
        self.alive = True
        self.state = "idle"
        self.sprites_idle = ["player_idle1", "player_idle2"]
        self.sprites_walk_right = ["player_walk1", "player_walk2"]
        self.sprites_walk_left = ["player_walk1_left", "player_walk2_left"]

    def update(self, platforms, enemies):
        global current_state, score, flag

        if not self.alive:
            return

        if keyboard.left:
            self.x -= self.speed
            self.facing_right = False
            self.state = "walk"
        elif keyboard.right:
            self.x += self.speed
            self.facing_right = True
            self.state = "walk"
        else:
            self.state = "idle"

        self.vel_y += 1
        self.y += self.vel_y

        player_rect = Rect(self.x, self.y, self.width, self.height)

        foot_margin = max(4, self.width // 4)
        foot_w = max(1, self.width - foot_margin * 2)
        foot_rect = Rect(self.x + foot_margin, self.y + self.height - 5, foot_w, 5)

        head_margin = max(6, self.width // 3)
        head_w = max(1, self.width - head_margin * 2)
        head_rect = Rect(self.x + head_margin, self.y, head_w, 6)

        for x, y, w, h in platforms:
            is_ground = (x == 0 and y == HEIGHT - 50 and w == WIDTH and h == 50)

            if is_ground:
                plat_rect = Rect(x, y, w, h)
            else:
                cloud_mid = images.terrain_grass_cloud_middle
                cloud_w = cloud_mid.get_width()
                tiles_count = max(1, math.ceil(w / cloud_w))
                visual_w = tiles_count * cloud_w
                plat_rect = Rect(x, y, visual_w, h)

            if foot_rect.colliderect(plat_rect) and self.vel_y > 0:
                self.y = y - self.height
                self.vel_y = 0
                self.is_jumping = False
                player_rect = Rect(self.x, self.y, self.width, self.height)
                foot_rect = Rect(self.x + foot_margin, self.y + self.height - 5, foot_w, 5)
                head_rect = Rect(self.x + head_margin, self.y, head_w, 6)

            if head_rect.colliderect(plat_rect) and self.vel_y < 0:
                self.y = y + h
                self.vel_y = 0
                player_rect = Rect(self.x, self.y, self.width, self.height)
                foot_rect = Rect(self.x + foot_margin, self.y + self.height - 5, foot_w, 5)
                head_rect = Rect(self.x + head_margin, self.y, head_w, 6)

        head_rect = Rect(self.x + head_margin, self.y, head_w, 6)

        if keyboard.up and not self.is_jumping:
            self.vel_y = -self.jump_power
            self.is_jumping = True
            if sounds_on:
                sounds.jump.play()

        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = min(HEIGHT - self.height, self.y)

        player_rect = Rect(self.x, self.y, self.width, self.height)

        self.frame_delay += 1
        if self.frame_delay >= 10:
            frames = self.sprites_walk_right if self.state == "walk" else self.sprites_idle
            self.frame = (self.frame + 1) % len(frames)
            self.frame_delay = 0

        for coin in coins:
            if coin.collected:
                continue

            coin_rect = coin.rect()

            if (
                player_rect.left <= coin_rect.left
                and player_rect.right >= coin_rect.right
                and player_rect.top <= coin_rect.top
                and player_rect.bottom >= coin_rect.bottom
            ):
                coin.collected = True
                score += 1
                if sounds_on:
                    sounds.coin.play()

        for enemy in enemies:
            hit_margin_x = max(12, int(enemy.width * 0.42))
            hit_margin_y = max(12, int(enemy.height * 0.42))
            enemy_rect = Rect(
                enemy.x + hit_margin_x,
                enemy.y + hit_margin_y,
                enemy.width - hit_margin_x * 2,
                enemy.height - hit_margin_y * 2,
            )

            if player_rect.colliderect(enemy_rect):
                self.alive = False
                if sounds_on:
                    sounds.hit.play()
                current_state = GAME_STATES["GAME_OVER"]

        if score >= 2:
            flag_rect = flag.rect()
            if (
                player_rect.left <= flag_rect.left
                and player_rect.right >= flag_rect.right
                and player_rect.top <= flag_rect.top
                and player_rect.bottom >= flag_rect.bottom
            ):
                current_state = GAME_STATES["WIN"]

    def draw(self):
        if not self.alive:
            return
        if self.state == "walk":
            sprite_name = (self.sprites_walk_right if self.facing_right else self.sprites_walk_left)[self.frame]
        else:
            sprite_name = self.sprites_idle[self.frame % len(self.sprites_idle)]
        screen.blit(getattr(images, sprite_name), (self.x, self.y))


class Enemy:
    def __init__(self, x, y, patrol_range, min_x=None, max_x=None):
        self.x = x
        self.sprites_right = ["barnacle_attack_a", "barnacle_attack_b"]
        self.sprites_left = ["barnacle_attack_a", "barnacle_attack_b"]
        enemy_frames = [images.barnacle_attack_a, images.barnacle_attack_b]
        self.width = max(img.get_width() for img in enemy_frames)
        self.height = max(img.get_height() for img in enemy_frames)
        self.y = y - self.height
        self.patrol_range = patrol_range
        self.direction = 1
        self.speed = 2
        self.frame = 0
        self.frame_delay = 0
        self.start_x = x
        self.min_x = min_x
        self.max_x = max_x

    def update(self):
        self.x += self.speed * self.direction

        left_bound = self.min_x if self.min_x is not None else (self.start_x - self.patrol_range)
        right_bound = self.max_x if self.max_x is not None else (self.start_x + self.patrol_range)

        current_list = self.sprites_right if self.direction > 0 else self.sprites_left
        sprite = getattr(images, current_list[self.frame])
        sprite_w = sprite.get_width()
        offset_x = (self.width - sprite_w) // 2

        min_x_allowed = left_bound - offset_x
        max_x_allowed = right_bound - sprite_w - offset_x

        if self.x < min_x_allowed:
            self.x = min_x_allowed
            self.direction = 1
        elif self.x > max_x_allowed:
            self.x = max_x_allowed
            self.direction = -1

        self.frame_delay += 1
        if self.frame_delay >= 15:
            self.frame = (self.frame + 1) % len(self.sprites_right)
            self.frame_delay = 0

    def draw(self):
        sprite_name = (self.sprites_right if self.direction > 0 else self.sprites_left)[self.frame]
        sprite = getattr(images, sprite_name)
        draw_x = self.x + (self.width - sprite.get_width()) // 2
        draw_y = self.y + (self.height - sprite.get_height())
        screen.blit(sprite, (draw_x, draw_y))


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        img = images.coin_gold
        self.width = img.get_width()
        self.height = img.get_height()

    def rect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        if self.collected:
            return
        bob = int(3 * math.sin((ui_tick + self.x) / 10))
        screen.blit(images.coin_gold, (self.x, self.y + bob))


class Flag:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames = ["flag_green_a", "flag_green_b"]
        self.frame = 0
        self.frame_delay = 0
        base = images.flag_green_a
        self.width = base.get_width()
        self.height = base.get_height()

    def rect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.frame_delay += 1
        if self.frame_delay >= 12:
            self.frame = (self.frame + 1) % len(self.frames)
            self.frame_delay = 0

    def draw(self):
        screen.blit(getattr(images, self.frames[self.frame]), (self.x, self.y))


class Button:
    def __init__(self, x, y, text, action):
        self.x = x
        self.y = y
        self.text = text
        self.action = action
        self.width = 200
        self.height = 50


platforms = [
    [0, HEIGHT - 50, WIDTH, 50],
    [200, HEIGHT - 150, 200, 20],
    [500, HEIGHT - 250, 200, 20],
    [100, HEIGHT - 350, 200, 20],
    [600, HEIGHT - 400, 100, 20],
]


def make_enemies():
    return [
        Enemy(300, HEIGHT - 50, 100, min_x=0, max_x=WIDTH),
        Enemy(550, HEIGHT - 250, 80, min_x=505, max_x=750),
        Enemy(150, HEIGHT - 350, 60, min_x=105, max_x=350),
    ]


def make_coins():
    coin_img = images.coin_gold
    coin_w = coin_img.get_width()
    coin_h = coin_img.get_height()

    plat_left = platforms[3]
    coin1_x = plat_left[0] + (plat_left[2] - coin_w) // 2 + 50
    coin1_y = plat_left[1] - coin_h

    plat_right = platforms[2]
    coin2_x = plat_right[0] + (plat_right[2] - coin_w) // 2
    coin2_y = plat_right[1] - coin_h

    return [Coin(coin1_x, coin1_y), Coin(coin2_x, coin2_y)]


def make_flag():
    flag_img = images.flag_green_a
    flag_w = flag_img.get_width()
    flag_h = flag_img.get_height()

    last_plat = platforms[4]
    flag_x = last_plat[0] + (last_plat[2] // 2) - (flag_w // 2) + 35
    flag_y = last_plat[1] - flag_h

    return Flag(flag_x, flag_y)


player = Player()
coins = make_coins()
flag = make_flag()
enemies = make_enemies()

buttons = [
    Button(WIDTH // 2 - 100, 200, "START GAME", "start"),
    Button(WIDTH // 2 - 100, 270, "MUSIC: ON", "toggle_music"),
    Button(WIDTH // 2 - 100, 340, "SOUNDS: ON", "toggle_sounds"),
    Button(WIDTH // 2 - 100, 410, "QUIT", "quit"),
]


def update():
    global current_state, music_on, sounds_on, ui_tick
    ui_tick += 1

    if current_state == GAME_STATES["PLAYING"]:
        player.update(platforms, enemies)
        [e.update() for e in enemies]
        flag.update()

    music.play("background") if music_on and not music.is_playing("background") else music.stop() if not music_on else None


def draw():
    screen.clear(); screen.fill((135,206,235))
    {GAME_STATES["MENU"]: draw_menu, GAME_STATES["PLAYING"]: draw_game,
     GAME_STATES["GAME_OVER"]: draw_game_over, GAME_STATES["WIN"]: draw_win}[current_state]()

def draw_menu():
    screen.fill((135, 206, 235))
    draw_platforms([[0, HEIGHT-50, WIDTH, 50]])
    draw_platforms([[160,185,480,20],[220,455,360,20]])

    title_y = 95
    screen.draw.text(
        "PLATFORMER ADVENTURE",
        center=(WIDTH // 2 + 2, title_y + 2),
        fontsize=60,
        color=(20, 60, 90),
    )
    screen.draw.text(
        "PLATFORMER ADVENTURE",
        center=(WIDTH // 2, title_y),
        fontsize=60,
        color="white",
    )

    bob = int(3 * math.sin(ui_tick / 10))

    menu_plat_x = 160
    menu_plat_y = 185
    menu_plat_w = 480

    coin_img = images.coin_gold
    coin_x = menu_plat_x + 70
    coin_y = menu_plat_y - coin_img.get_height()
    screen.blit(coin_img, (coin_x, coin_y + bob))

    flag_frame = "flag_green_a" if (ui_tick // 12) % 2 == 0 else "flag_green_b"
    flag_img = getattr(images, flag_frame)
    flag_x = menu_plat_x + menu_plat_w - flag_img.get_width() - 70
    flag_y = menu_plat_y - flag_img.get_height()
    screen.blit(flag_img, (flag_x, flag_y))

    for btn in buttons:
        hovered = mouse_pos_over_button(btn)
        lift = -2 if hovered else 0
        bx = btn.x
        by = btn.y + lift + 25

        bg = (40, 120, 200) if not hovered else (60, 170, 90)
        border = (20, 50, 90)

        screen.draw.filled_rect(Rect(bx, by, btn.width, btn.height), bg)
        screen.draw.rect(Rect(bx, by, btn.width, btn.height), border)

        screen.draw.text(
            btn.text,
            center=(bx + btn.width // 2, by + btn.height // 2),
            fontsize=30,
            color="white",
        )

    screen.draw.text(
        "Use ←/→ to move, ↑ to jump",
        center=(WIDTH // 2, 565),
        fontsize=26,
        color="white",
    )


def draw_game():
    draw_platforms(platforms)
    [c.draw() for c in coins]; flag.draw(); player.draw(); [e.draw() for e in enemies]

    if player.alive:
        screen.draw.text("ALIVE", (10, 10), fontsize=30, color="green")

    screen.draw.text(f"COINS: {score}/2", (10, 45), fontsize=24, color="white")


def draw_game_over():
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=80, color="red")
    screen.draw.text("Click to return to menu", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")


def draw_win():
    screen.draw.text("YOU WIN!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=80, color="green")
    screen.draw.text("Click to return to menu", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")


def on_mouse_down(pos):
    global current_state, music_on, sounds_on

    if current_state == GAME_STATES["MENU"]:
        for btn in buttons:
            if mouse_pos_over_button(btn):
                if btn.action == "start":
                    reset_game(); current_state = GAME_STATES["PLAYING"]
                elif btn.action == "toggle_music":
                    music_on = not music_on
                    btn.text = f"MUSIC: {'ON' if music_on else 'OFF'}"
                    if not music_on:
                        music.stop()
                elif btn.action == "toggle_sounds":
                    sounds_on = not sounds_on
                    btn.text = f"SOUNDS: {'ON' if sounds_on else 'OFF'}"
                elif btn.action == "quit":
                    quit()
    elif current_state in (GAME_STATES["GAME_OVER"], GAME_STATES["WIN"]): reset_game(); current_state = GAME_STATES["MENU"]


def on_key_down(key):
    global current_state
    if current_state == GAME_STATES["GAME_OVER"] and key == keys.R: reset_game(); current_state = GAME_STATES["MENU"]


def mouse_pos_over_button(button):
    return (
        button.x <= mouse_x <= button.x + button.width
        and button.y <= mouse_y <= button.y + button.height
    )


def on_mouse_move(pos):
    global mouse_x, mouse_y
    mouse_x, mouse_y = pos


def reset_game():
    global player, enemies, coins, score, flag
    player, enemies, coins, flag, score = Player(), make_enemies(), make_coins(), make_flag(), 0
    buttons[1].text = f"MUSIC: {'ON' if music_on else 'OFF'}"
    buttons[2].text = f"SOUNDS: {'ON' if sounds_on else 'OFF'}"


pgzrun.go()