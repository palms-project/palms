import tkinter as tk

import send_data

FONT = ("calibre", 14, "normal")
BOLD_FONT = ("calibre", 14, "bold")
SMALL_FONT = ("calibre", 12, "normal")


class MainApplication:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.frame = tk.Frame(master)
        self.master.title("PALMS v0.5.0")
        self.master.geometry("")
        self.master.resizable(False, False)

        self.x_position, self.x_label, self.x_entry = self.axis_widgets("X ±25mm")
        self.y_position, self.y_label, self.y_entry = self.axis_widgets("Y ±25mm")
        self.z_position, self.z_label, self.z_entry = self.axis_widgets("Z ±25mm")
        self.a_position, self.a_label, self.a_entry = self.axis_widgets("Rotational ±45°")
        self.b_position, self.b_label, self.b_entry = self.axis_widgets("Collimator ±25mm")

        self.update_button = tk.Button(self.frame, text="Update", command=self.update, font=FONT)

        self.x_label.grid(row=0, column=0)
        self.x_entry.grid(row=0, column=1)

        self.y_label.grid(row=1, column=0)
        self.y_entry.grid(row=1, column=1)

        self.z_label.grid(row=2, column=0)
        self.z_entry.grid(row=2, column=1)

        self.a_label.grid(row=3, column=0)
        self.a_entry.grid(row=3, column=1)

        self.b_label.grid(row=4, column=0)
        self.b_entry.grid(row=4, column=1)

        self.update_button.grid(row=5, column=1)

        self.frame.pack()

        self.current_data = {"x": 0.0, "y": 0.0, "z": 0.0, "a": 0.0, "b": 0.0}

    def update(self) -> None:
        """Update target values on server"""
        new_data = {
            "x": self.x_position.get(),
            "y": self.y_position.get(),
            "z": self.z_position.get(),
            "a": self.a_position.get(),
            "b": self.b_position.get(),
        }

        if self.verify_positions(new_data):
            try:
                send_data.send(self.change_position_scale(self.changed_values(new_data, self.current_data)))
            except send_data.ConnectionError as e:
                DialogBox(tk.Toplevel(self.master), "Error Updating Targets", e.message)
            else:
                self.current_data = new_data
        else:
            DialogBox(tk.Toplevel(self.master), "Invalid Position(s)", "One or more entered positions are invalid.")

    def axis_widgets(self, label_text: str):
        position_var = self.position_var()
        position_label = self.position_label(label_text)
        position_entry = self.position_entry(position_var)
        return position_var, position_label, position_entry

    def position_var(self) -> tk.DoubleVar:
        return tk.DoubleVar(value=0)

    def position_label(self, text: str) -> tk.Label:
        return tk.Label(self.frame, text=text, width=17, anchor=tk.W, font=BOLD_FONT)

    def position_entry(self, textvar: tk.DoubleVar) -> tk.Entry:
        return tk.Entry(self.frame, textvariable=textvar, font=FONT)

    @staticmethod
    def changed_values(new_data: dict, current_data: dict) -> dict:
        return {key: new_data[key] for key, current_value in current_data.items() if new_data[key] != current_value}

    @staticmethod
    def verify_positions(positions: dict) -> bool:
        for key, val in positions.items():
            if key == "a" and (val > 45 or val < -45):
                return False
            elif val > 25 or val < -25:
                return False
        return True

    @staticmethod
    def change_position_scale(positions: dict) -> dict:
        return {key: val + 45 if key == "a" else val + 25 for key, val in positions.items()}


class DialogBox:
    def __init__(self, master: tk.Toplevel, title: str, message: str):
        self.master = master
        self.frame = tk.Frame(master)
        self.master.title(title)
        self.master.geometry("")
        self.master.resizable(False, False)
        self.label = tk.Label(self.frame, text=message, font=FONT).pack(expand=1)
        self.frame.pack()


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
