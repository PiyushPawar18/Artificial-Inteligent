import tkinter as tk

class WaterJugApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Jug Solver")

        # Initialize jug capacities and current amounts
        self.jug1_capacity = 0
        self.jug2_capacity = 0
        self.jug1_amount = 0
        self.jug2_amount = 0
        
        # Create widgets
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

        self.button_solve = tk.Button(root, text="Solve", command=self.setup_jugs)
        self.button_solve.grid(row=3, column=0, columnspan=2, pady=10)

        self.canvas = tk.Canvas(root, width=500, height=300, bg="white")
        self.canvas.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.jug1_rect = None
        self.jug2_rect = None
        self.jug1_label = None
        self.jug2_label = None

        self.setup_jugs()

    def setup_jugs(self):
        try:
            self.jug1_capacity = int(self.entry_jug1.get())
            self.jug2_capacity = int(self.entry_jug2.get())
            self.desired_amount = int(self.entry_fill.get())
        except ValueError:
            self.show_error("Please enter valid numbers.")
            return

        self.jug1_amount = 0
        self.jug2_amount = 0

        self.canvas.delete("all")
        self.draw_jugs()

    def draw_jugs(self):
        # Jug 1
        self.jug1_rect = self.canvas.create_rectangle(50, 50, 150, 250, fill="lightblue", outline="black")
        self.jug1_label = self.canvas.create_text(100, 20, text=f"Jug 1 ({self.jug1_capacity}L)", fill="black")

        # Jug 2
        self.jug2_rect = self.canvas.create_rectangle(250, 50, 350, 250, fill="lightgreen", outline="black")
        self.jug2_label = self.canvas.create_text(300, 20, text=f"Jug 2 ({self.jug2_capacity}L)", fill="black")

        self.update_jug_status()

    def update_jug_status(self):
        self.canvas.delete("status")

        # Update Jug 1
        self.canvas.create_rectangle(50, 250 - (200 * self.jug1_amount / self.jug1_capacity),
                                     150, 250, fill="blue", outline="black", tags="status")
        self.canvas.create_text(100, 270, text=f"Jug 1: {self.jug1_amount}/{self.jug1_capacity}L", tags="status")

        # Update Jug 2
        self.canvas.create_rectangle(250, 250 - (200 * self.jug2_amount / self.jug2_capacity),
                                     350, 250, fill="green", outline="black", tags="status")
        self.canvas.create_text(300, 270, text=f"Jug 2: {self.jug2_amount}/{self.jug2_capacity}L", tags="status")

    def show_error(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_label = tk.Label(error_window, text=message)
        error_label.pack(padx=20, pady=20)
        ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterJugApp(root)
    root.mainloop()
