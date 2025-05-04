import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# API anahtarını yükle
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_recipe(materials: list[str]) -> dict:
    """
    Verilen malzemeleri kullanarak bir tarif oluşturur.
    
    Args:
        materials: Kullanılacak malzemelerin listesi
        
    Returns:
        Oluşturulan tarifin detayları
    """
    # Kullanılabilir modelleri listele
    available_models = genai.list_models()
    print("Kullanılabilir modeller:")
    for model in available_models:
        print(f"- {model.name}")
    
    # Gemini modelini başlat
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    # Malzemeleri virgülle ayırarak stringe çevir
    materials_str = ", ".join(materials)
    
    # Prompt oluştur
    prompt = f"""
    Aşağıdaki malzemeleri kullanarak bir yemek tarifi oluştur:
    Malzemeler: {materials_str}
    
    Lütfen şu formatta bir tarif oluştur:
    1. Tarifin adı
    2. Kısa bir açıklama
    3. Malzemeler listesi (verilen malzemeleri kullan)
    4. Adım adım yapılışı
    
    Tarifi Türkçe olarak ver.
    """
    
    # Tarifi oluştur
    response = model.generate_content(prompt)
    
    # Yanıtı işle
    recipe_text = response.text
    
    # Yanıtı parçalara ayır
    parts = recipe_text.split("\n\n")
    
    # Tarif detaylarını oluştur
    recipe = {
        "title": parts[0].strip(),
        "description": parts[1].strip() if len(parts) > 1 else "",
        "instructions": "\n".join(parts[2:]).strip(),
        "materials": materials
    }
    
    return recipe 