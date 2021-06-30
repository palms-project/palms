import tkinter as tk

from . import send_data

root = tk.Tk()
root.title("PALMS")
root.geometry("600x400")


def update():
    """Update target values on server."""
    x = x_target.get()
    y = y_target.get()
    z = z_target.get()
    a = a_target.get()
    b = b_target.get()
    send_data.send({"x": x, "y": y, "z": z, "a": a, "b": b})


def zero():
    send_data.send("")


# Axis Value tkinter Variables
x_target = tk.DoubleVar(value=0)
y_target = tk.DoubleVar(value=0)
z_target = tk.DoubleVar(value=0)
a_target = tk.DoubleVar(value=0)
b_target = tk.DoubleVar(value=0)

# Axis Labels
x_label = tk.Label(root, text="X Axis 0-50", font=("calibre", 10, "bold"))
y_label = tk.Label(root, text="Y Axis 0-50", font=("calibre", 10, "bold"))
z_label = tk.Label(root, text="Z axis 0-50", font=("calibre", 10, "bold"))
a_label = tk.Label(root, text="A axis 0-50", font=("calibre", 10, "bold"))
b_label = tk.Label(root, text="B axis 0-50", font=("calibre", 10, "bold"))

# Axis Value Entry Widget
x_entry = tk.Entry(root, textvariable=x_target, font=("calibre", 10, "normal"))
y_entry = tk.Entry(root, textvariable=y_target, font=("calibre", 10, "normal"))
z_entry = tk.Entry(root, textvariable=z_target, font=("calibre", 10, "normal"))
a_target = tk.Entry(root, textvariable=a_target, font=("calibre", 10, "normal"))
b_entry = tk.Entry(root, textvariable=b_target, font=("calibre", 10, "normal"))

# Update Values on Server Button Widget
update_button = tk.Button(root, text="Update", command=update)

# Zero All Axes Button
zero_button = tk.Button(root, text="Zero All Axes", command=zero)

# Positions of Widgets
x_label.grid(row=0, column=0)
x_entry.grid(row=0, column=1)

y_label.grid(row=1, column=0)
y_entry.grid(row=1, column=1)

z_label.grid(row=2, column=0)
z_entry.grid(row=2, column=1)

a_label.grid(row=3, column=0)
a_target.grid(row=3, column=1)

b_label.grid(row=4, column=0)
b_entry.grid(row=4, column=1)

update_button.grid(row=5, column=1)

zero_button.grid(row=5, column=0)

root.mainloop()
