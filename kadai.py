import pygame
import random

# 画面サイズ
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 40

# ゲームフィールドのサイズ
FIELD_WIDTH = 6
FIELD_HEIGHT = 12

# ぷよのサイズ
PUYO_SIZE = 40

# ぷよの色
PuyoColors = ["red", "green", "blue", "yellow", "purple"]

# ぷよのスプライト
class Puyo(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((PUYO_SIZE, PUYO_SIZE))
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect(topleft=(x * CELL_SIZE, y * CELL_SIZE))
        self.falling = True

    def move_down(self):
        if self.rect.y + CELL_SIZE < SCREEN_HEIGHT:
            self.rect.y += CELL_SIZE
        else:
            self.falling = False

    def move_left(self):
        if self.rect.x - CELL_SIZE >= 0:
            self.rect.x -= CELL_SIZE

    def move_right(self):
        if self.rect.x + CELL_SIZE < SCREEN_WIDTH:
            self.rect.x += CELL_SIZE

    def rotate(self):
        if self.color == "yellow":
            center = self.rect.center
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect(center=center)
        elif self.color == "purple":
            pass  # パープルぷよは回転しない

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# ゲームの初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# ぷよのグループ
puyo_group = pygame.sprite.Group()

# フィールドの初期化
field = [[None for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for puyo in puyo_group.sprites():
                    puyo.move_left()
            if event.key == pygame.K_RIGHT:
                for puyo in puyo_group.sprites():
                    puyo.move_right()
            if event.key == pygame.K_SPACE:
                for puyo in puyo_group.sprites():
                    puyo.rotate()

    # 新しいぷよを追加
    if len(puyo_group) == 0 or not any(puyo.falling for puyo in puyo_group.sprites()):
        puyo1 = Puyo(random.choice(PuyoColors), 2, 0)
        puyo2 = Puyo(random.choice(PuyoColors), 3, 0)
        puyo_group.add(puyo1, puyo2)

    # ぷよの落下
    for puyo in puyo_group.sprites():
        puyo.move_down()

    # フィールドへのぷよの追加
    for puyo in puyo_group.sprites():
        if not puyo.falling:
            x_index = puyo.rect.x // CELL_SIZE
            y_index = puyo.rect.y // CELL_SIZE
            field[y_index][x_index] = puyo.color

    # 画面のクリア
    screen.fill((0, 0, 0))

    # ぷよの描画
    for puyo in puyo_group.sprites():
        puyo.draw(screen)

    # 画面の更新
    pygame.display.flip()
    clock.tick(10)  # 落下速度

pygame.quit()

