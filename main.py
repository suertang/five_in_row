import tkinter as tk
import random

current_player = "X"  # X goes first

def ai_move():
    # Simple AI - find first empty spot
    for i in range(15):
        for j in range(15):
            if board[i][j]['text'] == "":
                board[i][j].config(text="O")
                check_win("O")
                return

def create_board():
    board = []
    for i in range(15):
        row = []
        for j in range(15):
            cell = tk.Button(root, text="", width=2, height=1,
                            command=lambda i=i, j=j: on_click(i, j))
            cell.grid(row=i, column=j)
            row.append(cell)
        board.append(row)
    return board

def on_click(i, j):
    global current_player
    
    if board[i][j]['text'] == "":
        board[i][j].config(text=current_player)
        check_win(current_player)
        
        # Switch players
        current_player = "O" if current_player == "X" else "X"
        
        # If it's O's turn, make AI move
        if current_player == "O":
            ai_move()
            current_player = "X"  # Switch back to X after AI move

def check_win(player):
    # Check horizontal
    for i in range(15):
        for j in range(11):
            if all(board[i][j+k]['text'] == player for k in range(5)):
                print(f"{player} wins!")
                return

    # Check vertical
    for i in range(11):
        for j in range(15):
            if all(board[i+k][j]['text'] == player for k in range(5)):
                print(f"{player} wins!")
                return

    # Check diagonal (top-left to bottom-right)
    for i in range(11):
        for j in range(11):
            if all(board[i+k][j+k]['text'] == player for k in range(5)):
                print(f"{player} wins!")
                return

    # Check diagonal (bottom-left to top-right)
    for i in range(4, 15):
        for j in range(11):
            if all(board[i-k][j+k]['text'] == player for k in range(5)):
                print(f"{player} wins!")
                return

if __name__ == "__main__":
    root = tk.Tk()
    board = create_board()
    root.mainloop()
