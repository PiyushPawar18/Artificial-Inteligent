import tkinter as tk
import random
import time

# Initialize the main window
root = tk.Tk()
root.title("Football Game")
root.geometry("600x400")

# Variables to keep track of the score
goals = 0
blocks = 0

# Create labels and buttons
info_label = tk.Label(root, text="Choose your shot: Left, Center, or Right", font=("Arial", 14))
info_label.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.pack(pady=20)

score_label = tk.Label(root, text=f"Goals: {goals} | Blocks: {blocks}", font=("Arial", 16))
score_label.pack(pady=20)

canvas = tk.Canvas(root, width=400, height=200)
canvas.pack()

# Draw the goal area
goal_area = canvas.create_rectangle(50, 50, 350, 150, outline="black", width=3)
ball = canvas.create_oval(180, 180, 220, 220, fill="black")
goalkeeper = canvas.create_rectangle(180, 50, 220, 100, fill="blue")

def reset_game():
    global goals, blocks
    goals = 0
    blocks = 0
    update_score()
    result_label.config(text="")
    canvas.coords(ball, 180, 180, 220, 220)
    canvas.coords(goalkeeper, 180, 50, 220, 100)

def update_score():
    score_label.config(text=f"Goals: {goals} | Blocks: {blocks}")

def animate_ball(goal_x):
    for i in range(10):
        canvas.move(ball, (goal_x - 200) / 10, -13)
        root.update()
        time.sleep(0.05)

def animate_goalkeeper(gk_x):
    current_pos = canvas.coords(goalkeeper)
    move_x = (gk_x - current_pos[0]) / 10  # Move goalkeeper smoothly to the chosen side
    for i in range(10):
        canvas.move(goalkeeper, move_x, 0)
        root.update()
        time.sleep(0.05)

def shoot(direction):
    global goals, blocks
    
    # Goalkeeper randomly chooses a side
    goalkeeper_choice = random.choice(["Left", "Center", "Right"])
    
    # Determine ball and goalkeeper positions
    if direction == "Left":
        goal_x = 70
    elif direction == "Center":
        goal_x = 200
    else:  # "Right"
        goal_x = 330
    
    if goalkeeper_choice == "Left":
        gk_x = 70
    elif goalkeeper_choice == "Center":
        gk_x = 200
    else:  # "Right"
        gk_x = 330
    
    animate_goalkeeper(gk_x)
    animate_ball(goal_x)
    
    if direction == goalkeeper_choice:
        result_label.config(text=f"Goalkeeper chose {goalkeeper_choice}. Shot Blocked!", fg="red")
        blocks += 1
    else:
        result_label.config(text=f"Goalkeeper chose {goalkeeper_choice}. Goal!", fg="green")
        goals += 1

    update_score()
    reset_ball()

def reset_ball():
    canvas.coords(ball, 180, 180, 220, 220)
    canvas.coords(goalkeeper, 180, 50, 220, 100)

# Create buttons for user to choose
left_button = tk.Button(root, text="Left", command=lambda: shoot("Left"), width=10)
left_button.pack(side="left", padx=20)

center_button = tk.Button(root, text="Center", command=lambda: shoot("Center"), width=10)
center_button.pack(side="left", padx=20)

right_button = tk.Button(root, text="Right", command=lambda: shoot("Right"), width=10)
right_button.pack(side="left", padx=20)

reset_button = tk.Button(root, text="Reset", command=reset_game, width=10)
reset_button.pack(side="left", padx=20)

# Start the main loop
root.mainloop()
