import json
import datetime
import requests
from bs4 import BeautifulSoup

# URL Target Pelindo
URL_PELINDO = 'https://idpcs.pelindo.co.id/apex/f?p=167:14'

# Header disesuaikan agar server Pelindo merespons dengan baris maksimal
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

# Parameter khusus Oracle APEX untuk memaksa menampilkan hingga 500/1000 baris
params = {
    'p167_max_rows': '1000',
    'pgR_max_rows': '1000',
    'pgR_min_row': '1'
}

def scrape_pelindo():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
    output = {
        "updated_at": timestamp,
        "status": "success",
        "data_html": ""
    }

    try:
        # Mengirim permintaan dengan parameter baris maksimum
        response = requests.get(URL_PELINDO, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mencari tabel utama di halaman Pelindo
        tables = soup.find_all('table')
        
        if tables:
            # Ambil tabel data (biasanya tabel dengan class 't-Report-report' atau tabel terbesar)
            target_table = None
            for table in tables:
                # Memilih tabel yang memiliki baris data lebih dari sekadar header
                if len(table.find_all('tr')) > 1:
                    target_table = table
                    break
            
            if target_table:
                output["data_html"] = str(target_table)
            else:
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
