import streamlit as st



st.set_page_config(
    page_title="Sistema de Abastecimento",
    page_icon="👋",
)

st.write("# Bem vindo ao sistema de Abastecimento ! 👋")

st.sidebar.success("Selecione o sistema de Abastecimento ou relatório para consulta.")

st.markdown(
    """
    Esse sistema tem como objetivo registro dos abasteccimento dos veiculos na base de SETE LAGOAS
    
    **👈 ATENÇÃO NO REGISTRO DE HODOMETRO
    
    **👈 QUALQUER NÃO CONFORMIDADE INFORMA O SUSPERVISOR DE FROTA
    
    **👈 ATENÇÃO NO REGISTRO DE COMBUSTIVEL INSERIDO AOS VEICULOS
    
    ### Ajuste e Suportes
    - Qualquer sugestão e feedback contatar
    [ismael.silva@grupocemig.com.br]

"""
)