import tkinter as tk
import random
import time

# Initialize the main window
root = tk.Tk()
root.title("Football Game")
root.geometry("800x500")

# Variables to keep track of the score and shots
goals = 0
blocks = 0
shots = 0
max_shots = 10  # Game ends after 10 shots

# Track the number of shots the user makes in each direction
user_shots = {"Left": 0, "Center": 0, "Right": 0}

# Load images
football_image = tk.PhotoImage(file="football360.png")
goal_image = tk.PhotoImage(file="footballnet.png")
goalkeeper_image = tk.PhotoImage(file="goalkeeper.png")  # Load the goalkeeper image

# Create labels and buttons
info_label = tk.Label(root, text="Choose your shot: Left, Center, or Right", font=("Arial", 14))
info_label.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.pack(pady=20)

score_label = tk.Label(root, text=f"Goals: {goals} | Blocks: {blocks} | Shots: {shots}/{max_shots}", font=("Arial", 16))
score_label.pack(pady=20)

canvas = tk.Canvas(root, width=800, height=400, bg="green")
canvas.pack()

# Draw the goal area and add a net image
canvas.create_image(350, 150, image=goal_image)

# Replace the ball with the football image
ball = canvas.create_image(350, 290, image=football_image)

# Create a goalkeeper image on the canvas
goalkeeper = canvas.create_image(350, 90, image=goalkeeper_image)  # Adjust the position as needed

def reset_game():
    global goals, blocks, shots, user_shots
    goals = 0
    blocks = 0
    shots = 0
    user_shots = {"Left": 0, "Center": 0, "Right": 0}  # Reset shot counts
    update_score()
    result_label.config(text="")
    canvas.coords(ball, 350, 290)
    canvas.coords(goalkeeper, 350, 90)  # Reset goalkeeper position

def update_score():
    score_label.config(text=f"Goals: {goals} | Blocks: {blocks} | Shots: {shots}/{max_shots}")

def animate_ball(goal_x):
    for i in range(10):
        canvas.move(ball, (goal_x - 350) / 10, -20)
        root.update()
        time.sleep(0.05)

def animate_goalkeeper(gk_x):
    current_pos = canvas.coords(goalkeeper)
    move_x = (gk_x - current_pos[0]) / 10  # Move goalkeeper smoothly to the chosen side
    for i in range(10):
        canvas.move(goalkeeper, move_x, 0)
        root.update()
        time.sleep(0.05)

def weighted_goalkeeper_choice():
    total_shots = sum(user_shots.values())
    
    # Assign higher weight to where the user shoots most often
    if total_shots == 0:
        return random.choice(["Left", "Center", "Right"])  # Random choice if no shots taken yet
    
    weights = {
        "Left": (user_shots["Left"] + 1) / (total_shots + 3),
        "Center": (user_shots["Center"] + 1) / (total_shots + 3),
        "Right": (user_shots["Right"] + 1) / (total_shots + 3)
    }
    
    # Randomly choose with probability based on past shots
    return random.choices(["Left", "Center", "Right"], weights=[weights["Left"], weights["Center"], weights["Right"]])[0]

def shoot(direction):
    global goals, blocks, shots
    
    if shots >= max_shots:
        result_label.config(text="Game Over! Click Reset to play again.", fg="red")
        return

    # Update the shot count for the user's direction
    user_shots[direction] += 1
    
    # Goalkeeper chooses a side based on weighted probabilities
    goalkeeper_choice = weighted_goalkeeper_choice()
    
    # Determine ball and goalkeeper positions
    goal_x = 150 if direction == "Left" else 350 if direction == "Center" else 550
    gk_x = 150 if goalkeeper_choice == "Left" else 350 if goalkeeper_choice == "Center" else 550
    
    animate_goalkeeper(gk_x)
    animate_ball(goal_x)
    
    shots += 1
    if direction == goalkeeper_choice:
        result_label.config(text=f"Goalkeeper chose {goalkeeper_choice}. Shot Blocked!", fg="red")
        blocks += 1
    else:
        result_label.config(text=f"Goalkeeper chose {goalkeeper_choice}. Goal!", fg="green")
        goals += 1

    update_score()
    reset_ball()

def reset_ball():
    canvas.coords(ball, 350, 290)
    canvas.coords(goalkeeper, 350, 90)  # Reset goalkeeper position

# Create buttons for user to choose
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

left_button = tk.Button(button_frame, text="Left", command=lambda: shoot("Left"), width=10)
left_button.grid(row=0, column=0, padx=10)

center_button = tk.Button(button_frame, text="Center", command=lambda: shoot("Center"), width=10)
center_button.grid(row=0, column=1, padx=10)

right_button = tk.Button(button_frame, text="Right", command=lambda: shoot("Right"), width=10)
right_button.grid(row=0, column=2, padx=10)

reset_button = tk.Button(root, text="Reset", command=reset_game, width=10)
reset_button.pack(pady=10)

# Start the main loop
root.mainloop()
