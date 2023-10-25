import tkinter as tk
import pyperclip
import win32gui
import win32con
import re

window_on_top = False

def time2frame(time_str):
    frame = 30
    try:
        time_str = re.sub(r'[：:]', ':', time_str)
        
        if ":" in time_str:
            minutes, seconds = map(int, time_str.split(":"))
            frame_count = (minutes * 60 + seconds) * frame
        else:
            seconds = int(time_str)
            frame_count = seconds * frame
        return round(frame_count)
    except ValueError:
        return None

def process_input():
    time_str = entry_time.get()
    frame_count = time2frame(time_str)
    
    if frame_count is not None:
        result_label.config(text=f"フレーム数: {frame_count}")
    else:
        result_label.config(text="有効な時間形式（分:秒または秒）を入力してください")

def clear_input():
    entry_time.delete(0, tk.END)

def copy_to_clipboard():
    time_str = entry_time.get()
    frame_count = time2frame(time_str)
    if frame_count is not None:
        pyperclip.copy(frame_count)
        copy_button.config(text="コピー完了！")
        result_label.config(text=f"フレーム数: {frame_count}")
    else:
        copy_button.config(text="コピー")
        result_label.config(text="有効な時間形式（分:秒または秒）を入力してください")

def toggle_on_top():
    global window_on_top
    title = window.title()
    if window_on_top:
        win32gui.EnumWindows(foreground_off, title)
        window_on_top = False
        toggle_on_top_button.config(text="最前面に表示")
    else:
        win32gui.EnumWindows(foreground_on, title)
        window_on_top = True
        toggle_on_top_button.config(text="最前面表示を解除")

def foreground_on(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return

def foreground_off(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

window = tk.Tk()
window.title("time2frame")
window.geometry("200x170")
window.iconbitmap("icon.ico")

time_label = tk.Label(window, text="時間（分:秒または秒）を入力してください:")
time_label.pack()
entry_time = tk.Entry(window)
entry_time.pack()

convert_button = tk.Button(window, text="変換", command=process_input)
convert_button.pack()

clear_button = tk.Button(window, text="クリア", command=clear_input)
clear_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

copy_button = tk.Button(window, text="コピー", command=copy_to_clipboard)
copy_button.pack()

toggle_on_top_button = tk.Button(window, text="最前面に表示", command=toggle_on_top)
toggle_on_top_button.pack()

window.mainloop()
