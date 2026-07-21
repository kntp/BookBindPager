import re
import sys
from pathlib import Path

# ----------------------------
# Remove Gutenberg header and footer
# ----------------------------
def remove_gutenberg_header_footer(text):
    start = re.search(r"\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK.* \*\*\*", text)
    end = re.search(r"\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK.* \*\*\*", text)

    if start and end:
        return text[start.end():end.start()]
    return text

# ----------------------------
# Normalize newline codes
# ----------------------------
def normalize_newlines(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")

# ----------------------------
# Restore wrapped lines back to paragraphs
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
            # Handle hyphenated word wrapping
            if buffer and buffer[-1].endswith("-"):
                buffer[-1] = buffer[-1][:-1] + stripped
            else:
                buffer.append(stripped)

    if buffer:
        paragraphs.append(" ".join(buffer))

    return paragraphs

# ----------------------------
# Remove extra spaces
# ----------------------------
def remove_extra_spaces(paragraphs):
    return [re.sub(r"\s+", " ", p).strip() for p in paragraphs]

# ----------------------------
# TXT Output (Customized version with empty line removal)
# ----------------------------
def paragraphs_to_txt(paragraphs):
    # Completely remove empty elements from the paragraph list
    paragraphs = [p for p in paragraphs if p]
    
    formatted_text = ""
    for i, p in enumerate(paragraphs):
        if i > 0:
            # Insert an empty line only before paragraphs starting with "CHAPTER" (for better readability in binding)
            # If you want to remove this space as well, delete the if statement below and simply use formatted_text += "\n"
            if p.upper().startswith("CHAPTER"):
                formatted_text += "\n\n"
            else:
                formatted_text += "\n"
        
        formatted_text += p
        
    return formatted_text

# ----------------------------
# Main process
# ----------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python format_gutenberg.py input.txt")
        return

    input_path = Path(sys.argv[1])

    # Output file name (Original name + _f.txt)
    output_txt_path = input_path.with_name(input_path.stem + "_f.txt")

    # Read file
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except UnicodeDecodeError:
        # Fallback in case UTF-8 decoding fails
        with open(input_path, "r", encoding="shift_jis") as f:
            text = f.read()

    # Processing pipeline
    text = normalize_newlines(text)
    text = remove_gutenberg_header_footer(text)

    paragraphs = merge_wrapped_lines(text)
    paragraphs = remove_extra_spaces(paragraphs)

    # Generate TXT output
    txt = paragraphs_to_txt(paragraphs)

    # Write to file
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(txt)

    print(f"Successfully formatted: {output_txt_path}")

if __name__ == "__main__":
    main()
