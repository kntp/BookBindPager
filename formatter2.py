import re
import sys
from pathlib import Path

# ----------------------------
# Gutenberg前後の削除
# ----------------------------
def remove_gutenberg_header_footer(text):
    start = re.search(r"\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK.* \*\*\*", text)
    end = re.search(r"\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK.* \*\*\*", text)

    if start and end:
        return text[start.end():end.start()]
    return text

# ----------------------------
# 改行コード統一
# ----------------------------
def normalize_newlines(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")

# ----------------------------
# 行折り返しを段落に戻す
# ----------------------------
def merge_wrapped_lines(text):
    lines = text.split("\n")
    paragraphs = []
    buffer = []

    for line in lines:
        stripped = line.strip()

        if stripped == "":
            if buffer:
                paragraphs.append(" ".join(buffer))
                buffer = []
        else:
            # ハイフン分割対応
            if buffer and buffer[-1].endswith("-"):
                buffer[-1] = buffer[-1][:-1] + stripped
            else:
                buffer.append(stripped)

    if buffer:
        paragraphs.append(" ".join(buffer))

    return paragraphs

# ----------------------------
# 余分な空白削除
# ----------------------------
def remove_extra_spaces(paragraphs):
    return [re.sub(r"\s+", " ", p).strip() for p in paragraphs]

# ----------------------------
# TXT出力（空行削除カスタマイズ版）
# ----------------------------
def paragraphs_to_txt(paragraphs):
    # 段落リストから空の要素を完全に除去
    paragraphs = [p for p in paragraphs if p]
    
    formatted_text = ""
    for i, p in enumerate(paragraphs):
        if i > 0:
            # 章（CHAPTER）で始まる段落の前だけ1行空ける（製本時の視認性のため）
            # もしここも詰めたければ、下の if 文を消して単に formatted_text += "\n" にしてください
            if p.upper().startswith("CHAPTER"):
                formatted_text += "\n\n"
            else:
                formatted_text += "\n"
        
        formatted_text += p
        
    return formatted_text

# ----------------------------
# メイン処理
# ----------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python format_gutenberg.py input.txt")
        return

    input_path = Path(sys.argv[1])

    # 出力ファイル名（元のファイル名 + _f.txt）
    output_txt_path = input_path.with_name(input_path.stem + "_f.txt")

    # 読み込み
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except UnicodeDecodeError:
        # 万が一UTF-8で失敗した場合の予備
        with open(input_path, "r", encoding="shift_jis") as f:
            text = f.read()

    # 処理パイプライン
    text = normalize_newlines(text)
    text = remove_gutenberg_header_footer(text)

    paragraphs = merge_wrapped_lines(text)
    paragraphs = remove_extra_spaces(paragraphs)

    # TXT出力生成
    txt = paragraphs_to_txt(paragraphs)

    # 書き出し
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(txt)

    print(f"Successfully formatted: {output_txt_path}")

if __name__ == "__main__":
    main()
