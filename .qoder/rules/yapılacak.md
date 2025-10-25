---
trigger: manual
---
🎯 AMAÇ:
Tamamen offline çalışan, Türkçe anlayan ve Python / HTML kod üretebilen yerel yapay zekâ sistemi oluştur.

🚀 GEREKSİNİMLER:
1️⃣ Kodlama dili: Python 3.10+
2️⃣ Model: CodeGemma-2B-Q4_K_M (GGUF sürümü)
3️⃣ Türkçe anlama: dbmdz/bert-base-turkish-cased
4️⃣ Kütüphaneler: transformers, torch, llama-cpp-python
5️⃣ Her şey offline çalışacak. Hugging Face modelleri ilk çalışmada indirilecek ve `models/` klasöründe saklanacak.
6️⃣ Sistem komut satırından çalışacak ve kullanıcıdan Türkçe istek alacak:
   - “bana python’da basit hesap makinesi kodu yaz”
   - “basit bir html form yap”
   - “css ile buton tasarla”
7️⃣ Yalnızca düzgün formatlı kod döndürecek. Açıklama veya yorum olmayacak.

📦 DOSYA YAPISI:
YeniAI/
│
├── main.py                # Ana kontrol akışı
├── nlu.py                 # Türkçe anlama
├── generator.py           # CodeGemma modeliyle kod üretimi
├── config.py              # Model yolları ve ayarlar
├── requirements.txt
└── models/
    ├── bert-base-turkish/
    └── CodeGemma-2B.Q4_K_M.gguf

⚙️ GÖREVLER:
1. Yukarıdaki yapıyı oluştur.
2. Aşağıdaki kodları dosyalara yerleştir:

────────────────────────────
📄 requirements.txt
────────────────────────────
transformers
torch
llama-cpp-python
────────────────────────────

📄 config.py
────────────────────────────
MODEL_NLU = "models/bert-base-turkish-cased"
MODEL_CODE = "models/CodeGemma-2B.Q4_K_M.gguf"
GPU_LAYERS = 20
MAX_TOKENS = 800
────────────────────────────

📄 nlu.py
────────────────────────────
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class IntentDetector:
    def __init__(self, model_path):
        print("🧠 Türkçe NLU modeli yükleniyor...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        print("✅ NLU modeli hazır!")

    def analyze(self, text):
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
────────────────────────────

📄 generator.py
────────────────────────────
from llama_cpp import Llama
from config import MODEL_CODE, GPU_LAYERS, MAX_TOKENS

class CodeGenerator:
    def __init__(self):
        print("💻 CodeGemma modeli yükleniyor...")
        self.llm = Llama(
            model_path=MODEL_CODE,
            n_ctx=4096,
            n_gpu_layers=GPU_LAYERS,
            n_threads=8,
            verbose=False
        )
        print("✅ CodeGemma yüklendi!")

    def generate_code(self, prompt, intent, language):
        if intent != "kod_isteği":
            return "Bu sistem yalnızca kod üretimi için yapılandırılmıştır."

        system_prompt = (
            f"Sen deneyimli bir {language} geliştiricisisin. "
            f"Kullanıcının isteğini yalnızca düzgün biçimlendirilmiş {language} kodu olarak yanıtla. "
            f"Açıklama veya yorum ekleme."
        )

        final_prompt = f"{system_prompt}\n\nKullanıcı isteği: {prompt}\n\n{language} kodu:\n"

        output = self.llm(
            prompt=final_prompt,
            max_tokens=MAX_TOKENS,
            temperature=0.6,
            stop=["Kullanıcı:"]
        )

        return output["choices"][0]["text"].strip()
────────────────────────────

📄 main.py
────────────────────────────
from nlu import IntentDetector
from generator import CodeGenerator
from config import MODEL_NLU

nlu = IntentDetector(MODEL_NLU)
coder = CodeGenerator()

print("\n🚀 CodeAI başlatıldı (Offline). Kod üretmek için komut yazın ('exit' ile çık):\n")

while True:
    query = input("💬 Komut: ")
    if query.lower() in ["exit", "çık", "quit"]:
        print("👋 Görüşmek üzere!")
        break

    intent, lang = nlu.analyze(query)
    print(f"🧩 Dil: {lang} | Niyet: {intent}")

    code = coder.generate_code(query, intent, lang)
    print("\n💻 Üretilen Kod:\n")
    print(code)
    print("\n" + "-"*60 + "\n")
────────────────────────────

📦 MODEL İNDİRME ADIMLARI (otomatik veya el ile):
────────────────────────────
mkdir models
cd models

# Türkçe anlama modeli
git clone https://huggingface.co/dbmdz/bert-base-turkish-cased

# CodeGemma modeli (1.1 GB)
wget https://huggingface.co/TheBloke/CodeGemma-2B-GGUF/resolve/main/CodeGemma-2B.Q4_K_M.gguf -O CodeGemma-2B.Q4_K_M.gguf
cd ..

────────────────────────────

✅ TAMAMLANINCA TEST:
python main.py

💬 Örnek sorgular:
- "bana python'da basit hesap makinesi kodu yaz"
- "basit bir html form tasarla"
────────────────────────────