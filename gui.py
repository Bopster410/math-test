import tkinter as tk
import re
from expressions import Expression
from collections import namedtuple

class DialogWindow(tk.Toplevel):
    def __init__(self, master):
        # Initial configuration
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

        self.focus()

        self._Input = namedtuple('Input', ['min_val', 'max_val'])
        self._user_input = None
        
        self.bind('<Return>', lambda e: self._confirm_input())

    def _create_widgets(self):
        # Label for minimum value
        self._min_val_lbl = tk.Label(self, text='Min value:')
        self._min_val_lbl.grid(row=0, column=0, pady=(20, 0))

        # Entry for minimum value
        self._min_val_entry = tk.Entry(self)
        self._min_val_entry.grid(row=1, column=0, sticky='we', padx=30, pady=(0, 10))
        
        # Label for maximum value
        self._max_val_lbl = tk.Label(self, text='Max value:')
        self._max_val_lbl.grid(row=2, column=0)

        # Entry for maximum value
        self._max_val_entry = tk.Entry(self)
        self._max_val_entry.grid(row=3, column=0, sticky='we', padx=30)

        # Confirmation button
        self._confirm_input_btn = tk.Button(self, text='Confrm', command=self._confirm_input)
        self._confirm_input_btn.grid(row=4, column=0, pady=(10, 0))

        # Error label
        self._error_message = tk.StringVar(value='')
        self._error_lbl = tk.Label(self, fg='#8d0e0e', textvariable=self._error_message)
        self._error_lbl.grid(row=5, column=0, sticky='new', pady=5)
    
    def _confirm_input(self):
        # Check with regex if values are numbers
        min_val_str = re.fullmatch(r'\d+', self._min_val_entry.get())
        max_val_str = re.fullmatch(r'\d+', self._max_val_entry.get())
        
        # If values are numbers
        if min_val_str and max_val_str:
            # Transform them to int
            min_val_int = int(min_val_str.string)
            max_val_int = int(max_val_str.string)

            # If values are correct, update variable with user input and close dialog 
            if min_val_int < max_val_int:
                self._user_input = self._Input(min_val=min_val_int, max_val=max_val_int)
                self.grab_release()
                self.destroy()
            else:
                self._error_message.set('Min value must be lower than the max value!')
        else:
            self._error_message.set('Incorrect values!') 

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input


class ExprApp(tk.Tk):
    def __init__(self):
        # Initial configuration
        super().__init__()
        self.geometry('800x800')
        self.configure(bg='#252526')
        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        # Initial values
        self.score = 0
        self.highscore = 0

        # Create widgets with slight delay, to avoid white flickering of background
        self.after(10, self._create_widgets)  
        # Not resizable
        self.resizable(False, False)

        # Enter button causes enter_cmd function to work
        self.bind('<Return>', lambda e: self.enter_cmd())
        
        # Open menu and get initial values
        self.open_menu() 
    
    # Update expression label
    def update_expr(self):
        # Generate new expression
        self._expression.gen()
        # Change corresponding StringVar
        self._expression_string.set(str(self._expression))
    
    # Update score label
    def update_score(self):
        self._score_string.set(f'score: {self.score}') 
    
    def set_highscore(self, new_highscore):
        if new_highscore >= 0:
            self.highscore = new_highscore

    def update_highscore(self):
        self._highscore_string.set(f'highscore: {self.highscore}')

    # Checks the answer
    def enter_cmd(self):
        # Get answer from entry
        answer = self._answer_entry.get()

        # If it's correct, increase the score
        if re.fullmatch(r'\d+', answer):
            if int(answer) == self._expression.answer:
                self.update_expr()
                self.score += 1
            else:
                if self.score > self.highscore:
                    self.set_highscore(self.score)
                    self.update_highscore()
                self.score = 0
        else:
            self.score = 0
        
        self.update_score()
        self._answer_entry.delete(0, len(answer))
    
    # Open dialog window to get new min/max values
    def open_menu(self):
        input = DialogWindow(self).get_input()
        if input:
            min_value, max_value = input.min_val, input.max_val
            self._expression = Expression(min_value=min_value, max_value=max_value)
            self.update_expr()
    
    def _create_widgets(self):
        self._menu_img = tk.PhotoImage(file='menu_img.png')
        self._menu_btn = tk.Button(self, image=self._menu_img, bg='#252526', fg='#252526', activebackground='#4a4a4c', borderwidth=0,command=self.open_menu)
        self._menu_btn.grid(row=0, column=0)

        self._highscore_string = tk.StringVar()
        self._highscore_label = tk.Label(self, textvariable=self._highscore_string, bg='#252526', fg='#b6bbc0', font=('Arial', 15))
        self.set_highscore(0)
        self.update_highscore()
        self._highscore_label.grid(row=0, column=1, padx=(0, 40), pady=5)

        self._score_string = tk.StringVar()
        self._score_label = tk.Label(self, textvariable=self._score_string, bg='#252526', fg='#b6bbc0', font=('Arial', 15))
        self.update_score()
        self._score_label.grid(row=1, column=1, padx=(0, 40), pady=5)

        self._expression_string = tk.StringVar(value='hello!!!')
        self._expression_label = tk.Label(self, textvariable=self._expression_string, bg='#252526', fg='#b6bbc0',font=('Arial', 30))
        self._expression_label.grid(row=2, column=0, columnspan=2, sticky='nswe')
        
        self._answer_entry = tk.Entry(self,bg='#333333', fg='#b6bbc0', insertbackground='white', font=('Arial', 20))
        self._answer_entry.grid(row=3, column=0, columnspan=2, sticky='nswe')
        self._answer_entry.focus_set()


if __name__ == '__main__':
    e = ExprApp()
    e.mainloop()