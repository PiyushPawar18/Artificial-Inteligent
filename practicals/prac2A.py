import tkinter as tk

class NQueenSolver:
    def __init__(self, size):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.solutions = []

    def is_safe(self, row, col):
        for i in range(col):
            if self.board[row][i]:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j]:
                return False
        for i, j in zip(range(row, self.size, 1), range(col, -1, -1)):
            if self.board[i][j]:
                return False
        return True

    def solve_nq_util(self, col):
        if col >= self.size:
            solution = []
            for i in range(self.size):
                solution.append(self.board[i][:])
            self.solutions.append(solution)
            return True

        res = False
        for i in range(self.size):
            if self.is_safe(i, col):
                self.board[i][col] = 1
                res = self.solve_nq_util(col + 1) or res
                self.board[i][col] = 0
        return res

    def solve_nq(self):
        self.solve_nq_util(0)
        return self.solutions

class NQueenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queen Solver")

        self.label_n = tk.Label(root, text="Board Size (N):")
        self.label_n.grid(row=0, column=0, padx=10, pady=10)
        
        self.entry_n = tk.Entry(root)
        self.entry_n.grid(row=0, column=1, padx=10, pady=10)
        
        self.button_solve = tk.Button(root, text="Solve", command=self.solve)
        self.button_solve.grid(row=1, column=0, columnspan=2, pady=10)

        self.solution_text = tk.Text(root, height=20, width=50)
        self.solution_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    
    def solve(self):
        n = int(self.entry_n.get())
        solver = NQueenSolver(n)
        solutions = solver.solve_nq()
        
        self.solution_text.delete(1.0, tk.END)
        if solutions:
            for sol_num, solution in enumerate(solutions, 1):
                self.solution_text.insert(tk.END, f"Solution {sol_num}:\n")
                for row in solution:
                    self.solution_text.insert(tk.END, f"{' '.join(str(e) for e in row)}\n")
                self.solution_text.insert(tk.END, "\n")
        else:
            self.solution_text.insert(tk.END, "No solution found")

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueenApp(root)
    root.mainloop()
