import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Дефиниране на вредни Е-номера
harmful_e_numbers = {
    "E407": "Карагенан (възпаления, храносмилателни проблеми)",
    "E621": "Натриев глутамат (главоболие, алергии)",
    "E262": "Натриев ацетат (дразни стомаха)",
    "E300": "Аскорбинова киселина (дразни стомаха)",
    "E330": "Лимонена киселина (уврежда емайла)",
    "E250": "Натриев нитрит (риск от онкологични заболявания)",
    "E952": "Цикламат - подсладител",
    "E471": "Емулгатор",
    "E472": "Емулгатор",
    "E450": "Дифосфати (проблеми с костите и бъбреците)"
}

st.title("OCR етикет + вредни съставки")

uploaded_file = st.file_uploader("Качи изображение на етикет:", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качен етикет', use_container_width=True)
    
    # Инициализиране на модела
    reader = easyocr.Reader(['bg', 'en'])
    
    with st.spinner('Анализиране на текста...'):
        img_array = np.array(image)
        result = reader.readtext(img_array)
        full_text = " ".join([res[1] for res in result])
        
        st.subheader("Разпознат текст:")
        st.write(full_text)
        
        # Търсене на съвпадения
        found_harmful = []
        for code, description in harmful_e_numbers.items():
            if code.upper() in full_text.upper():
                found_harmful.append(f"**{code}**: {description}")
        
        st.subheader("Открити вредни съставки:")
        if found_harmful:
            for item in found_harmful:
                st.error(item)
        else:
            st.success("Няма открити опасни Е-номера.")

    st.download_button("Изтегли текста", full_text, file_name="label_text.txt")
