
#!/usr/bin/env python3
import sys
from grammar_loader import load_grammar
from calc_transformer import CalcTransformer
from utils import printNode
from generator import Generator


args = sys.argv

# 文法の読み込み
parser = load_grammar("./calc_grammar.lark", start_rule="function")

# 入力ファイルの読み込み
text = open("./test.rs", encoding="utf-8", mode="r").read()

# 構文解析と結果の出力
try:
    tree = parser.parse(text)
    result = CalcTransformer().transform(tree)
    generator = Generator()
    generator.generate(result)
except Exception as e:
    print(f"エラーが発生しました: {e}")