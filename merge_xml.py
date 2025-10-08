import requests
import xml.etree.ElementTree as ET
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", nargs="+", required=True, help="Input XML URLs")
parser.add_argument("-o", "--output", required=True, help="Output file path")
args = parser.parse_args()

root = ET.Element("stations")

for url in args.input:
    print(f"Fetching {url}")
    r = requests.get(url)
    r.raise_for_status()
    xml_data = ET.fromstring(r.text)
    for media in xml_data.findall(".//media"):
        root.append(media)

timestamp = ET.Comment(f"Merged on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
root.insert(0, timestamp)

tree = ET.ElementTree(root)
tree.write(args.output, encoding="utf-8", xml_declaration=True)
print(f"✅ Merged XML saved to {args.output}")
