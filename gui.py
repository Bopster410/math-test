import tkinter as tk
import re
from expressions import Expression
from collections import namedtuple

class DialogWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry('400x200')
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)

        # Lift window on top
        self.lift()
        # Stay on top
        self.attributes('-topmost', True)
        # Create widgets with slight delay, to avoid white flickering of background
        self.after(10, self._create_widgets)  
        # Not resizable
        self.resizable(False, False)
        # Make other windows not clickable
        self.grab_set()

        self._Input = namedtuple('Input', ['min_val', 'max_val'])
        self._user_input = None
    
    def _create_widgets(self):
        self._min_val_lbl = tk.Label(self, text='Min value:')
        self._min_val_lbl.grid(row=0, column=0, pady=(20, 0))

        self._min_val_entry = tk.Entry(self)
        self._min_val_entry.grid(row=1, column=0, sticky='we', padx=30, pady=(0, 10))
        
        self._max_val_lbl = tk.Label(self, text='Max value:')
        self._max_val_lbl.grid(row=2, column=0)

        self._max_val_entry = tk.Entry(self)
        self._max_val_entry.grid(row=3, column=0, sticky='we', padx=30)

        self._confirm_input_btn = tk.Button(self, text='Confrm', command=self._confirm_input)
        self._confirm_input_btn.grid(row=4, column=0, pady=(10, 0))

        self._error_message = tk.StringVar(value='')
        self._error_lbl = tk.Label(self, fg='#8d0e0e', textvariable=self._error_message)
        self._error_lbl.grid(row=5, column=0, sticky='new', pady=5)
    
    def _confirm_input(self):
        min_val_str = re.fullmatch(r'\d+', self._min_val_entry.get())
        max_val_str = re.fullmatch(r'\d+', self._max_val_entry.get())
        if min_val_str and max_val_str:
            self._user_input = self._Input(min_val=int(min_val_str), max_val=int(max_val_str))
            self.grab_release()
            self.destroy()
        else:
            self._error_message.set('Incorrect values!') 

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input


class ExprApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x800')
        self.configure(bg='#252526')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.score = 0
        self.high_score = 0

        self.menu_img = tk.PhotoImage(file='menu_img.png')
        self.menu_btn = tk.Button(self, image=self.menu_img, bg='#252526', fg='#252526', activebackground='#4a4a4c', borderwidth=0,command=self.open_menu)
        self.menu_btn.grid(row=0, column=0)

        self.score_string = tk.StringVar()
        self.score_label = tk.Label(self, textvariable=self.score_string, bg='#252526', fg='#b6bbc0', font=('Arial', 15))
        self.update_score()
        self.score_label.grid(row=0, column=1, padx=(0, 40), pady=5)

        self.string = tk.StringVar(value='hello!!!')
        self.label = tk.Label(self, textvariable=self.string, bg='#252526', fg='#b6bbc0',font=('Arial', 30))
        self.label.grid(row=1, column=0, columnspan=2, sticky='nswe')
        
        self.input = tk.Entry(self,bg='#333333', fg='#b6bbc0', insertbackground='white', font=('Arial', 20))
        self.input.grid(row=2, column=0, columnspan=2, sticky='nswe')
        self.input.focus_set()

        self.bind('<Return>', lambda e: self.enter_cmd())
        
        self.open_menu() 
    
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
    
    def open_menu(self):
        input = DialogWindow(self).get_input()
        if input:
            min_value, max_value = input.min_val, input.max_val
            # TODO check this in the dialog window
            if min_value < max_value:
                self.expression = Expression(min_value=min_value, max_value=max_value)
                self.update_expr()

if __name__ == '__main__':
    e = ExprApp()
    e.mainloop()