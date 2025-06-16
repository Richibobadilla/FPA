
import pandas as pd
import streamlit as st

archivo = r"C:\\Users\\ricardo.bobadilla\\OneDrive - CIAL Dun & Bradstreet\\FINANZAS MX\\FP&A\\TEST\\PY\\variaciones_resultado.xlsx"
variaciones = pd.read_excel(archivo)

st.title("📊 Análisis de Variaciones por Mes")

meses = sorted(variaciones['MES'].unique())
mes_seleccionado = st.selectbox("Selecciona un mes para ver sus variaciones:", meses)

df_mes = variaciones[variaciones['MES'] == mes_seleccionado]

st.subheader(f"📅 Variaciones para el mes: {mes_seleccionado}")
st.dataframe(df_mes.style.format({
    "IMPORTE_REAL": "${:,.0f}",
    "IMPORTE_BUDGET": "${:,.0f}",
    "VARIACION_ABS": "${:,.0f}",
    "VARIACION_%": "{:.1f}%"
}))

st.success("✅ También puedes consultar el Excel generado directamente.")
