import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1200, 700
delta = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0)
}

accs = [a for a in range(1, 11)]


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect，爆弾Rectが画面外 or 画面内かを判定する関数
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向，縦方向の判定結果タプル（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img_r = pg.transform.flip(kk_img, True, False)

    senkai = {
        (0,-5):pg.transform.rotozoom(kk_img_r, 90, 2.0),
        (+5,-5):pg.transform.rotozoom(kk_img_r, -45, 2.0),
        (+5,0):pg.transform.rotozoom(kk_img_r, 0, 2.0),
        (+5,+5):pg.transform.rotozoom(kk_img_r, -45, 2.0),
        (0,+5):pg.transform.rotozoom(kk_img_r, -90, 2.0),
        (-5,+5):pg.transform.rotozoom(kk_img, 45, 2.0),
        (-5,0):pg.transform.rotozoom(kk_img, 0, 2.0),
        (-5,-5):pg.transform.rotozoom(kk_img, -45, 2.0),
        (0,0):pg.transform.rotozoom(kk_img, 0, 2.0)
    }  #こうかとんの身体の向きの回転

    kk_rct = kk_img.get_rect()
    kk_rct.center = WIDTH/2,HEIGHT/2

    bd_img = pg.Surface((20,20))  #練習1
    bd_img.set_colorkey((0,0,0))
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)
    bd_rct = bd_img.get_rect()  #爆弾Surfaceから爆弾rectを抽出する
    bd_rct.center = x, y  #爆弾rectの中心座標を乱数で指定する

    vx, vy = +5, +5  #練習2
    

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct):
            print("GAME OVER")
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, mv in delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        kk_img = senkai[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        #if tmr <= 9:
        #    vx += ((accs[tmr]*1.01) - 1)
        #    vy += ((accs[tmr]*1.01) - 1)
        bd_rct.move_ip(vx, vy)
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bd_img, bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(20)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()