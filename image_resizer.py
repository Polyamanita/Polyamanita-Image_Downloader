import os
from PIL import Image

# can be used after executing image_grabber.py
# os.system('mkdir img; cp images/*/google/* img/')

directory = 'img' # i.e. PYTHON_IMAGE_DOWNLOADER/img/[...]
size = 64

count = 0
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        image = Image.open(f)
        image_resize = image.resize((size, size))
        image_resize.save(f)
    count += 1
    print(count)

print('DONE')
