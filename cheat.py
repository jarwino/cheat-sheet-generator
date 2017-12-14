import sys, math
from pdf2image import convert_from_path
from PIL import Image

images = convert_from_path(sys.argv[1])
widths, heights = zip(*(i.size for i in images))

num_pages = int(sys.argv[2]) # num pages
num_per_row = int(sys.argv[3]) # num across
num_per_column = int(math.ceil(math.ceil(float(len(images))/ num_per_row) / num_pages))

im = 0

for i in range(num_pages):
    new_im = Image.new('RGB', (num_per_row * widths[0], num_per_column * heights[0]))
    new_im.paste((255, 255, 255), [0, 0, new_im.size[0], new_im.size[1]])
    x_offset = 0
    col_count = 0
    row_count = 0
    y_offset = 0
    for j in range(num_per_row * num_per_column):
        if im >= len(images):
            break
        if row_count == num_per_column:
            break
        if col_count == num_per_row:
            row_count += 1
            col_count = 0
            x_offset = 0
            y_offset += images[im].size[1]
        print("image at", (x_offset,y_offset))
        new_im.paste(images[im], (x_offset,y_offset))
        col_count += 1
        x_offset += images[im].size[0]

        im += 1

    new_im.show()
