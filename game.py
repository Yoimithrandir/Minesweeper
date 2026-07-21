import numpy as np
from board import MinesweeperBoard
#定义三种格子状态，hidden未翻开，open已翻开，flag插旗
HIDDEN = 0      
OPEN = 1
FLAG = 2

class MinesweeperGame:
    def __init__(self,board:MinesweeperBoard)->None:

        self._state=np.zeros(board.shape,dtype=int)   
        self.board=board
        self.game_over=False
        self.direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        self.win=False

    """
    主要两个函数，模拟左右键点击地图效果
    """
    #右键控制插旗
    def mouse3(self, position:tuple)->None:          
        if self._state[position]==HIDDEN:    #给隐藏格子插旗
            self._state[position]=FLAG
        elif self._state[position]==OPEN:    #对已翻开格子操作，无效操作
            pass
        else:                                #取消已插旗格子
            self._state[position]=HIDDEN
        return 
    
    #左键点击，进行点隐藏翻格子或点数字翻周围一片
    def mouse1(self,position:tuple)->None:
        if self._state[position]==FLAG:     #翻插了旗的格子，无效
            return
        elif self._state[position]==HIDDEN: #翻开格子
            self.open_cell(position)
                                            #已经探明周围雷情况下点数字
        elif self.board.data[position]>0 and self.board.data[position]==self.flag_count(position):                                                              
            self.num_expand(position)


    """
    其余工具函数，辅助判断
    """
    #如果翻到雷，更新game_over状态并返回
    def is_mine(self,position:tuple)->bool:
        if self.board.data[position]==-1:
            self.game_over=True
        return self.board.data[position]==-1
    
    #统计该位置周围旗数
    def flag_count(self,position):
        r,c=position
        pad_state = np.pad(self._state,pad_width=1,constant_values=HIDDEN)
        r,c=r+1,c+1
        window=pad_state[r-1:r+2,c-1:c+2]
        return (window==FLAG).sum()

    #翻开周围8个格子
    def num_expand(self,position:tuple)->None:
        r,c=position
        for dr,dc in self.direction:
            new_r,new_c=r+dr,c+dc
            if not self.is_valid((new_r,new_c)): continue

            if self._state[new_r,new_c]==FLAG: continue    
            elif self._state[new_r,new_c]==HIDDEN: self.open_cell((new_r,new_c))


    #翻到空格，会连续翻一片空白区域
    def blank_expand(self,position):
        r,c=position
        for dr,dc in self.direction:
            new_r,new_c=r+dr,c+dc

            if not self.is_valid((new_r,new_c)):    continue

            if self._state[new_r,new_c]==OPEN: continue

            if self._state[new_r,new_c]==FLAG: continue

            #剩余为HIDDEN情况
            self.open_cell((new_r,new_c))
    
    #翻开单个隐藏格子，可能触发self.blank_expand()
    def open_cell(self,position:tuple)->None:
        if self._state[position] == OPEN:
            return
        self._state[position]=OPEN
        if self.is_mine(position):
            return

        if self.board.data[position]==0:   self.blank_expand(position)#翻到空格,额外展开周围一片非雷空白区域
    
    #检查当前位置是否越界
    def is_valid(self,position:tuple)->bool:
        r,c=position
        return (0<= r<self.board.rows and 0<=c<self.board.columns)

    #显示当前局面情况
    def show_state(self)->None:
        str_board= np.full(self.board.shape, '?', dtype=str)

        open_mask = (self._state == OPEN)
        str_board[open_mask]=self.board.data[open_mask].astype(str)

        flag_mask = (self._state == FLAG)
        str_board[flag_mask]='🚩'

        open_mine_mask=open_mask*(self.board.data==-1)
        str_board[open_mine_mask]='💣'

        print('\n'.join(' '.join(row) for row in str_board))

    #胜利判断
    def check_win(self):
        safe_cell=self.board.data!=-1
        opened_cell=self._state==OPEN
        if np.all(safe_cell==opened_cell):       #非雷区域全部翻开
            self.win=True

        return self.win 



if __name__=="__main__":
    board = MinesweeperBoard(10,10,10,50)
    print("真实棋盘:")
    print(board)
    game = MinesweeperGame(board)

    print("初始:")
    game.show_state()

    game.mouse1((0,0))
    print("点击(0,0):")
    game.show_state()

    game.mouse3((5,2))
    print("插旗(5,2):")
    game.show_state()

    game.mouse1((5,1))
    print("点击(5,1):")
    game.show_state()

    print("game over:",game.game_over)