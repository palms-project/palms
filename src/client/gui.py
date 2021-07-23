import tkinter as tk

import send_data

root = tk.Tk()
root.title("PALMS v0.5.0")
root.geometry("")

current_data = {"x": 0.0, "y": 0.0, "z": 0.0, "a": 0.0, "b": 0.0}

FONT_SIZE = 14


def update() -> None:
    """Update target values on server"""
    new_data = {"x": x_target.get(), "y": y_target.get(), "z": z_target.get(), "a": a_target.get(), "b": b_target.get()}

    global current_data

    if verify_targets(new_data):
        try:
            send_data.send(change_position_scale(changed_values(new_data, current_data)))
        except send_data.ConnectionError as e:
            dialogue_box("Error Updating Targets", e.message)
        else:
            current_data = new_data
    else:
        dialogue_box("Invalid Position(s)", "One or more entered positions are invalid.")


def dialogue_box(title, message) -> None:
    dialogue_box = tk.Toplevel(root)
    dialogue_box.geometry("")
    dialogue_box.resizable(False, False)
    dialogue_box.title(title)
    tk.Label(dialogue_box, text=message, font=("calibre", 12, "normal")).pack(expand=1)


def changed_values(new_data: dict, current_data: dict) -> dict:
    return {key: new_data[key] for key, current_value in current_data.items() if new_data[key] != current_value}


def verify_targets(targets: dict) -> bool:
    for key, val in targets.items():
        if key == "a" and (val > 45 or val < -45):
            return False
        elif val > 25 or val < -25:
            return False
    return True


def change_position_scale(targets: dict) -> dict:
    return {key: val + 45 if key == "a" else val + 25 for key, val in targets.items()}


# Axis Value tkinter Variables
x_target = tk.DoubleVar(value=0)
y_target = tk.DoubleVar(value=0)
z_target = tk.DoubleVar(value=0)
a_target = tk.DoubleVar(value=0)
b_target = tk.DoubleVar(value=0)

# Axis Labels
label_kwargs = {"width": 17, "anchor": tk.W, "font": ("calibre", FONT_SIZE, "bold")}

x_label = tk.Label(root, text="X ±25mm", **label_kwargs)
y_label = tk.Label(root, text="Y ±25mm", **label_kwargs)
z_label = tk.Label(root, text="Z ±25mm", **label_kwargs)
a_label = tk.Label(root, text="Rotational ±45°", **label_kwargs)
b_label = tk.Label(root, text="Collimator ±25mm", **label_kwargs)

# Axis Value Entry Widget
entry_kwargs = {"font": ("calibre", FONT_SIZE, "normal")}

x_entry = tk.Entry(root, textvariable=x_target, **entry_kwargs)
y_entry = tk.Entry(root, textvariable=y_target, **entry_kwargs)
z_entry = tk.Entry(root, textvariable=z_target, **entry_kwargs)
a_entry = tk.Entry(root, textvariable=a_target, **entry_kwargs)
b_entry = tk.Entry(root, textvariable=b_target, **entry_kwargs)

# Update Values on Server Button Widget
update_button = tk.Button(root, text="Update", command=update, font=("calibre", FONT_SIZE, "normal"))

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
