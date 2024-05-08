import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime

# Configuração da conexão com o banco de dados

def get_connection():
    return psycopg2.connect(database = "provac_producao", 
                            user = "admin_provac", 
                            host= '192.168.0.232',
                            password = "Provac@2024",
                            port = 5432)

conn = get_connection()
# Função para inserir os dados no banco de dados
def inserir_dados(data, hora, veiculo, frota, quantidade, hodometro, status_oleo, motivo_oleo, status_pneus, motivo_pneus, status_agua, motivo_agua, status_ldianteiro, motivo_ldianteiro, status_ltraseiro, motivo_ltraseiro, status_lfreio, motivo_lfreio, status_lre, motivo_lre, status_bateria, motivo_bateria, status_limpbrisa, motivo_limpbrisa):
    cur = conn.cursor()
    cur.execute("INSERT INTO cemig.registros_abastecimento (data_abastecimento, hora_abastecimento, identificacao_veiculo, indentificacao_frota, quantidade_combustivel, hodometro, status_oleo, motivo_oleo, status_pneus, motivo_pneus, status_agua, motivo_agua, status_ldianteiro, motivo_ldianteiro, status_ltraseiro, motivo_ltraseiro, status_lfreio, motivo_lfreio, status_lre, motivo_lre, status_bateria, motivo_bateria, status_limpbrisa, motivo_limpbrisa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (data, hora, veiculo, frota, quantidade, hodometro, status_oleo, motivo_oleo, status_pneus, motivo_pneus, status_agua, motivo_agua, status_ldianteiro, motivo_ldianteiro, status_ltraseiro, motivo_ltraseiro, status_lfreio, motivo_lfreio, status_lre, motivo_lre, status_bateria, motivo_bateria, status_limpbrisa, motivo_limpbrisa))
    conn.commit()
    cur.close()

def consultar_registros(filtro_placa=None, filtro_frota=None, data_inicio=None, data_fim=None):
    conn = get_connection()
    query = 'SELECT * FROM cemig.registros_abastecimento'
    df = pd.read_sql_query(query, conn)
    if filtro_placa:
        placa = df.identificacao_veiculo.isin(filtro_placa)
        filtros = df[placa]
    if filtro_frota:
        frota = df.indentificacao_frota.isin(filtro_frota)
        filtros = df[frota]
    if filtro_frota and filtro_placa:
        filtros = df[placa&frota]
    return filtros
        

# Função auxiliar para criar campos de verificação
def criar_campo_verificacao(nome_item):
    status = st.radio(f"Status do {nome_item}", ["Conforme", "Não Conforme"], key=f"status_{nome_item}")
    motivo = ""
    if status == "Não Conforme":
        motivo = st.text_area(f"Motivo (Não Conforme) - {nome_item}", key=f"motivo_{nome_item}")
    return status, motivo
@st.cache_data
def load_data(query):
    with get_connection() as conn:
        return pd.read_sql_query(query, conn)
           
# Criação do formulário no Streamlit
st.title("Formulário de Abastecimento de Combustível")

with st.form("form_abastecimento"):
    data = st.date_input("Data do Abastecimento", datetime.now())
    hora = st.time_input("Hora do Abastecimento", datetime.now())
    veiculo = st.selectbox("Placa do Veículo", ['RJL5E08', 'RKK4G03', 'RJP4G52', 'RKD4G25', 'RHL0F89', 'RKB4J63', 'GHL8437', 'RHL5F80', 'RHL4E19', 'GGF6201', 
                                                'GHO1826', 'GHA1819', 'GGL5690', 'RJC4I83', 'RHL4D54', 'RHL2G42', 'RHL0G24', 'RIQ4I18', 'RHM3F04', 'GFR3832', 
                                                'FRP7508', 'FGY5996', 'BEK4J70', 'GDG8727', 'FCR6514', 'RJB4E69', 'RJI4J68', 'RKT4F30', 'KZO9B54', 'RHM3F09', 
                                                'RKA4F98', 'GGP4880', 'RIV4J27', 'RHL0G23', 'RIZ3J86', 'FUK1342', 'PUT0599', 'RHR8F94', 'RHJ3H84', 'LMS0A80', 
                                                'GDF1235', 'FPC3699', 'GEU2660', 'RHL5F78', 'RHE7C31', 'RHM3F07', 'FAF2E03', 'SHU1C79', 'GFX3I23', 'EZG8J12', 
                                                'GFC6I12', 'SSR7H19', 'RHLOG30', 'RHL0G18', 'RKC5C87', 'RHJ6B81', 'RHL4D55', 'RHM3F08', 'RHL6C64', 'RHL3F60', 
                                                'RHL3F58', 'RHK5H60', 'RHK5H56', 'RHK5H54', 'RHJ6F44', 'RHJ6F43', 'RHJ7A41', 'RHJ6F41', 'RHJ6F40', 'RHJ6F39', 
                                                'RHJ6F36', 'RHI9B66', 'RHI9B65', 'RHA2F60', 'BEY3E99', 'BEY2J71', 'GHG5573', 'RJF4E79', 'RHJ2B29', 'RHJ2B26', 
                                                'RHJ2B24', 'RHL0C97', 'RHL0C93', 'RHL0C91', 'RHL0C89', 'RHL0C86', 'RHL0C83', 'RHL0C82', 'RHL0C81', 'RHL0C80', 
                                                'RHL0C79', 'RHL0C78', 'RHL0C76', 'RHL0C75', 'RHL0C74', 'RHL0C72', 'RHL0D19', 'RHL0D18', 'RHL0D17', 'RHL0D16', 
                                                'RHL0D15', 'RHL0D12', 'RHL0D10', 'STH3G85', 'SUD1A32', 'SVM8A89', 'SWT1F10', 'SVG3D09', 'RFH3I18', 'RFH3I17', 
                                                'BDU8D06', 'RHJ2B28', 'RHM3F06', 'RHM3F03', 'RHL6C66', 'RHL6C65', 'RHL3F59', 'RHK5H59', 'RHK5H53', 'PHD1178', 
                                                'PHD1176', 'PHD1173', 'PHD1169', 'PHD1166', 'PHD1165', 'PHD1164', 'PHD0970', 'PHD0947', 'PHD0946', 'D0145716', 
                                                'D0145712', 'D0145710', 'D0145707', 'D0145706', 'D0145704', 'D0145703', 'D0145679', 'D0145676', 'D0145672', 
                                                'D0145670', 'D0145669', 'D0145665', 'D0145637', 'D0145633', 'D0145629', 'D0145618', 'D0145617', 'D0145616', 
                                                'D0145611', 'RHK5H52', 'RHJ6F42', 'RHJ6F38', 'RHJ6F37'], index=None)

    frota = st.selectbox("Número da Frota  ", ['7509', '9950', '9906', '9469', '5041', '8653', '9087', '7508', '4005', '4191', '9045', '9879', '9811', '9809', 
                                               '2148', '4498', '8332', '4569', '8340', '-', '4431', '7007', '8349', '8348', '9096', '8964', '9708', '9631', 
                                               '8363', '8264', '8244', '9682', '8995', '9636', '9577', '8601', '9966', '9794', '9774', '8232', '9761', '4922', 
                                               '9755', '9893', '8134', '9392', '5212', '5211', '5210', '5209', '5208', '7787', '7629', '2084', '3680', '8853', 
                                               '9857', '9915', '8978', '8138', '3785', '8051', '9857', '8853', '3785', '8051', '9915', '8138', '8978', '2129', 
                                               '8006', '3671', '8853', '3671', '3785', '8138', '9915', '2129', '8978', '8978', '8051', '8138', '8006', '3785', 
                                               '9915', '8051', '9857', '8006', '8853', '3671', '2129', '9857', '3671', '8006', '2129'], index=None)
    
    quantidade = st.number_input("Quantidade de Combustível (em litros)", min_value=0.0, format="%.2f")
    hodometro = st.number_input("valor Hodometro do veículo", min_value=0.0, format="%.0f")
    
    # Campos de verificação
    status_oleo, motivo_oleo = criar_campo_verificacao("Óleo")
    status_pneus, motivo_pneus = criar_campo_verificacao("Pneus")
    status_agua, motivo_agua = criar_campo_verificacao("Água do Radiador")
    status_ldianteiro, motivo_ldianteiro = criar_campo_verificacao("Luz do Farol Dianteiro")
    status_ltraseiro, motivo_ltraseiro = criar_campo_verificacao("Luz do Farol traseiro")
    status_lfreio, motivo_lfreio = criar_campo_verificacao("Luz do Freio")
    status_lre, motivo_lre = criar_campo_verificacao("Luz de Ré")
    status_bateria, motivo_bateria = criar_campo_verificacao("Bateria")
    status_limpbrisa, motivo_limpbrisa = criar_campo_verificacao("Limpadores de para-brisa")
    
    submitted = st.form_submit_button("Registrar Abastecimento")
    if submitted:
        inserir_dados(data, hora, veiculo, frota, quantidade, hodometro, status_oleo, motivo_oleo, status_pneus, motivo_pneus, status_agua, motivo_agua, status_ldianteiro, motivo_ldianteiro, status_ltraseiro, motivo_ltraseiro, status_lfreio, motivo_lfreio, status_lre, motivo_lre, status_bateria, motivo_bateria, status_limpbrisa, motivo_limpbrisa)
        st.success("Abastecimento registrado com sucesso!")
# Não esqueça de fechar a conexão com o banco de dados quando terminar

with st.sidebar:    
    st.title("Consulta de Abastecimento")

    # Campos para inserção dos filtros
    filtro_placa = st.sidebar.multiselect("Filtrar por placa:", ['RJL5E08', 'RKK4G03', 'RJP4G52', 'RKD4G25', 'RHL0F89', 'RKB4J63', 'GHL8437', 'RHL5F80', 'RHL4E19', 'GGF6201', 
                                                    'GHO1826', 'GHA1819', 'GGL5690', 'RJC4I83', 'RHL4D54', 'RHL2G42', 'RHL0G24', 'RIQ4I18', 'RHM3F04', 'GFR3832', 
                                                    'FRP7508', 'FGY5996', 'BEK4J70', 'GDG8727', 'FCR6514', 'RJB4E69', 'RJI4J68', 'RKT4F30', 'KZO9B54', 'RHM3F09', 
                                                    'RKA4F98', 'GGP4880', 'RIV4J27', 'RHL0G23', 'RIZ3J86', 'FUK1342', 'PUT0599', 'RHR8F94', 'RHJ3H84', 'LMS0A80', 
                                                    'GDF1235', 'FPC3699', 'GEU2660', 'RHL5F78', 'RHE7C31', 'RHM3F07', 'FAF2E03', 'SHU1C79', 'GFX3I23', 'EZG8J12', 
                                                    'GFC6I12', 'SSR7H19', 'RHLOG30', 'RHL0G18', 'RKC5C87', 'RHJ6B81', 'RHL4D55', 'RHM3F08', 'RHL6C64', 'RHL3F60', 
                                                    'RHL3F58', 'RHK5H60', 'RHK5H56', 'RHK5H54', 'RHJ6F44', 'RHJ6F43', 'RHJ7A41', 'RHJ6F41', 'RHJ6F40', 'RHJ6F39', 
                                                    'RHJ6F36', 'RHI9B66', 'RHI9B65', 'RHA2F60', 'BEY3E99', 'BEY2J71', 'GHG5573', 'RJF4E79', 'RHJ2B29', 'RHJ2B26', 
                                                    'RHJ2B24', 'RHL0C97', 'RHL0C93', 'RHL0C91', 'RHL0C89', 'RHL0C86', 'RHL0C83', 'RHL0C82', 'RHL0C81', 'RHL0C80', 
                                                    'RHL0C79', 'RHL0C78', 'RHL0C76', 'RHL0C75', 'RHL0C74', 'RHL0C72', 'RHL0D19', 'RHL0D18', 'RHL0D17', 'RHL0D16', 
                                                    'RHL0D15', 'RHL0D12', 'RHL0D10', 'STH3G85', 'SUD1A32', 'SVM8A89', 'SWT1F10', 'SVG3D09', 'RFH3I18', 'RFH3I17', 
                                                    'BDU8D06', 'RHJ2B28', 'RHM3F06', 'RHM3F03', 'RHL6C66', 'RHL6C65', 'RHL3F59', 'RHK5H59', 'RHK5H53', 'PHD1178', 
                                                    'PHD1176', 'PHD1173', 'PHD1169', 'PHD1166', 'PHD1165', 'PHD1164', 'PHD0970', 'PHD0947', 'PHD0946', 'D0145716', 
                                                    'D0145712', 'D0145710', 'D0145707', 'D0145706', 'D0145704', 'D0145703', 'D0145679', 'D0145676', 'D0145672', 
                                                    'D0145670', 'D0145669', 'D0145665', 'D0145637', 'D0145633', 'D0145629', 'D0145618', 'D0145617', 'D0145616', 
                                                    'D0145611', 'RHK5H52', 'RHJ6F42', 'RHJ6F38', 'RHJ6F37'])

    filtro_frota = st.sidebar.multiselect("Filtrar por frota:", 
                                ['7509', '9950', '9906', '9469', '5041', '8653', '9087', '7508', '4005', '4191', '9045', '9879', '9811', '9809', 
                                '2148', '4498', '8332', '4569', '8340', '-', '4431', '7007', '8349', '8348', '9096', '8964', '9708', '9631', 
                                '8363', '8264', '8244', '9682', '8995', '9636', '9577', '8601', '9966', '9794', '9774', '8232', '9761', '4922', 
                                '9755', '9893', '8134', '9392', '5212', '5211', '5210', '5209', '5208', '7787', '7629', '2084', '3680', '8853', 
                                '9857', '9915', '8978', '8138', '3785', '8051', '9857', '8853', '3785', '8051', '9915', '8138', '8978', '2129', 
                                '8006', '3671', '8853', '3671', '3785', '8138', '9915', '2129', '8978', '8978', '8051', '8138', '8006', '3785', 
                                '9915', '8051', '9857', '8006', '8853', '3671', '2129', '9857', '3671', '8006', '2129'])

    #data_inicio = st.sidebar.date_input("Data inicio: ", datetime.now())
    #data_fim = st.sidebar.date_input("Data fim: ", datetime.now())
    
    filtro = st.button("Aplicar Filtros")

# Botão para aplicar os filtros
if filtro:
    try:
        data = consultar_registros(filtro_placa=filtro_placa, filtro_frota=filtro_frota) #data_inicio=data_inicio)
        st.write(data)
    except:
        st.write("Nenhum registro encontrado com os filtros aplicados.")
else:
    st.write("Nenhum registro encontrado com os filtros aplicados.")
