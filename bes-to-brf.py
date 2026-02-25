#!/usr/bin/env python3
"""
BES to BRF converter
BESファイル（点字バイナリ形式）をBRFファイル（点字テキスト形式）に変換するスクリプト。

■ BESファイル構造
  [0x000〜0x0FF] ヘッダー部1（テキスト情報 + フィラー）
  [0x100〜0x1FF] ヘッダー部2（0xFF×3 + テキスト + フィラー）
  [0x200〜0x3FF] ヘッダー部3（フィラー）
  [0x400〜     ] データセクション（点字データ本体）

■ データセクション内のバイト種別
  0xFF             : ページ開始マーカー（直後に2バイトのページ情報が続く）
  0xFD             : 行データ開始マーカー
  0xFE             : 行データ終端マーカー（改行を出力）
  0x0D             : キャリッジリターン（無視）
  0xA0             : 点字スペース（空白セル）
  0xA1〜0xDF       : 点字文字（下位6ビットが点のパターン）

■ BESの点字バイトエンコード
  byte = 0xA0 + pattern  (pattern: 0〜63)
  pattern のビット: bit0=点1, bit1=点2, bit2=点3, bit3=点4, bit4=点5, bit5=点6

■ BRFエンコード（Braille Ready Format）
  点字文字を印刷可能なASCII文字（0x20〜0x5F）で表現する。
  変換テーブルは BESパターン → BRF文字コードのマッピングで定義。
"""

import sys
import os

# ----------------------------------------------------------------
# BESパターン(0〜63) → BRF文字コードの変換テーブル
# pattern = BESバイト - 0xA0
# ----------------------------------------------------------------
BES_PATTERN_TO_BRF = {
     0: 0x20,  # スペース（点なし）
     1: 0x41,  # A  (点1)
     2: 0x31,  # 1  (点2)
     3: 0x42,  # B  (点1,2)
     4: 0x27,  # シングルクォート  (点3)
     5: 0x4B,  # K  (点1,3)
     6: 0x32,  # 2  (点2,3)
     7: 0x4C,  # L  (点1,2,3)
     8: 0x40,  # アットマーク  (点4)
     9: 0x43,  # C  (点1,4)
    10: 0x49,  # I  (点2,4)
    11: 0x46,  # F  (点1,2,4)
    12: 0x2F,  # スラッシュ  (点3,4)
    13: 0x4D,  # M  (点1,3,4)
    14: 0x53,  # S  (点2,3,4)
    15: 0x50,  # P  (点1,2,3,4)
    16: 0x22,  # ダブルクォート  (点5)
    17: 0x45,  # E  (点1,5)
    18: 0x33,  # 3  (点2,5)
    19: 0x48,  # H  (点1,2,5)
    20: 0x39,  # 9  (点3,5)
    21: 0x4F,  # O  (点1,3,5)
    22: 0x36,  # 6  (点2,3,5)
    23: 0x52,  # R  (点1,2,3,5)
    24: 0x5E,  # キャレット  (点4,5)
    25: 0x44,  # D  (点1,4,5)
    26: 0x4A,  # J  (点2,4,5)
    27: 0x47,  # G  (点1,2,4,5)
    28: 0x3E,  # 大なり  (点3,4,5)
    29: 0x4E,  # N  (点1,3,4,5)
    30: 0x54,  # T  (点2,3,4,5)
    31: 0x51,  # Q  (点1,2,3,4,5)
    32: 0x2C,  # カンマ  (点6)
    33: 0x2A,  # アスタリスク  (点1,6)
    34: 0x35,  # 5  (点2,6)
    35: 0x3C,  # 小なり  (点1,2,6)
    36: 0x2D,  # ハイフン  (点3,6)
    37: 0x55,  # U  (点1,3,6)
    38: 0x38,  # 8  (点2,3,6)
    39: 0x56,  # V  (点1,2,3,6)
    40: 0x2E,  # ピリオド  (点4,6)
    41: 0x25,  # パーセント  (点1,4,6)
    42: 0x5B,  # 開き角かっこ  (点2,4,6)
    43: 0x24,  # ドルマーク  (点1,2,4,6)
    44: 0x2B,  # プラス  (点3,4,6)
    45: 0x58,  # X  (点1,3,4,6)
    46: 0x21,  # エクスクラメーション  (点2,3,4,6)
    47: 0x26,  # アンパサンド  (点1,2,3,4,6)
    48: 0x3B,  # セミコロン  (点5,6)
    49: 0x3A,  # コロン  (点1,5,6)
    50: 0x34,  # 4  (点2,5,6)
    51: 0x5C,  # バックスラッシュ  (点1,2,5,6)
    52: 0x30,  # 0  (点3,5,6)
    53: 0x5A,  # Z  (点1,3,5,6)
    54: 0x37,  # 7  (点2,3,5,6)
    55: 0x28,  # 開き丸かっこ  (点1,2,3,5,6)
    56: 0x5F,  # アンダースコア  (点4,5,6)
    57: 0x3F,  # クエスチョン  (点1,4,5,6)
    58: 0x57,  # W  (点2,4,5,6)
    59: 0x5D,  # 閉じ角かっこ  (点1,2,4,5,6)
    60: 0x23,  # シャープ  (点3,4,5,6)
    61: 0x59,  # Y  (点1,3,4,5,6)
    62: 0x29,  # 閉じ丸かっこ  (点2,3,4,5,6)
    63: 0x3D,  # イコール  (全点: 点1,2,3,4,5,6)
}

# BES データセクションの開始オフセット
DATA_OFFSET = 0x400

# 制御バイト
BYTE_PAGE_START   = 0xFF  # ページ開始（直後に2バイトのページ情報）
BYTE_LINE_HEADER  = 0xFD  # 行データ開始
BYTE_LINE_END     = 0xFE  # 行データ終端（改行）
BYTE_CR           = 0x0D  # キャリッジリターン（無視）
BYTE_SPACE        = 0xA0  # 点字スペース
BRAILLE_MIN       = 0xA0  # 点字バイトの最小値


def convert_bes_to_brf(input_path: str, output_path: str) -> None:
    """BESファイルをBRFファイルに変換する。"""

    with open(input_path, "rb") as f:
        data = f.read()

    if len(data) < DATA_OFFSET:
        raise ValueError(
            f"ファイルサイズが小さすぎます（{len(data)} バイト）。"
            f"BESファイルはデータセクションが 0x{DATA_OFFSET:04X} から始まる必要があります。"
        )

    section = data[DATA_OFFSET:]
    output_lines = []
    current_line = bytearray()

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
            # 行データ終端: 行末の余分なスペースを除いて出力
            line_bytes = bytes(current_line).rstrip(b' ')
            output_lines.append(line_bytes)
            current_line = bytearray()
            i += 1
            continue

        elif b == BYTE_CR:
            # CR: 無視
            i += 1
            continue

        elif b >= BRAILLE_MIN:
            # 点字バイト（スペースを含む）
            pattern = b - BRAILLE_MIN  # 0〜63
            brf_code = BES_PATTERN_TO_BRF.get(pattern, 0x3F)  # 不明は '?'
            current_line.append(brf_code)
            i += 1
            continue

        else:
            # その他のバイトは無視
            i += 1
            continue

    # 末尾に残った行があれば追加
    if current_line:
        output_lines.append(bytes(current_line).rstrip(b' '))

    # BRF出力: 行を CRLF で結合
    with open(output_path, "wb") as f:
        for line in output_lines:
            f.write(line + b"\r\n")

    print(f"変換完了: {input_path} -> {output_path}")
    print(f"  出力行数: {len(output_lines)} 行")


def main():
    if len(sys.argv) < 2:
        print("使い方: python bes_to_brf.py <input.bes> [output.brf]")
        print("  output.brf を省略した場合は input と同じ名前で .brf を生成します。")
        sys.exit(1)

    input_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        base = os.path.splitext(input_path)[0]
        output_path = base + ".brf"

    if not os.path.isfile(input_path):
        print(f"エラー: ファイルが見つかりません: {input_path}")
        sys.exit(1)

    convert_bes_to_brf(input_path, output_path)


if __name__ == "__main__":
    main()