# unicode-braille-to-nabcc.py
# Unicode点字をNABCC点字(ASCII点字)に変換
# 使い方:
# python unicode-braille-to-nabcc.py 入力ファイル 出力ファイル

import sys

UNICODE_TO_NABCC = str.maketrans({
    '\u2801': 'A', '\u2803': 'B', '\u2809': 'C', '\u2819': 'D',
    '\u2811': 'E', '\u280B': 'F', '\u281B': 'G', '\u2813': 'H',
    '\u280A': 'I', '\u281A': 'J', '\u2805': 'K', '\u2807': 'L',
    '\u280D': 'M', '\u281D': 'N', '\u2815': 'O', '\u280F': 'P',
    '\u281F': 'Q', '\u2817': 'R', '\u280E': 'S', '\u281E': 'T',
    '\u2825': 'U', '\u2827': 'V', '\u283A': 'W', '\u282D': 'X',
    '\u283D': 'Y', '\u2835': 'Z',
    '\u282F': '&', '\u283F': '=', '\u2837': '(', '\u282E': '!',
    '\u283E': ')', '\u2821': '*', '\u2823': '<', '\u2829': '%',
    '\u2839': '?', '\u2831': ':', '\u282B': '$', '\u283B': ']',
    '\u2833': '\\', '\u282A': '[',
    '\u2802': '1', '\u2806': '2', '\u2812': '3', '\u2832': '4',
    '\u2822': '5', '\u2816': '6', '\u2836': '7', '\u2826': '8',
    '\u2814': '9', '\u2834': '0',
    '\u280C': '/', '\u282C': '+', '\u281C': '>', '\u283C': '#',
    '\u2824': '-', '\u2804': "'", '\u2808': '@', '\u2818': '^',
    '\u2838': '_', '\u2810': '"', '\u2828': '.', '\u2830': ';',
    '\u2820': ',',
})

if len(sys.argv) != 3:
    print(f"使い方: python {sys.argv[0]} 入力ファイル 出力ファイル")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    with open(input_file, 'r', encoding='utf-8') as src, \
         open(output_file, 'w', encoding='utf-8') as dst:
        for line in src:
            dst.write(line.translate(UNICODE_TO_NABCC))
    print(f"変換完了: {input_file} -> {output_file}")
except FileNotFoundError as e:
    print(f"エラー: ファイルが見つかりません: {e}")
    sys.exit(1)
