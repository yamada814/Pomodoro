import tkinter as tk
from input import InputField

# 定数
BG_COLOR_SETTING = "#E6E6E6"
BG_COLOR_WORK = "#B3B3B3"
BG_COLOR_BREAK = "#000000"
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
INPUT_NAME = ("minute","second","repeat")

# メインウィンドウ
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro")
        self.geometry("380x260")
        self.resizable(False,False)

        # 各フレームを格納するコンテナの生成
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH,expand=True)

        # フレームの生成
        pages = [
            SettingPage(container,"Setting"),# 設定用ページ
            TimePage(container,"Work"),# workタイム表示用ページ
            TimePage(container,"Break")]# breakタイム表示用ページ
        self.frames_dict = dict(zip(PAGE_META.keys(),pages))

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
    def __init__(self,parent,page_meta_key):
        super().__init__(parent,page_meta_key)
        # 入力欄をまとめるコンテナ
        self.frame_fields = tk.Frame(self)
        self.frame_fields.pack(side=tk.TOP)
        # 各項目の入力欄
        self.fields = {}
        for index,name in enumerate(INPUT_NAME):
            f = InputField(self.frame_fields,name,bg=self.bg)
            f.place(index)
            self.fields[name] = f

        # スタートボタン
        self.button_start = tk.Button(
            self,
            text = "start",
            command=self.button_clicked
        )
        self.button_start.pack(side=tk.TOP)
    # スタートボタンクリック時の挙動
    def button_clicked(self):
        print("start!!")
        print(self.get_vars())

    # 各項目の入力値の取得
    def get_vars(self):
        self.vars = {name : self.fields[name].get_var() for name in INPUT_NAME}
        return self.vars
        
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
        self.time_label.pack(expand=True)

    # 残り時間を表示する
    def show_time(self,minute,second =60):
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
sample = SettingPage(root,"Setting")
sample.pack(fill=tk.BOTH,expand=True)
"""
sample = TimePage(root,"Work")
sample.pack(fill=tk.BOTH,expand=True)
sample.show_time(1)
"""
root.mainloop()
print("ポモドーロアプリを終了します")

