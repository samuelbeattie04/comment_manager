import requests
from bs4 import BeautifulSoup
from pathlib import Path

# URL of the webpage containing PDF links (replace with actual URL)
base_url = "https://example.com"
page_url = "index.html"

# Request the webpage
response = requests.get(f"{base_url}/{page_url}")
if response.status_code != 200:
    print(f"Failed to retrieve page. Status: {response.status_code}")
    exit(1)

# Parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Extract PDF links
pdf_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith(".pdf"):
        pdf_links.append(f"{base_url}/{href}")

# Save links to a file
output_file = Path("task1/task1_pdf_link.txt")
output_file.parent.mkdir(exist_ok=True)  # Ensure the folder exists

with output_file.open("w") as file:
    for link in pdf_links:
        file.write(link + '\n')

print(f"Saved {len(pdf_links)} PDF links to {output_file}")