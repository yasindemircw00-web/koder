from flask import Flask, render_template, request, jsonify
from nlu import IntentDetector
from generator import CodeGenerator
from config import MODEL_NLU, MODEL_CODE
import os

# Uygulamayı başlat
app = Flask(__name__)

# Model yollarını kontrol et ve gerekirse ayarla
nlu_model_path = MODEL_NLU
if not os.path.exists(nlu_model_path) and not nlu_model_path.startswith("dbmdz/"):
    # Yerel model dizini yoksa ve Hugging Face modeli değilse
    if os.path.exists("models/bert-base-turkish-cased"):
        nlu_model_path = "models/bert-base-turkish-cased"

# NLU ve Kod Üretici modüllerini yükle
nlu = IntentDetector(nlu_model_path)

# CodeGemma modeli varsa yükle
if os.path.exists(MODEL_CODE):
    coder = CodeGenerator()
else:
    coder = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    # data'nın None olma durumunu kontrol et
    if data is None:
        prompt = ''
    else:
        prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'Komut girilmedi'}), 400
    
    # NLU analizi
    intent, language = nlu.analyze(prompt)
    
    # Kod üretimi (eğer model yüklüyse)
    if coder:
        code = coder.generate_code(prompt, intent, language)
    else:
        code = "❌ CodeGemma modeli bulunamadı. Kod üretimi için 'models/CodeGemma-2B.Q4_K_M.gguf' dosyasını indirmeniz gerekiyor."
    
    return jsonify({
        'intent': intent,
        'language': language,
        'code': code
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)