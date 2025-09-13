import tkinter as tk
from input import InputField
from progress_bar import ProgressBar

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

# テスト用定数
DEBUG_MODE = True
DEFAULT_SECOND = 3 if DEBUG_MODE else 59

# ページの状態管理用 
# 各クラスのコンストラクタに page_state という変数名でkeyを渡すことで 各ページの設定情報を取得する
PAGE_META = {
    "Setting": {"title": "Setting", "bg": BG_COLOR_SETTING},
    "Work":    {"title": "Work",    "bg": BG_COLOR_WORK},
    "Break":   {"title": "Break",   "bg": BG_COLOR_BREAK},
}
# 入力項目名の一覧
INPUT_NAMES = ("Work","Break","Repeat")

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

# 各フレームの親クラス
class Page(tk.Frame):
    def __init__(self,parent,page_state):
        self.app = parent
        self.page_state = page_state
        self.page_info = PAGE_META[page_state]
        # 背景色の取得
        self.bg = self.page_info["bg"]
        super().__init__(parent,bg=self.bg)

        # ページタイトルの表示
        label = tk.Label(            
            self,
            text=self.page_info["title"],
            bg=self.bg,
            fg=FONT_COLOR,
            font=LABEL_FONT,
            padx=5,
            pady=5
        )
        label.pack(side=tk.TOP)

# 設定用フレームクラス
class SettingPage(Page):
    def __init__(self,parent,page_state,func):
        # スタートボタンにバインドする関数をインスタンス変数として保持
        self.func = func
        super().__init__(parent,page_state)

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
        # 各項目の入力値の取得
        for name in INPUT_NAMES:
            self.app.input_values[name] = int(self.fields[name].get_var())
        self.app.create_progress_bar()
        self.func("Work")
        
# 時間表示用フレームクラス
class TimePage(Page):
    def __init__(self,parent,page_state,func):
        self.page_state = page_state
        self.func = func
        super().__init__(parent,page_state)

        # サイクル数ラベル
        self.cycle_label = tk.Label(
            self,
            font = LABEL_FONT,
            fg = FONT_COLOR,
            bg = self.page_info["bg"],     
        )
        self.cycle_label.pack(side=tk.TOP)

        # 時間表示ラベル
        self.time_label = tk.Label(
            self,
            font=TIME_FONT,
            fg=FONT_COLOR,
            bg=self.page_info["bg"]
        )
        self.time_label.pack(fill=tk.BOTH,expand=True)

    # サイクル数ラベルの数値を更新する
    def update_cycle_label(self,current_cycle):
        self.cycle_label.config(
            text=f'{current_cycle} / {self.app.input_values["Repeat"]}')
    
    # 残り時間を表示し、再起的に更新する
    def show_time(self,minute,second=0):
        if minute == 0 and second == 0:
             self.func(self.app.update_page_state(self.page_state))
             return
        
        if second:
            second -= 1   
        elif minute:
            minute -= 1
            second = DEFAULT_SECOND

        self.time_label.config(text=f"{minute:0>2}:{second:0>2}")
        self.after(1_000,self.show_time,minute,second)


root = App()
root.mainloop()
print("ポモドーロアプリを終了します")

