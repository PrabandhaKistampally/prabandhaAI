import tkinter as tk
from tkinter import messagebox
import random

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder Game")
        self.root.geometry("800x600")
        
        # Game variables
        self.current_player = 1
        self.player1_pos = 1
        self.player2_pos = 1
        self.dice_value = 1
        
        # Snake positions (head, tail) - snakes go down
        self.snakes = {
            16: 6,   # Snake from 16 to 6
            47: 26,  # Snake from 47 to 26
            49: 11,  # Snake from 49 to 11
            56: 53,  # Snake from 56 to 53
            62: 19,  # Snake from 62 to 19
            64: 60,  # Snake from 64 to 60
            87: 24,  # Snake from 87 to 24
            93: 73,  # Snake from 93 to 73
            95: 75,  # Snake from 95 to 75
            98: 78   # Snake from 98 to 78
        }
        
        # Ladder positions (bottom, top) - ladders go up
        self.ladders = {
            1: 38,   # Ladder from 1 to 38
            4: 14,   # Ladder from 4 to 14
            9: 31,   # Ladder from 9 to 31
            21: 42,  # Ladder from 21 to 42
            28: 84,  # Ladder from 28 to 84
            36: 44,  # Ladder from 36 to 44
            51: 67,  # Ladder from 51 to 67
            71: 91,  # Ladder from 71 to 91
            80: 100  # Ladder from 80 to 100
        }
        
        # Snake colors (different colors for each snake)
        self.snake_colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
            "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"
        ]
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Create control panel
        self.create_control_panel()
        
        # Draw the board
        self.draw_board()
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)
        
    def create_control_panel(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)
        
        # Title
        title_label = tk.Label(control_frame, text="Snake & Ladder", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Player info
        self.player1_label = tk.Label(control_frame, text="Player 1: Position 1", font=("Arial", 12))
        self.player1_label.pack(pady=5)
        
        self.player2_label = tk.Label(control_frame, text="Player 2: Position 1", font=("Arial", 12))
        self.player2_label.pack(pady=5)
        
        # Current player
        self.current_player_label = tk.Label(control_frame, text="Current: Player 1", 
                                           font=("Arial", 14, "bold"), fg="blue")
        self.current_player_label.pack(pady=10)
        
        # Dice
        self.dice_label = tk.Label(control_frame, text="Dice: 1", font=("Arial", 16, "bold"))
        self.dice_label.pack(pady=10)
        
        # Roll dice button
        roll_button = tk.Button(control_frame, text="Roll Dice", command=self.roll_dice,
                              font=("Arial", 12), bg="#4CAF50", fg="white")
        roll_button.pack(pady=10)
        
        # New game button
        new_game_button = tk.Button(control_frame, text="New Game", command=self.new_game,
                                  font=("Arial", 12), bg="#2196F3", fg="white")
        new_game_button.pack(pady=10)
        
    def draw_board(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # Board dimensions
        board_size = 500
        cell_size = board_size // 10
        start_x = 50
        start_y = 50
        
        # Draw grid
        for row in range(10):
            for col in range(10):
                x1 = start_x + col * cell_size
                y1 = start_y + (9 - row) * cell_size  # Start from bottom
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Calculate cell number
                if row % 2 == 0:
                    cell_num = (row * 10) + col + 1
                else:
                    cell_num = (row * 10) + (10 - col)
                
                # Draw cell
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
                
                # Add number
                self.canvas.create_text(x1 + cell_size//2, y1 + cell_size//2, 
                                      text=str(cell_num), font=("Arial", 10, "bold"), fill="black")
        
        # Draw snakes
        snake_color_index = 0
        for head, tail in self.snakes.items():
            head_pos = self.get_cell_center(head)
            tail_pos = self.get_cell_center(tail)
            
            # Draw snake body (curved line)
            color = self.snake_colors[snake_color_index % len(self.snake_colors)]
            self.draw_curved_line(head_pos, tail_pos, color, width=8)
            
            # Draw snake head
            self.canvas.create_oval(head_pos[0]-5, head_pos[1]-5, head_pos[0]+5, head_pos[1]+5,
                                  fill=color, outline="black")
            
            snake_color_index += 1
        
        # Draw ladders
        for bottom, top in self.ladders.items():
            bottom_pos = self.get_cell_center(bottom)
            top_pos = self.get_cell_center(top)
            
            # Draw ladder (straight line with rungs)
            self.draw_ladder(bottom_pos, top_pos)
        
        # Draw players
        self.draw_players()
        
    def get_cell_center(self, cell_num):
        board_size = 500
        cell_size = board_size // 10
        start_x = 50
        start_y = 50
        
        # Calculate row and column
        row = (cell_num - 1) // 10
        col = (cell_num - 1) % 10
        
        # Adjust for snake pattern
        if row % 2 == 1:
            col = 9 - col
        
        x = start_x + col * cell_size + cell_size // 2
        y = start_y + (9 - row) * cell_size + cell_size // 2
        
        return (x, y)
    
    def draw_curved_line(self, start, end, color, width=3):
        # Create a curved line between two points
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2 - 30  # Curve upward
        
        # Create curved line using multiple line segments
        points = []
        for i in range(11):
            t = i / 10
            x = start[0] + t * (2 * mid_x - start[0] - end[0]) * t + (end[0] - start[0]) * t
            y = start[1] + t * (2 * mid_y - start[1] - end[1]) * t + (end[1] - start[1]) * t
            points.extend([x, y])
        
        self.canvas.create_line(points, fill=color, width=width, smooth=True)
    
    def draw_ladder(self, bottom, top):
        # Draw ladder with rungs
        color = "#F5F5DC"  # Cream color
        
        # Main ladder lines
        self.canvas.create_line(bottom[0]-10, bottom[1], top[0]-10, top[1], 
                              fill=color, width=6)
        self.canvas.create_line(bottom[0]+10, bottom[1], top[0]+10, top[1], 
                              fill=color, width=6)
        
        # Draw rungs
        steps = 5
        for i in range(1, steps):
            t = i / steps
            x = bottom[0] + t * (top[0] - bottom[0])
            y = bottom[1] + t * (top[1] - bottom[1])
            self.canvas.create_line(x-10, y, x+10, y, fill="brown", width=2)
    
    def draw_players(self):
        # Draw player 1 (red circle)
        pos1 = self.get_cell_center(self.player1_pos)
        self.canvas.create_oval(pos1[0]-15, pos1[1]-15, pos1[0]+15, pos1[1]+15,
                              fill="red", outline="black", width=2)
        self.canvas.create_text(pos1[0], pos1[1], text="P1", fill="white", font=("Arial", 8, "bold"))
        
        # Draw player 2 (blue circle)
        pos2 = self.get_cell_center(self.player2_pos)
        self.canvas.create_oval(pos2[0]-15, pos2[1]-15, pos2[0]+15, pos2[1]+15,
                              fill="blue", outline="black", width=2)
        self.canvas.create_text(pos2[0], pos2[1], text="P2", fill="white", font=("Arial", 8, "bold"))
    
    def roll_dice(self):
        # Roll dice
        self.dice_value = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {self.dice_value}")
        
        # Move player
        if self.current_player == 1:
            new_pos = self.player1_pos + self.dice_value
            if new_pos <= 100:
                self.player1_pos = new_pos
                # Check for snakes
                if self.player1_pos in self.snakes:
                    self.player1_pos = self.snakes[self.player1_pos]
                    messagebox.showinfo("Snake!", f"Player 1 hit a snake! Moved to position {self.player1_pos}")
                # Check for ladders
                elif self.player1_pos in self.ladders:
                    self.player1_pos = self.ladders[self.player1_pos]
                    messagebox.showinfo("Ladder!", f"Player 1 climbed a ladder! Moved to position {self.player1_pos}")
                
                self.player1_label.config(text=f"Player 1: Position {self.player1_pos}")
                
                # Check for win
                if self.player1_pos == 100:
                    messagebox.showinfo("Winner!", "Player 1 wins!")
                    return
        else:
            new_pos = self.player2_pos + self.dice_value
            if new_pos <= 100:
                self.player2_pos = new_pos
                # Check for snakes
                if self.player2_pos in self.snakes:
                    self.player2_pos = self.snakes[self.player2_pos]
                    messagebox.showinfo("Snake!", f"Player 2 hit a snake! Moved to position {self.player2_pos}")
                # Check for ladders
                elif self.player2_pos in self.ladders:
                    self.player2_pos = self.ladders[self.player2_pos]
                    messagebox.showinfo("Ladder!", f"Player 2 climbed a ladder! Moved to position {self.player2_pos}")
                
                self.player2_label.config(text=f"Player 2: Position {self.player2_pos}")
                
                # Check for win
                if self.player2_pos == 100:
                    messagebox.showinfo("Winner!", "Player 2 wins!")
                    return
        
        # Switch players
        self.current_player = 3 - self.current_player  # Switch between 1 and 2
        self.current_player_label.config(text=f"Current: Player {self.current_player}")
        
        # Redraw board
        self.draw_board()
    
    def new_game(self):
        self.player1_pos = 1
        self.player2_pos = 1
        self.current_player = 1
        self.dice_value = 1
        
        self.player1_label.config(text="Player 1: Position 1")
        self.player2_label.config(text="Player 2: Position 1")
        self.current_player_label.config(text="Current: Player 1")
        self.dice_label.config(text="Dice: 1")
        
        self.draw_board()
    
    def on_click(self, event):
        # Handle mouse clicks if needed
        pass

def main():
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()

if __name__ == "__main__":
    main() 