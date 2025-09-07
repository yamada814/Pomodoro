import tkinter as tk

class InputField(tk.Frame):
    def __init__(self,parent,name,bg):
        super().__init__(parent,bg=bg)
        
        self.var = tk.StringVar()
        self.label = tk.Label(
            self,
            text=name,
            bg=bg,
            width=10,
            justify=tk.CENTER,
            pady=10 
        )
        self.entry = tk.Entry(
            self,
            width = 5,
            justify=tk.RIGHT,
            textvariable=self.var,
            highlightthickness=0,
            borderwidth=0,
    
        )

    def place(self,index):
        self.label.grid(row=index,column=0)
        self.entry.grid(row=index,column=1,ipady=1)
    def get_var(self):
        return self.var.get()


  