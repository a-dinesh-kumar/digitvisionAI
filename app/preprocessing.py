import io
import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageOps
from typing import Tuple, Union

PILImage = Image.Image


def preprocess_image(image_input: Union[PILImage, bytes, str], target_size: Tuple[int, int] = (28, 28)) -> NDArray[np.float32]:

    # -------------------------
    # Step 1 : Read Image
    # -------------------------

    if isinstance(image_input, bytes):
        image = Image.open(io.BytesIO(image_input))

    elif isinstance(image_input, str):
        image = Image.open(image_input)

    elif isinstance(image_input, PILImage):
        image = image_input

    else:
        raise ValueError(f"Unsupported input type: {type(image_input)}")

    # -------------------------
    # Step 2 : Convert to Gray
    # -------------------------

    image = image.convert("L")

    # -------------------------
    # Step 3 : Detect Background
    # -------------------------

    img = np.array(image)

    border = np.concatenate([
        img[0, :],
        img[-1, :],
        img[:, 0],
        img[:, -1]
    ])

    if border.mean() > 127:
        image = ImageOps.invert(image)

    img = np.array(image)

    # -------------------------
    # Step 4 : Threshold
    # -------------------------

    binary = img > 50

    # -------------------------
    # Step 5 : Find Bounding Box
    # -------------------------

    coords = np.argwhere(binary)

    if coords.size != 0:

        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1

        image = image.crop((x0, y0, x1, y1))

    # -------------------------
    # Step 6 : Preserve Aspect Ratio
    # -------------------------

    width, height = image.size

    longest = max(width, height)

    square = Image.new("L", (longest, longest), 0)

    x = (longest - width) // 2
    y = (longest - height) // 2

    square.paste(image, (x, y))

    # -------------------------
    # Step 7 : Add Padding
    # -------------------------

    padding = int(longest * 0.15)

    padded = Image.new(
        "L",
        (longest + 2 * padding,
         longest + 2 * padding),
        0
    )

    padded.paste(square, (padding, padding))

    # -------------------------
    # Step 8 : Resize
    # -------------------------

    image = padded.resize(target_size, Image.LANCZOS)

    # -------------------------
    # Step 9 : Normalize
    # -------------------------

    img_array = np.array(image, dtype=np.float32)

    img_array = img_array / 255.0

    # -------------------------
    # Step 10 : Expand Dimension
    # -------------------------

    img_array = np.expand_dims(img_array, axis=0)

    return img_array