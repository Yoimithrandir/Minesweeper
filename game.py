import numpy as np
from board import MinesweeperBoard
class MinesweeperGame:
    def __init__(self,board):
        self.cell_state={'hidden':0,'open':1,'flag':2}      #0代表隐藏，1代表显示（格子翻开），2代表插旗
        self._visible_state=np.zeros(board.shape,dtype=int)   
        self.board=board
        self.game_over=False

    #右键控制插旗
    def mouse2(self, position:tuple)->None:          
        if self._visible_state[position]==self.cell_state['hidden']:    #给隐藏格子插旗
            self._visible_state[position]=self.cell_state['flag']
        elif self._visible_state[position]==self.cell_state['open']:    #对显示格子操作，无效操作
            pass
        else:                                                           #取消已插旗格子
            self._visible_state[position]=self.cell_state['hidden']
        return 
    
    #左键翻格子
    def mouse1(self,position:tuple):
        if self._visible_state[position]==self.cell_state['flag']:     #翻插旗格子，无效
            return
        elif self._visible_state[position]==self.cell_state['hidden']: #翻开格子，判断是否是雷
            self._visible_state[position]=self.cell_state['open']

            if self.board.board[position]==0:           self.expand(position)    #展开周围一片非雷空白区域
                
            self.is_mine(position)
        
                                                                        #已经探明周围雷情况下点数字
        elif self.board.board[position]>0 and self.board.board[position]==self.flag_count(position):                                                              
            self.expand_around(position)




    def is_mine(self,position):
        if self.board.board[position]==-1:
            self.game_over=True
        return self.board.board[position]==-1
    
    #统计该位置周围旗数
    def flag_count(self,position):
        r,c=position
        pad_state = np.pad(
            self._visible_state,
            pad_width=1,
            constant_values=self.cell_state['hidden']
        )
        r,c=r+1,c+1
        window=pad_state[r-1:r+2,c-1:c+2]
        return (window==self.cell_state['flag']).sum()

    #翻开周围8个格子
    def expand_around(self,position)->None:
        direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        r,c=position

        for dr,dc in direction:
            new_r,new_c=r+dr,c+dc
            valid=(new_r>=0) and (new_r<=self.board.rows-1) and (new_c>=0) and (new_c<=self.board.columns-1)
            if valid:
                self.mouse1((new_r,new_c))

    #翻到0，会连续翻一片空白区域
    def expand(self,position):
        direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        r,c=position
        for dr,dc in direction:
            new_r,new_c=r+dr,c+dc
            valid=(new_r>=0) and (new_r<=self.board.rows-1) and (new_c>=0) and (new_c<=self.board.columns-1)
            if not valid:    continue

            if self._visible_state[new_r,new_c]==self.cell_state['open']: continue

            if self._visible_state[new_r,new_c]==self.cell_state['flag']: continue

            if self.board.board[new_r,new_c]==-1: continue

            self._visible_state[new_r,new_c]=self.cell_state['open']   #翻开数字格或空格
            if self.board.board[new_r,new_c]==0:                       #翻开空格，递归
                self.expand((new_r,new_c))
    
    #显示当前局面情况
    def show_visible_state(self):
        str_board= np.full(self.board.shape, '?', dtype=str)
        open_mask = self._visible_state == self.cell_state['open']
        str_board[open_mask]=self.board.board[open_mask].astype(str)
        flag_mask = self._visible_state == self.cell_state['flag']
        str_board[flag_mask]='🚩'

        print('\n'.join(' '.join(row) for row in str_board))



if __name__=="__main__":
    board = MinesweeperBoard(10,10,10)
    print("真实棋盘:")
    print(board)
    game = MinesweeperGame(board)

    print("初始:")
    game.show_visible_state()

    game.mouse1((0,0))
    print("点击(0,0):")
    game.show_visible_state()

    game.mouse2((1,1))
    print("插旗(4,1):")
    game.show_visible_state()

    game.mouse1((2,2))
    print("点击(3,1):")
    game.show_visible_state()

    print("game over:",game.game_over)