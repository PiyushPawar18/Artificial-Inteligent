import tkinter as tk
import math

# Game configuration
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
BALL_RADIUS = 20
BULLET_RADIUS = 5
GUN_RADIUS = 50
ROTATION_SPEED = 0.05
BULLET_SPEED = 10
POINTS_TO_WIN = 3

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
        self.canvas.pack()

        self.user1_points = 0
        self.user2_points = 0

        self.user1_gun_angle = 0
        self.user2_gun_angle = 0

        # Create balls for each user
        self.user1_ball = self.create_ball(CANVAS_WIDTH//4, CANVAS_HEIGHT//2, "red")
        self.user2_ball = self.create_ball(3*CANVAS_WIDTH//4, CANVAS_HEIGHT//2, "blue")

        self.user1_gun = self.create_gun(CANVAS_WIDTH//4, CANVAS_HEIGHT//2)
        self.user2_gun = self.create_gun(3*CANVAS_WIDTH//4, CANVAS_HEIGHT//2)

        self.bullet = None

        # Bind keys to fire bullets
        self.root.bind("s", self.fire_bullet_user1)
        self.root.bind("k", self.fire_bullet_user2)

        self.update_game()

    def create_ball(self, x, y, color):
        return self.canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS,
                                       x + BALL_RADIUS, y + BALL_RADIUS, fill=color)

    def create_gun(self, cx, cy):
        gun_x = cx + GUN_RADIUS * math.cos(0)
        gun_y = cy + GUN_RADIUS * math.sin(0)
        return self.canvas.create_line(cx, cy, gun_x, gun_y, fill="white", width=5)

    def rotate_guns(self):
        self.user1_gun_angle += ROTATION_SPEED
        self.user2_gun_angle += ROTATION_SPEED

        self.update_gun_position(self.user1_gun, CANVAS_WIDTH//4, CANVAS_HEIGHT//2, self.user1_gun_angle)
        self.update_gun_position(self.user2_gun, 3*CANVAS_WIDTH//4, CANVAS_HEIGHT//2, self.user2_gun_angle)

    def update_gun_position(self, gun, cx, cy, angle):
        gun_x = cx + GUN_RADIUS * math.cos(angle)
        gun_y = cy + GUN_RADIUS * math.sin(angle)
        self.canvas.coords(gun, cx, cy, gun_x, gun_y)

    def fire_bullet_user1(self, event):
        if self.bullet is None:
            gun_coords = self.canvas.coords(self.user1_gun)
            bullet_x = gun_coords[2]
            bullet_y = gun_coords[3]
            self.bullet = self.canvas.create_oval(bullet_x - BULLET_RADIUS, bullet_y - BULLET_RADIUS,
                                                  bullet_x + BULLET_RADIUS, bullet_y + BULLET_RADIUS,
                                                  fill="yellow")
            self.bullet_direction_x = math.cos(self.user1_gun_angle) * BULLET_SPEED
            self.bullet_direction_y = math.sin(self.user1_gun_angle) * BULLET_SPEED

    def fire_bullet_user2(self, event):
        if self.bullet is None:
            gun_coords = self.canvas.coords(self.user2_gun)
            bullet_x = gun_coords[2]
            bullet_y = gun_coords[3]
            self.bullet = self.canvas.create_oval(bullet_x - BULLET_RADIUS, bullet_y - BULLET_RADIUS,
                                                  bullet_x + BULLET_RADIUS, bullet_y + BULLET_RADIUS,
                                                  fill="green")
            self.bullet_direction_x = math.cos(self.user2_gun_angle) * BULLET_SPEED
            self.bullet_direction_y = math.sin(self.user2_gun_angle) * BULLET_SPEED

    def move_bullet(self):
        if self.bullet:
            self.canvas.move(self.bullet, self.bullet_direction_x, self.bullet_direction_y)
            bullet_coords = self.canvas.coords(self.bullet)
            if bullet_coords[0] <= 0 or bullet_coords[2] >= CANVAS_WIDTH or \
               bullet_coords[1] <= 0 or bullet_coords[3] >= CANVAS_HEIGHT:
                self.canvas.delete(self.bullet)
                self.bullet = None
            else:
                self.check_collision()

    def check_collision(self):
        bullet_coords = self.canvas.coords(self.bullet)
        bullet_center_x = (bullet_coords[0] + bullet_coords[2]) / 2
        bullet_center_y = (bullet_coords[1] + bullet_coords[3]) / 2

        user1_ball_coords = self.canvas.coords(self.user1_ball)
        user2_ball_coords = self.canvas.coords(self.user2_ball)

        if self.is_collision(bullet_center_x, bullet_center_y, user2_ball_coords):
            self.user1_points += 1
            self.update_score()
            self.reset_bullet()

        elif self.is_collision(bullet_center_x, bullet_center_y, user1_ball_coords):
            self.user2_points += 1
            self.update_score()
            self.reset_bullet()

    def is_collision(self, bullet_x, bullet_y, ball_coords):
        ball_center_x = (ball_coords[0] + ball_coords[2]) / 2
        ball_center_y = (ball_coords[1] + ball_coords[3]) / 2
        distance = math.sqrt((bullet_x - ball_center_x) ** 2 + (bullet_y - ball_center_y) ** 2)
        return distance < (BALL_RADIUS + BULLET_RADIUS)

    def reset_bullet(self):
        self.canvas.delete(self.bullet)
        self.bullet = None

    def update_score(self):
        if self.user1_points == POINTS_TO_WIN:
            self.canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, text="User 1 Wins!", fill="white", font=("Helvetica", 24))
            self.end_game()
        elif self.user2_points == POINTS_TO_WIN:
            self.canvas.create_text(CANVAS_WIDTH//2, CANVAS_HEIGHT//2, text="User 2 Wins!", fill="white", font=("Helvetica", 24))
            self.end_game()

    def end_game(self):
        self.root.unbind("s")
        self.root.unbind("k")
        self.root.after_cancel(self.animation)

    def update_game(self):
        self.rotate_guns()
        self.move_bullet()
        self.animation = self.root.after(50, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dual Rotating Guns Game")
    game = Game(root)
    root.mainloop()
