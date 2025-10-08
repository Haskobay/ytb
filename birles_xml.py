import xml.etree.ElementTree as ET
import requests

# ---- Ayarlar ----
url1 = "https://raw.githubusercontent.com/Haskobay/ytb/refs/heads/main/xml/radyo.xml"
url2 = "https://raw.githubusercontent.com/Haskobay/ixemel/refs/heads/main/izlecan.xml"

def fetch_xml(url):
    print(f"Fetching: {url}")
    r = requests.get(url)
    r.raise_for_status()
    return ET.fromstring(r.text)

def combine_xml(root1, root2):
    combined_root = ET.Element("medias")
    for media in root1.findall("media"):
        combined_root.append(media)
    for media in root2.findall("media"):
        combined_root.append(media)
    return combined_root

def save_xml(root, filename="combined.xml"):
    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"XML saved as {filename}")

if __name__ == "__main__":
    r1 = fetch_xml(url1)
    r2 = fetch_xml(url2)
    combined = combine_xml(r1, r2)
    save_xml(combined)
