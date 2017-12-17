import sys, math
from subprocess import Popen, PIPE
from PIL import Image
from io import BytesIO

'''
The following 2 functions are from the pdf2image library (https://github.com/Belval/pdf2image)
'''

def __parse_pdftoppm_buffer(data):
    images = []

    index = 0

    while(index < len(data)):
        code, size, rgb = tuple(data[index:index + 40].split(b'\n')[0:3])
        size_x, size_y = tuple(size.split(b' '))
        file_size = len(code) + len(size) + len(rgb) + 3 + int(size_x) * int(size_y) * 3
        images.append(Image.open(BytesIO(data[index:index + file_size])))
        index += file_size

    return images

def convert_from_path(pdf_path, dpi=200, output_folder=None):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_path -> Path to the PDF that you want to convert
            dpi -> Image quality in DPI (default 200)
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
    """

    args = ['pdftoppm', '-r', str(dpi), pdf_path, ]

    if output_folder is not None:
        args.append(output_folder if output_folder[-1] == '/' else output_folder + '/')
        args.append('shell=True')

    proc = Popen(args, stdout=PIPE, stderr=PIPE)

    data, err = proc.communicate()

    if output_folder is not None:
        return __load_from_output_folder(output_folder)
    else:
        return __parse_pdftoppm_buffer(data)

'''
</end library code>
'''

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

    new_im.save(sys.argv[4] + "_" + str(i + 1) + '.pdf', "PDF", resolution=100.0)



