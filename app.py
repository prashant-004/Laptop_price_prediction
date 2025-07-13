import streamlit as st
import joblib
import numpy as np
import pandas as pd

pipe = joblib.load('pipe.pkl')
df = joblib.load('df.pkl')

st.set_page_config(page_title="Laptop Price Predictor", layout="centered")

st.markdown("<h1 style='text-align: center;'>Laptop Price Predictor 💻</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
company = col1.selectbox('Brand', sorted(df['Company'].unique()))
laptop_type = col2.selectbox('Type', sorted(df['TypeName'].unique()))
ram = col3.selectbox('Ram (in GB)', sorted([2, 4, 6, 8, 12, 16, 24, 32, 64]))

col4, col5, col6 = st.columns(3)
weight = col4.number_input('Weight of laptop in kg', min_value=0.8, max_value=4.5, value=2.0, step=0.1)
touchscreen = col5.selectbox('Touchscreen', ['No', 'Yes'])
panel = col6.selectbox('IPS Display', sorted(df['Panel'].unique()))

col7, col8, col9 = st.columns(3)
screen_size = col7.number_input('Screen Size (in Inches)', min_value=10.0, max_value=17.0, value=15.6, step=0.1)
resolution = col8.selectbox('Screen Resolution', [
    '1920x1080','1366x768','1600x900','3840x2160','3200x1800',
    '2880x1800','2560x1600','2560x1440','2304x1440'
])
processor = col9.selectbox('CPU Brand', sorted(df['Processor'].unique()))

col10, col11 = st.columns(2)
hdd = col10.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])
ssd = col11.selectbox('SSD (in GB)', [0, 8, 16, 32, 64, 128, 256, 512, 1024])

col12, col13 = st.columns(2)
gpu = col12.selectbox('GPU Brand', sorted(df['Gpu_Brand'].unique()))
os = col13.selectbox('OS Type', sorted(df['OpSys'].unique()))

memory_type = st.selectbox('Memory Type', [
    'SSD', 'HDD', 'HDD + SSD', 'HYBRID', 'FLASH STORAGE + HDD', 'HYBRID + SSD'
])

if st.button('Pridict Price'): 
    touchscreen_bin = 1 if touchscreen == 'Yes' else 0

    x_res, y_res = map(int, resolution.split('x'))
    ppi = ((x_res**2 + y_res**2) ** 0.5) / screen_size

    input_df = pd.DataFrame([{
        'Company': company,
        'TypeName': laptop_type,
        'Ram': ram,
        'Touchscreen': touchscreen_bin,
        'PPI': ppi,
        'HDD': hdd,
        'SSD': ssd,
        'Gpu_Brand': gpu,
        'OpSys': os,
        'Weight': weight,
        'Panel': panel,
        'Memory_Types': memory_type,
        'Processor': processor,
        'Inches': screen_size
    }])

    predicted_log_price = pipe.predict(input_df)[0]
    predicted_price = int(np.exp(predicted_log_price))

    st.markdown(f"<h2 style='text-align: center;'> Predicted Price: ₹ {predicted_price:,}</h2>", unsafe_allow_html=True)
