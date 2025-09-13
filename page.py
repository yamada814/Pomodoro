import tkinter as tk
import constant
from input import InputField

# 各フレームの親クラス
class Page(tk.Frame):
    def __init__(self,parent,page_state):
        self.app = parent
        self.page_state = page_state
        self.page_info = constant.PAGE_META[page_state]
        # 背景色の取得
        self.bg = self.page_info["bg"]
        super().__init__(parent,bg=self.bg)

        # ページタイトルの表示
        label = tk.Label(            
            self,
            text=self.page_info["title"],
            bg=self.bg,
            fg=constant.FONT_COLOR,
            font=constant.LABEL_FONT,
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
        for index,name in  enumerate(constant.INPUT_NAMES):
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
        for name in constant.INPUT_NAMES:
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
            font = constant.LABEL_FONT,
            fg = constant.FONT_COLOR,
            bg = self.page_info["bg"],     
        )
        self.cycle_label.pack(side=tk.TOP)

        # 時間表示ラベル
        self.time_label = tk.Label(
            self,
            font=constant.TIME_FONT,
            fg=constant.FONT_COLOR,
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
            second = constant.DEFAULT_SECOND

        self.time_label.config(text=f"{minute:0>2}:{second:0>2}")
        self.after(1_000,self.show_time,minute,second)
