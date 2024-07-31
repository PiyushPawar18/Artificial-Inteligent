import tkinter as tk
from tkinter import messagebox
import configparser

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        self.board = [""] * 9  # Empty board
        self.current_player = "X"  # Player X starts
        self.game_over = False

        self.create_ui()

    def create_ui(self):
        self.buttons = []
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)
        
        for i in range(9):
            button = tk.Button(self.board_frame, text="", font=("Arial", 40), width=5, height=2,
                               command=lambda i=i: self.make_move(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def make_move(self, index):
        if self.board[index] == "" and not self.game_over:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner(self.current_player):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.game_over = True
                return

            if "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.game_over = True
                return

            self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
