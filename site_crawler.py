import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# Fungsi utama untuk melakukan crawling dari URL yang diberikan
def crawl(url, max_pages=50):
    visited = set() 
    adjacency_list = {}

    # Header User-Agent agar server mengenali permintaan berasal dari browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Fungsi rekursif untuk melakukan crawl pada halaman
    def crawl_page(page_url):
        if page_url in visited or len(visited) >= max_pages:
            return

        visited.add(page_url)
        print(f"Crawling: {page_url}")

        try:
            # Mengirim permintaan HTTP GET ke halaman
            response = requests.get(page_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            # Jika ada error saat mengambil halaman, cetak pesan error dan kembali
            print(f"Error fetching {page_url}: {e}")
            return

        # Parse konten HTML dari halaman dengan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        # Loop melalui semua elemen <a> dengan atribut href
        for link in soup.find_all('a', href=True):
            full_url = urljoin(page_url, link['href'])
            if 'alanwalker' in full_url and full_url not in visited:
                links.append(full_url)

        # Simpan daftar links sebagai nilai dari page_url dalam adjacency_list
        adjacency_list[page_url] = links

        # Lakukan crawling secara rekursif pada setiap link yang ditemukan
        for link in links:
            crawl_page(link)

    # Mulai crawling dari halaman awal
    crawl_page(url)

    # Simpan hasil crawling (adjacency_list) ke dalam file JSON
    with open('crawled_site_data.json', 'w') as f:
        json.dump(adjacency_list, f, indent=4)
    print(f"Saved crawled data to 'crawled_site_data.json'.")

# Jika file ini dijalankan langsung, mulai crawling dari URL yang ditentukan
if __name__ == "__main__":
    url_to_crawl = 'https://alanwalker.com/'
    crawl(url_to_crawl)
