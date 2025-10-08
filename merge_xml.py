import xml.etree.ElementTree as ET
from datetime import datetime
import requests

# --- Kaynak XML dosyalarının URL'leri ---
urls = [
url1 = "https://raw.githubusercontent.com/Haskobay/ytb/refs/heads/main/xml/radyo.xml"
url2 = "https://raw.githubusercontent.com/Haskobay/ixemel/refs/heads/main/habertv.xml"
]

# --- XML dosyalarını indirip parse et ---
def fetch_xml(url):
    r = requests.get(url)
    r.raise_for_status()
    return ET.fromstring(r.text)

# --- Birleştirme işlemi ---
def merge_xml(sources):
    root = ET.Element("medialist")
    for src in sources:
        for media in src.findall("media"):
            root.append(media)
    return root

# --- XML dosyasını kaydet ---
def save_xml(root, filename="tum_listeler.xml"):
    tree = ET.ElementTree(root)
    with open(filename, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(root, encoding="utf-8"))
    print(f"✅ XML dosyası başarıyla oluşturuldu: {filename}")

# --- Ana işlem ---
def main():
    print("🔄 XML dosyaları indiriliyor ve birleştiriliyor...")
    sources = [fetch_xml(url) for url in urls]
    combined = merge_xml(sources)

    # Tarih bilgisini ekle
    info = ET.Comment(f"Oluşturulma zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    combined.insert(0, info)

    save_xml(combined, "tum_listeler.xml")

if __name__ == "__main__":
    main()
