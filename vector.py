class vector:
    """Base class for 2 dimensional position and scale"""

    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __add__(self, number):
        return vector(self.x + number[0], self.y + number[1])
    def __sub__(self, number):
        return vector(self.x - number[0], self.y - number[1])
    def __mul__(self, number):
        return vector(self.x * number[0], self.y * number[1])
    def __truediv__(self, number):
        return vector(self.x / number[0], self.y / number[1])
    
    def __len__(s):
        return 2
   
    def __getitem__(s, i):
        return [s.x, s.y][i]


ZERO = vector(0,0)