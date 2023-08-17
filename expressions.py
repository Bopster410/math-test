from random import randint

class Expression():
    def __init__(self, min_value=0, max_value=100):
        self.min = min_value
        self.max = max_value

        self.first = 0
        self.second = 0
        self.answer = 0
        self.sign = ''
    
    def __str__(self):
        return f'{self.first} {self.sign} {self.second} = ?'
    
    def gen(self):
        self.sign = ['+', '-', ':', '*'][randint(0, 3)]
        if self.sign == '+' or self.sign == '*':
            self.first = randint(self.min, self.max)
            self.second = randint(self.min, self.max)
            self.answer = self.first + self.second if self.sign == '+' else self.first * self.second
        elif self.sign == '-':
            self.first = randint(self.min + 1, self.max)
            self.second = randint(self.min, self.first)
            self.answer = self.first - self.second
        else:
            self.answer = randint(self.min, self.max)
            self.second = randint(self.min, self.max)
            self.first = self.answer * self.second

if __name__ == '__main__':
    e = Expression()
    e.gen()
    print(e)