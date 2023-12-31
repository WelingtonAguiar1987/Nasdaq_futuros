#BIBLIOTECAS IMPORTADAS:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st

# SIGLA E NOME DO ATIVO ANALISADO:
sigla_ativo = "MNQ=F"
nome_ativo = "NASDAQ 100 FUTUROS"

# DADOS HISTÓRICOS PERÍODO DE VENCIMENTO:
st.title("Análise do Nasdaq Futuros")

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
    
    
# Antes de calcular o 'range_do_dia', verifique se há dados no dataframe
if not dados_historico_vencimento.empty:
    dados_historico_vencimento['range'] = dados_historico_vencimento['High'] - dados_historico_vencimento['Low']
    range_do_dia = dados_historico_vencimento['range'][-1]
else:
    # Trate o caso em que o dataframe está vazio
    print("Não foram encontrados dados para o intervalo especificado.")
    range_do_dia = None




# DEMARCAÇÃO NO GRÁFICO DO DIA ATUAL:

input_inicio_marcacao = input('')
input_final_marcacao = input('')

# DATA DO PREGÃO ATUAL:

pregao_atual = dados_historico_vencimento.index[-1]

# PREÇO DO ÚLTIMO FECHAMENTO E ÚLTIMA ABERTURA:
# PREENCHER OS VALORES ABAIXO:

input_preco_ultimo_fechamento = float(input(''))
input_ultima_abertura = float(input(''))

def linha():
    print('-' * 37)

# CÁLCULO PARA ANÁLISE DESVIO PADRÃO:*
mais_2dp = (input_preco_ultimo_fechamento + (desvio_padrao * 2))
mais_1dp_e_meio = (input_preco_ultimo_fechamento + (meio_desvio_padrao * 3))
mais_1dp = (input_preco_ultimo_fechamento + (desvio_padrao))
mais_meio_desvio_padrao = (input_preco_ultimo_fechamento + meio_desvio_padrao)


menos_meio_desvio_padrao = (input_preco_ultimo_fechamento - meio_desvio_padrao)
menos_1dp = (input_preco_ultimo_fechamento - (desvio_padrao))
menos_1dp_e_meio = (input_preco_ultimo_fechamento - (meio_desvio_padrao * 3))
menos_2dp = (input_preco_ultimo_fechamento - (desvio_padrao * 2))



# PLOTAR GRÁFICO INTRADAY DO ATIVO ANALISADO:
grafico = plt.figure(figsize=(19.2, 8.2), facecolor='#111111', label=f"GRÁFICO INTRADIÁRIO DO {nome_ativo} ({sigla_ativo})")
ax = plt.axes()
ax.set_facecolor("#111111")
dados_historico_intraday['Adj Close'].plot(label='Nasdaq Futuros', lw=2, color='#33ffff')
plt.title(f"GRÁFICO INTRADIÁRIO DO {nome_ativo} ({sigla_ativo}), {pregao_atual}", color='#7fff00', fontsize=18 )
plt.ylabel('Preço do Ativo', color='r', fontsize=12)
plt.xlabel('Data Histórico', color='r', fontsize=12)
plt.axhline(mais_2dp, color='r', ls='--', lw=4, label=f'+ 2 DP: ....................... {mais_2dp:.2f}')
plt.axhline(mais_1dp_e_meio, color='r', lw=3, ls='--', label=f'+ 1 DP e Meio: ........... {mais_1dp_e_meio:.2f}')
plt.axhline(mais_1dp, color='r', ls='--', lw=2, label=f'+ 1 DP: ....................... {mais_1dp:.2f}')
plt.axhline(mais_meio_desvio_padrao, color='r', lw=1, ls='--', label=f'+ Meio DP: ................. {mais_meio_desvio_padrao:.2f}')
plt.axhline(input_preco_ultimo_fechamento, color='blue', ls='--', lw=2, label=f'Último Fechamento: ... {input_preco_ultimo_fechamento:.2f}')
plt.axhline(input_ultima_abertura, color='white', ls='--', lw=2, label=f'Última Abertura: ......... {input_ultima_abertura:.2f}')
plt.axhline(menos_meio_desvio_padrao, color='g', lw=1, ls='--', label=f'- Meio DP: ................... {menos_meio_desvio_padrao:.2f}')
plt.axhline(menos_1dp, color='g', ls='--', lw=2, label=f'- 1 DP: ......................... {menos_1dp:.2f}')
plt.axhline(menos_1dp_e_meio, color='g', lw=3, ls='--', label=f'- 1 DP e Meio: ............. {menos_1dp_e_meio:.2f}')
plt.axhline(menos_2dp, color='g', ls='--', lw=4, label=f'- 2 DP: ......................... {menos_2dp:.2f}')



# ESSE FILTRO, NO GRÁFICO, INICIA-SE APÓS MEIA NOITE (00:00), E TERMINA A MEIA NOITE (00:00) DO DIA DO FILTRO FINAL:
plt.axvline(inicio_marcacao, color='#ffd700', label='Inicio dia atual')
plt.axvline(final_marcacao, color='#ffd700', label='Fim dia atual')
plt.grid(axis='x', color='white')
plt.grid(axis='y', color='white')
ax.tick_params(axis='y', colors='white')
ax.tick_params(axis='x', colors='white')
ax.spines['bottom'].set_color('w')
ax.spines['top'].set_color('w')
ax.spines['left'].set_color('w')
ax.spines['right'].set_color('w')
plt.legend(facecolor='w', frameon=True, framealpha=0.8)
plt.show()

input()




