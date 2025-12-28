from PIL import Image, ImageDraw, ImageFont
from ranking import get_top10
from data import items
import os

def render_top10(items, output_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FONT_PATH = os.path.join(BASE_DIR, "fonts", "NotoSansSC-VariableFont_wght.ttf")


    # ====== 基本参数 ======
    WIDTH, HEIGHT = 400, 300
    MARGIN = 30
    LINE_HEIGHT = 40


    # ====== 创建画布 ======
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype(FONT_PATH, 30)
    text_font = ImageFont.truetype(FONT_PATH, 25)

    # ====== 标题 ======
    draw.text((MARGIN, 10), "冰箱冷宫Top10", fill="black", font=title_font)

    # ====== 内容 ======
    top10 = get_top10(items)

    COL_WIDTH = 180
    START_Y = 70

    for idx, item in enumerate(top10):

        col = idx // 5
        row = idx % 5

        x = MARGIN + col * COL_WIDTH
        y = START_Y + row * LINE_HEIGHT

        PADDING = 25
        RIGHT_X = x + COL_WIDTH - PADDING

        left = f"{idx+1}. {item['name']}"
        draw.text((x,y), left, fill="black", font=text_font)

        right = f" {item['days']}天"

        w = draw.textlength(right, font = text_font)
        draw.text((RIGHT_X - w, y), right, fill="black", font=text_font)


    # ====== 保存 ======
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

