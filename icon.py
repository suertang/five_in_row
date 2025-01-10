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

# 绘制示例棋子
dwg.add(dwg.circle(center=(128-34, 128-34), r=12, fill='black'))
dwg.add(dwg.circle(center=(128+34, 128+34), r=12, fill='white'))

# 保存SVG
dwg.save()

# 使用cairosvg将SVG转换为PNG
cairosvg.svg2png(url='icon.svg', write_to='icon.png')
