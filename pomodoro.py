import tkinter as tk
from input import InputField
from progress_bar import ProgressBar
from page import Page,SettingPage,TimePage
import constant



# メインウィンドウ
class App(tk.Tk):
    def __init__(self):
        # メインウィンドウの生成
        super().__init__()
        self.title("Pomodoro")
        self.geometry("380x260")
        self.resizable(False,False)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        # 入力値の管理
        self.input_values = {
            "Work" : 25,
            "Break" : 5,
            "Repeat" : 4
        }
        # サイクル数
        self.current_cycle = 0
        # 各ページの生成
        self.pages = {
            "Setting" : SettingPage(self,"Setting",self.switch_page), # 設定用ページ
            "Work" : TimePage(self,"Work",self.switch_page), # workタイム表示用ページ
            "Break" : TimePage(self,"Break",self.switch_page) # breakタイム表示用ページ
        }
        # ページを重ねる
        for p in self.pages.values():
            p.grid(row=0,column=0,sticky="nsew")
        self.pages["Setting"].tkraise()

        # 進捗バーを格納するコンテナの生成
        self.bar_container = tk.Frame(
            self,
            bd=1, 
            height= 8,
            width = self.winfo_width()
        )
        self.bar_container.grid(row=1,column=0,sticky="ew")

    def create_progress_bar(self):  
        # 進捗バーの表示
        self.bar = ProgressBar(self.bar_container,self.input_values,self.winfo_width())
 
    # 繰り返し回数の判定
    def is_repeat_end(self):
        return self.current_cycle > self.input_values["Repeat"]
    
    # ページを切り替える関数
    # WorkとBreakを交互に切り替え、repeatが0になったらSettingに切り替える
    def switch_page(self,next_page_key):
        if next_page_key == "Work":
            self.current_cycle += 1
            if self.is_repeat_end():
                    self.pages["Setting"].tkraise()
                    return
        next_page = self.pages[next_page_key]

        self.bar.change_color(self.current_cycle - 1,next_page_key)
        next_page.update_cycle_label(self.current_cycle)
        minute = self.input_values[next_page_key]
        next_page.tkraise()
        next_page.show_time(minute)
    
    # 次のページ名を取得する
    def update_page_state(self,page_state):
        if page_state == "Work":
            return "Break"
        elif page_state == "Break":
             return "Work"



root = App()
root.mainloop()
print("ポモドーロアプリを終了します")

