import time
import datetime as dt
import tkinter as tk
import sys

global not_alive
not_alive = 0

def adjust_hour(adj_hour):
    if adj_hour >= 13:
        adj_hour = adj_hour - 12
    elif adj_hour == 0:
        adj_hour = 12
    return adj_hour

def adjust_minute(adj_minute):
    return adj_minute

def alarm_window_open():
    height = "250"
    width = "600"
    window_name = "Alarm Finished"
    root = tk.Tk()
    root.title(window_name)
    root.configure(background = "black")
    set_window_size(root, width, height)

    def task():
        print('\a')
        root.after(1000, task)

    message = tk.Label(root, text = "WAKE UP!!!", fg = "white", bg = "black", font = (None, 16))
    message.place(x = int(width) / 2, y = int(height) / 3, anchor = "c")

    end_button = tk.Button(root, text = "Turn Off", command = lambda: end(root))
    end_button.place(x=int(width) / 3, y= 2 * int(height) / 3, anchor="c")

    snooze_button = tk.Button(root, text = "Snooze", command = lambda: snooze(root))
    snooze_button.place(x= 2 * int(width) / 3, y=2 * int(height) / 3, anchor="c")

    root.after(1000, task)
    root.mainloop()

def check_ap(ap):
    current_hour = int(dt.datetime.now().hour)
    if current_hour >= 12 and current_hour < 24:
        current_ap = "pm"
    else:
        current_ap = "am"
    if current_ap == ap:
        return 1
    return 0

def check_hour(ch_hour):
    ch_hour = int(ch_hour)
    current_hour = int(dt.datetime.now().hour)
    current_hour = adjust_hour(current_hour)
    if (ch_hour == current_hour):
        return 1
    return 0

def check_minute(ch_minute):
    ch_minute = int(ch_minute)
    current_minute = int(dt.datetime.now().minute)
    if ch_minute == current_minute:
        return 1
    return 0

def check_alarm_loop(hour, minute, ap):
    while 1:
        if check_hour(hour) and check_minute(minute) and check_ap(ap):
            alarm_window_open()
            return 0
        else:
            time.sleep(0.5)

def end(root):
    global not_alive
    root.destroy()
    not_alive = 1
    sys.exit(1)
    return

def set_window_size(root, height, width):
    geometry_string = height + "x" + width
    root.geometry(geometry_string)
    return

def snooze(root):
    root.destroy()
    return

if __name__ == "__main__":
    hour = ""
    minute = ""
    ap = ""
    alarm_status = 0

    for i, arg in enumerate(sys.argv):
        if i == 1:
            time_string = arg
    i = 0
    length = len(time_string)
    reach_colon = 0
    while i < length:
        if time_string[i] == " " and reach_colon == 1:
            ap = time_string[i + 1] + time_string[i + 2]
            break
        elif time_string[i] == ':':
            reach_colon = 1
        elif reach_colon == 0:
            hour = hour + time_string[i]
        else:
            minute = minute + time_string[i]
        i += 1

    while alarm_status == 0:
        alarm_status = check_alarm_loop(hour, minute, ap)
        if not_alive != 0:
            sys.stdout.flush()
            sys.exit(1)
        minute = str(int(minute) + 5)
        if int(minute) >= 60:
            minute = str(int(minute) - 60)
            hour = str(int(hour) + 1)
            if int(hour) > 12:
                hour = str(int(hour) - 12)
                if ap == "am":
                    ap = "pm"
                else:
                    ap = "am"
    sys.exit(1)
