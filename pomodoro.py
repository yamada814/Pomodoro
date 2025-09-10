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
# 入力項目名の一覧
INPUT_NAMES = ("Work","Break","Repeat")
# 入力値を管理するための辞書
INPUT_VALUES = {}
# メインウィンドウ
class App(tk.Tk):
    def __init__(self):
        # メインウィンドウの生成
        super().__init__()
        self.title("Pomodoro")
        self.geometry("380x260")
        self.resizable(False,False)
        """
        # 各フレームを格納するコンテナの生成
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH,expand=True)
        # 各ページをコンテナいっぱいに広げる
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)

        # 各フレームの生成
        self.pages = {
            "Setting" : SettingPage(self.container,"Setting",self.start_work), # 設定用ページ
            "Work" : TimePage(self.container,"Work"), # workタイム表示用ページ
            "Break" : TimePage(self.container,"Break") # breakタイム表示用ページ
        }
        """
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        # 各フレームの生成
        self.pages = {
            "Setting" : SettingPage(self,"Setting",self.start_work), # 設定用ページ
            "Work" : TimePage(self,"Work",), # workタイム表示用ページ
            "Break" : TimePage(self,"Break") # breakタイム表示用ページ
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
        # 背景色の取得
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
        # スタートボタンにバインドする関数をインスタンス変数として保持
        self.func = func
        super().__init__(parent,page_meta_key)

        # 入力欄をまとめるコンテナの生成
        self.field_container = tk.Frame(self,bg=self.bg)
        self.field_container.pack(side=tk.TOP,expand=True)
        # 各項目の入力欄の生成と配置
        self.fields = {}
        for index,name in  enumerate(INPUT_NAMES):
            input_field  = InputField(self.field_container,name,self.bg)
            self.fields[name] = input_field
            input_field.label.grid(row=index,column=0)
            input_field.entry.grid(row=index,column=1)
        
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
        self.func(INPUT_VALUES["Work"])

    # 各項目の入力値の取得
    def set_values(self):
        for name in INPUT_NAMES:
            INPUT_VALUES[name] = int(self.fields[name].get_var())
        #print(INPUT_VALUES)
        
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
        else:#secondもminuteも0の時
            return
        self.time_label.config(text=f"{minute:0>2}:{second:0>2}")
        self.after(1_000,self.show_time,minute,second)

root = App()

root.mainloop()
print("ポモドーロアプリを終了します")

