import streamlit as st
import easyocr
import numpy as np
from PIL import Image, ImageOps

# Речник с вредни съставки и информация за тях [cite: 147, 253, 257, 261]
harmful_ingredients = {
    "E621": "Мононатриев глутамат (главоболие, сърцебиене)",
    "Е621": "Мононатриев глутамат (главоболие, сърцебиене)", # Кирилица
    "E407": "Карагенан (възможни възпаления в червата)",
    "Е407": "Карагенан (възможни възпаления в червата)",
    "E450": "Дифосфати (риск за костите и бъбреците)",
    "Е450": "Дифосфати (риск за костите и бъбреците)",
    "E250": "Натриев нитрит (риск от онкологични заболявания)",
    "Е250": "Натриев нитрит (риск от онкологични заболявания)",
    "палмово масло": "Високо съдържание на наситени мазнини",
    "palm oil": "High saturated fat content",
    "захар": "Висок гликемичен индекс",
    "sugar": "High glycemic index"
}

st.set_page_config(page_title="AI Анализатор на Храни", layout="centered")

st.title("🔍 ИИ Анализатор на етикети")
st.write("Качете снимка на етикет, за да проверите за вредни съставки.")

# Избор на език за OCR [cite: 61]
languages = st.multiselect("Изберете езици на етикета:", ["bg", "en"], default=["bg", "en"])

# Опции за качване: Файл или Камера [cite: 57, 62]
upload_option = st.radio("Изберете метод:", ("Качване на файл", "Снимка с камера"))

if upload_option == "Качване на файл":
    uploaded_file = st.file_uploader("Изберете изображение...", type=["jpg", "jpeg", "png"])
else:
    uploaded_file = st.camera_input("Направете снимка на етикета")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качен етикет', use_column_width=True)
    
    with st.spinner('Анализиране на текста... Моля, изчакайте.'):
        # Превръщане на изображението в масив за EasyOCR [cite: 76]
        img_array = np.array(image)
        
        # Инициализиране на OCR четеца [cite: 67, 68]
        reader = easyocr.Reader(languages)
        result = reader.readtext(img_array, detail=0)
        
        full_text = " ".join(result).lower()
        
        st.subheader("📋 Резултати от анализа:")
        
        found_harmful = []
        for ingredient, description in harmful_ingredients.items():
            if ingredient.lower() in full_text:
                found_harmful.append(f"⚠️ **{ingredient}**: {description}")
        
        if found_harmful:
            st.error("Открити са потенциално вредни съставки:")
            for item in found_harmful:
                st.write(item)
        else:
            st.success("Не са открити критични вредни съставки от нашия списък.")
            
        with st.expander("Виж разпознатия текст"):
            st.write(full_text)

# Инструкции за публикуване [cite: 124, 127]
# За да работи това, създайте файл 'requirements.txt' със следното съдържание:
# streamlit
# easyocr
# numpy
# Pillow
