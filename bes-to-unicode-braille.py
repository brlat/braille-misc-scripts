#!/usr/bin/env python3
"""
bes-to-unicode-braille.py
BESファイル（点字バイナリ形式）をUnicode点字テキストに変換するスクリプト。

使い方:
  python bes_to_unicode_braille.py 入力ファイル.bes 出力ファイル.txt

■ 変換方式
  BESバイト = 0xA0 + pattern  (pattern: 0〜63)
  Unicode点字 = U+2800 + pattern
  つまり BESバイト - 0xA0 + 0x2800 = Unicode点字コードポイント

■ BESファイル構造
  [0x000〜0x3FF] ヘッダー部（メタデータ・フィラー）
  [0x400〜     ] データセクション（点字データ本体）

■ データセクション内の制御バイト
  0xFF : ページ開始マーカー（直後2バイトはページ情報）
  0xFD : 行データ開始マーカー（無視）
  0xFE : 行データ終端マーカー（改行を出力）
  0x0D : キャリッジリターン（無視）
  0xA0〜0xDF : 点字バイト（0xA0=スペース、0xA1〜0xDF=各種点字）
"""

import sys
import os

# BES データセクションの開始オフセット
DATA_OFFSET = 0x400

# 制御バイト
BYTE_PAGE_START  = 0xFF
BYTE_LINE_HEADER = 0xFD
BYTE_LINE_END    = 0xFE
BYTE_CR          = 0x0D
BRAILLE_MIN      = 0xA0

# Unicode点字ブロックの先頭
UNICODE_BRAILLE_BASE = 0x2800


def convert_bes_to_unicode_braille(input_path: str, output_path: str) -> None:
    """BESファイルをUnicode点字テキストファイルに変換する。"""

    with open(input_path, "rb") as f:
        data = f.read()

    if len(data) < DATA_OFFSET:
        raise ValueError(
            f"ファイルサイズが小さすぎます（{len(data)} バイト）。"
            f"BESファイルはデータセクションが 0x{DATA_OFFSET:04X} から始まる必要があります。"
        )

    section = data[DATA_OFFSET:]
    output_lines = []
    current_line = []

    i = 0
    while i < len(section):
        b = section[i]

        if b == BYTE_PAGE_START:
            # ページ開始マーカー: 直後の2バイトはページ情報（スキップ）
            i += 3
            continue

        elif b == BYTE_LINE_HEADER:
            # 行データ開始: 無視
            i += 1
            continue

        elif b == BYTE_LINE_END:
            # 行データ終端: 行末の余分なスペース（U+2800）を除いて出力
            line_str = ''.join(current_line).rstrip('\u2800')
            output_lines.append(line_str)
            current_line = []
            i += 1
            continue

        elif b == BYTE_CR:
            # CR: 無視
            i += 1
            continue

        elif b >= BRAILLE_MIN:
            # 点字バイト: pattern = b - 0xA0、Unicode点字 = U+2800 + pattern
            pattern = b - BRAILLE_MIN
            current_line.append(chr(UNICODE_BRAILLE_BASE + pattern))
            i += 1
            continue

        else:
            # その他のバイトは無視
            i += 1
            continue

    # 末尾に残った行があれば追加
    if current_line:
        output_lines.append(''.join(current_line).rstrip('\u2800'))

    # 出力: 行を改行で結合してUTF-8で書き出す
    with open(output_path, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")

    print(f"変換完了: {input_path} -> {output_path}")
    print(f"  出力行数: {len(output_lines)} 行")


def main():
    if len(sys.argv) != 3:
        print(f"使い方: python {sys.argv[0]} 入力ファイル.bes 出力ファイル.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.isfile(input_path):
        print(f"エラー: ファイルが見つかりません: {input_path}")
        sys.exit(1)

    convert_bes_to_unicode_braille(input_path, output_path)


if __name__ == "__main__":
    main()
