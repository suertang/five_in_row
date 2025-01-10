import tkinter as tk
from tkinter import messagebox
import random
import time
from collections import defaultdict
from threading import Timer
from PIL import Image, ImageTk
import svgwrite
import io

# 游戏常量
DIFFICULTY_LEVELS = {
    '简单': {'delay': 0.3, 'randomness': 0.3},
    '困难': {'delay': 0.5, 'randomness': 0.1},
    '地狱': {'delay': 0.8, 'randomness': 0.0}
}
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
    global current_player
    
    # 获取当前难度设置
    difficulty = difficulty_var.get()
    delay = DIFFICULTY_LEVELS[difficulty]['delay']
    randomness = DIFFICULTY_LEVELS[difficulty]['randomness']
    
    # 显示AI思考提示
    canvas.create_text(300, 300, text="AI思考中...", font=("Arial", 20), tags="thinking")
    root.update()
    
    # 添加延迟
    time.sleep(delay)
    
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
    
    # 根据难度选择位置
    if best_moves:
        # 简单模式有一定概率随机选择
        if random.random() < randomness:
            i, j = random.choice([(x,y) for x in range(15) for y in range(15) if board[x][y]['stone'] is None])
        else:
            i, j = random.choice(best_moves)
        
        # 移除思考提示
        canvas.delete("thinking")
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

def on_canvas_click(event):
    """处理棋盘点击事件"""
    # 计算点击的格子坐标
    i = round((event.y - 20) / 40)
    j = round((event.x - 20) / 40)
    # 确保点击在棋盘范围内
    if 0 <= i < 15 and 0 <= j < 15 and board[i][j]['stone'] is None:
        on_click(i, j)

def select_difficulty():
    """通过按钮选择难度并自动关闭"""
    difficulty_window = tk.Toplevel(root)
    difficulty_window.title("选择难度")
    difficulty_window.geometry("300x200")
    
    # 添加标题
    tk.Label(difficulty_window, text="请选择游戏难度", 
            font=("Arial", 14), pady=10).pack()
    
    # 创建按钮容器
    button_frame = tk.Frame(difficulty_window)
    button_frame.pack(pady=10)
    
    # 创建难度按钮
    for level in DIFFICULTY_LEVELS:
        btn = tk.Button(button_frame, text=level, width=10, font=("Arial", 12),
                       command=lambda l=level: on_difficulty_selected(l, difficulty_window))
        btn.pack(pady=5)
    
    # 使弹窗保持焦点
    difficulty_window.grab_set()
    root.wait_window(difficulty_window)
    
    return difficulty_var.get()

def on_difficulty_selected(level, window):
    """处理难度选择"""
    difficulty_var.set(level)
    window.destroy()
    update_difficulty_display()

def create_board():
    """创建棋盘"""
    global canvas, difficulty_var, difficulty_label
    board = []
    
    # 设置窗口标题和图标
    root.title("唐唐五子棋")
    
    # 加载离线图标
    try:
        icon = ImageTk.PhotoImage(file="icon.png")
        root.iconphoto(True, icon)
    except:
        pass  # 如果图标不存在则跳过
    
    # 创建棋盘
    canvas = tk.Canvas(root, width=15*40, height=15*40, bg='#F0D9B5')
    canvas.pack()
    
    # 在棋盘左上角添加难度显示
    difficulty_var = tk.StringVar()
    canvas.create_text(50, 30, text="难度：", font=("隶书", 16, "bold"), fill="white", tags="difficulty")
    difficulty_label = canvas.create_text(100, 30, text="", font=("隶书", 16, "bold"), fill="white", tags="difficulty")
    
    # 通过弹窗选择难度
    select_difficulty()
    
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
            # 切换回黑棋玩家
            if not check_win(WHITE):
                current_player = BLACK

def reset_game():
    """重置游戏"""
    global current_player
    # 重新选择难度
    select_difficulty()
    current_player = BLACK
    for i in range(15):
        for j in range(15):
            if board[i][j]['stone'] is not None:
                board[i][j]['canvas'].delete(board[i][j]['stone'])
                board[i][j]['stone'] = None
    # 重新绑定点击事件
    canvas.bind("<Button-1>", on_canvas_click)
    # 重置获胜标记
    if hasattr(root, 'win_window_shown'):
        delattr(root, 'win_window_shown')

def show_winner(player):
    """显示获胜者弹窗"""
    # 禁用棋盘点击
    for row in board:
        for cell in row:
            cell['canvas'].unbind("<Button-1>")
    
    win_window = tk.Toplevel(root)
    win_window.title("游戏结束")
    tk.Label(win_window, text=f"{'黑棋' if player == BLACK else '白棋'} 获胜！", 
             font=("Arial", 20)).pack(padx=20, pady=20)
    
    # 添加按钮容器
    button_frame = tk.Frame(win_window)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="重新开始", 
              command=lambda: [win_window.destroy(), reset_game()]).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="退出", 
              command=root.quit).pack(side=tk.LEFT, padx=10)

def check_win(player):
    """检查是否有五子连珠"""
    # 检查水平方向
    for i in range(15):
        for j in range(11):
            if all(board[i][j+k]['stone'] is not None and 
                   board[i][j+k]['canvas'].itemcget(board[i][j+k]['stone'], 'fill') == player 
                   for k in range(5)):
                # 确保只显示一次获胜窗口
                if not hasattr(root, 'win_window_shown'):
                    root.win_window_shown = True
                    show_winner(player)
                return True

    # 检查垂直方向
    for i in range(11):
        for j in range(15):
            if all(board[i+k][j]['stone'] is not None and 
                   board[i+k][j]['canvas'].itemcget(board[i+k][j]['stone'], 'fill') == player 
                   for k in range(5)):
                if not hasattr(root, 'win_window_shown'):
                    root.win_window_shown = True
                    show_winner(player)
                return True

    # 检查主对角线
    for i in range(11):
        for j in range(11):
            if all(board[i+k][j+k]['stone'] is not None and 
                   board[i+k][j+k]['canvas'].itemcget(board[i+k][j+k]['stone'], 'fill') == player 
                   for k in range(5)):
                if not hasattr(root, 'win_window_shown'):
                    root.win_window_shown = True
                    show_winner(player)
                return True

    # 检查副对角线
    for i in range(4, 15):
        for j in range(11):
            if all(board[i-k][j+k]['stone'] is not None and 
                   board[i-k][j+k]['canvas'].itemcget(board[i-k][j+k]['stone'], 'fill') == player 
                   for k in range(5)):
                if not hasattr(root, 'win_window_shown'):
                    root.win_window_shown = True
                    show_winner(player)
                return True
    
    return False

def update_difficulty_display():
    """更新难度显示"""
    canvas.itemconfig(difficulty_label, text=difficulty_var.get())

def create_difficulty_overlay():
    """创建难度选择覆盖层"""
    overlay = tk.Canvas(root, width=300, height=200, bg='#F0D9B5', highlightthickness=2, 
                       highlightbackground='#8B4513')
    overlay.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # 添加标题
    overlay.create_text(150, 30, text="请选择游戏难度", 
                       font=("隶书", 18, "bold"), fill="#8B4513")
    
    # 创建难度按钮
    y = 70
    for level in DIFFICULTY_LEVELS:
        btn = tk.Button(overlay, text=level, width=10, font=("隶书", 14),
                       bg='#8B4513', fg='white', activebackground='#A0522D',
                       command=lambda l=level: on_difficulty_selected(l, overlay))
        overlay.create_window(150, y, window=btn)
        y += 50
    
    return overlay

def select_difficulty():
    """通过覆盖层选择难度"""
    overlay = create_difficulty_overlay()
    # 禁用主窗口交互
    root.grab_set()
    return difficulty_var.get()

def on_difficulty_selected(level, overlay):
    """处理难度选择"""
    difficulty_var.set(level)
    overlay.destroy()
    root.grab_release()  # 恢复主窗口交互
    update_difficulty_display()

if __name__ == "__main__":
    root = tk.Tk()
    # 设置窗口大小和位置
    root.geometry("600x620+300+100")
    # 设置窗口背景色
    root.configure(bg='#F0D9B5')
    board = create_board()
    root.mainloop()
