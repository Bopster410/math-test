import tkinter as tk
import re
from expressions import Expression

class ExprApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x800')
        self.configure(bg='#252526')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.score = 0
        self.high_score = 0

        self.score_string = tk.StringVar()
        self.score_label = tk.Label(self, textvariable=self.score_string, bg='#252526', fg='#b6bbc0', font=('Arial', 15))
        self.update_score()
        self.score_label.grid(row=0, column=0, padx=5, pady=5)

        # TODO get min/max values from window before the test 
        min_value = 1000
        max_value = 10000
        self.expression = Expression(min_value=min_value, max_value=max_value)
        self.string = tk.StringVar()
        self.update_expr()

        self.label = tk.Label(self, textvariable=self.string, bg='#252526', fg='#b6bbc0',font=('Arial', 30))
        self.label.grid(row=1, column=0, sticky='nswe')
        
        self.input = tk.Entry(self,bg='#333333', fg='#b6bbc0', insertbackground='white', font=('Arial', 20))
        self.input.grid(row=2, column=0, sticky='nswe')
        self.input.focus_set()

        self.bind('<Return>', lambda e: self.enter_cmd())
    
    def update_expr(self):
        self.expression.gen()
        self.string.set(str(self.expression))
    
    def update_score(self):
        self.score_string.set(f'score: {self.score}') 

    def enter_cmd(self):
        answer = self.input.get()
        if re.fullmatch(r'\d+', answer):
            if int(answer) == self.expression.answer:
                self.update_expr()
                self.score += 1
            else:
                self.score = 0
        else:
            self.score = 0
        
        self.update_score()
        self.input.delete(0, len(answer))

if __name__ == '__main__':
    e = ExprApp()
    e.mainloop()