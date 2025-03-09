#pip install pathlib
#pip install pypdf
#task3
from pathib import Path
import pypdf


pdf_merger = PdfMerger()
pdf_merger.append(Path(base_path)/"combined.pdf")
page1_path = Path(base_path)/"pdf1.pdf"
pdf_merger.merge(0, page1_path)
pdf_merger.write("combined_output.pdf")