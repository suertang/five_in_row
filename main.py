import tkinter as tk
import random
from collections import defaultdict
#小圆圈棋子太小，看不清楚，特别是白棋 ai!
# 游戏常量
BLACK = "●"  # 黑棋先手
WHITE = "○"  # 白棋
EMPTY = ""
current_player = BLACK  # 黑棋先手

def evaluate_position(i, j, player):
    """评估当前位置的得分"""
    directions = [
        (1, 0),  # 水平
        (0, 1),  # 垂直
        (1, 1),  # 主对角线
        (1, -1)  # 副对角线
    ]
    
    score = 0
    for dx, dy in directions:
        count = 1
        # 正向搜索
        x, y = i + dx, j + dy
        while 0 <= x < 15 and 0 <= y < 15 and board[x][y]['text'] == player:
            count += 1
            x += dx
            y += dy
        # 反向搜索
        x, y = i - dx, j - dy
        while 0 <= x < 15 and 0 <= y < 15 and board[x][y]['text'] == player:
            count += 1
            x -= dx
            y -= dy
        # 根据连子数评分
        if count >= 5:
            return 10000  # 直接获胜
        score += count ** 2
    return score

def ai_move():
    """改进的AI算法"""
    best_score = -1
    best_moves = []
    
    # 遍历所有空位
    for i in range(15):
        for j in range(15):
            if board[i][j]['text'] == EMPTY:
                # 计算进攻和防守得分
                attack_score = evaluate_position(i, j, WHITE)
                defend_score = evaluate_position(i, j, BLACK)
                total_score = attack_score + defend_score
                
                # 记录最佳位置
                if total_score > best_score:
                    best_score = total_score
                    best_moves = [(i, j)]
                elif total_score == best_score:
                    best_moves.append((i, j))
    
    # 随机选择一个最佳位置
    if best_moves:
        i, j = random.choice(best_moves)
        board[i][j].config(text=WHITE, fg="white")
        check_win(WHITE)

def create_board():
    board = []
    for i in range(15):
        row = []
        for j in range(15):
            cell = tk.Button(root, text="", width=2, height=1,
                          font=("Arial", 12),
                          command=lambda i=i, j=j: on_click(i, j))
            cell.grid(row=i, column=j)
            row.append(cell)
        board.append(row)
    return board

def on_click(i, j):
    global current_player
    
    if board[i][j]['text'] == EMPTY:
        color = "black" if current_player == BLACK else "white"
        board[i][j].config(text=current_player, fg=color)
        check_win(current_player)
        
        # 切换玩家
        current_player = WHITE if current_player == BLACK else BLACK
        
        # 如果是电脑的回合，执行AI移动
        if current_player == WHITE:
            ai_move()
            current_player = BLACK  # 切换回玩家

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
