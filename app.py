import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Дефиниране на вредни Е-номера
harmful_e_numbers = {
    "E407": "Карагенан (възпаления, храносмилателни проблеми)",
    "E621": "Натриев глутамат (главоболие, алергии)",
    "E262": "Натриев ацетат (дразни стомаха)",
    "E300": "Аскорбинова киселина (в големи дози дразни стомаха)",
    "E330": "Лимонена киселина (уврежда зъбния емайл)",
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
    st.image(image, caption='Качен етикет')
    
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
            st.success("Няма открити опасни Е-номера.")
