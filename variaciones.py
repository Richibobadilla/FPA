import pandas as pd
import os
import streamlit.web.bootstrap

# --- CONFIGURACIÓN ---
archivo = r'C:\Users\ricardo.bobadilla\OneDrive - CIAL Dun & Bradstreet\FINANZAS MX\FP&A\TEST\PY\TEST.xlsx'
salida_excel = r'C:\Users\ricardo.bobadilla\OneDrive - CIAL Dun & Bradstreet\FINANZAS MX\FP&A\TEST\PY\variaciones_resultado.xlsx'

# --- LÓGICA DE NEGOCIO ---
def calcular_variaciones():
    real_df = pd.read_excel(archivo, sheet_name='REAL')
    budget_df = pd.read_excel(archivo, sheet_name='BUDGET')

    real_grouped = real_df.groupby(['MES', 'GASTO'])['IMPORTE'].sum().reset_index()
    budget_grouped = budget_df.groupby(['MES', 'GASTO'])['IMPORTE'].sum().reset_index()

    variaciones = pd.merge(
        real_grouped,
        budget_grouped,
        on=['MES', 'GASTO'],
        how='outer',
        suffixes=('_REAL', '_BUDGET')
    ).fillna(0)

    variaciones['VARIACION_ABS'] = variaciones['IMPORTE_REAL'] - variaciones['IMPORTE_BUDGET']
    variaciones['VARIACION_%'] = (variaciones['VARIACION_ABS'] / 
                                  variaciones['IMPORTE_BUDGET'].replace(0, pd.NA)) * 100

    variaciones.to_excel(salida_excel, index=False)
    print(f"✅ Archivo generado: {salida_excel}")

    return variaciones

# --- INTERFAZ STREAMLIT ---
def lanzar_streamlit():
    script_code = '''
import pandas as pd
import streamlit as st

archivo = r"{salida}"
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
'''.replace("{salida}", salida_excel.replace("\\", "\\\\"))

    # Guardar script temporal para Streamlit
    temp_script = os.path.join(os.getcwd(), "variaciones_ui_temp.py")
    with open(temp_script, "w", encoding="utf-8") as f:
        f.write(script_code)

    # Lanzar Streamlit
    streamlit.web.bootstrap.run(temp_script, "", [], None)

# --- MAIN ---
if __name__ == "__main__":
    calcular_variaciones()
    lanzar_streamlit()
