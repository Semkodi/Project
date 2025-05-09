import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class NumberGuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Zahlenratespiel")
        self.master.geometry("400x200")
        self.master.resizable(False, False)
        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding=20)
        frame.pack(expand=True, fill="both")

        self.label = ttk.Label(frame, text="Ich denke an eine Zahl zwischen 1 und 100.", font=("Segoe UI", 12, "bold"))
        self.label.pack(pady=(0, 15))

        entry_frame = ttk.Frame(frame)
        entry_frame.pack(pady=5)

        self.entry = ttk.Entry(entry_frame, width=10, font=("Segoe UI", 12))
        self.entry.pack(side="left")
        self.entry.focus_set()

        self.submit_button = ttk.Button(entry_frame, text="Raten", bootstyle="success", command=self.check_guess)
        self.submit_button.pack(side="left", padx=10)

        self.attempts_label = ttk.Label(frame, text="", font=("Segoe UI", 10))
        self.attempts_label.pack(pady=5)

        self.result_label = ttk.Label(frame, text="", font=("Segoe UI", 11, "italic"), bootstyle="info")
        self.result_label.pack(pady=10)

        self.play_again_button = ttk.Button(frame, text="Nochmal spielen", bootstyle="info", command=self.start_new_game)
        self.play_again_button.pack(pady=10)
        self.play_again_button.pack_forget()  # Erst unsichtbar

        self.master.bind("<Return>", lambda event: self.check_guess())

    def start_new_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10
        self.attempts_label.config(text=f"Versuche übrig: {self.max_attempts}")
        self.result_label.config(text="", bootstyle="info")
        self.entry.config(state="normal")
        self.submit_button.config(state="normal")
        self.play_again_button.pack_forget()
        self.entry.delete(0, "end")
        self.entry.focus_set()

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            attempts_left = self.max_attempts - self.attempts

            if guess == self.secret_number:
                self.result_label.config(text=f"Glückwunsch! Die Zahl war {self.secret_number}.", bootstyle="success")
                self.end_game(win=True)
            elif guess < self.secret_number:
                self.result_label.config(text="Zu niedrig!", bootstyle="warning")
            else:
                self.result_label.config(text="Zu hoch!", bootstyle="danger")

            if attempts_left == 0 and guess != self.secret_number:
                self.result_label.config(text=f"Game Over! Die Zahl war {self.secret_number}.", bootstyle="danger")
                self.end_game(win=False)
            else:
                self.attempts_label.config(text=f"Versuche übrig: {attempts_left}")

            self.entry.delete(0, "end")
            self.entry.focus_set()

        except ValueError:
            messagebox.showerror("Fehler", "Bitte gib eine gültige Zahl ein.")
            self.entry.delete(0, "end")
            self.entry.focus_set()

    def end_game(self, win):
        self.entry.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.play_again_button.pack(pady=10)

if __name__ == "__main__":
    root = ttk.Window(themename="cyborg")
    game = NumberGuessingGame(root)
    root.mainloop()
