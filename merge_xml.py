#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
import sys

def merge_xml_files():
    # BURAYA BİRLEŞTİRİLECEK DOSYALARI YAZ
    input_files = [
        "https://raw.githubusercontent.com/Haskobay/ytb/refs/heads/main/xml/radyo.xml",    # ← BUNLARI KENDİ DOSYALARINLA DEĞİŞTİR
        "https://raw.githubusercontent.com/Haskobay/ixemel/refs/heads/main/habertv.xml",    # ← BUNLARI KENDİ DOSYALARINLA DEĞİŞTİR
    ]
    
    # BURAYA ÇIKTI DOSYASINI YAZ
    output_file = "merged.xml"  # ← BUNU İSTEDİĞİN İSİMLE DEĞİŞTİR
    
    print("🟢 XML birleştirme başlıyor...")
    print(f"📁 Çalışma dizini: {os.getcwd()}")
    print(f"📁 Mevcut dosyalar: {os.listdir('.')}")
    
    # Var olan dosyaları bul
    existing_files = [f for f in input_files if os.path.exists(f)]
    print(f"🔍 Bulunan XML dosyaları: {existing_files}")
    
    if len(existing_files) < 2:
        print("❌ En az 2 XML dosyası gerekli!")
        # Test için örnek dosyalar oluştur
        print("🛠️ Test dosyaları oluşturuluyor...")
        with open("file1.xml", "w") as f:
            f.write('<?xml version="1.0"?><root><item id="1">Test1</item></root>')
        with open("file2.xml", "w") as f:
            f.write('<?xml version="1.0"?><root><item id="2">Test2</item></root>')
        existing_files = ["file1.xml", "file2.xml"]
    
    try:
        # İlk dosyayı temel al
        print(f"📖 Temel dosya: {existing_files[0]}")
        base_tree = ET.parse(existing_files[0])
        base_root = base_tree.getroot()
        
        # Diğer dosyaları birleştir
        for xml_file in existing_files[1:]:
            print(f"➕ Birleştiriliyor: {xml_file}")
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for element in root:
                base_root.append(element)
        
        # Kaydet - KESİN ÇÖZÜM
        print(f"💾 Kaydediliyor: {output_file}")
        
        # XML declaration ile kaydet
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            base_tree.write(f, encoding='unicode')
        
        print(f"✅ Yazma işlemi tamamlandı: {output_file}")
        
        # KONTROL
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"📄 Çıktı dosyası oluşturuldu: {output_file}")
            print(f"📏 Dosya boyutu: {file_size} byte")
            
            # İçeriği göster (ilk 500 karakter)
            with open(output_file, 'r') as f:
                content = f.read(500)
                print(f"📝 İçerik (ilk 500 karakter):\n{content}")
        else:
            print("❌ Çıktı dosyası oluşturulamadı!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = merge_xml_files()
    sys.exit(0 if success else 1)
