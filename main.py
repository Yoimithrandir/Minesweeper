import pygame

from board import MinesweeperBoard
from game import *

def draw_board(screen, font, rows, cols, cell_size, game):
    screen.fill((255,255,255))

    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)

            state = game._state[row,col]
            #格子未翻开
            if state == HIDDEN:
                pygame.draw.rect(screen,(160,160,160),rect)
            #格子已翻开
            elif state == OPEN:
                pygame.draw.rect(screen,(220,220,220),rect)

                value = game.board.data[row,col]
                #显示雷
                if value == -1:
                    text = font.render("*",True,(255,0,0))
                #显示数字
                elif value > 0:
                    text = font.render(str(value),True,(0,0,255))
                else:   text = None


                if text:
                    screen.blit(text,text.get_rect(center=rect.center))

            #显示旗子
            elif state == FLAG:
                pygame.draw.rect(screen, (160,160,160), rect)

                text = font.render("F",True,(255,0,0))

                screen.blit(text,text.get_rect(center=rect.center))

            pygame.draw.rect(screen,(0,0,0),rect,1)

#结算画面
def draw_result(screen, font, game):
    if game.win:
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(120)
        overlay.fill((0,255,0))

        screen.blit(overlay,(0,0))

        text = font.render("YOU WIN!",True,(0,100,0))

        screen.blit(text,text.get_rect(center=screen.get_rect().center))

    elif game.game_over:
        overlay = pygame.Surface(screen.get_size())

        overlay.set_alpha(120)
        overlay.fill((255,0,0))

        screen.blit(overlay,(0,0))

        text = font.render("GAME OVER",True,(120,0,0))

        screen.blit(text,text.get_rect(center=screen.get_rect().center))


if __name__ == "__main__":
    CELL_SIZE = 40
    SEED = 50
    # 手动设置
    ROWS = int(input("请输入行数："))
    COLS = int(input("请输入列数："))
    MINES = int(input("请输入雷数："))

    pygame.init()
    board = MinesweeperBoard(ROWS,COLS,MINES,seed=SEED)
    game = MinesweeperGame(board)

    screen = pygame.display.set_mode((COLS*CELL_SIZE,ROWS*CELL_SIZE))

    pygame.display.set_caption("Minesweeper")

    font = pygame.font.SysFont(None,30)

    clock = pygame.time.Clock()

    running=True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over or game.win:
                    continue

                x,y = event.pos
                row = y//CELL_SIZE
                col = x//CELL_SIZE
                pos=(row,col)
                if event.button == 1:
                    game.mouse1(pos)
                elif event.button == 3:
                    game.mouse3(pos)

        draw_board(screen,font,ROWS,COLS,CELL_SIZE,game)

        game.check_win()
        if game.game_over or game.win:      draw_result(screen,font,game)

        pygame.display.update()

        clock.tick(60)
    pygame.quit()