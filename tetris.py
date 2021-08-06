from typing import overload
import pygame as pg
import sys
from time import sleep


x, y = 20, 12
grid = [[0 for b in range(y)] for a in range(x)]   # 20行*12列个格子，20*20的格子之间的间隙是5
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
data = [[0, -1, 0, 1, 0, 2],
        [-1, -1, 0, -1, 0, 1],
        [0, -1, -1, 0, 0, 1],
        [0, -1, -1, 1, 0, 1],
        [0, -1, 1, 0, 1, 1],
        [0, 1, 1, 0, 1, 1],
        [0, 1, 1, -1, 1, 0]]

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


def draw_square(col, row, color):
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
    while col <= 11:
        pg.draw.rect(screen, WHITE, (col*25, row*25, 20, 20))  # 底墙
        grid[row][col] = 1
        col = col+1
    pg.display.update()


def move(row, col, rotate, category):
    row1, col1, row2, col2, row3, col3 = calculate_position(
        row, col, rotate, category)
    print("row1", row1)
    print("col1", col1)
    draw_square(col, row, RED)
    draw_square(col1, row1, RED)
    draw_square(col2, row2, RED)
    draw_square(col3, row3, RED)
    pg.display.update()
    draw_square(col, row, BLACK)   # 黑色是下一次循环更新
    draw_square(col1, row1, BLACK)
    draw_square(col2, row2, BLACK)
    draw_square(col3, row3, BLACK)


def overlap(row, col, rotate, category):
    row1, col1, row2, col2, row3, col3 = calculate_position(
        row, col, rotate, category)
    if grid[row][col] == 1 or grid[row1][col1] == 1 or grid[row2][col2] == 1 or grid[row3][col3] == 1:
        return 1
    else:
        return 0


def heap_up(row, col):
    if row == 0:
        print("Game Over!")
        pg.quit()
        sys.exit()
    else:
        draw_square(col, row, WHITE)  # 下落
        pg.display.update()
        grid[row][col] = 1


def erase_row():
    row = 0  # 从第0行开始
    print("begin erase")
    while row < 19:
        clear_line = 1
        col = 1
        while col <= 10:
            if grid[row][col] == 0:
                clear_line = 0
            col += 1
        print("clear line", clear_line)
        if clear_line == 1:
            col = 1
            while col <= 10:
                grid[row][col] = 0   # 重置状态
                draw_square(col, row, BLACK)
                col += 1
            drop_down(row)  # 上面的都落下来
        row += 1


def heap_up_erase(row, col, rotate, category):
    row1, col1, row2, col2, row3, col3 = calculate_position(
        row, col, rotate, category)
    heap_up(row, col)
    heap_up(row1, col1)
    heap_up(row2, col2)
    heap_up(row3, col3)
    erase_row()


def drop_down(row):
    row = row-1  # 删除行的上一行
    while row >= 0:
        col = 1
        while col <= 10:
            if grid[row][col] == 1:
                draw_square(col, row, BLACK)
                grid[row][col] = 0
                pg.display.update()
                heap_up(row+1, col)  # 堆积到删除行
            col += 1
        row -= 1


def calculate_position(row, col, rotate, category): #row,col 中心值
    i = 0
    list = []
    while i < 3:   # 出去一对基值，剩下的变化量是3对，每对2个,共6个
        ref_row = data[category][i*2]
        ref_col = data[category][i*2+1]
        rotate_count = 0
        while rotate_count < rotate: #旋转90度时，行列互换，列取负值
            # 替换
            a = ref_row  # a用于过渡
            ref_row = ref_col
            ref_col = a
            # 正负颠倒
            ref_col = -ref_col
            rotate_count += 1
        list.append(row+ref_row)
        list.append(col+ref_col)
        i += 1
    print(list)
    return(list)  # 返回3对，六个


def fall():
    rotate = 0
    row = 1     # 代表行从0开始第5个格子
    col = 5  # 代表列  从0开始第5列格子
    category = 0  # 旋转的种类,四个方块有7种
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
                    horizontal_distance -= 1
                if moving == "right":
                    horizontal_distance += 1
                if moving == "up":
                    rotate_distance += 1
        fall_number += 1
        if fall_number == 150:
            vertical_distance = 1
            fall_number = 0
        col = col + horizontal_distance
        row = row + vertical_distance
        rotate = rotate + rotate_distance
        if overlap(row, col, rotate, category):   #
            col = col - horizontal_distance
            row = row - vertical_distance
            rotate = rotate - rotate_distance
            if vertical_distance > 0 and horizontal_distance == 0:  # If 重叠 Then 堆积
                heap_up_erase(row, col, rotate, category)
                rotate = 0
                row = 0
                col = 5
                category += 1
                if category > 6:  # 四个方块最多7种类型
                    category = 0
        print("row", row)
        print("col", col)
        move(row, col, rotate, category)


if __name__ == '__main__':
    main()
