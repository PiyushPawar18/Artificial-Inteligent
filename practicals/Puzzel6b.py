import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import heapq
import threading

class PuzzleApp:
    def __init__(self, root, size):
        self.size = size
        self.tile_size = 400 // size
        self.tiles = [i for i in range(1, size*size)] + [0]
        self.empty_pos = self.tiles.index(0)
        self.move_count = 0  # Initialize move counter
        
        self.root = root
        self.root.title(f"{size}x{size} Puzzle")
        
        self.canvas = tk.Canvas(root, width=self.tile_size*size, height=self.tile_size*size)
        self.canvas.pack()

        self.info_label = tk.Label(root, text=f"Moves: {self.move_count}")
        self.info_label.pack()

        self.create_widgets()
        self.shuffle_tiles()
        self.draw_board()

    def create_widgets(self):
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.solve_button = tk.Button(self.root, text="Solve", command=self.start_solving)
        self.solve_button.pack()

    def shuffle_tiles(self):
        random.shuffle(self.tiles)
        self.empty_pos = self.tiles.index(0)
        while not self.is_solvable():
            random.shuffle(self.tiles)
            self.empty_pos = self.tiles.index(0)

    def draw_board(self):
        self.canvas.delete("all")
        colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightgoldenrodyellow', 'lightpink', 'lightcyan', 'lightgray', 'lightseagreen', 'lightsteelblue']
        
        for i, tile in enumerate(self.tiles):
            row = i // self.size
            col = i % self.size
            x1, y1 = col * self.tile_size, row * self.tile_size
            x2, y2 = x1 + self.tile_size, y1 + self.tile_size
            if tile != 0:
                color = colors[(tile - 1) % len(colors)]  # Assign color based on tile number
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                self.canvas.create_text(x1 + self.tile_size // 2, y1 + self.tile_size // 2, text=str(tile), font=('Arial', 24))
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')

    def on_click(self, event):
        col = event.x // self.tile_size
        row = event.y // self.tile_size
        clicked_pos = row * self.size + col
        
        if self.is_adjacent(clicked_pos, self.empty_pos):
            self.tiles[self.empty_pos], self.tiles[clicked_pos] = self.tiles[clicked_pos], self.tiles[self.empty_pos]
            self.empty_pos = clicked_pos
            self.move_count += 1  # Increment move counter
            self.info_label.config(text=f"Moves: {self.move_count}")  # Update move count display
            self.draw_board()
            if self.is_solved():
                messagebox.showinfo("Congratulations!", f"You solved the puzzle in {self.move_count} moves!")

    def is_adjacent(self, pos1, pos2):
        row1, col1 = pos1 // self.size, pos1 % self.size
        row2, col2 = pos2 // self.size, pos2 % self.size
        return abs(row1 - row2) + abs(col1 - col2) == 1

    def is_solved(self):
        return self.tiles == list(range(1, self.size*self.size)) + [0]

    def is_solvable(self):
        inversions = 0
        one_d_tiles = [tile for tile in self.tiles if tile != 0]
        for i in range(len(one_d_tiles)):
            for j in range(i + 1, len(one_d_tiles)):
                if one_d_tiles[i] > one_d_tiles[j]:
                    inversions += 1
        if self.size % 2 == 0:  # Even grid size
            empty_row_from_bottom = self.size - (self.empty_pos // self.size + 1)
            return (inversions + empty_row_from_bottom) % 2 == 0
        return inversions % 2 == 0

    def start_solving(self):
        self.solve_thread = threading.Thread(target=self.solve_puzzle)
        self.solve_thread.start()

    def solve_puzzle(self):
        initial_state = tuple(self.tiles)
        solution = self.a_star_search(initial_state)
        if solution is None:
            self.show_message("Solve", "No solution exists.")
        else:
            self.animate_solution(solution)

    def a_star_search(self, start_state):
        goal_state = tuple(list(range(1, self.size*self.size)) + [0])
        frontier = []
        heapq.heappush(frontier, (0, start_state, []))
        explored = set()
        explored.add(start_state)
        
        while frontier:
            _, current_state, path = heapq.heappop(frontier)
            if current_state == goal_state:
                return path
            
            current_index = current_state.index(0)
            current_row, current_col = divmod(current_index, self.size)
            
            for dx, dy, move in [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]:
                new_row, new_col = current_row + dx, current_col + dy
                if 0 <= new_row < self.size and 0 <= new_col < self.size:
                    new_index = new_row * self.size + new_col
                    new_state = list(current_state)
                    new_state[current_index], new_state[new_index] = new_state[new_index], new_state[current_index]
                    new_state_tuple = tuple(new_state)
                    if new_state_tuple not in explored:
                        new_path = path + [(current_index, new_index)]
                        priority = len(new_path) + self.heuristic(new_state_tuple)
                        heapq.heappush(frontier, (priority, new_state_tuple, new_path))
                        explored.add(new_state_tuple)
        return None

    def heuristic(self, state):
        distance = 0
        for i, tile in enumerate(state):
            if tile != 0:
                target_row, target_col = divmod(tile - 1, self.size)
                current_row, current_col = divmod(i, self.size)
                distance += abs(target_row - current_row) + abs(target_col - current_col)
        return distance

    def animate_solution(self, solution):
        for step in solution:
            empty_index, swap_index = step
            self.tiles[empty_index], self.tiles[swap_index] = self.tiles[swap_index], self.tiles[empty_index]
            self.empty_pos = swap_index
            self.draw_board()
            self.root.update()
            self.root.after(300)  # Pause for 300 ms between moves
        self.show_message("Solve", "Puzzle solved!")

    def show_message(self, title, message):
        self.root.after(0, lambda: messagebox.showinfo(title, message))

def main():
    while True:
        try:
            size = simpledialog.askinteger("Input", "Enter the board size", minvalue=2)
            if size is None:
                return
            if size <= 1:
                raise ValueError("Board size must be greater than 1.")
            root = tk.Tk()
            app = PuzzleApp(root, size)
            root.mainloop()
            break
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()
