import streamlit as st
from etl import FinancialProcessor  

def main():
    st.title("Projeto de Contabilidade")

    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    processor = FinancialProcessor("dados.xlsx")
    processor.process_records()
    processor.calculate_expenses()
    processor.calculate_revenue()

    despesas_2023 = processor.get_despesas_2023()
    despesas_2024 = processor.get_despesas_2024()
    receitas_2023 = processor.get_receitas_2023()
    receitas_2024 = processor.get_receitas_2024()
    receita_jan_2025 = processor.get_receitas_2025()

    if len(despesas_2023) != len(meses) or len(despesas_2024) != len(meses) or \
       len(receitas_2023) != len(meses) or len(receitas_2024) != len(meses):
        st.error("Erro: O número de dados processados não corresponde ao número de meses!")
        return

    mes_selecionado = st.selectbox("Escolha o mês para visualizar:", meses)
    indice_mes = meses.index(mes_selecionado)

    st.subheader(f"Dados de {mes_selecionado}")
    
    st.write(f"Despesas 2023: R$ {despesas_2023[indice_mes]:,.2f}")
    st.write(f"Despesas 2024: R$ {despesas_2024[indice_mes]:,.2f}")
    st.write(f"Receitas Brutas 2023: R$ {receitas_2023[indice_mes]:,.2f}")
    st.write(f"Receitas Brutas 2024: R$ {receitas_2024[indice_mes]:,.2f}")

    if mes_selecionado == "Janeiro":
        st.write(f"Receita Bruta 2025: R$ {receita_jan_2025:,.2f}")

if __name__ == "__main__":
    main()