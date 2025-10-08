import os
import requests
import xmltodict

API_KEY = os.getenv("YT_API_KEY_HABER")
CHANNEL_FILE = "data/haber.txt"
XML_PATH = "xml/haber.xml"

if not API_KEY:
    raise ValueError("YT_API_KEY_HABER environment variable is not set!")

def read_channels(path):
    if not os.path.exists(path):
        print(f"[ERROR] Channel file not found: {path}")
        return []
    ids = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ids.append(line.split()[0])
    return ids

def get_live_videos(channel_id):
    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"
    )
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print(f"[ERROR] API returned {r.status_code} for channel {channel_id}")
            return []
        data = r.json()
    except requests.RequestException as e:
        print(f"[ERROR] Request failed for {channel_id}: {e}")
        return []

    results = []
    for item in data.get("items", []):
        vid = item["id"]["videoId"]
        title = item["snippet"]["title"]
        thumb = item["snippet"]["thumbnails"]["high"]["url"]
        results.append({
            "title": title,
            "thumb": thumb,
            "type": "youtube",
            "src": vid
        })
    return results

def main():
    channels = read_channels(CHANNEL_FILE)
    media_items = []
    for cid in channels:
        media_items += get_live_videos(cid.strip())

    # Eğer hiç canlı yayın yoksa mesaj ekle
    if not media_items:
        media_items.append({
            "title": "No live videos currently",
            "thumb": "",
            "type": "info",
            "src": ""
        })

    xml_data = {"media": {"media": media_items}}
    xml_str = xmltodict.unparse(xml_data, pretty=True)

    os.makedirs(os.path.dirname(XML_PATH), exist_ok=True)
    with open(XML_PATH, "w", encoding="utf-8") as f:
        f.write(xml_str)

    print(f"XML written to {XML_PATH} with {len(media_items)} items.")

if __name__ == "__main__":
    main()
