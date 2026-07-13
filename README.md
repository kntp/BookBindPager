# BookBindPager - DIY Bookbinding Page Imposition Tool

A versatile Python-based page imposition and ordering tool designed for 
DIY bookbinding. Whether you are crafting a traditional hardcover book 
with folded signatures or a clean paperback with perfect binding, this 
tool calculates and generates the exact page sequences you need for 
seamless printing.

Perfect for pocketbooks (Bunko), paperbacks, hardcovers, and self-publishing creators!


------------------------------------------------------------------------
✨ Features
------------------------------------------------------------------------

1. Two Core Imposition Modes:
   
   - Perfect Binding Mode (PerfectBinder.py):
     Tailored for standard paperback/pocketbook glue binding. Fully 
     aligned with a practical manual cutting routine. Supports both 
     Left-to-Right (Western) and Right-to-Left (Japanese/Eastern 
     vertical text) layouts.
   
   - Book Signature Mode (BookBinderPro.py):
     Tailored for multi-sheet folded signatures (ideal for thread-sewn 
     hardcovers). Includes a smart 32-page adaptive scaling feature 
     that automatically handles leftover pages at the end of the book 
     by downsizing to 16-page or 8-page booklets.

2. Auto-Calculates Blank Pages:
   Automatically determines how many padding blank pages you need to 
   append to your original PDF to fit the signatures perfectly.

3. Clipboard Integration:
   Automatically copies the final comma-separated page sequence to your 
   clipboard for quick pasting into PDF imposition tools (like Adobe 
   Acrobat, PDF24, or CLI utilities).


------------------------------------------------------------------------
🚀 How It Works & Cutting Routines
------------------------------------------------------------------------

### 1. Perfect Binding Mode (PerfectBinder.py)
This script optimizes pages for A4 portrait printing (4 pages per sheet, 
double-sided) and aligns 100% with a highly efficient manual cutting routine:

1. Print on A4 Portrait, Duplex (Flip on long edge), 4up (4-in-1 layout).
2. Cut horizontally right down the middle while keeping the entire stack together.
3. Stack the entire top half directly on TOP of the bottom half.
4. *(Optional Hack: Trim the fore-edge here using a pre-gluing technique for ultra-clean edges)*
5. Cut vertically right down the middle.
6. Stack the entire right half directly on TOP of the left half.
7. Done! Your book is now perfectly ordered from page 1 to the end, ready for gluing.


### 2. Book Signature Mode (BookBinderPro.py)
Optimized for A4 landscape printing (8 pages per sheet, double-sided) to 
create folded booklets (signatures):

- 32-Page Base (Default): Folds groups of 4 nested A4 sheets. It automatically 
  scales down to 16-page (2 sheets) or 8-page (1 sheet) booklets at the end 
  to prevent wasting paper.
- 16-Page Mode (--16p): Folds 2 sheets with a cut-and-stack routine.
- 8-Page Mode (--8p): 1-sheet complete signature layout.


------------------------------------------------------------------------
💻 Usage
------------------------------------------------------------------------

Run the scripts via command line by passing the total page count of your document.

### Perfect Binding

[Command for Western Layout (Left-to-Right)]
python PerfectBinder.py [page_count]

[Example for a Japanese vertical-text novel (Right-to-Left)]
python PerfectBinder.py 120 --jp


### Book Signatures (Hardcover / Folded)

[Default: Adaptive 32-page signatures]
python BookBinderPro.py [page_count]

[16-page signatures (Cut-and-stack type)]
python BookBinderPro.py 120 --16p

[8-page signatures (1 sheet complete)]
python BookBinderPro.py 120 --8p


### Recommended Print Settings
To ensure the output sequences match your physical paper layout, apply 
these settings in your PDF print dialog:

- Paper Size: A4
- Orientation: Landscape (for BookBinderPro) / Portrait (for PerfectBinder)
- Duplex: Two-sided printing (Flip on Long Edge)
- Page Layout: 4 pages per sheet (4up / 4-in-1)


------------------------------------------------------------------------
🛠️ Requirements
------------------------------------------------------------------------

- Python 3.x
- Windows or Linux/macOS (For clipboard integration, Linux users may 
  need xclip installed)


------------------------------------------------------------------------
📄 License
------------------------------------------------------------------------

This project is open-source and available under the MIT License.
========================================================================
README.txt
「README.txt」を表示しています。