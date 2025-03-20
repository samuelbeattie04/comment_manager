import requests
from pathlib import Path

# Folder to save PDFs
download_folder = Path("task2")
download_folder.mkdir(exist_ok=True)

# Path to the file containing PDF links
links_file = download_folder / "task2_pdf_link.txt"

# Read PDF links from the file
if not links_file.exists():
    print("Error: task2_pdf_link.txt not found.")
    exit(1)

with links_file.open("r") as file:
    pdf_links = [line.strip() for line in file if line.strip()]

# Download each PDF
for pdf_link in pdf_links:
    pdf_name = Path(pdf_link).name  # Get filename from URL
    pdf_path = download_folder / pdf_name

    response = requests.get(pdf_link)
    if response.status_code == 200:
        pdf_path.write_bytes(response.content)
        print(f"Downloaded: {pdf_name}")
    else:
        print(f"Failed to download: {pdf_link} (Status {response.status_code})")

print("Task 2 complete.")