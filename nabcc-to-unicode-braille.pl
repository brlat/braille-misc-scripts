# nabcc-to-unicode-braille.pl
# .bseや.brlなどのNABCCのファイルをUnicode点字に変換
# 使い方:
# .bseや.brlのファイルを、utf8のテキストファイルに変換する。
# 改行コードはUnix式に変換する。
# ファイル名をsource.txtにする。
# その後、nabcc-to-unicode-braille.plを引数無しで実行する
# 変換結果は result.txt に保存される

#!/usr/bin/perl
use strict;
use warnings;
use open IN  => ":utf8";
use open OUT => ":utf8";

open(my $SOURCEFILE, '<:utf8', './source.txt') or die "Cannot open source file: $!";
open(my $RESULTFILE, '>:utf8', './result.txt') or die "Cannot open result file: $!";

while (my $line = <$SOURCEFILE>) {
    $line =~ s/A/\N{U+2801}/g;
    $line =~ s/B/\N{U+2803}/g;
    $line =~ s/C/\N{U+2809}/g;
    $line =~ s/D/\N{U+2819}/g;
    $line =~ s/E/\N{U+2811}/g;
    $line =~ s/F/\N{U+280B}/g;
    $line =~ s/G/\N{U+281B}/g;
    $line =~ s/H/\N{U+2813}/g;
    $line =~ s/I/\N{U+280A}/g;
    $line =~ s/J/\N{U+281A}/g;
    $line =~ s/K/\N{U+2805}/g;
    $line =~ s/L/\N{U+2807}/g;
    $line =~ s/M/\N{U+280D}/g;
    $line =~ s/N/\N{U+281D}/g;
    $line =~ s/O/\N{U+2815}/g;
    $line =~ s/P/\N{U+280F}/g;
    $line =~ s/Q/\N{U+281F}/g;
    $line =~ s/R/\N{U+2817}/g;
    $line =~ s/S/\N{U+280E}/g;
    $line =~ s/T/\N{U+281E}/g;
    $line =~ s/U/\N{U+2825}/g;
    $line =~ s/V/\N{U+2827}/g;
    $line =~ s/X/\N{U+282D}/g;
    $line =~ s/Y/\N{U+283D}/g;
    $line =~ s/Z/\N{U+2835}/g;
    $line =~ s/&/\N{U+282F}/g;
    $line =~ s/=/\N{U+283F}/g;
    $line =~ s/\(/\N{U+2837}/g;
    $line =~ s/\!/\N{U+282E}/g;
    $line =~ s/\)/\N{U+283E}/g;
    $line =~ s/\*/\N{U+2821}/g;
    $line =~ s/</\N{U+2823}/g;
    $line =~ s/%/\N{U+2829}/g;
    $line =~ s/\?/\N{U+2839}/g;
    $line =~ s/:/\N{U+2831}/g;
    $line =~ s/\$/\N{U+282B}/g;
    $line =~ s/\]/\N{U+283B}/g;
    $line =~ s/\\/\N{U+2833}/g;
    $line =~ s/\[/\N{U+282A}/g;
    $line =~ s/W/\N{U+283A}/g;
    $line =~ s/1/\N{U+2802}/g;
    $line =~ s/2/\N{U+2806}/g;
    $line =~ s/3/\N{U+2812}/g;
    $line =~ s/4/\N{U+2832}/g;
    $line =~ s/5/\N{U+2822}/g;
    $line =~ s/6/\N{U+2816}/g;
    $line =~ s/7/\N{U+2836}/g;
    $line =~ s/8/\N{U+2826}/g;
    $line =~ s/9/\N{U+2814}/g;
    $line =~ s/0/\N{U+2834}/g;
    $line =~ s/\//\N{U+280C}/g;
    $line =~ s/\+/\N{U+282C}/g;
    $line =~ s/>/\N{U+281C}/g;
    $line =~ s/#/\N{U+283C}/g;
    $line =~ s/-/\N{U+2824}/g;
    $line =~ s/'/\N{U+2804}/g;
    $line =~ s/@/\N{U+2808}/g;
    $line =~ s/\^/\N{U+2818}/g;
    $line =~ s/\_/\N{U+2838}/g;
    $line =~ s/"/\N{U+2810}/g;
    $line =~ s/\./\N{U+2828}/g;
    $line =~ s/;/\N{U+2830}/g;
    $line =~ s/,/\N{U+2820}/g;

    print $RESULTFILE $line;
}

close $SOURCEFILE;
close $RESULTFILE;
