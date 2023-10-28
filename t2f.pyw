import tkinter as tk
import pyperclip
import win32gui
import win32con
import re

copy_flag = False
window_on_top = False
frame = 30

def time2frame(time_str):
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

def toggle_frame():
    global frame
    if frame == 30:
        frame = 60
        toggle_frame_button.config(text="FPS: 60")
    else:
        frame = 30
        toggle_frame_button.config(text="FPS: 30")

def process_input():
    global copy_flag
    minutes_str = minutes_entry.get()
    seconds_str = seconds_entry.get()

    if not minutes_str:
        minutes_str = '0'
    
    if not seconds_str:
        seconds_str = '0'

    frame_count = time2frame(f"{minutes_str}:{seconds_str}")
    if frame_count == 0:
        result_label.config(text="数値が入力されていません。")
    elif frame_count is not None:
        result_label.config(text=f"フレーム数: {frame_count}")
        copy_flag = True

def clear_input():
    minutes_entry.delete(0, tk.END)
    seconds_entry.delete(0, tk.END)

def copy_to_clipboard():
    minutes_str = minutes_entry.get()
    seconds_str = seconds_entry.get()
    
    if not minutes_str:
        minutes_str = '0'
    
    if not seconds_str:
        seconds_str = '0'
    frame_count = time2frame(f"{minutes_str}:{seconds_str}")

    if frame_count:
        pyperclip.copy(frame_count)
        copy_button.config(text="コピー完了！")
        result_label.config(text=f"フレーム数: {frame_count}")
    else:
        copy_button.config(text="コピー")
        result_label.config(text="数値が入力されていません。")

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

def foreground_off(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

window = tk.Tk()
window.title("time2frame")
window.geometry("200x150")
window.iconbitmap("icon.ico")

toggle_frame_button = tk.Button(window, text="FPS: 30", command=toggle_frame)
toggle_frame_button.pack()

input_frame = tk.Frame(window)
input_frame.pack()

minutes_label = tk.Label(input_frame, text="分:")
minutes_label.pack(side=tk.LEFT)
minutes_entry = tk.Entry(input_frame, width=3)
minutes_entry.pack(side=tk.LEFT)

seconds_label = tk.Label(input_frame, text="秒:")
seconds_label.pack(side=tk.LEFT)
seconds_entry = tk.Entry(input_frame, width=3)
seconds_entry.pack(side=tk.LEFT)

button_frame = tk.Frame(window)
button_frame.pack()

clear_button = tk.Button(button_frame, text="クリア", command=clear_input)
clear_button.pack(side=tk.LEFT)

copy_button = tk.Button(button_frame, text="コピー", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT)

convert_button = tk.Button(button_frame, text="変換", command=process_input)
convert_button.pack(side=tk.LEFT)

result_label = tk.Label(window, text="")
result_label.pack()

toggle_on_top_button = tk.Button(window, text="最前面に表示", command=toggle_on_top)
toggle_on_top_button.pack()

window.mainloop()
