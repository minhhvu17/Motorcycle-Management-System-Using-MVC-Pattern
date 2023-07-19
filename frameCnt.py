from PIL import Image
import os


file_name = 'img/product_1.gif'
file_path = os.path.join(os.path.dirname(__file__), file_name)
image = Image.open(file_path)
frame_count = 0
while True:
    try:
        image.seek(frame_count)
        frame_count += 1
    except EOFError:
        break
print(frame_count)