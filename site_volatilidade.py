#BIBLIOTECAS IMPORTADAS:
import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st

# Configuração de páginas e layout:

st.set_page_config(
    page_title="Nasdaq 100 Futuros",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Distribuição de páginas do site:
st.sidebar.title('Menu')
pagina_selecionada = st.sidebar.selectbox('Opções:', ['Análise Macro', 'Daytrade'])


# SIGLA E NOME DO ATIVO ANALISADO:
sigla_ativo = "MNQ=F"
nome_ativo = "NASDAQ 100 FUTUROS"

# DADOS HISTÓRICOS PERÍODO DE VENCIMENTO:


# Seleções de páginas do site:
if pagina_selecionada == 'Análise Macro':
    st.title("Análise Macro do Nasdaq Futuros:")

    st.form(key='Filtros Datas:')
    input_data_inicial_vencimento = st.date_input('Selecione a dada inicial de vencimento: ', format='DD/MM/YYYY')
    input_data_final_vencimento = st.date_input('Selecione a dada final de vencimento: ', format='DD/MM/YYYY')

    dados_historico_vencimento = yf.download(sigla_ativo, input_data_inicial_vencimento, input_data_final_vencimento, interval='1d')
    dados_historico_vencimento['Volatilidade'] = dados_historico_vencimento['High'] - dados_historico_vencimento['Low']

    with st.container():
        st.dataframe(dados_historico_vencimento)
        dados_historico_vencimento['Adj Close'] = dados_historico_vencimento['Adj Close'].astype(float)
        st.header('Nasdaq Futuros - Historico')
        site = pd.DataFrame(dados_historico_vencimento['Adj Close'])
        st.line_chart(site, color='#33ffff')
    


        # FILTRO DE TODO O PERÍODO DE VENCIMENTO:
        periodo_vencimento_filtrado = dados_historico_vencimento['Volatilidade'][0:-1]

        # CÁLCULO DO DESVIO PADRÃO DE TODO ESSE VENCIMENTO:
        desvio_padrao = np.std(periodo_vencimento_filtrado)
        meio_desvio_padrao = desvio_padrao / 2
        print(f'Desvio Padrão: {desvio_padrao:.2f} Pontos.')
        print(f'Meio Desvio Padrão: {meio_desvio_padrao:.2f} Pontos.')
    
    
if pagina_selecionada == 'Daytrade':
    st.title("Análise para Daytrade do Nasdaq Futuros:")

    # DADOS HISTÓRICOS PERÍODO INTRADAY:
    st.form(key='Filtros Datas Intraday:')
    input_data_inicial_intraday = st.date_input('Selecione a dada inicial de intraday: ', format='DD/MM/YYYY')
    input_data_final_intraday = st.date_input('Selecione a dada final intraday: ', format='DD/MM/YYYY')

    dados_historico_intraday = yf.download(sigla_ativo, input_data_inicial_intraday, input_data_final_intraday, interval='5m')

    with st.container():
        st.dataframe(dados_historico_intraday)
        dados_historico_intraday['Adj Close'] = dados_historico_intraday['Adj Close'].astype(float)
        st.header('Nasdaq Futuros - Intraday')
        site = pd.DataFrame(dados_historico_intraday['Adj Close'])
        st.line_chart(site, color='#33ffff')
    
    












