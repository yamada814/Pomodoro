import tkinter as tk

class InputField(tk.Frame):
    def __init__(self,parent,name,bg):
        super().__init__(parent,bg=bg)
        
        self.var = tk.StringVar()
        self.label = tk.Label(
            parent,
            text=name,
            bg=bg,
            width=10,
            justify=tk.CENTER,
            pady=10 
        )
        self.entry = tk.Entry(
            parent,
            width = 5,
            justify=tk.RIGHT,
            textvariable=self.var,
            highlightthickness=0,
            borderwidth=0,    
        )

    def get_var(self):
        return self.var.get()




  