import tkinter as tk
import random
from collections import defaultdict
# 游戏常量
STONE_SIZE = 20  # 棋子半径
BLACK = "black"  # 黑棋先手
WHITE = "white"  # 白棋
EMPTY = None
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
        while 0 <= x < 15 and 0 <= y < 15 and board[x][y]['stone'] is not None and \
              board[x][y]['canvas'].itemcget(board[x][y]['stone'], 'fill') == player:
            count += 1
            x += dx
            y += dy
        # 反向搜索
        x, y = i - dx, j - dy
        while 0 <= x < 15 and 0 <= y < 15 and board[x][y]['stone'] is not None and \
              board[x][y]['canvas'].itemcget(board[x][y]['stone'], 'fill') == player:
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
            if board[i][j]['stone'] is None:
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
        x = j * 40 + 20
        y = i * 40 + 20
        stone = board[i][j]['canvas'].create_oval(
            x-STONE_SIZE, y-STONE_SIZE,
            x+STONE_SIZE, y+STONE_SIZE,
            fill=WHITE,
            outline='black'
        )
        board[i][j]['stone'] = stone
        check_win(WHITE)

def create_board():
    board = []
    canvas = tk.Canvas(root, width=15*40, height=15*40, bg='#F0D9B5')
    canvas.pack()
    
    # 绘制棋盘线
    for i in range(15):
        x = i * 40 + 20
        canvas.create_line(20, x, 580, x, width=2)
        canvas.create_line(x, 20, x, 580, width=2)
    
    # 创建存储棋子的二维列表
    for i in range(15):
        row = []
        for j in range(15):
            row.append({'canvas': canvas, 'stone': None})
        board.append(row)
    
    # 绑定点击事件
    def on_canvas_click(event):
        # 计算点击的格子坐标
        i = round((event.y - 20) / 40)
        j = round((event.x - 20) / 40)
        # 确保点击在棋盘范围内
        if 0 <= i < 15 and 0 <= j < 15 and board[i][j]['stone'] is None:
            on_click(i, j)
    
    canvas.bind("<Button-1>", on_canvas_click)
    
    return board

def on_click(i, j):
    global current_player
    
    # 只有当前玩家是人类（黑棋）时才处理点击
    if current_player == BLACK:
        x = j * 40 + 20
        y = i * 40 + 20
        stone = board[i][j]['canvas'].create_oval(
            x-STONE_SIZE, y-STONE_SIZE,
            x+STONE_SIZE, y+STONE_SIZE,
            fill=current_player,
            outline='black' if current_player == WHITE else 'white'
        )
        board[i][j]['stone'] = stone
        
        # 检查是否获胜
        if not check_win(current_player):
            # 切换玩家
            current_player = WHITE
            # 执行AI移动
            ai_move()

def show_winner(player):
    """显示获胜者弹窗"""
    win_window = tk.Toplevel(root)
    win_window.title("游戏结束")
    tk.Label(win_window, text=f"{'黑棋' if player == BLACK else '白棋'} 获胜！", 
             font=("Arial", 20)).pack(padx=20, pady=20)
    tk.Button(win_window, text="确定", command=root.quit).pack(pady=10)
    # 禁用棋盘点击
    for row in board:
        for cell in row:
            cell['canvas'].unbind("<Button-1>")

def check_win(player):
    """检查是否有五子连珠"""
    # Check horizontal
    for i in range(15):
        for j in range(11):
            if all(board[i][j+k]['stone'] is not None and 
                   board[i][j+k]['canvas'].itemcget(board[i][j+k]['stone'], 'fill') == player 
                   for k in range(5)):
                show_winner(player)
                return True

    # Check vertical
    for i in range(11):
        for j in range(15):
            if all(board[i+k][j]['stone'] is not None and 
                   board[i+k][j]['canvas'].itemcget(board[i+k][j]['stone'], 'fill') == player 
                   for k in range(5)):
                show_winner(player)
                return True

    # Check diagonal (top-left to bottom-right)
    for i in range(11):
        for j in range(11):
            if all(board[i+k][j+k]['stone'] is not None and 
                   board[i+k][j+k]['canvas'].itemcget(board[i+k][j+k]['stone'], 'fill') == player 
                   for k in range(5)):
                show_winner(player)
                return True

    # Check diagonal (bottom-left to top-right)
    for i in range(4, 15):
        for j in range(11):
            if all(board[i-k][j+k]['stone'] is not None and 
                   board[i-k][j+k]['canvas'].itemcget(board[i-k][j+k]['stone'], 'fill') == player 
                   for k in range(5)):
                show_winner(player)
                return True

if __name__ == "__main__":
    root = tk.Tk()
    board = create_board()
    root.mainloop()
