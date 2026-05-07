import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Дефиниране на вредни Е-номера и описания
harmful_ingredients = {
    "E407": "Карагенан - може да предизвика възпаления и храносмилателни проблеми.",
    "E621": "Натриев глутамат - подсилвател на вкуса, може да причини главоболие.",
    "E250": "Натриев нитрит - консервант, риск от онкологични заболявания.",
    "E450": "Дифосфати - могат да нарушат калциевия баланс и да увредят бъбреците.",
    "E952": "Цикламат - изкуствен подсладител.",
    "E262": "Натриев ацетат - може да дразни стомаха.",
    "E330": "Лимонена киселина - в големи дози уврежда зъбния емайл.",
    "E300": "Аскорбинова киселина - в големи дози дразни стомаха."
}

st.title("🧪 Анализатор на етикети")

# Качване на снимка
uploaded_file = st.file_uploader("Качете снимка на етикет:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качен етикет', use_container_width=True)
    
    # Инициализиране на EasyOCR
    reader = easyocr.Reader(['bg', 'en'])
    
    with st.spinner('ИИ анализира текста...'):
        img_array = np.array(image)
        result = reader.readtext(img_array)
        
        # Сортиране на текста отгоре-надолу
        result.sort(key=lambda x: x[0][0][1])
        
        detected_text = " ".join([res[1] for res in result])
        
        st.subheader("Разпознат текст:")
        st.info(detected_text)
        
        # Търсене на вредни съставки
        found_issues = []
        for key, description in harmful_ingredients.items():
            if key.upper() in detected_text.upper():
                found_issues.append(f"⚠️ **{key}**: {description}")
        
        st.subheader("Резултати:")
        if found_issues:
            for issue in found_issues:
                st.error(issue)
        else:
            st.success("Не са открити вредни съставки от нашия списък.")

    st.download_button("Изтегли текста", detected_text, file_name="label_text.txt")
