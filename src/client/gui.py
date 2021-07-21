import tkinter as tk

import send_data

root = tk.Tk()
root.title("PALMS v0.4.0")
root.geometry("600x400")

current_data = {"x": 0.0, "y": 0.0, "z": 0.0, "a": 0.0, "b": 0.0}


def update():
    """Update target values on server."""
    new_data = {"x": x_target.get(), "y": y_target.get(), "z": z_target.get(), "a": a_target.get(), "b": b_target.get()}
    send_data.send(changed_values(new_data, current_data))
    global current_data
    current_data = new_data


def changed_values(new_data: dict, current_data: dict) -> dict:
    return {key: new_data[key] for key, current_value in current_data.items() if new_data[key] != current_value}


# Axis Value tkinter Variables
x_target = tk.DoubleVar(value=0)
y_target = tk.DoubleVar(value=0)
z_target = tk.DoubleVar(value=0)
a_target = tk.DoubleVar(value=0)
b_target = tk.DoubleVar(value=0)

# Axis Labels
x_label = tk.Label(root, text="X Axis 0-50mm", font=("calibre", 10, "bold"))
y_label = tk.Label(root, text="Y Axis 0-50mm", font=("calibre", 10, "bold"))
z_label = tk.Label(root, text="Z axis 0-50mm", font=("calibre", 10, "bold"))
a_label = tk.Label(root, text="A axis 0-90°", font=("calibre", 10, "bold"))
b_label = tk.Label(root, text="B axis 0-50mm", font=("calibre", 10, "bold"))

# Axis Value Entry Widget
x_entry = tk.Entry(root, textvariable=x_target, font=("calibre", 10, "normal"))
y_entry = tk.Entry(root, textvariable=y_target, font=("calibre", 10, "normal"))
z_entry = tk.Entry(root, textvariable=z_target, font=("calibre", 10, "normal"))
a_entry = tk.Entry(root, textvariable=a_target, font=("calibre", 10, "normal"))
b_entry = tk.Entry(root, textvariable=b_target, font=("calibre", 10, "normal"))

# Update Values on Server Button Widget
update_button = tk.Button(root, text="Update", command=update)

# Positions of Widgets
x_label.grid(row=0, column=0)
x_entry.grid(row=0, column=1)

y_label.grid(row=1, column=0)
y_entry.grid(row=1, column=1)

z_label.grid(row=2, column=0)
z_entry.grid(row=2, column=1)

a_label.grid(row=3, column=0)
a_entry.grid(row=3, column=1)

b_label.grid(row=4, column=0)
b_entry.grid(row=4, column=1)

update_button.grid(row=5, column=1)


root.mainloop()
