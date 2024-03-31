# yamlout.pl - Liblouis テーブルのチェック用のyamlファイルを作るためのスクリプト
# 自分でかいたyamlout_myself.plと、それをChatGPTで書き直してもらったyamlout_openai.plがあります
# 使い方は同じ
# source.txtに変換前の文字列を1行に1項目ずつ書く
# result.txtに変換後の点字パターンをsource.txtに対応するように書く
# yamlout.plを引数無し」で実行する
# 結果はout.yamlに出力される

use open IN  => ":utf8";
use open OUT => ":utf8";

open(SOURCEFILE, '<./source.txt');
open(RESULTFILE, '<./result.txt');
open(YAMLFILE, '>./out.yaml');

while($source = <SOURCEFILE> and $result = <RESULTFILE>){
chomp($source);
chomp($result);

print YAMLFILE ("  - [$source, $result]\n");
}
