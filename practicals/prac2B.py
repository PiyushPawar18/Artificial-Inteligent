import tkinter as tk
from tkinter import ttk

def moveTower(height, fromPole, toPole, withPole, moves):
    if height >= 1:
        moveTower(height - 1, fromPole, withPole, toPole, moves)  # Move tower of size height-1 to auxiliary pole
        moves.append((fromPole, toPole))                          # Move the largest disk to the target pole
        moveTower(height - 1, withPole, toPole, fromPole, moves)  # Move the tower from auxiliary to target pole

class TowerOfHanoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi Solver")

        self.label_disks = tk.Label(root, text="Number of Disks:")
        self.label_disks.grid(row=0, column=0, padx=10, pady=10)

        self.entry_disks = tk.Entry(root)
        self.entry_disks.grid(row=0, column=1, padx=10, pady=10)

        self.button_solve = tk.Button(root, text="Solve", command=self.solve)
        self.button_solve.grid(row=1, column=0, columnspan=2, pady=10)

        self.solution_text = tk.Text(root, height=20, width=50)
        self.solution_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def solve(self):
        num_disks = int(self.entry_disks.get())
        moves = []
        moveTower(num_disks, "A", "B", "C", moves)
        
        self.solution_text.delete(1.0, tk.END)
        for i, move in enumerate(moves, 1):
            self.solution_text.insert(tk.END, f"Step {i}: Move disk from {move[0]} to {move[1]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoiApp(root)
    root.mainloop()
