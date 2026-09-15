import json
import datetime
import requests
from bs4 import BeautifulSoup

# URL Target Pelindo (Ganti dengan URL halaman/tabel yang ingin diambil jika berbeda)
URL_PELINDO = 'https://idpcs.pelindo.co.id/apex/f?p=167:14'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def scrape_pelindo():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
    output = {
        "updated_at": timestamp,
        "status": "success",
        "data_html": ""
    }

    try:
        response = requests.get(URL_PELINDO, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mencari tabel di dalam halaman Pelindo
        tables = soup.find_all('table')
        
        if tables:
            # Mengambil tabel pertama yang ditemukan
            output["data_html"] = str(tables[0])
        else:
            output["status"] = "warning"
            output["data_html"] = "<p>Tabel data tidak ditemukan pada halaman target.</p>"

    except Exception as e:
        output["status"] = "error"
        output["data_html"] = f"<p>Gagal mengambil data dari Pelindo: {str(e)}</p>"

    # Simpan hasil scraping ke file data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    scrape_pelindo()
