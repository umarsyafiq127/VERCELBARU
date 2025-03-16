import io
from rembg import remove
from PIL import Image

def remove_background(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    output = remove(image)

    img_byte_arr = io.BytesIO()
    output.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()

print(f"remove bisa")
