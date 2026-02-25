# braille-misc-scripts 点字データを操作するためのスクリプトなど

## .bes形式点字データをNABCC(ASCII点字、.brf形式)データに変換するPythonスクリプト

.bes形式の点字データはサピエ図書館の点字データの形式です。

テクノツール社の「点字編集システム」で作成できる点字データ形式です。バイナリデータになっています。

- [点字編集システム | テクノツール株式会社]https://ttools.co.jp/product/eyes/BES/()

他の点字データ形式、.bseや.brl、.brfなどは、NABCCまたはASCII点字と呼ばれる、アルファベットや記号を点字に対応させたデータで、テキストファイルになっています。

この.bes点字データをNABCC(ASCII点字、.brf形式)に変換するPythonスクリプトを、Claude AIに作ってもらいました。

* bes-to-brf.py

というスクリプトで、次のように変換したい.besファイルを引数に指定すると、.brf形式に変換したファイルを出力します。

> python bes-tobrf.py sample.bes

まだうまく変換できないところがあると思います。
例えば、.besには見出し行の設定などがありますが、その行がどう出力されるかはまだ確認していません。

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

