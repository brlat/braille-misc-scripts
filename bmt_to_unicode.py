#!/usr/bin/env python3
"""
BMT形式の点字ファイルをUnicode点字テキストに変換するスクリプト

【.bmtファイル構造】
  ヘッダー: 128バイト (0x00〜0x7F)
    - オフセット 0x52: ページあたりの行数
    - オフセット 0x53: 行あたりの点字セル数
    - オフセット 0x7C: データ形式識別 (3 = 3バイトレコード形式, 0 = 1バイト形式)

  【データ形式1: 3バイトレコード形式 (ヘッダー 0x7C = 0x03)】
    各3バイト: [0x00][点字バイト][0x00]
    第2バイト（中央）が点字データ。第1・第3バイトは常に 0x00。

  【データ形式2: 1バイト形式 (ヘッダー 0x7C = 0x00)】
    1バイト = 1点字セル
    0x00 = 行区切り（この行の終端）
    0x80 = 空白点字セル (U+2800)
    0x01〜0x7F, 0x81〜0xFF = 点字セルデータ

【ビットマッピング (BMTバイト → Unicode U+2800+)】
  BMTビット4 → Unicodeビット0 (ドット1: 左列上段)
  BMTビット5 → Unicodeビット1 (ドット2: 左列中段)
  BMTビット6 → Unicodeビット2 (ドット3: 左列下段)
  BMTビット0 → Unicodeビット3 (ドット4: 右列上段)
  BMTビット1 → Unicodeビット4 (ドット5: 右列中段)
  BMTビット2 → Unicodeビット5 (ドット6: 右列下段)
  BMTビット7 → Unicodeビット6 (ドット7: 左列最下段・8点用)
  BMTビット3 → Unicodeビット7 (ドット8: 右列最下段・8点用)
"""

import sys
import os

HEADER_SIZE = 0x80  # 128バイト


def bmt_byte_to_unicode(bmt: int) -> str:
    """BMTの1バイト点字コードをUnicode点字文字に変換する"""
    u = 0
    u |= ((bmt >> 4) & 0x07)        # BMT bit4,5,6 → Unicode bit0,1,2 (ドット1,2,3)
    u |= ((bmt & 0x07) << 3)        # BMT bit0,1,2 → Unicode bit3,4,5 (ドット4,5,6)
    u |= ((bmt >> 7) & 0x01) << 6   # BMT bit7     → Unicode bit6     (ドット7)
    u |= ((bmt >> 3) & 0x01) << 7   # BMT bit3     → Unicode bit7     (ドット8)
    return chr(0x2800 + u)


def convert_bmt_to_unicode(input_path: str, output_path: str) -> int:
    """
    .bmtファイルをUnicode点字テキストファイルに変換する。

    Args:
        input_path:  変換元の.bmtファイルパス
        output_path: 出力先テキストファイルパス

    Returns:
        変換した点字セル数（行区切りを除く）
    """
    with open(input_path, 'rb') as f:
        data = f.read()

    if len(data) < HEADER_SIZE:
        raise ValueError(
            f"ファイルが小さすぎます: {len(data)}バイト (ヘッダー{HEADER_SIZE}バイト必要)"
        )

    header = data[:HEADER_SIZE]
    data_section = data[HEADER_SIZE:]
    record_size = header[0x7C]  # データ形式識別バイト

    lines = []

    if record_size == 3:
        # --- 3バイトレコード形式 ---
        # [0x00][点字バイト][0x00] の繰り返し
        # 中央の1バイトが点字データ
        num_chars = len(data_section) // 3
        for i in range(num_chars):
            bmt_byte = data_section[i * 3 + 1]
            lines.append(bmt_byte_to_unicode(bmt_byte))
        text = '\n'.join(lines)

    elif record_size == 2:
        # --- 2バイト形式 ---
        # 2バイトずつ処理: 各バイトが1点字セル、[0x00][0x00] が行区切り
        # 連続する [0x00][0x00] はページ区切り等の構造マーカーであり空白行を生成しない
        current_row: list[str] = []
        i = 0
        n = len(data_section)
        while i + 1 < n:
            b1 = data_section[i]
            b2 = data_section[i + 1]
            i += 2
            if b1 == 0x00 and b2 == 0x00:
                if current_row:
                    lines.append(''.join(current_row))
                    current_row = []
            else:
                for b in (b1, b2):
                    if b == 0x80:
                        current_row.append('\u2800')  # 空白点字セル (U+2800)
                    elif b != 0x00:
                        current_row.append(bmt_byte_to_unicode(b))
        if current_row:
            lines.append(''.join(current_row))
        text = '\n'.join(lines)

    else:
        # --- 1バイト形式 ---
        # 各バイトが1点字セル、0x00が行区切り、0x80が空白点字セル
        current_row: list[str] = []
        for b in data_section:
            if b == 0x00:
                line = ''.join(current_row)
                current_row = []
                if line or (lines and lines[-1] != ''):
                    lines.append(line)
            elif b == 0x80:
                current_row.append('\u2800')  # 空白点字セル (U+2800)
            else:
                current_row.append(bmt_byte_to_unicode(b))
        if current_row:
            lines.append(''.join(current_row))
        while lines and lines[-1] == '':
            lines.pop()
        text = '\n'.join(lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text + '\n')

    char_count = sum(1 for c in text if '\u2800' <= c <= '\u28ff')
    return char_count


def main():
    if len(sys.argv) < 2:
        print("使い方: python3 bmt_to_unicode.py <入力.bmt> [出力.txt]")
        print()
        print("  出力ファイル名を省略すると、入力ファイルと同じフォルダに")
        print("  入力ファイル名の拡張子を .txt に変えたファイルを作成します。")
        sys.exit(1)

    input_path = sys.argv[1]

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        base = os.path.splitext(input_path)[0]
        output_path = base + '.txt'

    if not os.path.isfile(input_path):
        print(f"エラー: ファイルが見つかりません: {input_path}", file=sys.stderr)
        sys.exit(1)

    count = convert_bmt_to_unicode(input_path, output_path)
    print(f"変換完了: {count}文字 → {output_path}")


if __name__ == '__main__':
    main()
