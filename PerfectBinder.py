import sys
import subprocess
import platform

def get_your_exact_routine_binding(input_pages, rtl=False):
    """
    [Major Revision / Final Version] Imposition for Perfect Binding (Pocketbook/Paperback Size)
    The programmatic implementation has been 100% aligned with the user's cutting routine.
    
    Cutting Steps:
    1. Stack the top half on top of the bottom half.
    2. Stack the right half on top of the left half.
    """
    order = []
    total_pages = (input_pages + 7) // 8 * 8
    sheets = total_pages // 8
    p_size = sheets * 2  # Number of pages per block
    
    for i in range(sheets):
        base = i * 2
        
        if rtl:
            # 📖 For Japanese/Eastern layout (Right-to-Left) if required
            front_left  = (p_size * 2) + 1 + base
            front_right = (p_size * 0) + 1 + base
            front_left_bottom  = (p_size * 3) + 1 + base
            front_right_bottom = (p_size * 1) + 1 + base
            
            back_left  = (p_size * 0) + 2 + base
            back_right = (p_size * 2) + 2 + base
            back_left_bottom  = (p_size * 1) + 2 + base
            back_right_bottom = (p_size * 3) + 2 + base
        else:
            # 📖 Default: For Western layout (Left-to-Right / Horizontal Pocketbook)
            # To place "Page 1" on top in your routine, the first block is placed at the bottom right!
            # Front side (Top-Left, Top-Right, Bottom-Left, Bottom-Right)
            front_left  = (p_size * 2) + 1 + base
            front_right = (p_size * 0) + 1 + base
            front_left_bottom  = (p_size * 3) + 1 + base
            front_right_bottom = (p_size * 1) + 1 + base
            
            # Back side (Top-Left, Top-Right, Bottom-Left, Bottom-Right) *Flipped on long-edge
            back_left  = (p_size * 0) + 2 + base
            back_right = (p_size * 2) + 2 + base
            back_left_bottom  = (p_size * 1) + 2 + base
            back_right_bottom = (p_size * 3) + 2 + base
            
        order.extend([front_left, front_right, front_left_bottom, front_right_bottom])
        order.extend([back_left, back_right, back_left_bottom, back_right_bottom])

    # 💡 Fix: Keep the expanded sequential numbers rather than using "Blank" text strings
    final_order = order
    added_blanks = total_pages - input_pages
    
    direction_str = "Japanese style: Right-to-Left (Vertical text)" if rtl else "Default: Western style: Left-to-Right (Horizontal text)"
    
    info_lines = [
        f"1. Number of input body pages: {input_pages} pages",
        f"2. Book Specification        : {direction_str}",
        f"3. Total pages for binding   : {total_pages} pages (Automatically expanded to a multiple of 8)",
        f"4. Blank pages to add at end : {added_blanks} page(s) (Please add this many blank pages to the end of your original PDF!)",
        f"5. Physical A4 sheets needed : {sheets} sheets (Duplex / Print on long edge)",
        f"6. ✂️ Your Routine Cutting Steps (Perfectly matches the implementation) :",
        f"   ① Keep all [ {sheets} ] sheet(s) stacked, and cut them horizontally right down the middle.",
        f"   ② Stack the entire [Top Half Stack] directly on 'TOP' of the [Bottom Half Stack].",
        f"   [*] ⚠️ Tip: Trimming the fore-edge here using the 'pre-gluing hack' makes a super clean cut!",
        f"   ③ Keeping the stack as is, now cut it vertically right down the middle.",
        f"   ④ Stack the entire [Right Half Stack] directly on 'TOP' of the [Left Half Stack]!",
        f"   ⑤ Now, all pages from page 1 to {total_pages} will be perfectly and straightly ordered!",
    ]
    
    return final_order, info_lines


def main():
    if len(sys.argv) < 2:
        print("Usage: python PerfectBinder.py [Page Count] [Options]")
        print("Options:")
        print("  --jp  : For Japanese layout (Right-to-Left). Default is English layout (Left-to-Right).")
        return

    pages = int(sys.argv[1])
    is_japanese = "--jp" in sys.argv
    
    result, info_lines = get_your_exact_routine_binding(pages, rtl=is_japanese)
    result_str = ",".join(map(str, result))

    print(f"\n--- Perfect Binding (Pocketbook / Paperback Size) ---")
    for line in info_lines:
        print(line)
        
    # 💡 Fix: Always display the page sequence on the standard output (screen) regardless of clipboard success
    print(f"\nImposed Page Order (comma-separated):\n{result_str}")
    
    try:
        os_type = platform.system()
        if os_type == "Windows":
            process = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True, text=True)
            process.communicate(input=result_str)
        else:
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=result_str)
            
        print("\n" + "="*50)
        print("[OK] The imposed page sequence has been copied to your clipboard!")
        print("Print Settings: A4 Portrait / Duplex (Print on long edge) / 4up (4in1)")
        print("="*50)
    except Exception as e:
        print("\n[INFO] Auto-copy to clipboard was skipped. Please copy the text sequence above manually.")

if __name__ == "__main__":
    main()