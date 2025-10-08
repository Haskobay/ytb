import os
import requests
import xmltodict

API_KEY = os.getenv("YT_API_KEY_HABER")
CHANNEL_FILE = "data/haber.txt"
XML_PATH = "xml/haber.xml"

if not API_KEY:
    raise ValueError("YT_API_KEY_HABER environment variable is not set!")

def read_channels(path):
    ids = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ids.append(line.split()[0])
    except FileNotFoundError:
        print(f"Channel file not found: {path}")
    return ids

def get_live_videos(channel_id):
    url = (
        f"https://www.googleapis.com/youtube/v3/search?"
        f"part=snippet&channelId={channel_id}&eventType=live&type=video&key={API_KEY}"
    )
    try:
        r = requests.get(url)
        if r.status_code != 200:
            print(f"Failed to fetch channel {channel_id}: {r.status_code} {r.text}")
            return []
        data = r.json()
    except requests.RequestException as e:
        print(f"Request failed for channel {channel_id}: {e}")
        return []

    items = data.get("items", [])
    if not items:
        print(f"No live videos found for channel {channel_id}")

    results = []
    for item in items:
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
    if not channels:
        print("No channels found in the file.")
        return

    media_items = []
    for cid in channels:
        media_items += get_live_videos(cid.strip())

    if not media_items:
        print("No live videos found for any channel. XML will be empty.")

    xml_data = {"mediaList": {"media": media_items}}
    xml_str = xmltodict.unparse(xml_data, pretty=True)

    os.makedirs(os.path.dirname(XML_PATH), exist_ok=True)
    with open(XML_PATH, "w", encoding="utf-8") as f:
        f.write(xml_str)

    print(f"XML written to {XML_PATH} with {len(media_items)} items.")

if __name__ == "__main__":
    main()
