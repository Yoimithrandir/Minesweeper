import numpy as np

class MinesweeperBoard:
    def __init__(self,rows:int,columns:int,num_of_mines:int,seed=50)->None:
        self.rows=rows
        self.columns=columns
        self.num_of_mines=num_of_mines
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        self.rng=np.random.default_rng(seed=seed)
        self.generate()

    #validation check
    @property
    def rows(self):
        return self._rows
    @rows.setter
    def rows(self,rows:int):
        if not isinstance(rows,int):
            raise TypeError("rows should be integer")
        if rows<=0:
            raise ValueError("rows should be positive")
        
        self._rows=rows

    @property
    def columns(self):
        return self._columns
    @columns.setter
    def columns(self,columns:int):
        if not isinstance(columns,int):
            raise TypeError("columns should be integer")
        if columns<=0:
            raise ValueError("columns should be positive")
        
        self._columns=columns
        
    @property
    def num_of_mines(self):
        return self._num_of_mines
    @num_of_mines.setter
    def num_of_mines(self,num_of_mines:int):
        if not isinstance(num_of_mines,int):
            raise TypeError("nums of mines should be integer")
        if num_of_mines<=0:
            raise ValueError('nums of mines should be positive')
        if num_of_mines>=self.rows*self.columns:
            raise ValueError("Too many mines for the board")
        self._num_of_mines=num_of_mines

    #以下getter方便调用数据
    @property
    def shape(self):
        return self.board.shape
    @property
    def data(self):
        return self.board
    
    #随机选一定区域指定为雷
    def place_mines(self)->None:
        mines_array=self.rng.choice(self.rows*self.columns,size=self.num_of_mines,replace=False)
        self.board.reshape(-1)[mines_array] = -1
    #计算雷附近的数字
    def calculate_numbers(self)->None:
        mines_r,mines_c=np.where(self.board<0)

        is_mine=(self.board==-1)
        pad_mines=np.pad(self.board,1,'constant',constant_values=0)
        for r,c in zip(mines_r,mines_c):
            r,c=r+1,c+1       #pad之后加上offset
            pad_mines[r-1:r+2,c-1:c+2]+=1           #雷周围一圈数字+1
        self.board=pad_mines[1:self.rows+1,1:self.columns+1]
        self.board[is_mine]=-1
    #生成地图
    def generate(self)->None:
        self.place_mines()
        self.calculate_numbers()
    #打印地图
    def __str__(self)->str:
        str_board=self.board.astype(str)+' '
        str_board[str_board=='-1 ']='* '
        return '\n'.join(''.join(row) for row in str_board)
        
if __name__=="__main__":
    My_Board=MinesweeperBoard(20,20,20,seed=80)
    print(My_Board)
            