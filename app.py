import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Настройка на заглавието и темата
st.set_page_config(page_title="AI Food Chemist", page_icon="🧪")

# Речник с вредни съставки за проверка
harmful_ingredients = {
    "E407": "Карагенан - може да причини възпаления и стомашни проблеми [cite: 827, 936-939].",
    "E621": "Натриев глутамат - подсилвател на вкуса, може да причини главоболие [cite: 828, 940-943].",
    "E250": "Натриев нитрит - консервант, риск от онкологични заболявания [cite: 836-837].",
    "E450": "Дифосфати - риск за бъбреците и костите при прекомерна консумация [cite: 880, 932-935].",
    "E952": "Цикламат - подсладител [cite: 838-840, 911].",
    "E262": "Натриев ацетат - дразни стомаха [cite: 830-831].",
    "E330": "Лимонена киселина - уврежда зъбния емайл [cite: 834-835].",
    "E300": "Аскорбинова киселина - в големи дози дразни стомаха [cite: 832-833].",
    "ЗАХАР": "Високо съдържание на захар - риск от затлъстяване и диабет.",
    "ПАЛМОВО": "Палмово масло - съдържа вредни наситени мазнини."
}

st.title("🧪 Как ИИ помага да разберем храната") [cite: 680-683]
st.write("Качете снимка на етикет, за да открием вредните добавки.")

uploaded_file = st.file_uploader("Изберете изображение на етикет...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качен етикет', use_container_width=True)
    
    # Инициализиране на EasyOCR [cite: 746-751]
    reader = easyocr.Reader(['bg', 'en'])
    
    with st.spinner('Анализиране на съставките...'):
        img_array = np.array(image)
        result = reader.readtext(img_array)
        
        # Сортиране на текста отгоре-надолу, за да не се смесват колоните
        result.sort(key=lambda x: x[0][0][1])
        
        detected_text = " ".join([res[1] for res in result])
        
        st.subheader("Разпознат текст:")
        st.info(detected_text)
        
        # Проверка за вредни добавки [cite: 708, 711]
        found_issues = []
        for key, description in harmful_ingredients.items():
            if key.upper() in detected_text.upper():
                found_issues.append(f"⚠️ **{key}**: {description}")
        
        st.subheader("Резултати от анализа:")
        if found_issues:
            for issue in found_issues:
                st.error(issue)
        else:
            st.success("Не са открити вредни съставки от нашия списък.") [cite: 920]

    st.download_button("Изтегли разпознатия текст", detected_text, file_name="label_text.txt") [cite: 931]
