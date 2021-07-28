import json
import tkinter as tk
import traceback
from pathlib import Path

import appdirs
import send_data

FONT = ("calibre", 14, "normal")
BOLD_FONT = ("calibre", 14, "bold")


class MainApplication:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.report_callback_exception = self.report_callback_exception
        self.frame = tk.Frame(master)
        self.master.title("PALMS v0.7.0")
        self.master.geometry("")
        self.master.resizable(False, False)
        self.master.grid_columnconfigure(0, weight=1, uniform="spam")
        self.master.grid_columnconfigure(1, weight=1, uniform="spam")

        self.make_axis_widgets()
        self.make_buttons()

        self.settings = Settings()

        self.frame.pack()

        self.current_data = {"x": 0.0, "y": 0.0, "z": 0.0, "a": 0.0, "b": 0.0}

    def make_axis_widgets(self) -> None:
        self.x_position, self.x_label, self.x_entry = self.axis_widgets("X 0-50mm", 0)
        self.y_position, self.y_label, self.y_entry = self.axis_widgets("Y 0-50mm", 1)
        self.z_position, self.z_label, self.z_entry = self.axis_widgets("Z 0-50mm", 2)
        self.a_position, self.a_label, self.a_entry = self.axis_widgets("Rotational 0-90°", 3)
        self.b_position, self.b_label, self.b_entry = self.axis_widgets("Collimator 0-50mm", 4)

    def make_buttons(self) -> None:
        self.buttons_widget = tk.Frame(self.frame)

        self.buttons_widget.grid_columnconfigure(0, weight=2, minsize=410, uniform="spam")
        self.buttons_widget.grid_columnconfigure(1, weight=1, uniform="spam")
        self.buttons_widget.grid_columnconfigure(2, weight=1, uniform="spam")

        self.update_button = tk.Button(
            self.buttons_widget,
            text="Update",
            command=self.update,
            font=FONT,
            bg="#000000",  # black
            fg="#FFFFFF",  # white
            activeforeground="#000000",  # black
            activebackground="#FFFFFF",  # white
        )

        self.lock_button = tk.Button(
            self.buttons_widget,
            text="Lock",
            #            command=print,
            font=FONT,
            bg="#000000",  # black
            fg="#FFFFFF",  # white
            activeforeground="#000000",  # black
            activebackground="#FFFFFF",  # white
        )

        self.settings_button = tk.Button(
            self.buttons_widget,
            text="Settings",
            #            command=lambda: SettingsWindow(tk.Toplevel(self.master), self.settings),
            font=FONT,
            bg="#000000",  # black
            fg="#FFFFFF",  # white
            activeforeground="#000000",  # black
            activebackground="#FFFFFF",  # white
        )

        self.update_button.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
        self.lock_button.grid(row=0, column=1, padx=10, pady=10, sticky="nesw")
        self.settings_button.grid(row=0, column=2, padx=10, pady=10, sticky="nesw")

        self.buttons_widget.grid(row=5, columnspan=2)

    def axis_widgets(self, label_text: str, row: int):
        position_var = self.position_var()
        position_label = self.position_label(label_text).grid(row=row, column=0)
        position_entry = self.position_entry(position_var).grid(row=row, column=1)
        return position_var, position_label, position_entry

    def position_var(self) -> tk.DoubleVar:
        return tk.DoubleVar(value=0)

    def position_label(self, text: str) -> tk.Label:
        return tk.Label(self.frame, text=text, width=17, anchor=tk.W, font=BOLD_FONT)

    def position_entry(self, textvar: tk.DoubleVar) -> tk.Entry:
        return tk.Entry(self.frame, textvariable=textvar, font=FONT)

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
                send_data.send(self.changed_values(new_data, self.current_data))
            except send_data.ServerConnectionError as e:
                DialogBox(tk.Toplevel(self.master), "Error Updating Targets", e.message)
            else:
                self.current_data = new_data
        else:
            DialogBox(tk.Toplevel(self.master), "Invalid Position(s)", "One or more entered positions are invalid.")

    @staticmethod
    def changed_values(new_data: dict, current_data: dict) -> dict:
        return {key: new_data[key] for key, current_value in current_data.items() if new_data[key] != current_value}

    @staticmethod
    def verify_positions(positions: dict) -> bool:
        for key, val in positions.items():
            if key == "a" and (val > 90 or val < 0):
                return False
            if val > 50 or val < 0:
                return False
        return True

    def report_callback_exception(self, *args):
        DialogBox(
            tk.Toplevel(self.master),
            "Error",
            f"An unexpected error has occurred.\nTraceback:\n\n{''.join(traceback.format_exception(*args))}",
        )


class Settings:
    def __init__(self):
        self._settings_path = self._make_settings_path()
        with open(self._settings_path) as settings_file:
            self._state = json.load(settings_file)

    def __getitem__(self, key):
        return self._state[key]

    def __setitem__(self, key, value):
        self._state[key] = value
        with open(self._settings_path, "w") as settings_file:
            json.dump(self._state, settings_file)

    def __contains__(self, m):
        return m in self._state

    def _make_settings_path(self):
        settings_path = Path(appdirs.user_config_dir("PALMS", "RE")) / "settings.json"

        settings_path.parents[0].mkdir(parents=True, exist_ok=True)

        if not settings_path.is_file():
            settings_path.touch()
            with open(settings_path, "w") as settings_file:
                json.dump({}, settings_file)

        return settings_path

    def add_setting(self, name: str, default_state: bool) -> None:
        if name not in self:
            self[name] = default_state


class SettingsWindow:
    def __init__(self, master: tk.Toplevel, settings):
        self.master = master
        self.frame = tk.Frame(master)
        self.master.title("Settings")
        self.master.geometry("")
        self.master.resizable(False, False)

        # Make settings window grab focus so there can only be one spawned
        self.frame.focus_set()
        self.frame.grab_set()

        self.settings = settings

        self.frame.pack()

    def setting_widgets(self, name: str, row: int):
        setting_label = self.setting_label(name).grid(row=row, column=0, padx=10, pady=10)
        setting_button = self.setting_button(name).grid(row=row, column=1)
        return setting_label, setting_button

    def setting_label(self, name: str):
        return tk.Label(self.frame, text=name, font=BOLD_FONT)

    def setting_button(self, name: str):
        setting_button = tk.Button(
            self.frame, text="Turn Off" if self.settings[name] else "Turn On", font=FONT, padx=10, pady=30
        )
        setting_button.config(command=lambda: self.flip_setting(name, setting_button))
        return setting_button

    def flip_setting(self, name: str, button: tk.Button) -> None:
        self.settings[name] = not self.settings[name]
        if self.settings[name]:
            button.config(text="Turn Off")
        else:
            button.config(text="Turn On")
        DialogBox(
            tk.Toplevel(self.master),
            "Restart PALMS",
            f"Restart PALMS to {'enable' if self.settings[name] else 'disable'} {name}.",
            grab_focus=True,
        )


class DialogBox:
    def __init__(self, master: tk.Toplevel, title: str, message: str, grab_focus: bool = False):
        self.master = master
        self.frame = tk.Frame(master)
        self.master.title(title)
        self.master.geometry("")
        self.master.resizable(False, False)
        self.label = tk.Label(self.frame, text=message, font=FONT).pack(expand=1)

        if grab_focus:
            self.frame.focus_set()
            self.frame.grab_set()

        self.frame.pack()


def main():
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
