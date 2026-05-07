import streamlit as st [cite: 142]
import easyocr [cite: 143]
import numpy as np [cite: 144]
from PIL import Image [cite: 145]

# Дефиниране на вредни Е-номера и техните описания [cite: 147]
harmful_e_numbers = {
    "E407": "Карагенан (възпаления, храносмилателни проблеми) [cite: 148, 257]",
    "E621": "Натриев глутамат (главоболие, алергии) [cite: 150, 261]",
    "E262": "Натриев ацетат (дразни стомаха) [cite: 152]",
    "E300": "Аскорбинова киселина (в големи дози дразни стомаха) [cite: 154]",
    "E330": "Лимонена киселина (уврежда зъбния емайл) [cite: 156]",
    "E250": "Натриев нитрит (риск от онкологични заболявания) [cite: 158]",
    "E952": "Цикламат - подсладител [cite: 160, 161]",
    "E471": "Емулгатор [cite: 163]",
    "E472": "Емулгатор [cite: 165]",
    "E450": "Дифосфати (проблеми с костите и бъбреците) [cite: 253, 255]"
}

st.title("OCR етикет + вредни съставки [cite: 188]")

# Опция за качване на снимка или използване на камера [cite: 57, 62]
uploaded_file = st.file_uploader("Качи изображение на етикет: [cite: 190]", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file) [cite: 145]
    st.image(image, caption='Качен етикет', use_column_width=True)
    
    # Инициализиране на EasyOCR за български и английски [cite: 61, 67]
    reader = easyocr.Reader(['bg', 'en']) [cite: 68]
    
    with st.spinner('Анализиране на текста...'):
        # Преобразуване на изображението за обработка [cite: 76]
        img_array = np.array(image)
        result = reader.readtext(img_array)
        
        # Извличане на целия текст [cite: 71]
        full_text = " ".join([res[1] for res in result])
        st.subheader("Разпознат текст:")
        st.write(full_text)
        
        # Търсене на вредни съставки [cite: 59]
        found_harmful = []
        for code, description in harmful_e_numbers.items():
            if code.upper() in full_text.upper():
                found_harmful.append(f"**{code}**: {description}")
        
        st.subheader("Открити вредни съставки (Е-кодове): [cite: 240]")
        if found_harmful:
            for item in found_harmful:
                st.error(item)
        else:
            st.success("Няма открити Е-номера. [cite: 241]")

    # Бутон за изтегляне на отчет [cite: 252]
    st.download_button("Изтегли отчет като .txt [cite: 252]", full_text, file_name="report.txt")
