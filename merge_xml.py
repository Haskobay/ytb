#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
from datetime import datetime

def merge_xml_files():
    # BURAYA BİRLEŞTİRİLECEK DOSYALARI YAZ
    input_files = [
        "https://raw.githubusercontent.com/Haskobay/ytb/refs/heads/main/xml/radyo.xml",    # ← BUNLARI KENDİ DOSYALARINLA DEĞİŞTİR
        "https://raw.githubusercontent.com/Haskobay/ixemel/refs/heads/main/habertv.xml",    # ← BUNLARI KENDİ DOSYALARINLA DEĞİŞTİR
    ]
    
    # BURAYA ÇIKTI DOSYASINI YAZ
    output_file = "merged.xml"  # ← BUNU İSTEDİĞİN İSİMLE DEĞİŞTİR
    
    # Var olan dosyaları bul
    existing_files = [f for f in input_files if os.path.exists(f)]
    
    if len(existing_files) < 2:
        print("En az 2 XML dosyası gerekli!")
        return False
    
    try:
        # İlk dosyayı temel al
        base_tree = ET.parse(existing_files[0])
        base_root = base_tree.getroot()
        
        # Diğer dosyaları birleştir
        for xml_file in existing_files[1:]:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for element in root:
                base_root.append(element)
        
        # Kaydet
        base_tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"✅ Dosyalar birleştirildi: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    merge_xml_files()
