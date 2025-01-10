import svgwrite
import cairosvg

def create_stone(filename, color, gradient_stops, highlight=True):
    """创建单个棋子图像"""
    dwg = svgwrite.Drawing(filename + '.svg', size=(40, 40))
    
    # 创建渐变
    gradient = dwg.radialGradient(center=(0.5, 0.5), r=0.5)
    for stop in gradient_stops:
        gradient.add_stop_color(stop[0], stop[1])
    dwg.defs.add(gradient)
    
    # 绘制棋子
    dwg.add(dwg.circle(center=(20, 20), r=19, fill=gradient.get_paint_server()))
    
    # 添加高光
    if highlight:
        dwg.add(dwg.circle(center=(12, 12), r=6, fill='white', opacity=0.8))
    
    # 保存并转换
    dwg.save()
    cairosvg.svg2png(url=filename + '.svg', write_to=filename + '.png')

# 创建黑棋
create_stone('black_stone', 'black', [
    (0, '#000000'),
    (0.7, '#333333'), 
    (1, '#666666')
])

# 创建白棋
create_stone('white_stone', 'white', [
    (0, '#FFFFFF'),
    (0.7, '#F0F0F0'),
    (1, '#CCCCCC')
])

# 创建图标
dwg = svgwrite.Drawing('icon.svg', size=(256, 256))
dwg.add(dwg.rect(insert=(0, 0), size=(256, 256), fill='#F0D9B5'))

# 绘制棋盘
for i in range(15):
    x = i * 17 + 13
    dwg.add(dwg.line((13, x), (243, x), stroke='black', stroke_width=1))
    dwg.add(dwg.line((x, 13), (x, 243), stroke='black', stroke_width=1))

# 绘制天元
dwg.add(dwg.circle(center=(128, 128), r=4, fill='black'))

# 保存并转换图标
dwg.save()
cairosvg.svg2png(url='icon.svg', write_to='icon.png')
