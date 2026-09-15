import json
import requests
from bs4 import BeautifulSoup

# Ambil data dari Pelindo
url = 'https://idpcs.pelindo.co.id/apex/f?p=167:14' # Ganti dengan URL target
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
# Contoh logika sederhana mengambil isi tabel
table_data = []
# ... (Proses ekstraksi HTML ke list/dictionary) ...

# Simpan hasil scraping ke file JSON
with open('data.json', 'w') as f:
    json.dump({"updated_at": "Terakhir diperbarui", "data": table_data}, f)
