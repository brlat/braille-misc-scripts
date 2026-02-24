# braille-misc-scripts
点字データを操作するためのスクリプトなど

## ASCII点字(NABCC点字)とユニコード点字を変換するPythonスクリプト

日本で使われている.bseや.brlや、アメリカなどで使われている.brfはASCII点字(NABCC点字)で、アルファベットや記号に点字を割り当てたテキストファイルです。

例えばABCFIがアルファベットの「abcfi」または日本点字の「あいうえお」の点字に対応しています。

(サピエ図書館の点字データの.besはNABCCではなく、独自のバイナリデータです)

ユニコード点字は⠁⠃⠉⠙⠑⠋⠛⠊⠚のようなものです。

これらを変換するPythonスクリプトをClaudeに作ってもらいました。

1. nabcc-to-unicode-braille.py - NABCCからユニコード点字に変換
2. unicode-braille-tonabcc.py - ユニコード点字からNABCCに変換

使い方:

python nabcc-tounicode-braille.py source.brl dest.txt

python unicode-braille-tonabcc.py source.txt dest.brl


## nabcc-to-unicode-braille.pl - .bseや.brlなどのNABCC点字ファイルをUnicode点字のテキストファイルに変換するperlスクリプト

使い方:

.bseや.brlのファイルを、utf8のテキストファイルに変換する。

改行コードはUnix式に変換する。

ファイル名をsource.txtにする。

その後、nabcc-to-unicode-braille.plを引数無しで実行する

変換結果は result.txt に保存される

