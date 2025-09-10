import tkinter as tk
from progress_bar import ProgressBar

root = tk.Tk()
root.title("Sample")
root.geometry("380x260")
input_values = {"Work":25,"Break":5,"Repeat":3}
progressBar = ProgressBar(root,input_values)
progressBar.pack(side=tk.BOTTOM)

root.mainloop()
