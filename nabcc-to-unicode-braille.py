# nabcc-to-unicode-braille.py
# .bseや.brlなどのNABCCのファイルをUnicode点字に変換
# 使い方:
# python nabcc-to-unicode-braille.py 入力ファイル 出力ファイル

import sys

NABCC_TABLE = str.maketrans({
    'A': '\u2801', 'B': '\u2803', 'C': '\u2809', 'D': '\u2819',
    'E': '\u2811', 'F': '\u280B', 'G': '\u281B', 'H': '\u2813',
    'I': '\u280A', 'J': '\u281A', 'K': '\u2805', 'L': '\u2807',
    'M': '\u280D', 'N': '\u281D', 'O': '\u2815', 'P': '\u280F',
    'Q': '\u281F', 'R': '\u2817', 'S': '\u280E', 'T': '\u281E',
    'U': '\u2825', 'V': '\u2827', 'W': '\u283A', 'X': '\u282D',
    'Y': '\u283D', 'Z': '\u2835',
    '&': '\u282F', '=': '\u283F', '(': '\u2837', '!': '\u282E',
    ')': '\u283E', '*': '\u2821', '<': '\u2823', '%': '\u2829',
    '?': '\u2839', ':': '\u2831', '$': '\u282B', ']': '\u283B',
    '\\': '\u2833', '[': '\u282A',
    '1': '\u2802', '2': '\u2806', '3': '\u2812', '4': '\u2832',
    '5': '\u2822', '6': '\u2816', '7': '\u2836', '8': '\u2826',
    '9': '\u2814', '0': '\u2834',
    '/': '\u280C', '+': '\u282C', '>': '\u281C', '#': '\u283C',
    '-': '\u2824', "'": '\u2804', '@': '\u2808', '^': '\u2818',
    '_': '\u2838', '"': '\u2810', '.': '\u2828', ';': '\u2830',
    ',': '\u2820',
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
            dst.write(line.translate(NABCC_TABLE))
    print(f"変換完了: {input_file} -> {output_file}")
except FileNotFoundError as e:
    print(f"エラー: ファイルが見つかりません: {e}")
    sys.exit(1)
