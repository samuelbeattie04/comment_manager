#Coursework 1 Guidlines
#pip install beautifulsoup4
#pip install requests
#pip install re

#task1
import requests
from bs4 import BeautifulSoup

# URL from which pdfs to be downloaded
base_url = ""
page_url = ""
# Requests URL and get response object
response = requests.get(f"{base_url}/{page_url}")
# Verify the url and status code
print(response.url)
print(response.status_code)

# Parse text obtained
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')
                      
pdf_alink_result = []
for link in pdf_links:
    if ('.pdf' in link.get('href')):
        pdf_alink_result.append(link['href'])
print(pdf_alink_result)

i = 0
for each in pdf_alink_result:
    i+=1
    # Get response object for link
    response = requests.get(f"{base_url}/{each}")
    # Write content in pdf file
    with open('task1_pdf_link.txt', 'w') as file:
        for pdf_link in pdf_links:
            file.write(pdf_link + '\n')