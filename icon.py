import svgwrite
import cairosvg

# 创建SVG图标
dwg = svgwrite.Drawing('icon.svg', size=(256, 256))

# 绘制背景
dwg.add(dwg.rect(insert=(0, 0), size=(256, 256), fill='#F0D9B5'))

# 绘制棋盘
for i in range(15):
    x = i * 17 + 13
    dwg.add(dwg.line((13, x), (243, x), stroke='black', stroke_width=1))
    dwg.add(dwg.line((x, 13), (x, 243), stroke='black', stroke_width=1))

# 绘制天元
dwg.add(dwg.circle(center=(128, 128), r=4, fill='black'))

# 绘制3D黑棋
black_gradient = dwg.radialGradient(center=(0.5, 0.5), r=0.5)
black_gradient.add_stop_color(0, '#000000')
black_gradient.add_stop_color(0.7, '#333333')
black_gradient.add_stop_color(1, '#666666')
dwg.defs.add(black_gradient)

dwg.add(dwg.circle(center=(128-34, 128-34), r=12, fill=black_gradient.get_paint_server()))
# 添加高光
dwg.add(dwg.circle(center=(128-34-4, 128-34-4), r=4, fill='white', opacity=0.8))

# 绘制3D白棋
white_gradient = dwg.radialGradient(center=(0.5, 0.5), r=0.5)
white_gradient.add_stop_color(0, '#FFFFFF')
white_gradient.add_stop_color(0.7, '#F0F0F0')
white_gradient.add_stop_color(1, '#CCCCCC')
dwg.defs.add(white_gradient)

dwg.add(dwg.circle(center=(128+34, 128+34), r=12, fill=white_gradient.get_paint_server()))
# 添加高光
dwg.add(dwg.circle(center=(128+34-4, 128+34-4), r=4, fill='white', opacity=0.8))

# 保存SVG
dwg.save()

# 使用cairosvg将SVG转换为PNG
cairosvg.svg2png(url='icon.svg', write_to='icon.png')
