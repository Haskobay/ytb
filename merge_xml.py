#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
import subprocess

def merge_xml_files():
    # BURAYA BİRLEŞTİRİLECEK DOSYALARI YAZ
    file1 = "https://raw.githubusercontent.com/Haskobay/ytb/refs/heads/main/xml/radyo.xml"
    file2 = "https://raw.githubusercontent.com/Haskobay/ixemel/refs/heads/main/habertv.xml"
    output_file = "merged.xml"
    
    print("=== XML BİRLEŞTİRME BAŞLIYOR ===")
    print(f"Çalışma dizini: {os.getcwd()}")
    print(f"Mevcut dosyalar: {os.listdir('.')}")
    
    # Dosya kontrolü
    if not os.path.exists(file1):
        print(f"HATA: {file1} bulunamadı!")
        return False
    if not os.path.exists(file2):
        print(f"HATA: {file2} bulunamadı!")
        return False
    
    print(f"✅ {file1} bulundu")
    print(f"✅ {file2} bulundu")
    
    try:
        # Dosyaları oku
        tree1 = ET.parse(file1)
        root1 = tree1.getroot()
        tree2 = ET.parse(file2)
        root2 = tree2.getroot()
        
        print(f"📊 {file1} root: {root1.tag}")
        print(f"📊 {file2} root: {root2.tag}")
        
        # Birleştirme
        for element in root2:
            root1.append(element)
        
        print(f"🔗 Birleştirme tamamlandı")
        
        # DOSYA YAZMA - 3 FARKLI YÖNTEM
        print(f"💾 Dosyaya yazılıyor: {output_file}")
        
        # Yöntem 1: Direkt write
        tree1.write(output_file, encoding='utf-8', xml_declaration=True)
        print("✅ Yöntem 1: write() tamamlandı")
        
        # Kontrol
        if os.path.exists(output_file):
            size = os.path.getsize(output_file)
            print(f"✅ DOSYA OLUŞTU: {output_file} ({size} byte)")
            
            # İçeriği göster
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read(200)
                print(f"📝 İlk 200 karakter:\n{content}")
        else:
            print("❌ DOSYA OLUŞMADI!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    merge_xml_files()
