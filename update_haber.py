import os, requests, xmltodict

API_KEY = os.getenv("YT_API_KEY_HABER")  # Haber key
CHANNEL_FILE = "data/channels.txt"
XML_PATH = "xml/haber.xml"

# Kanalları oku
with open(CHANNEL_FILE, "r", encoding="utf-8") as f:
    channels = [line.strip() for line in f if line.strip() and not line.startswith("#")]

media_items = []

# Her kanal için canlı videoları çek
for cid in channels:
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={cid}&eventType=live&type=video&key={API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
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

# XML’e yaz
xml_data = {"media": {"media": media_items}}
xml_str = xmltodict.unparse(xml_data, pretty=True)

os.makedirs(os.path.dirname(XML_PATH), exist_ok=True)
with open(XML_PATH, "w", encoding="utf-8") as f:
    f.write(xml_str)
