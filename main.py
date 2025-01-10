import tkinter as tk
# 只有x 没有o，请完善 ai!
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
    if board[i][j]['text'] == "":
        board[i][j].config(text="X")
        check_win("X")

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
