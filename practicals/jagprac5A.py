import tkinter as tk

def pour(jug1, jug2, max1, max2, fill, visited, moves):
    if jug1 == fill or jug2 == fill:
        moves.append((jug1, jug2))
        return True

    if (jug1, jug2) in visited:
        return False

    visited.add((jug1, jug2))
    moves.append((jug1, jug2))

    # Fill Jug1
    if pour(max1, jug2, max1, max2, fill, visited, moves):
        return True
    # Fill Jug2
    if pour(jug1, max2, max1, max2, fill, visited, moves):
        return True
    # Empty Jug1
    if pour(0, jug2, max1, max2, fill, visited, moves):
        return True
    # Empty Jug2
    if pour(jug1, 0, max1, max2, fill, visited, moves):
        return True
    # Pour Jug1 to Jug2
    if jug1 + jug2 <= max2:
        if pour(0, jug1 + jug2, max1, max2, fill, visited, moves):
            return True
    else:
        if pour(jug1 - (max2 - jug2), max2, max1, max2, fill, visited, moves):
            return True
    # Pour Jug2 to Jug1
    if jug1 + jug2 <= max1:
        if pour(jug1 + jug2, 0, max1, max2, fill, visited, moves):
            return True
    else:
        if pour(max1, jug2 - (max1 - jug1), max1, max2, fill, visited, moves):
            return True

    moves.pop()
    return False

class WaterJugApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Jug Solver")

        self.label_jug1 = tk.Label(root, text="Jug 1 Capacity:")
        self.label_jug1.grid(row=0, column=0, padx=10, pady=10)

        self.entry_jug1 = tk.Entry(root)
        self.entry_jug1.grid(row=0, column=1, padx=10, pady=10)

        self.label_jug2 = tk.Label(root, text="Jug 2 Capacity:")
        self.label_jug2.grid(row=1, column=0, padx=10, pady=10)

        self.entry_jug2 = tk.Entry(root)
        self.entry_jug2.grid(row=1, column=1, padx=10, pady=10)

        self.label_fill = tk.Label(root, text="Desired Amount:")
        self.label_fill.grid(row=2, column=0, padx=10, pady=10)

        self.entry_fill = tk.Entry(root)
        self.entry_fill.grid(row=2, column=1, padx=10, pady=10)

        self.button_solve = tk.Button(root, text="Solve", command=self.solve)
        self.button_solve.grid(row=3, column=0, columnspan=2, pady=10)

        self.solution_text = tk.Text(root, height=20, width=50)
        self.solution_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def solve(self):
        jug1_capacity = int(self.entry_jug1.get())
        jug2_capacity = int(self.entry_jug2.get())
        desired_amount = int(self.entry_fill.get())

        visited = set()
        moves = []
        
        self.solution_text.delete(1.0, tk.END)
        
        if pour(0, 0, jug1_capacity, jug2_capacity, desired_amount, visited, moves):
            for i, move in enumerate(moves):
                self.solution_text.insert(tk.END, f"Step {i+1}: Jug1 = {move[0]}, Jug2 = {move[1]}\n")
        else:
            self.solution_text.insert(tk.END, "No solution found")

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterJugApp(root)
    root.mainloop()
