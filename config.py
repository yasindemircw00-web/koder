# Model yollarını güncelleyelim
MODEL_NLU = "models/bert-base-turkish-cased"

# CodeGemma modeli için doğru yolu kullan
MODEL_CODE = "models/codegemma-2b-Q3_K_M.gguf/codegemma-2b-Q3_K_M.gguf"

GPU_LAYERS = 20
MAX_TOKENS = 800
# Eğer modeller bulunamazsa, yerel modelleri kullan
import os

# BERT modeli için tam yol
if os.path.exists("models/bert-base-turkish-cased/config.json"):
    MODEL_NLU = "models/bert-base-turkish-cased"
else:
    # Hugging Face model adı (online erişim gerektirir)
    MODEL_NLU = "dbmdz/bert-base-turkish-cased"

# CodeGemma modeli için tam yol
if not os.path.exists(MODEL_CODE):
    # Eğer yerel dosya yoksa, indirilmesi gerektiğini belirt
    MODEL_CODE = "models/CodeGemma-2B.Q4_K_M.gguf"

