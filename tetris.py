import pygame as pg
import sys
from time import sleep

x = 0
y = 0
x, y = 20, 12
grid = [[0 for b in range(y)] for a in range(x)]   # 20*12个格子，20*20的格子之间的间隙是5
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

pg.init()
screen = pg.display.set_mode((640, 500))

# rect1 = pg.draw.rect( (x_coordinate, y_coordinate), (#a rgb color), (#size of rect in pixels) )


def main():
    draw_wall()
    draw_ground()
    fall()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()


def fall():
    row = 0     # 代表行从0开始第5个格子
    col = 5  # 代表列  从0开始第5列格子
    number = 0
    while 1:
        pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20))  # 下落
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    moving = "left"
                    print("Left arrow key has been pressed.")
                elif event.key == pg.K_RIGHT:
                    moving = "right"
                    print("Right arrow key has been pressed.")
                elif event.key == pg.K_UP:
                    moving = "up"
                    print("Up arrow key has been pressed.")
                elif event.key == pg.K_DOWN:
                    moving = "down"
                    print("Down arrow key has been pressed.")
            else:
                moving = "hello"
            pg.draw.rect(screen, BLACK, (col*25, row*25, 20, 20))  # 清除
            pg.display.update()
            if (moving == "left" ) and col>1:   #防止撞到左墙
                col -= 1
            if (moving == "right") and col<10:    #防止撞到右墙
                col += 1
            if moving == "up":
                row -= 1
            if moving == "down":
                col += 1
            pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20))  # 下落
            pg.display.update()
        
        if  number == 100:
            number = 0
            print("row:",row)
            print("col：",col)
            print("Grid:",grid[row+1][col])
            if grid[row+1][col] == 0:
                pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20))  # 下落
                pg.display.update()
                # sleep(1)
                pg.draw.rect(screen, BLACK, (col*25, row*25, 20, 20))  # 清除
                pg.display.update()
                row = row+1
            else:
                if row==0:
                    print("Game Over!")
                    pg.quit()
                    sys.exit()
                else:
                    pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20))  # 下落
                    pg.display.update()
                    grid[row][col] = 1
                    row = 0
        else:
            number=number +1
   
               
def draw_wall():
    y = 0  # 代表列的格子个数
    row = 0 # 代表行
    number = 0
    while number < 19: #0~18共19层
        pg.draw.rect(screen, WHITE, (0, row*25, 20, 20))  # 左墙
        y=0
        grid[row][y] = 1
        pg.draw.rect(screen, WHITE, (11*25, row*25, 20, 20)) # 右墙
        y=11
        grid[row][y]=1
        row=row+1  # 下一行
        number=number+1
    pg.display.update()


def draw_ground():
    row=19  # 一共0~19层共20层格子，上面有19层
    col=0  
    number=0
    while number < 12:
        pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20))  # 底墙
        grid[row][col]=1
        col=col+1
        number=number+1
    pg.display.update()

if __name__ == '__main__':
    main()
