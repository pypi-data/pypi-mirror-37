# -*- coding: utf -*-
from image2char import tool
from PIL import Image

img_path1 = 'input1.jpg'


def main():
    try:
        img1 = Image.open(img_path1)

        img1 = img1.resize((60, 60), Image.ANTIALIAS)
        matrix = tool.to_chars(img1, density=1, scale=2, reversed=False)
        for i in range(len(matrix)):
            print(''.join(matrix[i]))
    except Exception:
        print('install is not successful, maybe you need to install pillow:')
        print('\t apt-get install python3-pillow')


if __name__ == '__main__':
    main()
