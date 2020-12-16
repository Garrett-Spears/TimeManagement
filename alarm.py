import datetime as dt
import os
import psutil
import tkinter as tk
import tkinter.font as font
import signal
import subprocess
import sys

class AlarmData:
    def __init__(self):
        self.sub = -1
        self.hour = -1
        self.minute = -1
        self.am_or_pm = 'n'
        self.output = ""

class HashTable:
    def __init__(self):
        self.table = [None] * 100
        self.size = 0
        self.capacity = 10

class Row:
    def __init__(self):
        self.row = None
        self.button = None
        self.display = None

DIRTY = sys.maxsize
hours = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
minutes = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60"]
time_of_day = ["am", "pm"]
alarm = [[0, 0] for i in range(1)]
alarms_set = ["" for i in range(1)]
alarm_rows = []
active_alarms = HashTable()
temp_alarm = [1, 1]
am_or_pm = "am"
alarm_set = 0
snoozing = 0
i = 1

def add_alarm_row(master, i, w, h, no_insert, status):
    global am_or_pm
    struct = AlarmData()
    struct.hour = int(alarm[i][0])
    struct.minute = int(alarm[i][1])
    struct.am_or_pm = am_or_pm
    alarm_time = str(alarm[i][0]) + ":" + str(alarm[i][1]) + " " + struct.am_or_pm
    retval = 0

    if no_insert == 0:
        retval = hash_insertion(active_alarms, struct)
    if retval == -1:
        return None
    if struct.hour < 10:
        alarm_time = "  " + alarm_time

    row = tk.Frame(master, width=w - 16, height=h)
    row.configure(highlightthickness = 1, highlightbackground = "white", bg = "black")
    alarm_display = tk.Label(row, text = alarm_time, font = (None, int(7 * h / 16)), pady = int(h / 4), padx = int(w / 12))
    alarm_display.configure(fg = "white", bg = "black")
    row.pack(fill="x")
    alarm_display.pack(side = tk.LEFT)

    if status == 0:
        alarm_button = tk.Button(row, text = "Set", relief = "raised", width = int(w / 60), bg = "green")
    else:
        alarm_button = tk.Button(row, text="Turn Off", relief="raised", width=int(w / 60), bg="FireBrick")

    alarm_button.configure(command = lambda: toggle_alarm_button(alarm_button, alarm_display))
    alarm_button.pack(pady = (int(h / 3), int(h / 22)))
    delete_button = tk.Button(row, text = "Delete", relief = "raised", bg = "Orange", width = int(w / 60))
    delete_button.configure(command = lambda: delete_alarm(row, alarm_time))
    delete_button.pack(pady = (int(h / 22), int(h / 3)))

    temp_alarm[0] = 1
    temp_alarm[1] = 1
    am_or_pm = "am"
    selected_row = Row()
    selected_row.row = row
    selected_row.button = alarm_button
    selected_row.display = alarm_time

    return selected_row

def adjust_hour(hour):
    if (int(hour) >= 13):
        hour = str(int(hour) - 12)
    elif (int(hour) == 0):
        hour = "12"
    return hour

def adjust_minute(minute):
    if (int(minute) <= 9):
        minute = "0" + minute
    return minute

def change_alarm_hour(value):
    temp_alarm[0] = value

def change_alarm_minute(value):
    temp_alarm[1] = value

def change_time_of_day(value):
    global am_or_pm
    am_or_pm = value

def create_button(root, string, function_call):
    button = tk.Button(root, text = string, command = function_call)
    return button

def create_label(root, var, text_size):
    label = tk.Label(root, textvariable = var, font = (None, text_size))
    return label

def delete_alarm(row, alarm_time):
    global i
    l = 0
    hour = ""
    minute = ""
    ap = ""
    alarm_time.replace(" ", "")
    length = len(alarm_time)
    flag = 0

    while l < length:
        if alarm_time[l] == ':':
            flag += 1
        elif alarm_time[l] == ' ':
            l = l
        elif flag == 0:
            hour = hour + alarm_time[l]
        elif flag == 1:
            minute = minute + alarm_time[l] + alarm_time[l + 1]
            flag += 1
            l += 1
        elif flag == 2:
            ap = ap + alarm_time[l] + alarm_time[l + 1]
            l += 1
        l += 1

    search_struct = AlarmData()
    search_struct.hour = int(hour)
    search_struct.minute = int(minute)
    search_struct.am_or_pm = ap
    hash_deletion(active_alarms, search_struct)
    k = 0
    flag = 0
    length = len(alarm_rows)

    while k < length:
        if alarm_rows[k] is not None:
            if flag == 1:
                ((alarm_rows[k]).row).pack(fill = "x")
                k += 1
                continue
            elif (alarm_rows[k]).display == alarm_time:
                alarm_rows.remove(alarm_rows[k])
                k -= 1
                length -= 1
                flag = 1
        k += 1
    row.destroy()
    canvas.configure(scrollregion=canvas.bbox("all"))
    i -= 1
    return

def do_nothing():
    return

def exit_function():
    i = 0
    length = active_alarms.capacity
    save_file = open("saved_alarms.txt", "w")

    while i < length:
        if (active_alarms.table)[i] == -1 or (active_alarms.table)[i] == DIRTY or (active_alarms.table)[i] is None:
            i += 1
            continue
        else:
            if (((active_alarms.table)[i]).sub) is None or (((active_alarms.table)[i]).sub) == -1:
                save_file.write("-1")
            else:
                save_file.write(str((((active_alarms.table)[i]).sub).pid))

            save_file.write(" ")
            save_file.write(str((active_alarms.table)[i].hour))
            save_file.write(" ")
            save_file.write(str((active_alarms.table)[i].minute))
            save_file.write(" ")
            save_file.write(str((active_alarms.table)[i].am_or_pm))
            save_file.write("\n")
        i += 1
    save_file.close()
    root.destroy()

def expand_hash_table(table):
    new_capacity = table.capacity * 2 + 1
    new_table = [None] * new_capacity
    i = 0

    while i < table.capacity:
        if (table.table)[i] == None:
            i += 1
        else:
            value = (table.table)[i]
            hash_value = hash(value.hour * value.minute)
            i = 0
            while i < new_capacity:
                hash_value = hash_value % new_capacity
                if new_table[hash_value] == None:
                    new_table[hash_value] = value
                    break
                elif new_table[hash_value] == DIRTY:
                    new_table[hash_value] = value
                    break
                else:
                    hash_value += 1
                    i += 1
    table.table = new_table
    table.capacity = new_capacity
    return

def find_and_turn_off_alarm(target_time):
    i = 1
    while (i < len(alarms_set)):
        if (alarms_set[i] == target_time):
            alarms_set.pop(i)
            return

def find_row(display):
    k = 0
    length = len(alarm_rows)

    while k < length:
        if trim(alarm_rows[k].display) == display:
            return k
        k += 1
    return -1

def get_time_string():
    hour = str(dt.datetime.now().hour)
    minute = str(dt.datetime.now().minute)
    if int(hour) > 12:
        ap = "pm"
    else:
        ap = "am"
    hour = adjust_hour(hour)
    minute = adjust_minute(minute)
    return (hour + ":" + minute + " " + ap)

def hash_deletion(table, value):
    index = hash_search(table, value)

    if index == -1:
        return
    else:
        if ((table.table)[index]).sub != -1:
            ((table.table)[index]).sub.kill()
        ((table.table)[index]).sub = -1
        (table.table)[index] = DIRTY
        table.size -= 1
        return

def hash_insertion(table, value):
    if (table.capacity - table.size) <= 0:
        expand_hash_table(table)

    hash_value = hash(value.hour * value.minute)
    i = 0

    while i < table.capacity:
        hash_value = hash_value % table.capacity
        if (table.table)[hash_value] == None:
            (table.table)[hash_value] = value
            table.size += 1
            return 0
        elif (table.table)[hash_value] == DIRTY:
            (table.table)[hash_value] = value
            table.size += 1
            return 0
        else:
            if ((table.table)[hash_value]).hour == value.hour and ((table.table)[hash_value]).minute == value.minute and ((table.table)[hash_value]).am_or_pm == value.am_or_pm:
                print("Duplicate value trying to be inserted!!")
                return -1
            hash_value += 1
            i += 1
    return 1

def hash_search(table, value):
    i = 0
    hash_value = hash(value.hour * value.minute)

    while i < table.capacity:
        hash_value = hash_value % table.capacity
        if (table.table)[hash_value] == DIRTY:
            hash_value += 1
            i += 1
            continue
        elif (table.table)[hash_value] is None:
            hash_value += 1
            i += 1
        elif ((table.table)[hash_value]).hour == value.hour and ((table.table)[hash_value]).minute == value.minute:
            return hash_value
        else:
            hash_value += 1
            i += 1
    return -1

def init():
    if not (os.path.exists("saved_alarms.txt")):
        open("saved_alarms.txt", "x")
    file = open("saved_alarms.txt", "r")
    for line in file:
        j = 0
        for word in line.split():
            if j == 0:
                subpro = int(word)
                processID = -1
                if subpro != -1:
                    for proc in psutil.process_iter():
                        try:
                            # Get process name & pid from process object.
                            processName = proc.name()
                            processID = proc.pid
                            if processID == subpro:
                                break
                            else:
                                processID = -1
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            pass
                if processID != -1:
                    os.kill(processID, signal.SIGTERM)
            elif j == 1:
                h = word
            elif j == 2:
                m = word
            else:
                ap = word
                temp_time = h + ":" + m + " " + ap
                temp_struct = AlarmData()
                if subpro != -1:
                    p = subprocess.Popen([sys.executable, "active_alarm.py", temp_time])
                else:
                    p = -1
                temp_struct.sub = p
                temp_struct.hour = int(h)
                temp_struct.minute = int(m)
                temp_struct.am_or_pm = ap
                hash_insertion(active_alarms, temp_struct)
            j += 1
    file.close()

def init_alarms(master, h, w, i):
    global am_or_pm
    k = 0
    length = len(active_alarms.table)

    while k < length:
        if (active_alarms.table)[k] is None or (active_alarms.table)[k] == DIRTY:
            k += 1
            continue
        else:
            hour = str(((active_alarms.table)[k]).hour)
            minute = str(((active_alarms.table)[k]).minute)

            if int(minute) >= 0 and int(minute) <= 9:
                minute = "0" + minute

            temp_alarm[0] = hour
            temp_alarm[1] = minute
            am_or_pm = ((active_alarms.table)[k]).am_or_pm
            alarm.append(temp_alarm)
            if ((active_alarms.table)[k]).sub == -1 or ((active_alarms.table)[k]).sub is None:
                status = 0
            else:
                status = 1
            alarm_rows.append(add_alarm_row(master, i, w, h, 1, status))
            i += 1
            k += 1
    return i

def keep_it_running():
    global alarm_set
    global i
    global snoozing

    if (alarm_set == 1):
        if (temp_alarm[0] == 1):
            temp_alarm[0] = "12"
        if (temp_alarm[1] == 1):
            temp_alarm[1] = "00"
        alarm.append(temp_alarm)
        alarm_rows.append(add_alarm_row(big_boi, i, int(width), int(height) / 8, 0, 0))
        i += 1
        alarm_set = 0

    k = 0

    while k < len(active_alarms.table):
        if (active_alarms.table)[k] is not None and (active_alarms.table)[k] != DIRTY:
            if ((active_alarms.table)[k]).sub != -1 and ((active_alarms.table)[k]).sub != None:
                if (((active_alarms.table)[k]).sub).poll() == 1:
                    ((active_alarms.table)[k]).sub = -1
                    find_time = str(((active_alarms.table)[k]).hour) + ":" + str(((active_alarms.table)[k]).minute) + " " + str(((active_alarms.table)[k]).am_or_pm)
                    row_index = find_row(find_time)

                    if row_index != -1 and (alarm_rows[row_index].button).cget('text') == "Turn Off":
                        (alarm_rows[row_index].button).config(text = "Set", bg = "green")
        k += 1
    root.after(50, keep_it_running)

def name_window(root, window_name):
    root.title(window_name)
    return

def nw_window():
    def alarm_created():
        global alarm_set
        alarm_set = 1
        add_alarm_window.destroy()

    h = int(height) / 2
    w = int(width) / 2
    add_alarm_window = tk.Toplevel(root, height = h - 50, width = w, bg = "black")
    add_alarm_window.resizable(width = "false", height = "false")
    add_alarm_window.title("Add Alarm")
    add_alarm_window.transient(root)
    add_alarm_window.grab_set()
    nw_title = tk.Label(add_alarm_window, text = "Add Alarm", font = (None, int(h / 12)), anchor = tk.CENTER)
    nw_title.configure(fg = "white", bg = "black")
    nw_title.place(x = w / 2, y = h / 5, anchor = tk.CENTER)
    create_alarm_button = create_button(add_alarm_window, "Create Alarm", alarm_created)
    create_alarm_button.place(x = w / 2, y = 3 * h / 5, anchor = tk.CENTER)
    var1 = tk.StringVar()
    var2 = tk.StringVar()
    var3 = tk.StringVar()
    var1.set(hours[11])
    var2.set(minutes[0])
    var3.set(time_of_day[0])
    dropdown_menu_1 = tk.OptionMenu(add_alarm_window, var1, *hours, command=change_alarm_hour)
    dropdown_menu_1.pack()
    dropdown_menu_1.place(x = w / 4, y = 2 * h / 5, anchor = tk.CENTER)
    dropdown_menu_2 = tk.OptionMenu(add_alarm_window, var2, *minutes, command=change_alarm_minute)
    dropdown_menu_2.pack()
    dropdown_menu_2.place(x = 2 * w / 4, y = 2 * h / 5, anchor = tk.CENTER)
    dropdown_menu_3 = tk.OptionMenu(add_alarm_window, var3, *time_of_day, command=change_time_of_day)
    dropdown_menu_3.pack()
    dropdown_menu_3.place(x=3 * w / 4, y= 2 * h / 5, anchor = tk.CENTER)
    return

def reset_scrollregion(event):
    canvas.config(scrollregion=canvas.bbox("all"))

def set_label(var, string):
    var.set(string)
    return

def set_window_size(root, height, width):
    geometry_string = height + "x" + width
    root.geometry(geometry_string)
    return

def toggle_alarm_button(alarm_button, display_time):
    temp_time = display_time.cget("text")
    length = len(temp_time)
    reach_colon = 0
    hour = ""
    minute = ""
    l = 0

    while l < length:
        if temp_time[l] == " " and reach_colon == 1:
            ap = temp_time[l + 1] + temp_time[l + 2]
            break
        if temp_time[l] == ':':
            reach_colon = 1
        elif reach_colon == 0:
            hour = hour + temp_time[l]
        else:
            minute = minute + temp_time[l]
        l += 1
    if (alarm_button["text"] == "Set"):
        alarm_button.config(text = "Turn Off", bg = "FireBrick")
        sys.stdout.flush()
        command = "active_alarm.py"
        struct = AlarmData()
        struct.hour = int(hour)
        struct.minute = int(minute)
        struct.am_or_pm = ap
        index = hash_search(active_alarms, struct)
        p = subprocess.Popen([sys.executable, command, temp_time])
        (((active_alarms).table)[index]).sub = p
        (((active_alarms).table)[index]).output = p.poll()
    else:
        alarm_button.config(text = "Set", bg = "green")
        temp_struct = AlarmData()
        temp_struct.hour = int(hour)
        temp_struct.minute = int(minute)
        temp_struct.am_or_pm = ap
        index = hash_search(active_alarms, temp_struct)
        ((active_alarms.table)[index]).sub.kill()
        ((active_alarms.table)[index]).sub = -1
    return

def trim(spaced_string):
    return spaced_string.lstrip();

if __name__ == "__main__":
    height = "750"
    width = "750"
    window_name = "Alarm"
    init()

    root = tk.Tk()
    root.resizable(height = "false", width = "false")
    name_window(root, window_name)
    set_window_size(root, height, width)

    canvas = tk.Canvas(root, width = width, height = height)
    canvas.configure(bg = "black")
    canvas.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)

    big_boi = tk.Frame(canvas)
    big_boi.configure(bg = "black")
    canvas.create_window((0,0), window = big_boi, anchor = tk.NW, width = int(width))

    top_frame = tk.Frame(big_boi, width = int(width), height = int(height) / 5, highlightthickness = 1, bg = "black")
    top_frame.pack(fill = tk.BOTH)

    yscroll = tk.Scrollbar(canvas, orient = tk.VERTICAL, command = canvas.yview)
    canvas.configure(yscrollcommand = yscroll.set)
    yscroll.pack(side = tk.RIGHT, fill = tk.Y)

    big_boi.bind("<Configure>", reset_scrollregion)

    title = tk.StringVar()
    title_text_size = int(int(height) / 20)
    title_label = create_label(top_frame, title, title_text_size)
    set_label(title, "Alarm App")
    title_label.configure(bg = "black", fg = "white")
    title_label.pack(side = tk.LEFT, padx = int(width) / 15, ipady = int(height) / 30)
    i = init_alarms(big_boi, int(height) / 8, int(width), i)

    root.protocol('WM_DELETE_WINDOW', exit_function)
    add_alarm_button = create_button(top_frame, "+", nw_window)
    plus_font = font.Font(size = int(int(width) / 50))
    add_alarm_button['font'] = plus_font
    add_alarm_button.pack(side = tk.RIGHT, padx = int(width) / 6)

    root.after(50, keep_it_running)

    root.mainloop()
