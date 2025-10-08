import os
import requests
import xmltodict

API_KEY = os.getenv("YT_API_KEY_CANLI")
CHANNEL_FILE = "data/canli_kanallar.txt"
XML_PATH = "xml/canli.xml"

if not API_KEY:
    raise ValueError("YT_API_KEY_CANLI environment variable is not set!")

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

def get_videos(channel_id, event_type=None):
    """event_type: 'live', 'upcoming', veya None"""
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&type=video&key={API_KEY}"
    if event_type:
        url += f"&eventType={event_type}"
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print(f"[ERROR] API returned {r.status_code} for channel {channel_id}: {r.text}")
            return []
        data = r.json()
    except requests.RequestException as e:
        print(f"[ERROR] Request failed for channel {channel_id}: {e}")
        return []

    # Debug log: API yanıtını göster
    print(f"[DEBUG] Channel {channel_id} returned {len(data.get('items', []))} items for event_type={event_type}")

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
        # Hem live hem upcoming videoları al
        media_items += get_videos(cid.strip(), event_type="live")
        media_items += get_videos(cid.strip(), event_type="upcoming")

    if not media_items:
        media_items.append({
            "title": "No live or upcoming videos",
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
