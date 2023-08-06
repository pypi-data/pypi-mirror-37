import argparse
from PIL import Image
from image2char import tool

# init argsparser
parser = argparse.ArgumentParser(description='''
    welcome to image2char cmd tool
    你可以使用这个工具将本地/网络的图片转成字符画
''')
parser.add_argument('image')
parser.add_argument(
    '-d',
    '--dentisy',
    help='dentisy, 分辨率, 取值0-1 默认为0.5',
    type=float,
    default=0.5)
parser.add_argument(
    '-s', '--scale', help='scale, 字符集高宽比, 默认为2', type=float, default=2)
parser.add_argument(
    '-r', '--reversed', help='reversed, 是否翻转黑白', action='store_true')
parser.add_argument(
    '-c', '--charset', help='charset, 字符集, 默认使用经典ascii字符集', default=None)
parser.add_argument(
    '-u', '--url', help='是否使用url, 将image_path路径设定为url', action='store_true')
parser.add_argument('-w', '--width', help='改变图片的初始宽度', type=int)
args = parser.parse_args()

# get img
img = None
if args.url:
    img = tool.from_url(args.image)
else:
    img = tool.from_path(args.image)

if args.width:
    height = int(args.width * img.size[1] / img.size[0])
    width = int(args.width)
    img = img.resize((width, height), Image.ANTIALIAS)

print(args.scale)
scanner = tool.get_scanner(density=args.dentisy, scale=args.scale)
scanner.scan(img, reversed=args.reversed, char_list=args.charset)
scanner.print_result()
