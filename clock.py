import datetime as dt
import math
import tkinter as tk

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

def adjust_second(second):
    if (int(second) <= 9):
        second = "0" + second
    return second

def am_or_pm(hour):
    if (int(hour) >= 12):
        return "pm"
    return "am"

def clock():
    place_sec_hand()
    place_min_hand()
    place_hour_hand()
    digital_str = get_digital_string()
    set_label(display, digital_str)
    date_str = get_date_string()
    set_label(date_var, date_str)
    root.after(50, clock)

def create_canvas(root, height, width):
    canvas = tk.Canvas(root, height = height, width = width)
    return canvas

def create_label(root, var, text_size):
    label = tk.Label(root, textvariable = var, font = (None, text_size))
    return label

def create_circle(canvas, x0, y0, x1, y1):
    circle = canvas.create_oval(x0, y0, x1, y1)
    return circle

def display_text(canvas, x, y, num_string):
    canvas.create_text(x, y, text = num_string)
    return

def draw_line(canvas, x0, y0, x1, y1):
    line = canvas.create_line(x0, y0, x1, y1)
    return line

def get_date_string():
    date = dt.datetime.today().strftime("%A, %B %d, %Y")
    return date

def get_digital_string():
    hour = get_hour()
    time_of_day = am_or_pm(hour)
    hour = adjust_hour(hour)
    minute = get_minute()
    minute = adjust_minute(minute)
    second = get_second()
    second = adjust_second(second)
    digital_string = hour + ":" + minute + ":" + second + time_of_day + '\n'
    return digital_string

def get_hour():
    hour = str(dt.datetime.now().hour)
    return hour

def get_minute():
    minute = str(dt.datetime.now().minute)
    return minute

def get_second():
    second = str(dt.datetime.now().second)
    return second

def get_x(radius, degrees, mid):
    rads = degrees * math.pi / 180
    x = radius * math.cos(rads) + mid
    return x

def get_y(radius, degrees, mid):
    rads = degrees * math.pi / 180
    y = radius * math.sin(rads) + mid
    return y

def name_window(root, window_name):
    root.title(window_name)
    return

def place_hour_hand():
    global hour_hand
    canv.delete(hour_hand)
    current_hour = dt.datetime.now().hour
    current_minute = dt.datetime.now().minute
    current_second = dt.datetime.now().second
    x = get_x(radius_hour_hand, ((current_hour * 60 * 60 + current_minute * 60 + current_second) - 10800) / 120, middle_of_circle_x)
    y = get_y(radius_hour_hand, ((current_hour * 60 * 60 + current_minute * 60 + current_second) - 10800) / 120, middle_of_circle_y)
    hour_hand = draw_line(canv, middle_of_circle_x, middle_of_circle_y, x, y)
    canv.pack()

def place_min_hand():
    global minute_hand
    canv.delete(minute_hand)
    current_minute = dt.datetime.now().minute
    current_second = dt.datetime.now().second
    x = get_x(radius_minute_hand, ((current_minute * 60 + current_second) - 900) / 10, middle_of_circle_x)
    y = get_y(radius_minute_hand, ((current_minute * 60 + current_second) - 900) / 10, middle_of_circle_y)
    minute_hand = draw_line(canv, middle_of_circle_x, middle_of_circle_y, x, y)
    canv.pack()

def place_sec_hand():
    global second_hand
    canv.delete(second_hand)
    current_second = dt.datetime.now().second
    x = get_x(radius_second_hand, (current_second - 15) * 6, middle_of_circle_x)
    y = get_y(radius_second_hand, (current_second - 15) * 6, middle_of_circle_y)
    second_hand = draw_line(canv, middle_of_circle_x, middle_of_circle_y, x, y)
    canv.pack()

def set_label(var, string):
    var.set(string)
    return

def set_window_size(root, height, width):
    geometry_string = height + "x" + width
    root.geometry(geometry_string)
    return

if __name__ == "__main__":
    height = "500"
    width = "500"
    window_name = "Clock"
    window_background_color = "black"
    text_color = "white"
    x0 = int(width) / 5
    y0 = int(height) / (int(height) / 10)
    x1 = int(width) - int(width) / 5
    y1 = x1 - x0 + y0

    circle_height = y1 - y0
    circle_width = x1 - x0
    radius = circle_height / 2

    middle_of_circle_y = y0 + circle_height / 2
    middle_of_circle_x = x0 + circle_width / 2

    root = tk.Tk()
    root.resizable(width = "false", height = "false")
    name_window(root, window_name)
    set_window_size(root, height, width)

    canv = create_canvas(root, height, width)
    outer_circle = create_circle(canv, x0, y0, x1, y1)
    inner_circle = create_circle(canv, middle_of_circle_x - 5, middle_of_circle_y - 5, middle_of_circle_x + 5, middle_of_circle_y + 5)
    canv.itemconfig(outer_circle, fill = "white")
    canv.itemconfig(inner_circle, fill = 'black')
    canv.config(bg = window_background_color)

    display = tk.StringVar()
    digital_text_size = int(int(height) / 17)
    digital = create_label(root, display, digital_text_size)
    digital.config(fg = text_color, bg = window_background_color)
    middle_of_digital_y = y1 + (int(height) - y1) / 2
    middle_of_digital_x = int(width) / 2
    digital.place(x = middle_of_digital_x, y = middle_of_digital_y, anchor = "center")
    time_string = get_digital_string()
    set_label(display, time_string)

    date_var = tk.StringVar()
    date_text_size = int(int(height) / 30)
    date_label = create_label(root, date_var, date_text_size)
    date_label.config(fg = text_color, bg = window_background_color)
    middle_of_digital_y = middle_of_digital_y + digital_text_size / 2
    date_label.place(x = middle_of_digital_x, y = middle_of_digital_y, anchor = "center")
    date_string = get_date_string()
    set_label(date_var, time_string)

    i = 30
    num = "4"
    spoke_length = circle_height / 10
    reduced_radius = radius - spoke_length
    numbers_radius = radius - circle_height / 8.5

    while (i <= 360):
        x = get_x(radius, i, middle_of_circle_x)
        y = get_y(radius, i, middle_of_circle_y)
        second_x = get_x(reduced_radius, i, middle_of_circle_x)
        second_y = get_y(reduced_radius, i, middle_of_circle_y)
        draw_line(canv, x, y, second_x, second_y)
        num_x = get_x(numbers_radius, i, middle_of_circle_x)
        num_y = get_y(numbers_radius, i, middle_of_circle_y)
        display_text(canv, num_x, num_y, num)
        if (int(num) == 12):
            num = "1"
        else:
            num = str(int(num) + 1)
        i += 30

    i = 6
    spoke_length = circle_height / 25
    reduced_radius = radius - spoke_length
    while (i <= 360):
        x = get_x(radius, i, middle_of_circle_x)
        y = get_y(radius, i, middle_of_circle_y)
        second_x = get_x(reduced_radius, i, middle_of_circle_x)
        second_y = get_y(reduced_radius, i, middle_of_circle_y)
        draw_line(canv, x, y, second_x, second_y)
        i += 6

    second_hand = draw_line(canv, 0, 0, 0, 0)
    minute_hand = draw_line(canv, 0, 0, 0, 0)
    hour_hand = draw_line(canv, 0, 0, 0, 0)
    radius_second_hand = radius - radius / 8
    radius_minute_hand = radius - radius / 4
    radius_hour_hand = radius - radius / 2

    clock()

    root.mainloop()