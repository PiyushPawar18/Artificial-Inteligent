import tkinter as tk
import math

# Game configuration
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
BALL_RADIUS = 20
BULLET_RADIUS = 5
GUN_RADIUS = 50
ROTATION_SPEED = 0.05
BULLET_SPEED = 10
POINTS_TO_WIN = 3
MAX_BULLETS = 3
MAX_REFLECTIONS = 3

# Box configuration
BOX_WIDTH = 700
BOX_HEIGHT = 500
BOX_X = (CANVAS_WIDTH - BOX_WIDTH) // 2
BOX_Y = (CANVAS_HEIGHT - BOX_HEIGHT) // 2

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack()

        self.user1_points = 0
        self.user2_points = 0
        self.user1_gun_angle = 0
        self.user2_gun_angle = 0

        # Create the box
        self.box = self.canvas.create_rectangle(BOX_X, BOX_Y, BOX_X + BOX_WIDTH, BOX_Y + BOX_HEIGHT, outline="white")

        # Create balls for each user
        self.user1_ball = self.create_ball(BOX_X + BOX_WIDTH // 4, BOX_Y + BOX_HEIGHT // 2, "red")
        self.user2_ball = self.create_ball(BOX_X + 3 * BOX_WIDTH // 4, BOX_Y + BOX_HEIGHT // 2, "blue")

        self.user1_gun = self.create_gun(BOX_X + BOX_WIDTH // 4, BOX_Y + BOX_HEIGHT // 2)
        self.user2_gun = self.create_gun(BOX_X + 3 * BOX_WIDTH // 4, BOX_Y + BOX_HEIGHT // 2)

        self.user1_bullets = []
        self.user2_bullets = []

        # Display scores
        self.score_display = self.canvas.create_text(CANVAS_WIDTH // 2, 50, text=self.get_score_text(), fill="white", font=("Helvetica", 24))

        # Bind keys to fire bullets
        self.root.bind("s", self.fire_bullet_user1)
        self.root.bind("k", self.fire_bullet_user2)

        self.update_game()

    def create_ball(self, x, y, color):
        return self.canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill=color)

    def create_gun(self, cx, cy):
        gun_x = cx + GUN_RADIUS * math.cos(0)
        gun_y = cy + GUN_RADIUS * math.sin(0)
        return self.canvas.create_line(cx, cy, gun_x, gun_y, fill="white", width=5)

    def rotate_guns(self):
        self.user1_gun_angle += ROTATION_SPEED
        self.user2_gun_angle -= ROTATION_SPEED

        self.update_gun_position(self.user1_gun, BOX_X + BOX_WIDTH // 4, BOX_Y + BOX_HEIGHT // 2, self.user1_gun_angle)
        self.update_gun_position(self.user2_gun, BOX_X + 3 * BOX_WIDTH // 4, BOX_Y + BOX_HEIGHT // 2, self.user2_gun_angle)

    def update_gun_position(self, gun, cx, cy, angle):
        gun_x = cx + GUN_RADIUS * math.cos(angle)
        gun_y = cy + GUN_RADIUS * math.sin(angle)
        self.canvas.coords(gun, cx, cy, gun_x, gun_y)

    def fire_bullet_user1(self, event):
        if len(self.user1_bullets) < MAX_BULLETS:
            gun_coords = self.canvas.coords(self.user1_gun)
            bullet_x = gun_coords[2]
            bullet_y = gun_coords[3]
            bullet_id = self.canvas.create_oval(bullet_x - BULLET_RADIUS, bullet_y - BULLET_RADIUS,
                                                bullet_x + BULLET_RADIUS, bullet_y + BULLET_RADIUS,
                                                fill="purple")
            self.user1_bullets.append({
                'id': bullet_id,
                'direction_x': math.cos(self.user1_gun_angle) * BULLET_SPEED,
                'direction_y': math.sin(self.user1_gun_angle) * BULLET_SPEED,
                'reflections': 0
            })

    def fire_bullet_user2(self, event):
        if len(self.user2_bullets) < MAX_BULLETS:
            gun_coords = self.canvas.coords(self.user2_gun)
            bullet_x = gun_coords[2]
            bullet_y = gun_coords[3]
            bullet_id = self.canvas.create_oval(bullet_x - BULLET_RADIUS, bullet_y - BULLET_RADIUS,
                                                bullet_x + BULLET_RADIUS, bullet_y + BULLET_RADIUS,
                                                fill="yellow")
            self.user2_bullets.append({
                'id': bullet_id,
                'direction_x': math.cos(self.user2_gun_angle) * BULLET_SPEED,
                'direction_y': math.sin(self.user2_gun_angle) * BULLET_SPEED,
                'reflections': 0
            })

    def move_bullets(self):
        for bullet in self.user1_bullets[:]:
            self.move_bullet(bullet, self.user1_bullets)

        for bullet in self.user2_bullets[:]:
            self.move_bullet(bullet, self.user2_bullets)

    def move_bullet(self, bullet, bullet_list):
        self.canvas.move(bullet['id'], bullet['direction_x'], bullet['direction_y'])
        bullet_coords = self.canvas.coords(bullet['id'])

        # Reflect the bullet off the box's walls up to MAX_REFLECTIONS
        if bullet_coords[0] <= BOX_X or bullet_coords[2] >= BOX_X + BOX_WIDTH:
            if bullet['reflections'] < MAX_REFLECTIONS:
                bullet['direction_x'] = -bullet['direction_x']
                bullet['reflections'] += 1
        if bullet_coords[1] <= BOX_Y or bullet_coords[3] >= BOX_Y + BOX_HEIGHT:
            if bullet['reflections'] < MAX_REFLECTIONS:
                bullet['direction_y'] = -bullet['direction_y']
                bullet['reflections'] += 1

        # If the bullet goes out of the canvas, remove it
        if bullet_coords[0] <= 0 or bullet_coords[2] >= CANVAS_WIDTH or bullet_coords[1] <= 0 or bullet_coords[3] >= CANVAS_HEIGHT:
            self.remove_bullet(bullet, bullet_list)
        else:
            self.check_collision(bullet, bullet_list)

    def check_collision(self, bullet, bullet_list):
        bullet_coords = self.canvas.coords(bullet['id'])
        bullet_center_x = (bullet_coords[0] + bullet_coords[2]) / 2
        bullet_center_y = (bullet_coords[1] + bullet_coords[3]) / 2

        user1_ball_coords = self.canvas.coords(self.user1_ball)
        user2_ball_coords = self.canvas.coords(self.user2_ball)

        if self.is_collision(bullet_center_x, bullet_center_y, user2_ball_coords):
            self.user1_points += 1
            self.update_score()
            self.remove_bullet(bullet, bullet_list)

        elif self.is_collision(bullet_center_x, bullet_center_y, user1_ball_coords):
            self.user2_points += 1
            self.update_score()
            self.remove_bullet(bullet, bullet_list)

    def is_collision(self, bullet_x, bullet_y, ball_coords):
        ball_center_x = (ball_coords[0] + ball_coords[2]) / 2
        ball_center_y = (ball_coords[1] + ball_coords[3]) / 2
        distance = math.sqrt((bullet_x - ball_center_x) ** 2 + (bullet_y - ball_center_y) ** 2)
        return distance < (BALL_RADIUS + BULLET_RADIUS)

    def remove_bullet(self, bullet, bullet_list):
        self.canvas.delete(bullet['id'])
        bullet_list.remove(bullet)

    def update_score(self):
        self.canvas.itemconfig(self.score_display, text=self.get_score_text())
        if self.user1_points == POINTS_TO_WIN:
            self.canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text="User 1 Wins!", fill="white", font=("Helvetica", 24))
            self.end_game()
        elif self.user2_points == POINTS_TO_WIN:
            self.canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text="User 2 Wins!", fill="white", font=("Helvetica", 24))
            self.end_game()

    def get_score_text(self):
        return f"User 1: Points {self.user1_points}  |  User 2: Points {self.user2_points}"

    def end_game(self):
        self.root.unbind("s")
        self.root.unbind("k")
        self.root.after_cancel(self.animation)

    def update_game(self):
        self.rotate_guns()
        self.move_bullets()
        self.animation = self.root.after(50, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
