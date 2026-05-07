import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Настройка на страницата
st.set_page_config(page_title="AI Анализатор на храни", page_icon="🧪")

# Речник с вредни добавки и описания [cite: 147-166, 253-264]
harmful_ingredients = {
    "E407": "Карагенан - може да предизвика възпаления и храносмилателни проблеми [cite: 148, 257-260].",
    "E621": "Натриев глутамат - подсилвател на вкуса, може да причини главоболие [cite: 150, 261-264].",
    "E250": "Натриев нитрит - консервант, свързан с риск от онкологични заболявания[cite: 158].",
    "E450": "Дифосфати - могат да нарушат калциевия баланс и да увредят бъбреците [cite: 253-256].",
    "E952": "Цикламат - изкуствен подсладител[cite: 160].",
    "E262": "Натриев ацетат - може да дразни стомаха[cite: 152].",
    "E330": "Лимонена киселина - в големи количества уврежда зъбния емайл[cite: 156].",
    "E102": "Тартразин - синтетичен оцветител[cite: 88].",
    "E133": "Брилянтно синьо - синтетичен оцветител[cite: 98].",
    "ПАЛМОВО": "Палмово масло - често съдържа наситени мазнини, вредни за сърцето[cite: 59].",
    "ЗАХАР": "Високо съдържание на захар - риск от диабет и затлъстяване."
}

st.title("🧪 Как ИИ помага да разберем храната") [cite: 1-4]
st.write("Качете снимка на етикет, за да проверим за вредни съставки.") [cite: 57, 190]

# Качване на файл или снимка от камера [cite: 57, 62]
uploaded_file = st.file_uploader("Изберете изображение...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качен етикет', use_container_width=True) [cite: 73-75]
    
    # Инициализиране на EasyOCR за български и английски [cite: 61, 67-72]
    reader = easyocr.Reader(['bg', 'en'])
    
    with st.spinner('ИИ анализира етикета...'): [cite: 30-31]
        img_array = np.array(image) [cite: 76]
        result = reader.readtext(img_array)
        
        # Сортиране на текста отгоре-надолу (по Y координата), за да не се бъркат колоните
        result.sort(key=lambda x: x[0][0][1])
        
        # Събиране на разпознатия текст
        detected_text = " ".join([res[1] for res in result])
        
        st.subheader("Разпознат текст:")
        st.info(detected_text)
        
        # Проверка за вредни съставки [cite: 59]
        found_issues = []
        for key, description in harmful_ingredients.items():
            if key.upper() in detected_text.upper():
                found_issues.append(f"⚠️ **{key}**: {description}")
        
        # Показване на резултатите [cite: 60, 240-245]
        st.subheader("Анализ на съставките:")
        if found_issues:
            for issue in found_issues:
                st.error(issue)
        else:
            st.success("Не са открити вредни Е-номера или съставки от нашия списък.") [cite: 241]

    # Бутон за изтегляне на отчет [cite: 251-252]
    st.download_button("Изтегли отчет (.txt)", detected_text, file_name="label_report.txt")
