import pygame as pg
import sys
from time import sleep


x, y = 20, 12
grid = [[0 for b in range(y)] for a in range(x)]   # 20行*12列个格子，20*20的格子之间的间隙是5
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
    row1=0
    col1 =6
    number = 0
    while 1:
        draw_square(col,row,WHITE)     # 下落
        draw_square(col1,row1,WHITE)
        row, col,row1,col1 = handle_move(row, col,row1,col1)
        if number == 800:  # 控制下落的速度
            number = 0
            print("row:", row)
            print("col：", col)
            print("Grid:", grid[row+1][col])
            if grid[row+1][col] == 1 or grid[row1+1][col1] == 1:  # 下行有，堆积
                row = heap_up(row, col)  # 堆积
                row = heap_up(row1, col1)  # 堆积
                erase(row)
                erase(row1)
                row =0   #从0行的头开始
                row1=0
            else:
                draw_square(col,row,WHITE)
                draw_square(col,row,BLACK)
                draw_square(col1,row1,WHITE)
                draw_square(col1,row1,BLACK)
                row = row+1
                row1 = row1+1
        else:
            number = number + 1

def draw_square(col,row,color):
    pg.draw.rect(screen, color, (col*25, row*25, 20, 20))  # 下落
    pg.display.update()

def draw_wall():
    y = 0  # 代表列的格子个数
    row = 0  # 代表行
    number = 0
    while number < 19:  # 0~18共19层
        pg.draw.rect(screen, WHITE, (0, row*25, 20, 20))  # 左墙
        y = 0
        grid[row][y] = 1
        pg.draw.rect(screen, WHITE, (11*25, row*25, 20, 20))  # 右墙
        y = 11
        grid[row][y] = 1
        row = row+1  # 下一行
        number = number+1
    pg.display.update()


def draw_ground():
    row = 19  # 一共0~19层共20层格子，上面有19层
    col = 0
    number = 0
    while number < 12:
        pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20))  # 底墙
        grid[row][col] = 1
        col = col+1
        number = number+1
    pg.display.update()


def handle_move(row, col,row1,col1):
    moving = "None"
    for event in pg.event.get():
        moving = "none"
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
            moving = "None"
    if moving != "None":
        draw_square(col,row,BLACK)
        draw_square(col1,row1,BLACK)
        pg.display.update()
        if (moving == "left") and grid[row][col-1] == 0:  # 防止撞到左墙以及左侧无方块
            col -= 1
            col1 -= 1
        if (moving == "right") and grid[row1][col1+1] == 0:  # 防止撞到右墙以及右侧无方块
            col += 1
            col1 += 1
        if moving == "up":
            row -= 1
            row1 -= 1
        if moving == "down" and grid[row+1][col] == 0 and grid[row1+1][col1] == 0 :  # 防止出底界
            row += 1
            row1 += 1
        draw_square(col,row,WHITE)
        draw_square(col1,row1,WHITE)
    return row, col,row1,col1


def heap_up(row, col):
    if row == 0:
        print("Game Over!")
        pg.quit()
        sys.exit()
    else:
        pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20))  # 下落
        pg.display.update()
        grid[row][col] = 1
        return row


def erase(row):
    clear_line = 1
    y = 1   #从第1格开始，第0格是墙
    while y < 11:
        if grid[row][y] == 0:
            clear_line = 0
        y += 1
    col = 1
    while clear_line == 1 and col < 11:
        pg.draw.rect(screen, BLACK, (col*25, row*25, 20, 20))  # 消除行
        grid[row][col] = 0   # 重置状态
        col+=1
    pg.display.update()
    if clear_line == 1 :
      drop_down(row)  # 上面的都落下来

def drop_down(row):
    while row-1>=0:
        col =1
        while  col<11 :
            if grid[row-1][col] == 1:
                pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20)) 
                grid[row][col] = 1
                pg.display.update()
                pg.draw.rect(screen, BLACK, (col*25, (row-1)*25, 20, 20))
                grid[row-1][col] = 0   
                pg.display.update()
            col+=1
        row -=1



if __name__ == '__main__':
    main()
