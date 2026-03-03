# braille-misc-scripts 点字データを操作するためのスクリプトなど

## KGS社の.bmt形式の点字データをユニコード点字に変換するPythonスクリプト

KGS社の点字ディスプレイ「ブレイルメモスマート」シリーズで使用されている.bmt形式の点字データをユニコード点字に変換するPythonスクリプトです。

関係するスクリプトが2つあります。

1. bmt_to_unicode.py - .bmtファイルをユニコード点字のテキストファイルに変換します。8点のデータは、下付き8点になります。
2. braille_dot_shifter.py - ユニコード点字の7 8の点を1 4の点の上に移動します。下付き8点を上付き8点に変換します。

使い方:

> python bmt_to_unicode.py source.bmt

実行すると、source.txtというファイル名で、元の.bmtの内容をユニコード点字で出力します。

8点のデータの場合は、下付き8点の形で出力されます。

これをbraille_dot_shifter.pyで上付き8点に変換できます。

使い方:

> python braille_dot_shifter.py source.txt dest.txt

dest.txtは、Source.txtの7 8 の点が1 4の点の上に移動した、上付き8点のユニコードデータになっています。

## .bes形式点字データをユニコード点字に変換するPythonスクリプト
サピエ図書館の点字データは.bes形式です。

ブレイルメモスマートやブレイルセンスなどの点字ディスプレイで開いて読むことができます。

スクリーンリーダーNVDAやiOS/Mac OSのVoiceOverに点字ディスプレイを接続すると、ユニコード点字を、点字として表示できます。

.bes形式をユニコード点字に変換すると、特別なソフト・アプリがなくても、テキストエディタなどで開くことで点字を読むことができます。

.besからユニコード点字に変換するスクリプトをClaude AIに作ってもらいました。

* bes-to-unicode-braille.py

というスクリプトで、次のように使用します:

> python bes-to-unicode-braille.py input.bes output.txt

変換する.besファイルと、出力するユニコード点字ファイルの名前を引数で指定します。

## .bes形式点字データをNABCC(ASCII点字、.brf形式)データに変換するPythonスクリプト

.bes形式の点字データはサピエ図書館の点字データの形式です。

テクノツール社の「点字編集システム」で作成できる点字データ形式です。バイナリデータになっています。

- [点字編集システム | テクノツール株式会社](https://ttools.co.jp/product/eyes/BES/)

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

