import sys
import subprocess

def get_optimized_32page_signature(input_pages):
    """
    [New Feature] 4-sheet layer, 32-page signature base (Auto-scaling at the end)
    Basically, 4 sheets of paper make 32 pages. Depending on the remaining pages 
    of the last signature, it automatically scales down to a 16-page signature 
    (2 sheets) or an 8-page signature (1 sheet).
    """
    order = []
    current_page = 1
    remaining_pages = input_pages
    sig_count = 1
    
    # List to store navigation and warning text for each signature
    navigation_lines = []
    
    total_sheets = 0
    total_calculated_pages = 0

    while remaining_pages > 0:
        sig_size = 32
        sheets_in_sig = 4
        current_sig_name = "32-page signature (4 A4 sheets)"
        
        # Determine auto-scaling for the final signature
        if remaining_pages <= 24:
            if remaining_pages <= 8:
                sig_size = 8
                sheets_in_sig = 1
                current_sig_name = "8-page signature (1 A4 sheet)"
            elif remaining_pages <= 16:
                sig_size = 16
                sheets_in_sig = 2
                current_sig_name = "16-page signature (2 A4 sheets)"
            else:
                sig_size = 32
                sheets_in_sig = 4
                current_sig_name = "32-page signature (4 A4 sheets)"

        sig_start = current_page
        sig_end = current_page + sig_size - 1
        total_calculated_pages += sig_size

        # Create imposition navigation text
        if sig_size < 32:
            warn_msg = (
                f"\n" + "!" * 65 + "\n"
                f"[⚠️ PRINTING WARNING: Final Signature Size Reduced ⚠️]\n"
                f"The final signature (#{sig_count}) was automatically downsized due to low remaining pages.\n"
                f" -> Signature Type: {current_sig_name}\n"
                f" -> Target Pages  : Pages {sig_start} to {sig_end}\n"
                f" Please load exactly [ {sheets_in_sig} ] sheet(s) of A4 paper into the printer tray.\n"
                f"" + "!" * 65
            )
            navigation_lines.append(warn_msg)
        else:
            navigation_lines.append(f"Signature #{sig_count}: {current_sig_name} (Target: {sig_start}-{sig_end}p)")

        # Imposition calculation (4p front / 4p back per A4 sheet = 8 pages total)
        # Dynamic calculation of top/bottom jump width (quarter) based on sig_size to fix bugs
        quarter = sig_size // 4
        for sheet in range(sheets_in_sig):
            front_left = sig_end - (sheet * 2)
            front_right = sig_start + (sheet * 2)
            front_left_bottom = front_left - quarter
            front_right_bottom = front_right + quarter
            order.extend([front_left, front_right, front_left_bottom, front_right_bottom])
            
            back_left = sig_start + 1 + (sheet * 2)
            back_right = sig_end - 1 - (sheet * 2)
            back_left_bottom = back_left + quarter
            back_right_bottom = back_right - quarter
            order.extend([back_left, back_right, back_left_bottom, back_right_bottom])
            
        total_sheets += sheets_in_sig
        current_page += sig_size
        remaining_pages -= sig_size
        sig_count += 1
        
    added_blanks = total_calculated_pages - input_pages
    
    info_lines = [
        f"1. Number of input body pages: {input_pages} pages",
        f"2. Total pages required for binding: {total_calculated_pages} pages",
        f"3. Blank pages to add at the end: {added_blanks} page(s) (Please add this many blank pages to the end of your original PDF!)",
        f"4. Physical A4 sheets needed   : {total_sheets} sheets (Duplex / Print on long edge)",
        f"5. Binding instructions          : Fold each signature (groups of 4, 2, or 1 sheets) in half and nest them!",
        f"\n--- Signature Configurations & Printing Navigation ---"
    ]
    
    info_lines.extend(navigation_lines)
    
    return order, info_lines, "Adaptive 32-page based signature (4-sheet base with auto-optimization at the end)"


def get_16page_signature_v2(input_pages):
    """[For Oz / Volume 2] 16-page 1-signature (Set of 2 A4 sheets)"""
    total_pages = (input_pages + 15) // 16 * 16
    signatures = total_pages // 16
    sheets = signatures * 2
    pages_list = []
    
    for i in range(signatures):
        base = i * 16
        pages_list.extend([base+8, base+9, base+4, base+13])
        pages_list.extend([base+10, base+7, base+14, base+3])
        pages_list.extend([base+6, base+11, base+2, base+15])
        pages_list.extend([base+12, base+5, base+16, base+1])
    
    info = [
        f"1. Number of input pages      : {input_pages} pages",
        f"2. Total PDF pages required   : {total_pages} pages",
        f"3. Blank pages to add at end  : {total_pages - input_pages} page(s)",
        f"4. Physical A4 sheets needed  : {sheets} sheets (Duplex / Print on long edge)",
        f"5. Binding instructions        : Cut the 2-sheet set horizontally (top/bottom), then place the top stack onto the bottom stack!"
    ]
    return pages_list, info, "16-page signature (Cut-and-stack type / Oz Specification)"


def get_8page_signature(input_pages):
    """[For Volume 1] 8-page 1-signature (1 A4 sheet complete)"""
    total_pages = (input_pages + 7) // 8 * 8
    sheets = total_pages // 8
    pages_list = []
    for i in range(sheets):
        base = i * 8
        pages_list.extend([base+2, base+7, base+4, base+5, base+8, base+1, base+6, base+3])
    
    info = [
        f"1. Input: {input_pages}P", 
        f"2. Total PDF: {total_pages}P", 
        f"3. Blank pages to add at end: {total_pages - input_pages} page(s)",
        f"4. A4 sheets: {sheets} sheet(s)"
    ]
    return pages_list, info, "8-page signature"


def main():
    if len(sys.argv) < 2:
        print("Usage: python BookBinderPro.py [page_count] [option (--32p / --16p / --8p)]")
        print("* If no option is provided, it defaults to the 32p-based signature with auto-optimization.")
        return

    pages = int(sys.argv[1])
    opt = sys.argv[2] if len(sys.argv) > 2 else "--32p"

    if opt == "--8p":
        result, info_lines, name = get_8page_signature(pages)
    elif opt == "--16p":
        result, info_lines, name = get_16page_signature_v2(pages)
    else:
        result, info_lines, name = get_optimized_32page_signature(pages)

    result_str = ",".join(map(str, result))

    # --- Screen Output Section ---
    print(f"\n--- {name} Bookbinding Data ---")
    for line in info_lines:
        print(line)
    
    print(f"\nImposed Page Order (comma-separated):\n{result_str}")
    
    # Transfer to clipboard
    try:
        process = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True, text=True)
        process.communicate(input=result_str)
        print("\n" + "="*50)
        print("[OK] The above page sequence has been copied to your clipboard!")
        print("Print Settings: A4 Landscape / Duplex (Print on long edge) / 4up (4in1)")
        print("="*50)
    except:
        print("\n[INFO] Auto-copy to clipboard was skipped. Please copy the text sequence above manually.")

if __name__ == "__main__":
    main()