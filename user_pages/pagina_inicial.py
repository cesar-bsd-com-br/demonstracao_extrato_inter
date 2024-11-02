import pandas as pd
import os, sys, re, math
import decimal
import time
import streamlit as st

from datetime import datetime, date

sys.path.append('.')
sys.path.append('..')

def formatarMoeda(valor: float, simbolo: str = 'R$') -> str:
  textoFormatado = f'{simbolo} {valor:_.2f}'
  textoFormatado = textoFormatado.replace('.', ',')
  textoFormatado = textoFormatado.replace('_', '.')
  return textoFormatado

st.title('Demonstrativo de extrato bancário Inter')

arquivoUpload = st.file_uploader(
  label = 'Extrato em formato CSV', 
  type = ['csv'], 
  accept_multiple_files = False, 
  key = 'arquivoUpload'
)

if not arquivoUpload:
  st.stop()

if not os.path.isdir('./tmp'):
  os.mkdir('./tmp')

caminhoCompletoArquivo = f'./tmp/{arquivoUpload.name}'
with open(caminhoCompletoArquivo, 'w+b') as arquivo:
  arquivo.write(arquivoUpload.getvalue())

dfExtrato = pd.read_csv(caminhoCompletoArquivo, sep = ';', skiprows = 4)
dfExtrato['Valor'] = dfExtrato['Valor'].apply(lambda x: x.replace('.', ''))
dfExtrato['Valor'] = dfExtrato['Valor'].apply(lambda x: x.replace(',', '.'))
dfExtrato['Valor'] = pd.to_numeric(dfExtrato['Valor'])

dfExtrato['Data Lançamento'] = dfExtrato['Data Lançamento'].apply(lambda x: datetime.strptime(x, r'%d/%m/%Y').date())
dfExtrato = dfExtrato[dfExtrato['Valor'] > 0]
dfExtrato['Mês'] = dfExtrato['Data Lançamento'].apply(lambda x: x.strftime(r'%Y-%m'))
dfExtrato = dfExtrato.drop(columns = ['Saldo', 'Data Lançamento', 'Histórico'])
dfExtrato.sort_values(by = ['Mês', 'Descrição'], inplace = True)
dfExtrato = dfExtrato[['Mês', 'Descrição', 'Valor']]

dfAgrupado = dfExtrato.groupby(by = ['Mês'])['Valor'].sum().reset_index()
dfPessoa = dfExtrato.groupby(by = ['Descrição'])['Valor'].sum().reset_index()
dfPessoa = dfPessoa.sort_values(by = ['Valor'], ascending = False)

formatoExtrato = dfExtrato.style.format(
  {
    'Mês': lambda x: (x[5 : 7] + '/' + x[0 : 4]),
    'Valor' : lambda x: '{:,.2f}'.format(x),
  },
  thousands = '.',
  decimal = ','
)

formatoAgrupado = dfAgrupado.style.format(
  {
    'Mês': lambda x: (x[5 : 7] + '/' + x[0 : 4]),
    'Valor' : lambda x: '{:,.2f}'.format(x),
  },
  thousands = '.',
  decimal = ','
)

formatoPessoa = dfPessoa.style.format(
  {
    'Valor' : lambda x: '{:,.2f}'.format(x),
  },
  thousands = '.',
  decimal = ','
)

colDetalhe, colPessoa, colMes, colTotal = st.columns([2, 2, 2, 1])
totalRecebido: float = dfExtrato['Valor'].sum()

with colDetalhe:
  st.caption('Extrato detalhado - recebimentos')
  st.dataframe(formatoExtrato, hide_index = True)

with colPessoa:
  st.caption('Extrato resumido - recebimentos por pessoa')
  st.dataframe(
    data = formatoPessoa,
    hide_index = True,
  )

with colMes:
  st.caption('Extrato resumido - recebimentos por mês')
  st.dataframe(
    data = formatoAgrupado,
    hide_index = True,
  )

with colTotal:
  st.metric(
    label = 'Total recebido no período',
    value = formatarMoeda(valor = totalRecebido, simbolo = '')
  )

os.remove(caminhoCompletoArquivo)
