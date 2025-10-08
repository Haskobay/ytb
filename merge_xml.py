import xml.etree.ElementTree as ET
import requests

# GitHub'daki XML dosyalarının ham linkleri
url1 = "https://raw.githubusercontent.com/Haskobay/ytb/refs/heads/main/xml/radyo.xml"
url2 = "https://raw.githubusercontent.com/Haskobay/ixemel/refs/heads/main/habertv.xml"

# XML'leri çek
resp1 = requests.get(url1)
resp2 = requests.get(url2)

root1 = ET.fromstring(resp1.text)
root2 = ET.fromstring(resp2.text)

# Yeni root oluştur
combined_root = ET.Element("medias")

# list1’den tüm <media> ekle
for media in root1.findall("media"):
    combined_root.append(media)

# list2’den tüm <media> ekle
for media in root2.findall("media"):
    combined_root.append(media)

# Yeni XML dosyası oluştur
tree = ET.ElementTree(combined_root)
tree.write("combined.xml", encoding="utf-8", xml_declaration=True)

print("İki liste birleştirildi ve combined.xml olarak artifact olarak saklanacak.")
