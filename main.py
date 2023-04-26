import streamlit as st
import pandas as pd

from datetime import datetime

def formatear_fecha(fecha_str):
    fecha = datetime.strptime(fecha_str, '%Y-%m')
    return fecha.strftime('%Y-%m-%d')

def read_file(uploaded_file):
    df_base = pd.read_csv(uploaded_file)
    return df_base

def show_income_and_cost(df_base, anio):
    
    df_base = df_base.dropna()
    df_base['Fecha'] = pd.to_datetime(df_base['Fecha'], format="%d/%m/%Y", errors='coerce')
    df_base['Mes'] = df_base['Fecha'].dt.to_period("M").dt.to_timestamp()
    #df_base['Mes'] = df_base['Mes'].apply(lambda x: x.strftime('%m %Y'))

    df_base['Mes'] = pd.to_datetime(df_base['Mes'], format='%m %Y')
    df_base = df_base.loc[df_base['Mes'].dt.year == anio]
    df_base['Mes'] = df_base['Mes'].apply(lambda x: x.strftime('%m %Y'))

    df_base = df_base[['Mes', 'Ingreso/Egreso', 'Monto']]
    df_base = df_base.groupby(['Mes', 'Ingreso/Egreso']).agg('sum')
    

    df_pivoted = df_base.pivot_table(index='Mes', columns='Ingreso/Egreso', values='Monto', aggfunc='sum')
    df_pivoted = df_pivoted.reset_index().rename_axis(None, axis=1)
    df_pivoted = df_pivoted.set_index('Mes')
    df_pivoted.fillna(0, inplace=True)
    
    st.bar_chart(df_pivoted)

def show_accumulated_profit(df_base, anio):
    df_base = df_base.dropna()
    df_base['Fecha'] = pd.to_datetime(df_base['Fecha'], format="%d/%m/%Y", errors='coerce')
    df_base['Mes'] = df_base['Fecha'].dt.to_period("M").dt.to_timestamp()

    #aqui hay que trabajar
    df_base['Mes'] = pd.to_datetime(df_base['Mes'], format='%m %Y')
    #df_base = df_base.loc[df_base['Mes'].dt.year == 2023]
    #df_base['Mes'] = df_base['Mes'].apply(lambda x: x.strftime('%m %Y'))


    df_base = df_base[['Mes', 'Ingreso/Egreso', 'Monto']]
    df_base = df_base.groupby(['Mes', 'Ingreso/Egreso']).agg('sum')


    df_pivoted = df_base.pivot_table(index='Mes', columns='Ingreso/Egreso', values='Monto', aggfunc='sum')
    df_pivoted = df_pivoted.reset_index().rename_axis(None, axis=1)
    df_pivoted = df_pivoted.set_index('Mes')
    df_pivoted.fillna(0, inplace=True)

    df_pivoted['Utilidad'] = df_pivoted['Ingreso'] - df_pivoted['Egreso']
    df_pivoted['Utilidad Acumulada'] = df_pivoted['Utilidad'].cumsum()

    df_pivoted = df_pivoted.reset_index()
    df_pivoted = df_pivoted.loc[df_pivoted['Mes'].dt.year == anio]
    df_pivoted['Mes'] = df_pivoted['Mes'].apply(lambda x: x.strftime('%m %Y'))
    df_pivoted = df_pivoted.set_index('Mes')
    
    df_pivoted = df_pivoted[['Utilidad Acumulada']]

    st.line_chart(df_pivoted)
    st.dataframe(df_pivoted)
    
    
def main():
    st.title('Flujo Empresa')
    uploaded_file = st.file_uploader("Sube el excel generado en Notion")
    anio = st.selectbox('Selecciona el año',(2023, 2024, 2025))
    if uploaded_file is not None:
        df_base = read_file(uploaded_file)
        show_income_and_cost(df_base, anio)
        show_accumulated_profit(df_base, anio)

if __name__ == "__main__":
    main()