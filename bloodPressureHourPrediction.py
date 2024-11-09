import streamlit as st
import pandas as pd
import numpy as np

def load_data():
    data = pd.read_csv('presion_fecha_puerta_del_tiempo.csv')
    
    data['hora'] = pd.to_datetime(data['fecha']).dt.hour
    
    hourly_stats = data.groupby('hora')['presion'].agg(['mean', 'std']).reset_index()
    hourly_stats.columns = ['hora', 'mean', 'std']
    
    hourly_stats['normal_min'] = hourly_stats['mean'] - hourly_stats['std']
    hourly_stats['normal_max'] = hourly_stats['mean'] + hourly_stats['std']
    
    hourly_stats.set_index('hora', inplace=True)
    
    return hourly_stats

hourly_stats = load_data()

st.title("Verificación de Presión (Normal o Anormal)")
st.write("Ingresa la hora y la presión para determinar si es normal o Anormal.")

hora = st.slider("Selecciona la hora (0 a 23)", 0, 23, 12)
presion = st.number_input("Ingresa la presión (psi)", value=0)

if st.button("Verificar"):
    if hora in hourly_stats.index:
        hour_stats = hourly_stats.loc[hora]
        
        if hour_stats['normal_min'] <= presion <= hour_stats['normal_max']:
            resultado = "Normal"
        else:
            resultado = "Anormal"
        
        st.success(f"Resultado: La presión es {resultado}.")
        st.write(f"Rango normal para la hora {hora}: {hour_stats['normal_min']:.2f} - {hour_stats['normal_max']:.2f} psi")
    else:
        st.warning("No se encontraron datos suficientes para esta hora.")
