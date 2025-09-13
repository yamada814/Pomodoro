import tkinter as tk

# タイマーの進捗状況を画面下部にバー形式で表示するクラス
class ProgressBar(tk.Frame):
    def __init__(self,parent,input_values,total_wid):
        super().__init__(parent)
        # 入力値の取得
        work_time = input_values["Work"]
        break_time = input_values["Break"]
        repeat = input_values["Repeat"]

        # バーの生成
        work_bar_wid,break_bar_wid = self.calc(total_wid,work_time,break_time,repeat)
        self.work_bars = []
        self.break_bars = []
        for _ in range(repeat):
            # Worktimeバーの生成
            work_bar = tk.Frame(
                parent,
                bg="#B3B3B3",
                bd=1,
                width=work_bar_wid,
                height=8
                )
            self.work_bars.append(work_bar)
            # Breaktimeバーの生成
            break_bar = tk.Frame(
                parent,
                bg="#FFFFFF",
                bd=1,
                width=break_bar_wid,
                height=8
                )
            self.break_bars.append(break_bar)

            # 各バーの配置
            work_bar.pack(side=tk.LEFT)
            break_bar.pack(side=tk.LEFT)
 
    # 進捗バーの幅を取得する
    def calc(self,total_wid,work_time,break_time,repeat):
        self.work_bar_wid = (total_wid / repeat) * (work_time / (work_time + break_time))
        self.break_bar_wid = (total_wid / repeat) - self.work_bar_wid
        return (self.work_bar_wid, self.break_bar_wid)
    
    # 稼働中サイクル部分のバーの色を変える
    def change_color(self,index,page_key):
        if page_key == "Work":
            if index > 0:
                self.break_bars[index-1].config(bg="#FFFFFF")
            self.work_bars[index].config(bg="#000000")
        elif page_key == "Break":
            self.work_bars[index].config(bg="#B3B3B3")
            self.break_bars[index].config(bg="#000000")






    

        



