from pathlib import Path
from pypdf import PdfMerger

# Folder containing PDFs
pdf_folder = Path("task3")
output_pdf = pdf_folder / "combined_output.pdf"

# Get all PDFs in the folder
pdf_files = sorted(pdf_folder.glob("*.pdf"))

# Ensure there are PDFs to merge
if not pdf_files:
    print("No PDFs found in task3 folder.")
    exit(1)

# Merge PDFs
merger = PdfMerger()
for pdf in pdf_files:
    merger.append(str(pdf))
    print(f"Added: {pdf.name}")

# Save merged PDF
merger.write(str(output_pdf))
merger.close()

print(f"Merged PDF saved as {output_pdf}")