import tkinter as tk
import pyperclip
import win32gui
import win32con
import re

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
    time_str = entry_time.get()
    frame_count = time2frame(time_str)
    
    if frame_count is not None:
        result_label.config(text=f"フレーム数: {frame_count}")
    else:
        result_label.config(text="有効な時間形式を入力してください")

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
        result_label.config(text="有効な時間形式を入力してください")

def toggle_on_top():
    global window_on_top
    title = window.title()
    def foreground_on(hwnd, title):
        name = win32gui.GetWindowText(hwnd)
        if name.find(title) >= 0:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def foreground_off(hwnd, title):
        name = win32gui.GetWindowText(hwnd)
        if name.find(title) >= 0:
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    if window_on_top:
        win32gui.EnumWindows(foreground_off, title)
        window_on_top = False
        toggle_on_top_button.config(text="最前面に表示")
    else:
        win32gui.EnumWindows(foreground_on, title)
        window_on_top = True
        toggle_on_top_button.config(text="最前面表示を解除")

window = tk.Tk()
window.title("time2frame")
window.geometry("200x150")
window.iconbitmap("icon.ico")

toggle_frame_button = tk.Button(window, text="FPS: 30", command=toggle_frame)
toggle_frame_button.pack()

time_label = tk.Label(window, text="分:秒を入力してください:")
time_label.pack()
entry_time = tk.Entry(window)
entry_time.pack()

button_frame = tk.Frame(window) 

clear_button = tk.Button(button_frame, text="クリア", command=clear_input)
clear_button.pack(side=tk.LEFT)  

copy_button = tk.Button(button_frame, text="コピー", command=copy_to_clipboard)
copy_button.pack(side=tk.LEFT)  

convert_button = tk.Button(button_frame, text="変換", command=process_input)
convert_button.pack(side=tk.LEFT) 

button_frame.pack() 

result_label = tk.Label(window, text="")
result_label.pack()

toggle_on_top_button = tk.Button(window, text="最前面に表示", command=toggle_on_top)
toggle_on_top_button.pack()

window.mainloop()
