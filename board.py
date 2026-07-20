import numpy as np

class MinesweeperBoard:
    def __init__(self,rows:int,columns:int,num_of_mines:int)->None:
        self.rows=rows
        self.columns=columns
        self.num_of_mines=num_of_mines
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        self.generate()

    #validation check
    @property
    def rows(self):
        return self._rows
    @rows.setter
    def rows(self,rows):
        if not isinstance(rows,int):
            raise TypeError("rows should be integer")
        if rows<=0:
            raise ValueError("rows should be positive")
        
        self._rows=rows

    @property
    def columns(self):
        return self._columns
    @columns.setter
    def columns(self,columns):
        if not isinstance(columns,int):
            raise TypeError("columns should be integer")
        if columns<=0:
            raise ValueError("columns should be positive")
        
        self._columns=columns
        
    @property
    def num_of_mines(self):
        return self._num_of_mines
    @num_of_mines.setter
    def num_of_mines(self,num_of_mines):
        if not isinstance(num_of_mines,int):
            raise TypeError("nums of mines should be integer")
        if num_of_mines<=0:
            raise ValueError('nums of mines should be positive')
        if num_of_mines>=self.rows*self.columns:
            raise ValueError("Too many mines for the board")
        self._num_of_mines=num_of_mines

    @property
    def shape(self):
        return self.board.shape
    #随机选一定区域指定为雷
    def place_mines(self)->None:
        mines_array=np.random.choice(self.rows*self.columns,size=self.num_of_mines,replace=False)
        self.board.reshape(-1)[mines_array] = -1
    #计算雷附近的数字
    def calculate_numbers(self):
        direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        mines_r,mines_c=np.where(self.board<0)
        is_mine=(self.board==-1)
        for dr,dc in direction:
            new_r,new_c=mines_r+dr,mines_c+dc
            valid=(new_r>=0) & (new_r<=self.rows-1) & (new_c>=0) & (new_c<=self.columns-1)
            np.add.at(self.board,(new_r[valid],new_c[valid]),1)
        
        self.board[is_mine]=-1
    
    def generate(self):
        self.place_mines()
        self.calculate_numbers()

    def __str__(self):
        str_board=self.board.astype(str)+' '
        str_board[str_board=='-1 ']='* '
        return '\n'.join(''.join(row) for row in str_board)
        
My_Board=MinesweeperBoard(20,20,20)
print(My_Board)
            