# Yerel Türkçe Kod Üretici AI

Bu proje, tamamen offline çalışan, Türkçe anlayan ve Python/HTML/CSS/JavaScript kodu üretebilen bir yapay zeka sistemidir.

## Özellikler

- Tamamen offline çalışır
- Türkçe komutları anlar
- Python, HTML, CSS ve JavaScript kodu üretir
- Açık kaynak modeller kullanır (CodeGemma, BERT)

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

2. Modelleri indirin:
   - `models/bert-base-turkish-cased` klasörüne [dbmdz/bert-base-turkish-cased](https://huggingface.co/dbmdz/bert-base-turkish-cased) modelini indirin
   - `models/CodeGemma-2B.Q4_K_M.gguf` dosyasını [TheBloke/CodeGemma-2B-GGUF](https://huggingface.co/TheBloke/CodeGemma-2B-GGUF) adresinden indirin

## Kullanım

```
python main.py
```

## Örnek Komutlar

- "bana python'da basit hesap makinesi kodu yaz"
- "basit bir html form tasarla"
- "css ile buton tasarla"
- "javascript ile todo list uygulaması yap"

## Dosya Yapısı

```
koder/
│
├── main.py                # Ana kontrol akışı
├── nlu.py                 # Türkçe anlama
├── generator.py           # CodeGemma modeliyle kod üretimi
├── config.py              # Model yolları ve ayarlar
├── requirements.txt       # Gerekli kütüphaneler
├── README.md              # Bu dosya
└── models/                # Modellerin saklandığı klasör
    ├── bert-base-turkish-cased/
    └── CodeGemma-2B.Q4_K_M.gguf
```