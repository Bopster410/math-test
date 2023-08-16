from random import randint

class Expression():
    def __init__(self):
        self.first = 0
        self.second = 0
        self.answer = 0
        self.sign = ''
    
    def __str__(self):
        return f'{self.first} {self.sign} {self.second} = ?'
    
    def gen(self):
        self.sign = ['+', '-', ':', '*'][randint(0, 3)]
        if self.sign == '+' or self.sign == '*':
            self.first = randint(1000, 10000)
            self.second = randint(1000, 10000)
            self.answer = self.first + self.second if self.sign == '+' else self.first * self.second
        elif self.sign == '-':
            self.first = randint(1001, 10000)
            self.second = randint(1000, self.first)
            self.answer = self.first - self.second
        else:
            self.answer = randint(100, 1000)
            self.second = randint(100, 1000)
            self.first = self.answer * self.second

if __name__ == '__main__':
    e = Expression()
    e.gen()
    print(e)