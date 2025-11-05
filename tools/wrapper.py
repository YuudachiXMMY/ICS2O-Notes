import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_relative_assets(base_url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all(['a', 'img'])
    for tag in tags:
        href = tag.get('href') or tag.get('src')
        if not href or href.startswith('http') or href.startswith('//'):
            continue
        file_url = urljoin(base_url, href)
        file_path = os.path.join(output_dir, href)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print(f"Downloading {href}...")
        try:
            file_data = requests.get(file_url)
            file_data.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(file_data.content)
        except Exception as e:
            print(f"Failed to download {href}: {e}")
    print("All relative files and images downloaded successfully.")

# Example usage:
# download_files("https://example.com/files/", "./files")
download_relative_assets("http://www.gorskicompsci.ca/ICD2O.html", "./")