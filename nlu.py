from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

class IntentDetector:
    def __init__(self, model_path):
        print("🧠 Türkçe NLU modeli yükleniyor...")
        
        # Model dosyasının varlığını kontrol et
        if not os.path.exists(model_path) and not model_path.startswith("dbmdz/"):
            # Yerel model dizini yoksa ve Hugging Face modeli değilse
            if not os.path.exists("models/bert-base-turkish-cased"):
                print("❌ BERT modeli bulunamadı!")
                print("💡 Çözüm: 'models/bert-base-turkish-cased' klasörüne https://huggingface.co/dbmdz/bert-base-turkish-cased modelini indirin.")
                self.tokenizer = None
                self.model = None
                return
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            print("✅ NLU modeli hazır!")
        except Exception as e:
            print(f"❌ NLU modeli yüklenirken hata oluştu: {e}")
            print("💡 Çözüm: Model dosyalarının doğru yerde olduğundan emin olun veya internet bağlantınızı kontrol edin.")
            self.tokenizer = None
            self.model = None

    def analyze(self, text):
        # Eğer model yüklenmemişse, varsayılan değerleri döndür
        if self.tokenizer is None or self.model is None:
            lower = text.lower()
            
            # Basit dil tespiti
            if "python" in lower:
                lang = "Python"
            elif "html" in lower:
                lang = "HTML"
            elif "css" in lower:
                lang = "CSS"
            elif "javascript" in lower or "js" in lower:
                lang = "JavaScript"
            else:
                lang = "Python"

            # Niyet belirleme
            if any(x in lower for x in ["kod", "program", "örnek", "tasarla", "oluştur"]):
                intent = "kod_isteği"
            else:
                intent = "bilgi_sorgusu"

            return intent, lang
        
        lower = text.lower()

        # Basit dil tespiti
        if "python" in lower:
            lang = "Python"
        elif "html" in lower:
            lang = "HTML"
        elif "css" in lower:
            lang = "CSS"
        elif "javascript" in lower or "js" in lower:
            lang = "JavaScript"
        else:
            lang = "Python"

        # Niyet belirleme
        if any(x in lower for x in ["kod", "program", "örnek", "tasarla", "oluştur"]):
            intent = "kod_isteği"
        else:
            intent = "bilgi_sorgusu"

        return intent, lang