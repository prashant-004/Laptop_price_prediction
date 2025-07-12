import streamlit as st
import joblib
import numpy as np
import pandas as pd


pipe = joblib.load('pipe.pkl')
df = joblib.load('df.pkl')

st.title("Laptop Predictor")

company = st.selectbox('Brand',df['Company'].unique())

type = st.selectbox('Type',df['TypeName'].unique())

ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

panel = st.selectbox('Panel',df['Panel'].unique())

Memory_Types = st.selectbox('Memory_Types',['SSD', 'HDD', 'HDD + SSD', 'HYBRID',
       'FLASH STORAGE + HDD', 'HYBRID + SSD'])

weight = st.number_input(
    'Weight of the Laptop (in kg)', 
    min_value=0.8, 
    max_value=4.5, 
    value=2.0,      
    step=0.1        
)

Processor = st.selectbox('Processor',df['Processor'].unique())

touchscreen = st.selectbox('Touchscreen',['No','Yes'])

screen_size = st.selectbox('Scrensize in inches', [10.1, 11.6, 12.5, 13.3, 14.0, 15.0, 15.6, 16.0])

resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

hdd = st.selectbox('HDD(in GB)',[0,128,512,1024,2048])

ssd = st.selectbox('SSD(in GB)',[0,8,16,32,64,128,256,512,1024])

gpu = st.selectbox('GPU',df['Gpu_Brand'].unique())

os = st.selectbox('OS',df['OpSys'].unique())


if st.button('Predict Price'):
    ppi = None
    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0


    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size
    
    query = np.array([company,type,ram,touchscreen,ppi,hdd,ssd,gpu,os,weight,panel,Memory_Types])

    query_df = pd.DataFrame([{
    'Company': company,
    'TypeName': type,
    'Ram': ram,
    'Touchscreen': touchscreen,
    'PPI': ppi,
    'HDD': hdd,
    'SSD': ssd,
    'Gpu_Brand': gpu,
    'OpSys': os,
    'Weight': weight,
    'Panel': panel,
    'Memory_Types': Memory_Types,
    'Processor': Processor,           
    'Inches': screen_size                 
    }])


    
    st.title(f" Predicted Price: ₹ {int(np.exp(pipe.predict(query_df)[0]))}")

