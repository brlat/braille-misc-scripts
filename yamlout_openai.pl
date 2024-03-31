# yamlout.pl - Liblouis テーブルのチェック用のyamlファイルを作るためのスクリプト
# 自分でかいたyamlout_myself.plと、それをChatGPTで書き直してもらったyamlout_openai.plがあります
# 使い方は同じ
# source.txtに変換前の文字列を1行に1項目ずつ書く
# result.txtに変換後の点字パターンをsource.txtに対応するように書く
# yamlout.plを引数無し」で実行する
# 結果はout.yamlに出力される

use strict;
use warnings;
use open qw(:std :utf8);

my $source_file = "./source.txt";
my $result_file = "./result.txt";
my $yaml_file   = "./out.yaml";

open my $source_fh, '<', $source_file or die "Cannot open $source_file: $!";
open my $result_fh, '<', $result_file or die "Cannot open $result_file: $!";
open my $yaml_fh, '>', $yaml_file or die "Cannot open $yaml_file: $!";

while (defined(my $source = <$source_fh>) and defined(my $result = <$result_fh>)) {
    chomp($source);
    chomp($result);
    print $yaml_fh "  - [$source, $result]\n";
}

close $source_fh;
close $result_fh;
close $yaml_fh;
