import pygame
pygame.init

pygame.display.init
pygame.display.set_caption("Test")
bg = pygame.image.load("bg.jpg")
human = pygame.image.load("human1.jpg")
rect_human = human.get_rect()
display_screen = pygame.display.set_mode((1000, 500))
keyboard_input = 0
clock = pygame.time.Clock()
running = False
x = 0
y = 0
moving = "none"
white = (255, 255, 255)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving = "left"
                print("Left arrow key has been pressed.")
            elif event.key == pygame.K_RIGHT:
                moving = "right"
                print("Right arrow key has been pressed.")
            elif event.key == pygame.K_UP:
                moving = "up"
                print("Up arrow key has been pressed.")
            elif event.key == pygame.K_DOWN:
                moving = "down"
                print("Down arrow key has been pressed.")
        else:
            moving = "hello"
    surf = pygame.Surface((rect_human.w, rect_human .h))
    display_screen.blit(bg, [0, 0])
    display_screen.blit(surf, (x, y))
    if moving == "left":
        x -= 5
    if moving == "right":
        x += 5
    if moving == "up":
        y -= 5
    if moving == "down":
        y += 5
    display_screen.blit(human, [x, y])
    clock.tick(60)
    pygame.display.update()
    pygame.display.flip()
