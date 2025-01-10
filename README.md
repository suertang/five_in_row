# 唐唐五子棋

一个简单的五子棋游戏，支持人机对战和不同难度选择。

## 功能特点
- 人机对战
- 三种难度选择：简单、困难、地狱
- 漂亮的棋盘和棋子视觉效果
- 自动检测五子连珠
- 获胜提示和重新开始功能

## 运行要求
- Python 3.6+
- 安装依赖包（见requirements.txt）

## 如何运行
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行游戏：
   ```bash
   python main.py
   ```

## 游戏控制
- 点击棋盘落子
- 游戏结束后可选择重新开始或退出
- 可在游戏开始时选择难度

## 文件说明
- `main.py` - 主程序
- `icon.py` - 图标生成脚本
- `icon.png` - 程序图标
- `black_stone.png` - 黑棋图片
- `white_stone.png` - 白棋图片
