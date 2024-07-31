import tkinter as tk
from tkinter import messagebox

def dfs_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next_node in graph[start] - set(path):
        yield from dfs_paths(graph, next_node, goal, path + [next_node])

class DFSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DFS Path Finder")
        
        self.graph = {
            'A': {'B', 'C'},
            'B': {'A', 'D', 'E'},
            'C': {'A', 'F'},
            'D': {'B'},
            'E': {'B', 'F'},
            'F': {'C', 'E'}
        }
        
        self.create_widgets()

    def create_widgets(self):
        self.start_label = tk.Label(self.root, text="Start Node:")
        self.start_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.start_entry = tk.Entry(self.root)
        self.start_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.goal_label = tk.Label(self.root, text="Goal Node:")
        self.goal_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.goal_entry = tk.Entry(self.root)
        self.goal_entry.grid(row=1, column=1, padx=10, pady=10)
        
        self.find_paths_button = tk.Button(self.root, text="Find Paths", command=self.find_paths)
        self.find_paths_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.paths_text = tk.Text(self.root, height=10, width=40)
        self.paths_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def find_paths(self):
        start = self.start_entry.get().strip().upper()
        goal = self.goal_entry.get().strip().upper()
        
        if start not in self.graph or goal not in self.graph:
            messagebox.showerror("Error", "Invalid start or goal node.")
            return
        
        paths = list(dfs_paths(self.graph, start, goal))
        
        self.paths_text.delete('1.0', tk.END)
        if paths:
            for path in paths:
                self.paths_text.insert(tk.END, " -> ".join(path) + "\n")
        else:
            self.paths_text.insert(tk.END, "No paths found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DFSApp(root)
    root.mainloop()

