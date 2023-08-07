import pygame
import math
import random
import sys
import time

pygame.init()
win = pygame.display.set_mode((512, 576))
pygame.display.set_caption("Minesweeper 10 x 10")
win.fill((0, 244, 0))
pygame.display.update()

width = 42
height = 42
grid = []
land = []
mines = []
neighbors = []
flags = []

font = pygame.font.Font('freesansbold.ttf', 24)

run = True


def draw_tile(x, y, color):
    pygame.draw.rect(win, color, (50 * x + 6, 50 * y + 6, width, height))


def init_board():
    for i in range(10):
        for j in range(10):
            grid.append((i, j))

    for i in range(3, 7):
        for j in range(3, 7):
            land.append((i, j))

    for i in range(2, 8):
        for j in range(2, 8):
            if 0 < land.count((i - 1, j)) and land.count((i, j)) == 0:
                neighbors.append((i, j))
            if 0 < land.count((i + 1, j)) and land.count((i, j)) == 0:
                neighbors.append((i, j))
            if 0 < land.count((i, j + 1)) and land.count((i, j)) == 0:
                neighbors.append((i, j))
            if 0 < land.count((i, j - 1)) and land.count((i, j)) == 0:
                neighbors.append((i, j))

    count = 0
    while count < 7:
        a = random.choice(neighbors)
        land.append(a)
        neighbors.remove(a)
        count += 1


def place_mines():
    unpopulated = [x for x in grid if x not in land]
    for x in range(10):
        mine = random.choice(unpopulated)
        unpopulated.remove(mine)
        mines.append(mine)


def find_adjacent_mines():
    for x in land:
        adjacent_mines = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == j == 0:
                    continue
                elif mines.count((x[0] + i, x[1] + j)) > 0:
                    adjacent_mines += 1
        text = font.render(str(adjacent_mines), True, (255, 0, 0), (237, 201, 78))
        text_rect = text.get_rect()
        text_rect.center = (50 * x[0] + 25, 50 * x[1] + 25)
        win.blit(text, text_rect)


def draw_grid():
    for i in range(10):
        for j in range(10):
            draw_tile(i, j, (0, 255, 0))
    for coord in land:
        draw_tile(coord[0], coord[1], (237, 201, 78))
    for f in flags:
        draw_tile(f[0], f[1], (0, 0, 0))

    find_adjacent_mines()


init_board()
place_mines()  # goes before draw_grid() so that mines isn't empty
draw_grid()

while run:

    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            square_coordinates = (math.floor(pos[0] / 50), math.floor(pos[1] / 50))
            if land.count(square_coordinates) == 0 and grid.count(square_coordinates) > 0:
                land.append(square_coordinates)
            if mines.count(square_coordinates) > 0:
                for x in mines:
                    draw_tile(x[0], x[1], (255, 0, 0))
                    pygame.display.update()
                    time.sleep(0.25)
                time.sleep(2)
                sys.exit()
            draw_grid()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            pos = pygame.mouse.get_pos()
            square_coordinates = (math.floor(pos[0] / 50), math.floor(pos[1] / 50))
            if flags.count(square_coordinates) == 0:
                flags.append(square_coordinates)
            draw_grid()

    game_time = font.render("Time: " + str(math.floor(pygame.time.get_ticks() / 1000)), True, (255, 0, 0),
                            (237, 201, 78))
    game_time_rect = game_time.get_rect()
    game_time_rect.center = (384, 520)
    win.blit(game_time, game_time_rect)
    pygame.display.update()

    mines_to_uncover = [x for x in mines if x not in flags]
    if len(mines_to_uncover) == 0:
        win.fill((0, 255, 255))
        winning_text = font.render('You win!', True, (255, 0, 0), (255, 255, 255))
        winning_rect = winning_text.get_rect()
        winning_rect.center = (255, 255)
        win.blit(winning_text, winning_rect)
        pygame.display.update()
        time.sleep(3)
        sys.exit()
