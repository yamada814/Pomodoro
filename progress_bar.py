import tkinter as tk


class ProgressBar(tk.Frame):
    def __init__(self,parent,input_values,total_wid):
        super().__init__(parent)
        # 入力値の取得
        work_time = input_values["Work"]
        break_time = input_values["Break"]
        repeat = input_values["Repeat"]
       
        # バーの取得
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
                height = 2
                )
            self.work_bars.append(work_bar)
            # Breaktimeバーの生成
            break_bar = tk.Frame(
                parent,
                bg="#FFFFFF",
                bd=1,
                width=break_bar_wid,
                height = 2
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




    

        



