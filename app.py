from utils import DicionarioEntradas, DicionarioSaidas, DicionariosMovimentacoesBancarias

import streamlit as st
import requests
import numpy as np
import pandas as pd

print(DicionarioEntradas)

def main():
    # Título da aplicação
    st.title("Projeto de Contabilidade")

    # Exibir os dicionários no Streamlit
    st.subheader("Dicionário de Entradas")
    st.write(DicionarioEntradas)

    st.subheader("Dicionário de Saídas")
    st.write(DicionarioSaidas)

    st.subheader("Dicionário de Movimentações Bancárias")
    st.write(DicionariosMovimentacoesBancarias)


main()