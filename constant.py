
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
