import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mapa das Unidades | UNA", page_icon="🗺️", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #f4f6f9; }
        .main { background-color: #f4f6f9; }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ Mapeamento Geoespacial & Indicadores por Unidade")
st.markdown("Visualização geográfica dos polos da UNA integrada com o volume de disponibilidades e capacidade docente.")
st.markdown("---")

@st.cache_data
def carregar_dados():
    file_path = 'aderencias_base_professores_revisado.xlsx'
    xls = pd.ExcelFile(file_path)
    return (
        pd.read_excel(xls, sheet_name='Base_RH'),
        pd.read_excel(xls, sheet_name='DispDoc_Aderencias'),
        pd.read_excel(xls, sheet_name='DispDoc_Professores'),
        pd.read_excel(xls, sheet_name='DispDoc_Disponibilidades')
    )

df_rh, df_ader, df_prof, df_disp = carregar_dados()

# Dicionário de coordenadas fixas aproximadas para as unidades da UNA em BH / Minas Gerais
# (Garante que o mapa plote os pontos perfeitamente mesmo se a base vier apenas com o texto da unidade)
coordenadas_unidades = {
    'Aimorés': {'lat': -19.9245, 'lon': -43.9450},
    'Liberdade': {'lat': -19.9281, 'lon': -43.9383},
    'Centro': {'lat': -19.9213, 'lon': -43.9388},
    'Barreiro': {'lat': -19.9792, 'lon': -44.0261},
    'Linha Verde': {'lat': -19.8351, 'lon': -43.9272},
    'Contagem': {'lat': -19.9315, 'lon': -44.0539},
    'Betim': {'lat': -19.9676, 'lon': -44.1983},
    'Sete Lagoas': {'lat': -19.4627, 'lon': -44.2486},
    'Cataguases': {'lat': -21.3886, 'lon': -42.6978},
    'Pouso Alegre': {'lat': -22.2300, 'lon': -45.9356}
}

# Agrupando dados por unidade da base de disponibilidades
if 'Unidade' in df_disp.columns:
    df_map_resumo = df_disp.groupby('Unidade').agg(
        Total_Disponibilidades=('Professor', 'count'),
        Professores_Unicos=('Professor', 'nunique')
    ).reset_index()

    # Mapeando lat e lon com base no nome da unidade
    df_map_resumo['lat'] = df_map_resumo['Unidade'].apply(lambda x: next((v['lat'] for k, v in coordenadas_unidades.items() if k.lower() in str(x).lower()), -19.9208))
    df_map_resumo['lon'] = df_map_resumo['Unidade'].apply(lambda x: next((v['lon'] for k, v in coordenadas_unidades.items() if k.lower() in str(x).lower()), -43.9378))
else:
    df_map_resumo = pd.DataFrame(columns=['Unidade', 'Total_Disponibilidades', 'Professores_Unicos', 'lat', 'lon'])

# Métricas Executivas da Página de Mapa
c1, c2, c3 = st.columns(3)
c1.metric("🏫 Unidades Mapeadas", len(df_map_resumo))
c2.metric("📌 Total de Vagas/Horários Mapeados", int(df_map_resumo['Total_Disponibilidades'].sum()) if not df_map_resumo.empty else 0)
c3.metric("👨‍🏫 Cobertura Geográfica", "Minas Gerais (BH e Região)")

st.markdown("##")

# Filtro de busca textual específico para a tabela/mapa
busca_mapa = st.text_input("🔍 Filtrar unidade no mapa e na tabela:", key="busca_mapa", placeholder="Digite o nome da unidade...")
df_tabela_mapa = df_map_resumo.copy()
if busca_mapa and busca_mapa.strip() != "":
    mask = df_tabela_mapa.astype(str).apply(lambda x: x.str.contains(busca_mapa, case=False, na=False)).any(axis=1)
    df_tabela_mapa = df_tabela_mapa[mask]

# Exibição do Mapa Nativo do Streamlit com os pontos filtrados
if not df_tabela_mapa.empty and 'lat' in df_tabela_mapa.columns:
    st.subheader("📍 Localização Espacial dos Polos UNA")
    st.map(df_tabela_mapa, latitude='lat', longitude='lon', size='Total_Disponibilidades', color=None, zoom=11)
else:
    st.info("Nenhuma unidade encontrada para os critérios de busca informados.")

st.markdown("---")
st.subheader("📋 Consolidado Analítico por Unidade")
st.dataframe(df_tabela_mapa[['Unidade', 'Total_Disponibilidades', 'Professores_Unicos']], use_container_width=True, hide_index=True)