#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os

def merge_xml_files():
    # BURAYA BİRLEŞTİRİLECEK 2 XML DOSYASINI YAZ
    file1 = "https://raw.githubusercontent.com/Haskobay/ytb/refs/heads/main/xml/radyo.xml"    # ← İlk dosya
    file2 = "https://raw.githubusercontent.com/Haskobay/ixemel/refs/heads/main/habertv.xml"    # ← İkinci dosya
    output_file = "merged.xml"  # ← Çıktı dosyası
    
    print("🟢 XML birleştirme başlıyor...")
    
    # Dosyalar var mı kontrol et
    if not os.path.exists(file1):
        print(f"❌ {file1} bulunamadı!")
        return False
    if not os.path.exists(file2):
        print(f"❌ {file2} bulunamadı!")
        return False
    
    try:
        # İlk dosyayı oku
        print(f"📖 Okunuyor: {file1}")
        tree1 = ET.parse(file1)
        root1 = tree1.getroot()
        
        # İkinci dosyayı oku
        print(f"📖 Okunuyor: {file2}")
        tree2 = ET.parse(file2)
        root2 = tree2.getroot()
        
        # İkinci dosyanın TÜM içeriğini birinciye ekle
        print("🔗 Dosyalar birleştiriliyor...")
        for element in root2:
            root1.append(element)
        
        # Kaydet
        print(f"💾 Kaydediliyor: {output_file}")
        tree1.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"✅ Başarılı! {output_file} oluşturuldu.")
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    merge_xml_files()
