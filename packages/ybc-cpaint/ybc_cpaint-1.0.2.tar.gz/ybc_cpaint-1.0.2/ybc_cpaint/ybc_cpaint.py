from PIL import Image


# 灰度值小（暗）的用列表开头的符号，灰度值大（亮）的用列表末尾的符号。
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

length = len(ascii_char)

# 将256灰度映射到列表的70个字符上
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]

# 将图片转换为字符画
def charpaint(img, width = 80, height = 80, output = "output.txt"):
    im = Image.open(img)
    im = im.resize((width,height), Image.NEAREST)
    txt = ""
    for i in range(height):
        for j in range(width):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'
    print(txt)

    # 字符画输出到文件
    with open(output,'w') as f:
        f.write(txt)



