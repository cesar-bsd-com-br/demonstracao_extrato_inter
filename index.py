import pandas as pd
import streamlit as st

import decimal, warnings, locale

from decimal import *

locale.setlocale(locale.LC_TIME, 'pt_BR')
getcontext().prec = 40
warnings.simplefilter(action = 'ignore', category = UserWarning)

paginaInicial = st.navigation(
  {
    'Início': [
      st.Page(page = 'user_pages/pagina_inicial.py', title = 'Página inicial', icon = ':material/grade:', default = True),
    ],
  }
)

# Configurar o layout da página
st.set_page_config(
  layout = "wide",
  page_title = 'Página inicial',
  page_icon = '👋',
  initial_sidebar_state = 'collapsed'
)

paginaInicial.run()
