import tkinter as tk
from input import InputField

# 定数
BG_COLOR_SETTING = "#E6E6E6"
BG_COLOR_WORK = "#B3B3B3"
BG_COLOR_BREAK = "#FFFFFF"
FONT_COLOR = "#000000"
BUTTON_BG_COLOR = "#FFFFFF"
COMMON_FONT = "Menlo"
LABEL_FONT = (COMMON_FONT,18,"bold")
TIME_FONT = (COMMON_FONT,70,"bold")
SETTING_FONT = (COMMON_FONT,15)

# ページの状態管理用 
# 各クラスのコンストラクタに page_meta_key という変数名でkeyを渡すことで 各ページの設定情報を取得する
PAGE_META = {
    "Setting": {"title": "Setting", "bg": BG_COLOR_SETTING},
    "Work":    {"title": "Work",    "bg": BG_COLOR_WORK},
    "Break":   {"title": "Break",   "bg": BG_COLOR_BREAK},
}
# 入力用エントリーのラベル名
INPUT_NAME = ("Work","Break","Repeat")

# メインウィンドウ
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.geometry("380x260")
        self.resizable(False,False)

        # 各フレームを格納するコンテナの生成
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH,expand=True)

        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)

        # フレームの生成
        self.pages = {
            "Setting" : SettingPage(self.container,"Setting",self.start_work), # 設定用ページ
            "Work" : TimePage(self.container,"Work"), # workタイム表示用ページ
            "Break" : TimePage(self.container,"Break") # breakタイム表示用ページ
        }
        # ページを重ねる
        for p in self.pages.values():
            p.grid(row=0,column=0,sticky="nsew")

        self.show("Setting")
    
    def show(self,name):
        self.pages[name].tkraise()
    
    def start_work(self,work_time):
        self.show("Work")
        self.pages["Work"].show_time(work_time-1)


# 各フレームの親クラス
class Page(tk.Frame):
    def __init__(self,parent,page_meta_key):
        self.bg = PAGE_META[page_meta_key]["bg"]
        super().__init__(parent,bg=self.bg)

        # ページタイトルの表示
        label = tk.Label(            
            self,
            text=PAGE_META[page_meta_key]["title"],
            bg=self.bg,
            fg=FONT_COLOR,
            font=LABEL_FONT,
            padx=5,
            pady=5
        )
        label.pack(side=tk.TOP)

# 設定用フレームクラス
class SettingPage(Page):
    def __init__(self,parent,page_meta_key,func):
        self.func = func
        super().__init__(parent,page_meta_key)

        # 入力欄をまとめるコンテナ
        self.frame_fields = tk.Frame(self)
        self.frame_fields.pack(side=tk.TOP)
        # 各項目の入力欄
        self.fields = {}
        for index,name in enumerate(INPUT_NAME):
            f = InputField(self.frame_fields,name,bg=self.bg)
            f.place(index)
            f.pack(fill=tk.BOTH,expand=True)
            self.fields[name] = f


        # スタートボタン
        self.button_start = tk.Button(
            self,
            text = "start",
            command=self.button_clicked,  
            highlightbackground=self.bg,        
        )
        self.button_start.pack(side=tk.TOP,pady=15)
    # スタートボタンクリック時の挙動
    def button_clicked(self):
        self.set_values()
        self.func(self.work_time)

    # 各項目の入力値の取得
    def set_values(self):
        self.work_time = int(self.fields["Work"].get_var())
        self.break_time = int(self.fields["Break"].get_var())
        self.repeat = int(self.fields["Repeat"].get_var())
       # print(self.work_time,self.break_time,self.repeat)
        
# 時間表示用フレームクラス
class TimePage(Page):
    def __init__(self,parent,page_meta_key):
        super().__init__(parent,page_meta_key)

        self.time_label = tk.Label(
            self,
            font=TIME_FONT,
            fg=FONT_COLOR,
            bg=PAGE_META[page_meta_key]["bg"]
        )
        self.time_label.pack(fill=tk.BOTH,expand=True)

    # 残り時間を表示する
    def show_time(self,minute,second=60):
        if second:
            second -= 1   
        elif minute:
            minute -= 1
            second = 59
        else:
            return
        self.time_label.config(text=f"{minute:0>2}:{second:0>2}")
        self.after(1_000,self.show_time,minute,second)

root = App()

root.mainloop()
print("ポモドーロアプリを終了します")

