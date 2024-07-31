import tkinter as tk
from tkinter import ttk

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]  # Queue initialized with the start node and its path
    while queue:
        (vertex, path) = queue.pop(0)  # Dequeue the first element
        for next_node in graph[vertex] - set(path):  # Explore neighbors not yet in the path
            if next_node == goal:
                yield path + [next_node]  # Yield the path if goal is reached
            else:
                queue.append((next_node, path + [next_node]))  # Enqueue the new path

# Example graph
graph = {
    'A': {'B', 'C'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'C', 'E'}
}

class BFSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BFS Path Finder")
        
        self.label_start = tk.Label(root, text="Start Node:")
        self.label_start.grid(row=0, column=0, padx=10, pady=10)
        
        self.entry_start = tk.Entry(root)
        self.entry_start.grid(row=0, column=1, padx=10, pady=10)
        
        self.label_goal = tk.Label(root, text="Goal Node:")
        self.label_goal.grid(row=1, column=0, padx=10, pady=10)
        
        self.entry_goal = tk.Entry(root)
        self.entry_goal.grid(row=1, column=1, padx=10, pady=10)
        
        self.button_find_paths = tk.Button(root, text="Find Paths", command=self.find_paths)
        self.button_find_paths.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.paths_text = tk.Text(root, height=10, width=40)
        self.paths_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    def find_paths(self):
        start = self.entry_start.get()
        goal = self.entry_goal.get()
        paths = list(bfs_paths(graph, start, goal))
        
        self.paths_text.delete(1.0, tk.END)
        if paths:
            for path in paths:
                self.paths_text.insert(tk.END, f"Path: {path}\n")
        else:
            self.paths_text.insert(tk.END, "No path found")

if __name__ == "__main__":
    root = tk.Tk()
    app = BFSApp(root)
    root.mainloop()
