from base64 import b64encode
from pathlib import Path

def get_b64_image(img_path):
    safe_path = Path(img_path)
    with open(safe_path, 'rb') as img_file:
        encoded = b64encode(img_file.read())

    filetype = safe_path.parts[-1].lower().split('.')[1]
    if filetype == 'jpg':
        filetype = 'jpeg'

    trimmed_img = str(encoded[3:])[2:-1]
    encoded_image = f'data:image/{filetype};base64,/9j{trimmed_img}'
    return encoded_image

def asset_safe_name(name):
    safe_name = name
    for char in ['_', ',', '!', '\'', '(', ')']:
        safe_name = safe_name.replace(char, '')
    return safe_name[:31]
