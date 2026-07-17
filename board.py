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

    #随机选一定区域指定为雷
    def place_mines(self):
        mines_array=np.random.choice(self.rows*self.columns,size=self.num_of_mines,replace=False)
        for item in mines_array:
            self.board[item//self.columns , item % self.columns]=-1
    #计算雷附近的数字
    def calculate_numbers(self):
        direction=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for row in range(self.rows):
            for column in range(self.columns):
                if self.board[row,column]!=-1:
                    continue
                #给雷周围一圈的非雷区域计数+1
                for dr,dc in direction:
                    if (row+dr>=0 and row+dr<=self.rows-1) and (column+dc>=0 and column+dc<=self.columns-1):
                        if self.board[row+dr,column+dc]==-1:
                            continue #不用操作雷的区域
                        else:
                            self.board[row+dr,column+dc]+=1
    
    def generate(self):
        self.place_mines()
        self.calculate_numbers()

    def __str__(self):
        result = ""
        for row in self.board:
            for item in row:
                if item == -1:
                    result += "*"
                else:
                    result += f"{item} "
            result += "\n"
        return result

        
My_Board=MinesweeperBoard(20,20,20)
print(My_Board)
            