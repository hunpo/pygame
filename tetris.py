from typing import overload
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



def main():
    draw_wall_ground()
    fall()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

def draw_square(col,row,color):
    pg.draw.rect(screen, color, (col*25, row*25, 20, 20))  # 下落
    # pg.display.update()

def draw_wall_ground():
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
    row = 19  # 一共0~19层共20层格子，上面有19层
    col = 0
    while col <=11:
        pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20))  # 底墙
        grid[row][col] = 1
        col = col+1
    pg.display.update()

def move(row,col,rotate):
    row1,col1 = calculate_position(row,col,rotate)
    print("row1",row1)
    print("col1",col1)
    draw_square(col,row,WHITE)
    draw_square(col1,row1,WHITE)
    pg.display.update()
    draw_square(col,row,BLACK)   # 黑色是下一次循环更新
    draw_square(col1,row1,BLACK)


def overlap(row,col,rotate):
    row1,col1 = calculate_position(row,col,rotate)
    print("row",row)
    print("col",col)
    print("row1",row1)
    print("col1",col1)
    if grid[row][col] == 1 or grid[row1][col1] == 1:
       return 1
    else:
       return 0

def heap_up(row, col):
    if row == 0:
        print("Game Over!")
        pg.quit()
        sys.exit()
    else:
        draw_square(col,row,WHITE)  # 下落
        pg.display.update()
        grid[row][col] = 1

def erase_row():
    row = 0   #从第0行开始
    print("begin erase")
    while row< 19:
        clear_line = 1
        col =1
        while  col <= 10:
            if grid[row][col] == 0:
                clear_line = 0
            col += 1
        print("clear line",clear_line)
        if clear_line ==1:
            col =1
            while  col <= 10:
                grid[row][col] = 0   # 重置状态
                draw_square(col,row,BLACK)
                col+=1
            drop_down(row)  # 上面的都落下来
        row+=1

def heap_up_erase(row,col,rotate):
    row1,col1 = calculate_position(row,col,rotate)
    heap_up(row, col)
    heap_up(row1, col1)
    erase_row()


    

def drop_down(row):
    row=row-1 # 删除行的上一行
    while row>=0:
        col =1
        while  col<=10 :
            if grid[row][col] == 1:
                draw_square(col,row,BLACK)
                grid[row][col] = 0   
                pg.display.update()
                heap_up(row+1, col)  #堆积到删除行
            col+=1
        row -=1

def calculate_position(row,col,rotate):
    row1 = row
    col1 = col
    if rotate == 0:
       col1= col+1 
    if rotate == 1:
        row1 =row+1
    if rotate==2:
        col1=col-1
    if rotate ==3:
        row1=row-1
    if rotate == 4:
        rotate =0
    return row1,col1

def fall():
    rotate = 0
    row = 0     # 代表行从0开始第5个格子
    col = 5  # 代表列  从0开始第5列格子
    fall_number = 0
    while 1:
        horizontal_distance = 0
        vertical_distance = 0
        rotate_distance = 0
        moving = "None"
        for event in pg.event.get():
            # moving = "none"
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
                if moving == "left":  
                    horizontal_distance  -= 1
                if moving == "right":  
                    horizontal_distance   += 1
                if moving == "up":
                    rotate_distance += 1
        print("horizontal_distance",horizontal_distance)
        print("rotate_distance",rotate_distance)   
        fall_number += 1
        if fall_number ==50:
            vertical_distance = 1
            fall_number = 0
        col = col + horizontal_distance
        row = row + vertical_distance
        rotate = rotate +rotate_distance
        if overlap(row,col,rotate):   # 
            col = col - horizontal_distance
            row = row - vertical_distance
            rotate = rotate - rotate_distance
            if vertical_distance>0 and horizontal_distance ==0: # If 重叠 Then 堆积
                heap_up_erase(row, col,rotate)
                rotate = 0
                row = 0  
                col = 5  
        print("row",row)
        print("col",col)
        move(row,col,rotate)


  
if __name__ == '__main__':
    main()
