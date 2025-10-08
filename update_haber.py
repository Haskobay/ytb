import os, requests, xmltodict

API_KEY = os.getenv("YT_API_KEY_HABER")
CHANNEL_FILE = "data/channels.txt"
XML_PATH = os.path.join(os.getcwd(), "xml", "haber.xml")  # absolute path

# Kanalları oku, sadece ID kısmı
with open(CHANNEL_FILE, "r", encoding="utf-8") as f:
    channels = [line.split()[0] for line in f if line.strip()]

media_items = []

for cid in channels:
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={cid}&eventType=live&type=video&key={API_KEY}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        for item in data.get("items", []):
            vid = item["id"]["videoId"]
            title = item["snippet"]["title"]
            thumb = item["snippet"]["thumbnails"]["high"]["url"]
            media_items.append({
                "title": title,
                "thumb": thumb,
                "type": "youtube",
                "src": vid
            })
    except Exception as e:
        print(f"⚠️ Kanal {cid} hatası: {e}")

# XML dizini yoksa oluştur
xml_dir = os.path.dirname(XML_PATH)
os.makedirs(xml_dir, exist_ok=True)

# XML yaz
try:
    xml_data = {"media": {"media": media_items}}
    xml_str = xmltodict.unparse(xml_data, pretty=True)
    with open(XML_PATH, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print("✅ XML yazıldı:", XML_PATH)
    print("Toplam video:", len(media_items))
except Exception as e:
    print("❌ XML yazma hatası:", e)
