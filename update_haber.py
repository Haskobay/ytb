import os, requests, xmltodict

API_KEY = os.getenv("YT_API_KEY")
CHANNEL_FILE = "data/channels.txt"
XML_PATH = "xml/haber.xml"

def read_channels(path):
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
    r = requests.get(url)
    data = r.json()

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
    print("API anahtarı alındı mı:", bool(API_KEY))
    channels = read_channels(CHANNEL_FILE)
    print("Toplam kanal:", len(channels))

    media_items = []
    for cid in channels:
        videos = get_live_videos(cid.strip())
        print(f"Kanal {cid} için {len(videos)} canlı yayın bulundu.")
        media_items += videos

    # Eğer hiç video yoksa bile XML doğru şekilde oluşsun
    xml_data = {"medias": {"media": media_items}}
    xml_str = xmltodict.unparse(xml_data, pretty=True)

    os.makedirs(os.path.dirname(XML_PATH), exist_ok=True)
    with open(XML_PATH, "w", encoding="utf-8") as f:
        f.write(xml_str)
    print(f"{XML_PATH} dosyasına {len(media_items)} kayıt yazıldı.")

if __name__ == "__main__":
    main()
