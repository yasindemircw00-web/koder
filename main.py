from nlu import IntentDetector
from generator import CodeGenerator
from config import MODEL_NLU

def main():
    print("\n🚀 CodeAI başlatılıyor...")
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

if __name__ == "__main__":
    main()