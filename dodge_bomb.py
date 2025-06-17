import os
import sys
import pygame as pg
import random 
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sbb_accs = [a for a in range(1, 11)]


def main() -> None:
    vx = random.randint(0,1100)
    vy = random.randint(0,650)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bb_imgs, bb_accs = make_bomb_imgs_accs()
    bb_img = bb_imgs[0]
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_rct = bb_img.get_rect()
    bb_rct.center = vx,vy
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    numx, numy = 5.0, 5.0
    orient_timer = 0
    orient_next = random.randint(100, 250)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        vx += numx
        vy += numy

        key_lst = pg.key.get_pressed()
        DELTA = {
            pg.K_UP:    (0, -5),
            pg.K_DOWN:  (0, +5),
            pg.K_LEFT:  (-5, 0),
            pg.K_RIGHT: (+5, 0)
        }
        sum_mv = [0, 0]
        for key, (dx, dy) in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += dx
                sum_mv[1] += dy
        old_pos = kk_rct.topleft
        kk_rct.move_ip(sum_mv)
        bb_rct.move_ip(numx, numy)

        # こうかとん画像の向きを移動量に応じて切り替え
        kk_img = get_kk_img(tuple(sum_mv))

        screen.blit(bg_img, [0, 0])
        screen.blit(bb_img, bb_rct)
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

        # こうかとんが画面外に出ない処理
        x_ok, y_ok = check_bound(kk_rct)
        if not x_ok or not y_ok:
            kk_rct.topleft = old_pos
            screen.blit(kk_img, kk_rct)

        x_ok, y_ok = check_bound(bb_rct)
        if not x_ok:
            numx *= -1  
        if not y_ok:
            numy *= -1  

        if kk_rct.colliderect(bb_rct):
            GameOver()

        orient_timer += 1
        if orient_timer >= orient_next:
            numx, numy = calc_orientation(bb_rct, kk_rct, (numx, numy))
            orient_timer = 0
            orient_next = random.randint(100, 250)

        # tmrの値に応じて段階を決定
        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        acc = bb_accs[idx]
        bb_rct = bb_img.get_rect(center=bb_rct.center)
        bb_rct.move_ip(numx * acc, numy * acc)
        
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    x_ok: bool = True  
    y_ok: bool = True  
    if rct.left < 0 or rct.right > WIDTH:
        x_ok = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        y_ok = False
    return x_ok, y_ok

def GameOver() -> None:
    screen = pg.display.get_surface()
    
    go_img = pg.Surface((WIDTH, HEIGHT))
    go_img.fill((0, 0, 0))
    go_img.set_alpha(180)
    screen.blit(go_img, (0, 0))
    font = pg.font.SysFont(None, 120)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    img = pg.image.load("fig/8.png")
    img = pg.transform.rotozoom(img, 0, 1.0)
    img_rect_l = img.get_rect(midright=(text_rect.left-40, HEIGHT//2))
    img_rect_r = img.get_rect(midleft=(text_rect.right+40, HEIGHT//2))
    screen.blit(text, text_rect)
    screen.blit(img, img_rect_l)
    screen.blit(img, img_rect_r)
    pg.display.update()
    time.sleep(5)
    return main()
    
#爆弾の大きさと速度に関する変数
def make_bomb_imgs_accs() -> tuple[list[pg.Surface], list[float]]:
    bb_imgs: list[pg.Surface] = []
    bb_accs: list[float] = [a/3 for a in range(1, 11)]
    for r in range(1, 11):
        bb_img: pg.Surface = pg.Surface((20*r, 20*r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    移動量の合計値タプルに対応する向きのこうかとん画像Surfaceを返す
    """
    # 向きごとの画像を辞書で用意（例: 8方向＋静止）
    kk_img = pg.image.load("fig/3.png")
    kf_img = pg.image.load("fig/3.png")
    kf_img = pg.transform.flip(kf_img, False, True)

    direction_imgs = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 0.9),         # 静止
        (5, 0): pg.transform.rotozoom(kf_img, 180, 0.9),       # 右
        (5, -5): pg.transform.rotozoom(kf_img, 225, 0.9),      # 右上
        (0, -5): pg.transform.rotozoom(kf_img, 270, 0.9),      # 上
        (-5, -5): pg.transform.rotozoom(kk_img, 315, 0.9),     # 左上
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 0.9),        # 左
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 0.9),       # 左下
        (0, 5): pg.transform.rotozoom(kf_img, 90, 0.9),        # 下
        (5, 5): pg.transform.rotozoom(kf_img, 135, 0.9),       # 右下
    }
    # 合計移動量を8方向に丸める
    dx, dy = sum_mv
    key = (0, 0)
    if dx > 0 and dy == 0:
        key = (5, 0)
    elif dx > 0 and dy < 0:
        key = (5, -5)
    elif dx == 0 and dy < 0:
        key = (0, -5)
    elif dx < 0 and dy < 0:
        key = (-5, -5)
    elif dx < 0 and dy == 0:
        key = (-5, 0)
    elif dx < 0 and dy > 0:
        key = (-5, 5)
    elif dx == 0 and dy > 0:
        key = (0, 5)
    elif dx > 0 and dy > 0:
        key = (5, 5)
    return direction_imgs[key]

def calc_orientation(
    org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]
) -> tuple[float, float]:
    """
    orgから見てdstがどこにあるかを計算し，方向ベクトル（ノルム√50）を返す
    近すぎる場合はcurrent_xyを返す
    """
    ox, oy = org.center
    dx, dy = dst.center
    vx, vy = dx - ox, dy - oy
    norm = (vx**2 + vy**2) ** 0.5
    if norm == 0:
        return (0, 0)
    if norm < 300:
        return current_xy  # 慣性
    scale = (50 ** 0.5) / norm
    return (vx * scale, vy * scale)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
