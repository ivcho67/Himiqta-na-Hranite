import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Списък с вредни добавки
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

st.title("Анализатор на етикети за вредни съставки")

uploaded_file = st.file_uploader("Качете снимка на етикет:", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Качен етикет')
    
    # Зареждане на OCR модела
    reader = easyocr.Reader(['bg', 'en'])
    
    with st.spinner('Анализиране...'):
        img_array = np.array(image)
        result = reader.readtext(img_array)
        full_text = " ".join([res[1] for res in result])
        
        st.subheader("Разпознат текст:")
        st.write(full_text)
        
        found = [f"**{c}**: {d}" for c, d in harmful_e_numbers.items() if c in full_text.upper()]
        
        st.subheader("Резултати:")
        if found:
            for item in found:
                st.error(item)
        else:
            st.success("Не са открити опасни Е-номера от нашия списък.")
