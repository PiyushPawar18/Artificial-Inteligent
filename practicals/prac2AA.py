import tkinter as tk
from tkinter import messagebox

class NQueenSolver:
    def __init__(self, size):
        self.size = size
        self.solutions = []

    def is_safe(self, board, row, col):
        for i in range(col):
            if board[row][i]:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j]:
                return False
        for i, j in zip(range(row, self.size, 1), range(col, -1, -1)):
            if board[i][j]:
                return False
        return True

    def solve_nq_util(self, board, col):
        if col >= self.size:
            solution = [row[:] for row in board]
            self.solutions.append(solution)
            return True

        res = False
        for i in range(self.size):
            if self.is_safe(board, i, col):
                board[i][col] = 1
                res = self.solve_nq_util(board, col + 1) or res
                board[i][col] = 0
        return res

    def solve_nq(self):
        board = [[0] * self.size for _ in range(self.size)]
        self.solve_nq_util(board, 0)
        return self.solutions

class NQueenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queen Solver")

        self.size = 0
        self.board = []
        self.canvas = None
        self.solutions = []
        self.current_solution_index = 0

        self.label_n = tk.Label(root, text="Board Size (N):")
        self.label_n.grid(row=0, column=0, padx=10, pady=10)
        
        self.entry_n = tk.Entry(root)
        self.entry_n.grid(row=0, column=1, padx=10, pady=10)
        
        self.button_setup = tk.Button(root, text="Setup", command=self.setup_board)
        self.button_setup.grid(row=1, column=0, columnspan=2, pady=10)

        self.button_solve = tk.Button(root, text="Solve", command=self.solve)
        self.button_solve.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.button_check = tk.Button(root, text="Check Solution", command=self.check_solution)
        self.button_check.grid(row=3, column=0, columnspan=2, pady=10)

        self.button_next = tk.Button(root, text="Next", command=self.show_next_solution, state=tk.DISABLED)
        self.button_next.grid(row=4, column=0, padx=10, pady=10)

        self.button_previous = tk.Button(root, text="Previous", command=self.show_previous_solution, state=tk.DISABLED)
        self.button_previous.grid(row=4, column=1, padx=10, pady=10)

        self.button_reset = tk.Button(root, text="Reset", command=self.reset)
        self.button_reset.grid(row=5, column=0, columnspan=2, pady=10)

        self.status = tk.Label(root, text="")
        self.status.grid(row=6, column=0, columnspan=2, pady=10)

    def setup_board(self):
        self.size = int(self.entry_n.get())
        if self.size <= 0:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for the board size.")
            return
        
        if self.canvas:
            self.canvas.destroy()
        
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg='white')
        self.canvas.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        
        self.board = [[0] * self.size for _ in range(self.size)]
        self.draw_board()
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_board(self):
        if self.canvas:
            self.canvas.delete("all")
            cell_size = 300 // self.size
            for row in range(self.size):
                for col in range(self.size):
                    x1 = col * cell_size
                    y1 = row * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size
                    color = 'white' if (row + col) % 2 == 0 else 'black'
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                    if self.board[row][col]:
                        self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill='red')

    def on_canvas_click(self, event):
        if not self.canvas:
            return
        
        cell_size = 300 // self.size
        col = event.x // cell_size
        row = event.y // cell_size

        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col]:
                self.board[row][col] = 0
            else:
                if sum(self.board[i][col] for i in range(self.size)) == 0:
                    self.board[row][col] = 1
                else:
                    messagebox.showwarning("Invalid Move", "You can only place one queen per column.")
            self.draw_board()

    def check_solution(self):
        if not self.size:
            messagebox.showerror("Error", "Setup is required before checking the solution.")
            return
        
        solver = NQueenSolver(self.size)
        solutions = solver.solve_nq()
        
        user_solution = [row[:] for row in self.board]
        if any(user_solution == sol for sol in solutions):
            self.status.config(text="Congratulations! You solved the puzzle.")
            messagebox.showinfo("You Win!", "Congratulations! You have solved the puzzle.")
        else:
            self.status.config(text="Incorrect solution. Try again.")
            messagebox.showinfo("Try Again", "The current configuration is not a valid solution.")

    def solve(self):
        if not self.size:
            messagebox.showerror("Error", "Setup is required before solving the puzzle.")
            return
        
        solver = NQueenSolver(self.size)
        self.solutions = solver.solve_nq()
        
        if self.solutions:
            self.current_solution_index = 0
            self.status.config(text=f"Found {len(self.solutions)} solution(s).")
            self.button_next.config(state=tk.NORMAL)
            self.button_previous.config(state=tk.DISABLED)
            self.draw_solution(self.solutions[self.current_solution_index])
        else:
            self.status.config(text="No solutions found.")
            self.button_next.config(state=tk.DISABLED)
            self.button_previous.config(state=tk.DISABLED)

    def draw_solution(self, solution):
        if not self.canvas:
            return

        self.canvas.delete("all")
        cell_size =300 // self.size
        for row in range(self.size):
            for col in range(self.size):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                if solution[row][col]:
                    self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill='red')

    def show_next_solution(self):
        if self.solutions and self.current_solution_index < len(self.solutions) - 1:
            self.current_solution_index += 1
            self.draw_solution(self.solutions[self.current_solution_index])
            self.button_previous.config(state=tk.NORMAL)
            if self.current_solution_index == len(self.solutions) - 1:
                self.button_next.config(state=tk.DISABLED)
        if self.current_solution_index == 0:
            self.button_previous.config(state=tk.DISABLED)

    def show_previous_solution(self):
        if self.solutions and self.current_solution_index > 0:
            self.current_solution_index -= 1
            self.draw_solution(self.solutions[self.current_solution_index])
            self.button_next.config(state=tk.NORMAL)
            if self.current_solution_index == 0:
                self.button_previous.config(state=tk.DISABLED)
        if self.current_solution_index == len(self.solutions) - 1:
            self.button_next.config(state=tk.NORMAL)

    def reset(self):
        self.size = 0
        self.board = []
        self.solutions = []
        self.current_solution_index = 0

        if self.canvas:
            self.canvas.destroy()
        
        self.canvas = None
        self.entry_n.delete(0, tk.END)
        self.status.config(text="")
        self.button_next.config(state=tk.DISABLED)
        self.button_previous.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueenApp(root)
    root.mainloop()
