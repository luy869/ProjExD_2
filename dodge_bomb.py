import os
import sys
import pygame as pg
import random 


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    vx = random.randint(0,1100)
    vy = random.randint(0,650)
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bb_img = pg.Surface((20,20))
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
    numx = 5
    numy = 5
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
        # 爆弾は速度分だけ移動
        bb_rct.move_ip(numx, numy)
        screen.blit(bb_img,bb_rct)
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if check_bound(kk_rct) == 0:
            kk_rct.topleft = old_pos
            screen.blit(kk_img, kk_rct)
        # 爆弾の範囲チェック
        x_ok, y_ok = check_bound(bb_rct)
        if not x_ok:
            numx *= -1  # X方向反転
        if not y_ok:
            numy *= -1  # Y方向反転

            

        

def check_bound(rct):
    x_ok = True  # X座標が範囲内か
    y_ok = True  # Y座標が範囲内か
    if rct.left < 0 or rct.right > WIDTH:
        x_ok = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        y_ok = False
    return x_ok, y_ok

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
