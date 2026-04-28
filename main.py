import tkinter as tk
import random
import json
import os

SAVE_FILE = "game_data.json"

class GuessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Guess Game Pro")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.dark_mode = False

        self.load_data()
        self.create_start_screen()

    # ---------------- DATA ---------------- #
    def load_data(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                self.wins = data.get("wins", 0)
                self.losses = data.get("losses", 0)
                self.highscore = data.get("highscore", 0)
        else:
            self.wins = self.losses = self.highscore = 0

    def save_data(self):
        with open(SAVE_FILE, "w") as f:
            json.dump({
                "wins": self.wins,
                "losses": self.losses,
                "highscore": self.highscore
            }, f)

    # ---------------- START SCREEN ---------------- #
    def create_start_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text="🎯 Guess Game Pro",
                 font=("Segoe UI", 18, "bold")).pack(pady=20)

        tk.Button(frame, text="▶ Start Game",
                  command=self.create_game_screen,
                  width=20).pack(pady=10)

        tk.Button(frame, text="🌙 Toggle Theme",
                  command=self.toggle_theme,
                  width=20).pack(pady=10)

        tk.Button(frame, text="❌ Exit",
                  command=self.root.quit,
                  width=20).pack(pady=10)

    # ---------------- GAME SCREEN ---------------- #
    def create_game_screen(self):
        self.clear_screen()

        self.difficulty = tk.StringVar(value="Easy")

        top = tk.Frame(self.root)
        top.pack(pady=10)

        tk.OptionMenu(top, self.difficulty, "Easy", "Medium", "Hard").pack()

        self.instruction = tk.Label(self.root, text="")
        self.instruction.pack()

        self.entry = tk.Entry(self.root, justify="center", font=("Arial", 14))
        self.entry.pack(pady=10)

        self.entry.bind('<Return>', lambda e: self.check_guess())

        tk.Button(self.root, text="Submit", command=self.check_guess).pack()

        self.result = tk.Label(self.root, text="")
        self.result.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="")
        self.timer_label.pack()

        self.history_label = tk.Label(self.root, text="")
        self.history_label.pack()

        self.score_label = tk.Label(self.root, text="")
        self.score_label.pack(pady=10)

        tk.Button(self.root, text="🔙 Back", command=self.create_start_screen).pack(pady=5)

        self.restart_btn = tk.Button(self.root, text="Play Again", command=self.restart_game)
        self.restart_btn.pack_forget()

        self.restart_game()

    # ---------------- GAME LOGIC ---------------- #
    def set_difficulty(self):
        level = self.difficulty.get()

        if level == "Easy":
            self.max_num, self.attempts = 10, 5
        elif level == "Medium":
            self.max_num, self.attempts = 50, 7
        else:
            self.max_num, self.attempts = 100, 10

    def restart_game(self):
        self.set_difficulty()
        self.secret = random.randint(1, self.max_num)
        self.time_left = 30
        self.history = []

        self.entry.delete(0, tk.END)
        self.result.config(text="")
        self.restart_btn.pack_forget()

        self.instruction.config(text=f"Guess between 1 and {self.max_num}")
        self.update_score()
        self.run_timer()

    def run_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"⏱ {self.time_left}s")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.run_timer)
        else:
            self.end_game("⏰ Time's up!", "red")

    def check_guess(self):
        guess = self.entry.get()

        if not guess.isdigit():
            self.result.config(text="⚠ Invalid input!", fg="orange")
            return

        guess = int(guess)
        self.history.append(guess)
        self.history_label.config(text=f"Guesses: {self.history}")

        if guess == self.secret:
            self.wins += 1
            self.highscore = max(self.highscore, self.wins)
            self.end_game("🎉 Correct!", "green")
        else:
            self.attempts -= 1
            if self.attempts == 0:
                self.losses += 1
                self.end_game(f"💀 Number was {self.secret}", "red")
            else:
                self.give_hint(guess)

        self.update_score()
        self.save_data()

    def give_hint(self, guess):
        diff = abs(self.secret - guess)

        if diff <= 2:
            hint = "🔥 Very Close"
        elif diff <= 5:
            hint = "🙂 Close"
        else:
            hint = "❄ Far"

        direction = "Higher" if guess < self.secret else "Lower"

        self.result.config(text=f"{hint} | {direction} | Attempts: {self.attempts}")

    def end_game(self, msg, color):
        self.result.config(text=msg, fg=color)
        self.restart_btn.pack(pady=10)
        self.root.after_cancel(self.timer_id)

    def update_score(self):
        self.score_label.config(
            text=f"Wins: {self.wins} | Losses: {self.losses} | High Score: {self.highscore}"
        )

    # ---------------- UTIL ---------------- #
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg = "#1e1e1e" if self.dark_mode else "#f0f4f8"
        fg = "white" if self.dark_mode else "black"

        self.root.config(bg=bg)
        for widget in self.root.winfo_children():
            try:
                widget.config(bg=bg, fg=fg)
            except:
                pass


# Run
root = tk.Tk()
app = GuessGame(root)
root.mainloop()