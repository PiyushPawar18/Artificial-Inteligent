import tkinter as tk
from tkinter import messagebox

class TowerOfHanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi")

        self.num_disks = 0
        self.poles = {'A': [], 'B': [], 'C': []}
        self.initial_poles = {'A': [], 'B': [], 'C': []}  # Store initial state
        self.move_count = 0  # Move counter

        # Create canvas
        self.canvas = tk.Canvas(root, width=600, height=300, bg='white')
        self.canvas.pack()

        # Draw poles
        self.pole_positions = {'A': (100, 200), 'B': (300, 200), 'C': (500, 200)}
        self.draw_poles()

        # Create input and buttons
        self.label_disks = tk.Label(root, text="Number of Disks:")
        self.label_disks.pack(padx=10, pady=5)

        self.entry_disks = tk.Entry(root)
        self.entry_disks.pack(padx=10, pady=5)

        self.button_setup = tk.Button(root, text="Setup", command=self.setup)
        self.button_setup.pack(padx=10, pady=5)

        self.button_solve = tk.Button(root, text="Solve", command=self.solve)
        self.button_solve.pack(padx=10, pady=5)

        self.button_reset = tk.Button(root, text="Reset", command=self.reset)
        self.button_reset.pack(padx=10, pady=5)

        self.status = tk.Label(root, text="")
        self.status.pack(padx=10, pady=5)

        self.move_label = tk.Label(root, text="Moves: 0")
        self.move_label.pack(padx=10, pady=5)

        # Set up variables for drag and drop
        self.selected_disk = None
        self.selected_pole = None

        # Colors for the disks
        self.disk_colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'brown']

    def draw_poles(self):
        self.canvas.delete("all")
        for pole, pos in self.pole_positions.items():
            x, y = pos
            self.canvas.create_line(x, y - 150, x, y + 50, width=5)
            self.canvas.create_text(x, y + 70, text=pole, font=('Arial', 16))

    def draw_disks(self):
        self.canvas.delete("disks")
        for pole, disks in self.poles.items():
            x, y = self.pole_positions[pole]
            for i, disk in enumerate(disks):
                disk_width = 50 + disk * 30
                color = self.disk_colors[disk % len(self.disk_colors)]  # Use different colors
                self.canvas.create_rectangle(x - disk_width // 2, y - 30 * (i + 1),
                                             x + disk_width // 2, y - 30 * i,
                                             fill=color, outline='black', tags="disks")
                self.canvas.create_text(x, y - 30 * (i + 1) + 15, text=str(disk), tags="disks")

    def setup(self):
        try:
            self.num_disks = int(self.entry_disks.get())
            if self.num_disks <= 0:
                raise ValueError
            self.poles = {'A': list(range(self.num_disks, 0, -1)), 'B': [], 'C': []}
            self.initial_poles = {'A': list(range(self.num_disks, 0, -1)), 'B': [], 'C': []}  # Store initial state
            self.move_count = 0  # Reset move counter
            self.update_move_label()
            self.draw_poles()
            self.draw_disks()
            self.status.config(text="Setup complete. Click on disks to move them.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for the number of disks.")

    def solve(self):
        if self.num_disks == 0:
            messagebox.showerror("Error", "Setup is required before solving.")
            return
        self.status.config(text="Solving...")
        self.move_count = 0  # Reset move counter
        moves = []
        self.moveTower(self.num_disks, 'A', 'C', 'B', moves)
        self.perform_moves(moves)
        self.status.config(text="Solved!")

    def moveTower(self, height, fromPole, toPole, withPole, moves):
        if height >= 1:
            self.moveTower(height - 1, fromPole, withPole, toPole, moves)
            moves.append((fromPole, toPole))
            self.moveTower(height - 1, withPole, toPole, fromPole, moves)

    def perform_moves(self, moves):
        for move in moves:
            from_pole, to_pole = move
            disk = self.poles[from_pole].pop()
            self.poles[to_pole].append(disk)
            self.move_count += 1
            self.update_move_label()
            self.draw_disks()
            self.root.update()
            self.root.after(500)  # Pause for 500 ms

    def update_move_label(self):
        self.move_label.config(text=f"Moves: {self.move_count}")

    def reset(self):
        if self.num_disks == 0:
            messagebox.showerror("Error", "Setup is required before resetting.")
            return
        self.poles = self.initial_poles.copy()  # Reset to initial state
        self.move_count = 0  # Reset move counter
        self.update_move_label()
        self.draw_disks()
        self.status.config(text="Puzzle reset. You can start again.")

    def on_click(self, event):
        x, y = event.x, event.y
        for pole, pos in self.pole_positions.items():
            pole_x, pole_y = pos
            if abs(x - pole_x) < 50 and pole_y - 150 < y < pole_y:
                if self.selected_disk is None:
                    if self.poles[pole]:
                        self.selected_disk = self.poles[pole].pop()
                        self.selected_pole = pole
                else:
                    if not self.poles[pole] or self.selected_disk < self.poles[pole][-1]:
                        self.poles[pole].append(self.selected_disk)
                        self.selected_disk = None
                        self.selected_pole = None
                        self.move_count += 1  # Increment move count on drop
                        self.update_move_label()
                        if self.check_win():
                            self.status.config(text="Congratulations! You solved the puzzle.")
                            messagebox.showinfo("You Win!", "Congratulations! You have solved the puzzle.")
                    else:
                        # Invalid move, put the disk back
                        self.poles[self.selected_pole].append(self.selected_disk)
                        self.selected_disk = None
                        self.selected_pole = None
                self.draw_disks()

    def check_win(self):
        return len(self.poles['C']) == self.num_disks

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoiGUI(root)
    root.bind("<Button-1>", app.on_click)
    root.mainloop()
