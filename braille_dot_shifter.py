
import sys

def get_transformed_braille_char(char: str) -> str:
    """
    Transforms a single Unicode braille character by shifting all dots one row down.
    Dots in the bottom row wrap around to the top row.

    If the character is not a braille pattern (U+2800-U+28FF), it's returned unchanged.

    Args:
        char: A single character string.

    Returns:
        The transformed braille character or the original character.
    """
    BRAILLE_BASE = 0x2800
    if not (BRAILLE_BASE <= ord(char) <= BRAILLE_BASE + 0xFF):
        return char

    offset = ord(char) - BRAILLE_BASE
    new_offset = 0

    # Standard Unicode Braille dot mapping (bit positions):
    # Dot 1: bit 0 (0x01) | Dot 4: bit 3 (0x08)
    # Dot 2: bit 1 (0x02) | Dot 5: bit 4 (0x10)
    # Dot 3: bit 2 (0x04) | Dot 6: bit 5 (0x20)
    # Dot 7: bit 6 (0x40) | Dot 8: bit 7 (0x80)

    # Left column dots: 1 -> 2, 2 -> 3, 3 -> 7, 7 -> 1 (wrap around)
    # If old Dot 7 is set (bit 6), set new Dot 1 (bit 0)
    if (offset >> 6) & 1:
        new_offset |= (1 << 0)
    # If old Dot 1 is set (bit 0), set new Dot 2 (bit 1)
    if (offset >> 0) & 1:
        new_offset |= (1 << 1)
    # If old Dot 2 is set (bit 1), set new Dot 3 (bit 2)
    if (offset >> 1) & 1:
        new_offset |= (1 << 2)
    # If old Dot 3 is set (bit 2), set new Dot 7 (bit 6)
    if (offset >> 2) & 1:
        new_offset |= (1 << 6)

    # Right column dots: 4 -> 5, 5 -> 6, 6 -> 8, 8 -> 4 (wrap around)
    # If old Dot 8 is set (bit 7), set new Dot 4 (bit 3)
    if (offset >> 7) & 1:
        new_offset |= (1 << 3)
    # If old Dot 4 is set (bit 3), set new Dot 5 (bit 4)
    if (offset >> 3) & 1:
        new_offset |= (1 << 4)
    # If old Dot 5 is set (bit 4), set new Dot 6 (bit 5)
    if (offset >> 4) & 1:
        new_offset |= (1 << 5)
    # If old Dot 6 is set (bit 5), set new Dot 8 (bit 7)
    if (offset >> 5) & 1:
        new_offset |= (1 << 7)

    return chr(BRAILLE_BASE + new_offset)

def main():
    """
    Main function to process the file.
    """
    if len(sys.argv) != 3:
        print("使用法: python braille_dot_shifter.py <入力ファイル名> <出力ファイル名>")
        print("例: python braille_dot_shifter.py totoro.bmt output.txt")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        with open(input_filename, 'r', encoding='utf-8') as f_in:
            content = f_in.read()
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_filename}' が見つかりません。")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: 入力ファイルの読み込み中にエラーが発生しました: {e}")
        sys.exit(1)

    # Transform the entire content character by character
    transformed_content = "".join(get_transformed_braille_char(c) for c in content)

    try:
        with open(output_filename, 'w', encoding='utf-8') as f_out:
            f_out.write(transformed_content)
    except Exception as e:
        print(f"エラー: 出力ファイルへの書き込み中にエラーが発生しました: {e}")
        sys.exit(1)

    print(f"変換が完了しました。結果を '{output_filename}' に保存しました。")

if __name__ == '__main__':
    main()
