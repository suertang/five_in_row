import svgwrite
import cairosvg

# 创建图标
dwg = svgwrite.Drawing('icon.svg', size=(256, 256))

# 添加木质纹理背景
wood_gradient = dwg.linearGradient((0,0), (1,1))
wood_gradient.add_stop_color(0, '#E6C9A8')
wood_gradient.add_stop_color(0.5, '#D2B48C')
wood_gradient.add_stop_color(1, '#C19A6B')
dwg.defs.add(wood_gradient)
dwg.add(dwg.rect(insert=(0, 0), size=(256, 256), fill=wood_gradient.get_paint_server()))

# 添加3D棋盘边框
dwg.add(dwg.rect(insert=(10, 10), size=(236, 236), 
                fill='none', stroke='#8B4513', stroke_width=4))
dwg.add(dwg.rect(insert=(12, 12), size=(232, 232), 
                fill='none', stroke='#A0522D', stroke_width=2))

# 绘制棋盘线
for i in range(15):
    x = i * 17 + 13
    # 添加阴影效果
    dwg.add(dwg.line((13, x+1), (243, x+1), stroke='#A0522D', stroke_width=1))
    dwg.add(dwg.line((x+1, 13), (x+1, 243), stroke='#A0522D', stroke_width=1))
    # 主线条
    dwg.add(dwg.line((13, x), (243, x), stroke='#8B4513', stroke_width=1))
    dwg.add(dwg.line((x, 13), (x, 243), stroke='#8B4513', stroke_width=1))

# 绘制天元
dwg.add(dwg.circle(center=(128, 128), r=4, fill='#8B4513'))

# 添加示例棋子
# 黑棋
black_gradient = dwg.radialGradient(center=(0.5, 0.5), r=0.5)
black_gradient.add_stop_color(0, '#000000')
black_gradient.add_stop_color(1, '#333333')
dwg.defs.add(black_gradient)
dwg.add(dwg.circle(center=(128-34, 128-34), r=12, fill=black_gradient.get_paint_server()))

# 白棋
white_gradient = dwg.radialGradient(center=(0.5, 0.5), r=0.5)
white_gradient.add_stop_color(0, '#FFFFFF')
white_gradient.add_stop_color(1, '#F0F0F0')
dwg.defs.add(white_gradient)
dwg.add(dwg.circle(center=(128+34, 128+34), r=12, fill=white_gradient.get_paint_server()))

# 保存并转换图标
dwg.save()
cairosvg.svg2png(url='icon.svg', write_to='icon.png')
