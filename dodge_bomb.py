import os
import sys
import pygame as pg
import random 


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    rmb_xy = 0
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,1100), random.randint(0,650)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

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
        screen.blit(bb_img,bb_rct)
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if check_bound(kk_rct) == 0:
            kk_rct.topleft = old_pos
            screen.blit(kk_img, kk_rct)
            

        

def check_bound(rct):
    if rct.x > 1050 or rct.x < 0:
        return False
    if rct.y > 600 or rct.y < 0:
        return False
    return True



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
