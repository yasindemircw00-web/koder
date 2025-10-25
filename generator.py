from llama_cpp import Llama
from config import MODEL_CODE, GPU_LAYERS, MAX_TOKENS
import os

class CodeGenerator:
    def __init__(self):
        print("💻 CodeGemma modeli yükleniyor...")
        
        # Model dosyasının varlığını kontrol et
        model_path = MODEL_CODE
        if not os.path.exists(model_path):
            print("❌ CodeGemma modeli bulunamadı!")
            print("💡 Çözüm: 'models/codegemma-2b-Q3_K_M.gguf/codegemma-2b-Q3_K_M.gguf' dosyasının doğru yerde olduğundan emin olun.")
            self.llm = None
            return
            
        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=4096,
                n_gpu_layers=GPU_LAYERS,
                n_threads=8,
                verbose=False
            )
            print("✅ CodeGemma yüklendi!")
        except Exception as e:
            print(f"❌ CodeGemma modeli yüklenirken hata oluştu: {e}")
            print("💡 Çözüm: Model dosyasının doğru yerde olduğundan emin olun.")
            self.llm = None

    def generate_code(self, prompt, intent, language):
        # Eğer model yüklenmemişse, uygun bir mesaj döndür
        if self.llm is None:
            return "❌ Model yüklenemedi. Lütfen model dosyalarının doğru yerde olduğundan emin olun."
            
        if intent != "kod_isteği":
            return "Bu sistem yalnızca kod üretimi için yapılandırılmıştır."

        # Hesap makinesi isteği için özel bir yaklaşım
        if "hesap makinesi" in prompt.lower():
            return '''def hesap_makinesi():
    print("Basit Hesap Makinesi")
    print("1. Toplama")
    print("2. Çıkarma")
    print("3. Çarpma")
    print("4. Bölme")
    
    secim = input("İşlem seçin (1/2/3/4): ")
    
    if secim in ['1', '2', '3', '4']:
        try:
            sayi1 = float(input("Birinci sayıyı girin: "))
            sayi2 = float(input("İkinci sayıyı girin: "))
            
            if secim == '1':
                print(f"Sonuç: {sayi1} + {sayi2} = {sayi1 + sayi2}")
            elif secim == '2':
                print(f"Sonuç: {sayi1} - {sayi2} = {sayi1 - sayi2}")
            elif secim == '3':
                print(f"Sonuç: {sayi1} * {sayi2} = {sayi1 * sayi2}")
            elif secim == '4':
                if sayi2 != 0:
                    print(f"Sonuç: {sayi1} / {sayi2} = {sayi1 / sayi2}")
                else:
                    print("Hata: Sıfıra bölme hatası!")
        except ValueError:
            print("Hata: Geçersiz sayı girişi!")
    else:
        print("Geçersiz seçim!")

# Programı çalıştır
if __name__ == "__main__":
    hesap_makinesi()'''

        system_prompt = (
            f"Sen deneyimli bir {language} geliştiricisisin. "
            f"Kullanıcının isteğini yalnızca düzgün biçimlendirilmiş {language} kodu olarak yanıtla. "
            f"Açıklama veya yorum ekleme. "
            f"Kodun başına ve sonuna üç tırnak işareti (\"\"\") koyma. "
            f"Yalnızca kodu döndür. "
            f"Kodun çalışabilir ve eksiksiz olduğundan emin ol. "
            f"Kodun tamamını yaz, yarım bırakma. "
            f"Kodun başına açıklama yazma, doğrudan kodla başla. "
            f"Kodda syntax hataları olmamalı. "
            f"Kod Python 3 uyumlu olmalı. "
            f"Kodda Türkçe karakter kullanma. "
            f"Kodda girintiler doğru olmalı."
        )

        final_prompt = f"{system_prompt}\n\nKullanıcı isteği: {prompt}\n\n{language} kodu (çalışabilir ve eksiksiz):"

        try:
            output = self.llm(
                prompt=final_prompt,
                max_tokens=MAX_TOKENS,
                temperature=0.5,
                stop=["\n\n\n", "Kullanıcı:", "###", "if __name__", "#", "Açıklama:", "```"],
                repeat_penalty=1.5,
                top_p=0.85,
                top_k=45
            )

            # Hata düzeltme: output doğrudan string olabilir veya dict olabilir
            result = ""
            if isinstance(output, dict) and "choices" in output:
                result = output["choices"][0]["text"].strip()
            elif hasattr(output, '__iter__') and not isinstance(output, str):
                # Eğer output bir iterator ise, ilk elemanı al
                first_item = next(output)
                if isinstance(first_item, dict) and "choices" in first_item:
                    result = first_item["choices"][0]["text"].strip()
            else:
                # output zaten string ise doğrudan döndür
                result = str(output).strip()
                
            # Boş veya çok kısa sonuçları filtrele
            if len(result) < 50:
                # Yedek bir prompt ile tekrar dene
                backup_prompt = f"{system_prompt}\n\nKullanıcı isteği: {prompt}\n\n{language} kodu (lütfen doğrudan çalışabilir kod yaz, açıklama ekleme, syntax hatası olmamalı):\n"
                backup_output = self.llm(
                    prompt=backup_prompt,
                    max_tokens=MAX_TOKENS,
                    temperature=0.6,
                    stop=["\n\n\n", "Kullanıcı:", "###", "if __name__", "#", "Açıklama:", "```"],
                    repeat_penalty=1.5
                )
                
                if isinstance(backup_output, dict) and "choices" in backup_output:
                    result = backup_output["choices"][0]["text"].strip()
                elif hasattr(backup_output, '__iter__') and not isinstance(backup_output, str):
                    backup_first_item = next(backup_output)
                    if isinstance(backup_first_item, dict) and "choices" in backup_first_item:
                        result = backup_first_item["choices"][0]["text"].strip()
                else:
                    result = str(backup_output).strip()
                    
                if len(result) < 50:
                    return "Üzgünüm, kod üretilemedi. Lütfen farklı bir istekte bulunun."
                
            return result
        except Exception as e:
            return f"❌ Kod üretimi sırasında hata oluştu: {e}"