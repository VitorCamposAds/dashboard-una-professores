import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Mapa das Unidades | UNA", page_icon="🗺️", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #f4f6f9; }
        .main { background-color: #f4f6f9; }
    </style>
""", unsafe_allow_html=True)

st.title("🗺️ Mapeamento Geoespacial & Indicadores por Unidade")
st.markdown("Visualização geográfica interativa dos campi presenciais da UNA integrada com o volume de disponibilidades e capacidade docente.")
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

# Dicionário exato com as 17 unidades oficiais da rede
coordenadas_unidades = {
    'Aimorés': {'lat': -19.9245, 'lon': -43.9450, 'estado': 'MG'},
    'Liberdade': {'lat': -19.9281, 'lon': -43.9383, 'estado': 'MG'},
    'Centro': {'lat': -19.9213, 'lon': -43.9388, 'estado': 'MG'},
    'Barreiro': {'lat': -19.9792, 'lon': -44.0261, 'estado': 'MG'},
    'Linha Verde': {'lat': -19.8351, 'lon': -43.9272, 'estado': 'MG'},
    'Contagem': {'lat': -19.9315, 'lon': -44.0539, 'estado': 'MG'},
    'Betim': {'lat': -19.9676, 'lon': -44.1983, 'estado': 'MG'},
    'Buritis': {'lat': -19.9482, 'lon': -43.9654, 'estado': 'MG'},
    'Sete Lagoas': {'lat': -19.4627, 'lon': -44.2486, 'estado': 'MG'},
    'Cataguases': {'lat': -21.3886, 'lon': -42.6978, 'estado': 'MG'},
    'Pouso Alegre': {'lat': -22.2300, 'lon': -45.9356, 'estado': 'MG'},
    'Uberlândia': {'lat': -18.9186, 'lon': -48.2772, 'estado': 'MG'},
    'Uberaba': {'lat': -19.7475, 'lon': -47.9317, 'estado': 'MG'},
    'Goiânia': {'lat': -16.6864, 'lon': -49.2643, 'estado': 'GO'},
    'Jataí': {'lat': -17.8814, 'lon': -51.7144, 'estado': 'GO'},
    'Itumbiara': {'lat': -18.4219, 'lon': -49.2153, 'estado': 'GO'},
    'Rio Verde': {'lat': -17.7944, 'lon': -50.9192, 'estado': 'GO'}
}

# Cria o DataFrame base com as exatas 17 unidades
df_base_unidades = pd.DataFrame([
    {'Unidade': k, 'Unidade_Key': k.strip().lower(), 'lat': v['lat'], 'lon': v['lon'], 'Estado': v['estado']} 
    for k, v in coordenadas_unidades.items()
])

if 'Unidade' in df_disp.columns:
    df_disp_presencial = df_disp[
        ~df_disp['Unidade'].astype(str).str.contains("digital|ead|virtual|online", case=False, na=False)
    ].copy()

    # Normaliza a chave de unidade na planilha para bater certinho no cruzamento
    df_disp_presencial['Unidade_Key'] = df_disp_presencial['Unidade'].astype(str).str.strip().str.lower()

    df_agrupado = df_disp_presencial.groupby('Unidade_Key').agg(
        Total_Disponibilidades=('Professor', 'count'),
        Professores_Unicos=('Professor', 'nunique')
    ).reset_index()

    # Faz o merge usando a chave normalizada
    df_map_resumo = pd.merge(df_base_unidades, df_agrupado, on='Unidade_Key', how='left')
    
    df_map_resumo['Total_Disponibilidades'] = df_map_resumo['Total_Disponibilidades'].fillna(0).astype(int)
    df_map_resumo['Professores_Unicos'] = df_map_resumo['Professores_Unicos'].fillna(0).astype(int)
else:
    df_map_resumo = df_base_unidades.copy()
    df_map_resumo['Total_Disponibilidades'] = 0
    df_map_resumo['Professores_Unicos'] = 0

# Força a contagem para exibir rigorosamente as 17 unidades oficiais na métrica
c1, c2, c3 = st.columns(3)
c1.metric("🏫 Campi Presenciais Mapeados", len(df_base_unidades))
c2.metric("📌 Total de Vagas nos Polos Físicos", int(df_map_resumo['Total_Disponibilidades'].sum()))
c3.metric("🌍 Estados Abrangidos", df_map_resumo['Estado'].nunique())

st.markdown("##")

busca_mapa = st.text_input("🔍 Filtrar unidade no mapa e na tabela:", key="busca_mapa", placeholder="Digite o nome da unidade...")
df_tabela_mapa = df_map_resumo.copy()
if busca_mapa and busca_mapa.strip() != "":
    mask = df_tabela_mapa.astype(str).apply(lambda x: x.str.contains(busca_mapa, case=False, na=False)).any(axis=1)
    df_tabela_mapa = df_tabela_mapa[mask]

if not df_tabela_mapa.empty:
    st.subheader("📍 Mapa Interativo dos Campi (Passe o mouse para ver os dados)")
    
    max_val = df_tabela_mapa['Total_Disponibilidades'].max()
    max_val = max_val if max_val > 0 else 1
    df_tabela_mapa['radius'] = df_tabela_mapa['Total_Disponibilidades'].apply(lambda x: int((x / max_val) * 2500 + 1000) if x > 0 else 800)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_tabela_mapa,
        get_position=["lon", "lat"],
        get_radius="radius",
        get_fill_color=[200, 16, 46, 200],  # Vermelho UNA
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1,
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(
        latitude=-18.5,
        longitude=-45.0,
        zoom=5.5,
        pitch=0,
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="light",
        tooltip={
            "html": "<b>Unidade:</b> {Unidade}<br/><b>Estado:</b> {Estado}<br/><b>Total de Horários:</b> {Total_Disponibilidades}<br/><b>Professores Únicos:</b> {Professores_Unicos}",
            "style": {"backgroundColor": "#C8102E", "color": "white", "fontFamily": "sans-serif", "padding": "10px"}
        }
    )

    st.pydeck_chart(r, use_container_width=True)
else:
    st.info("Nenhuma unidade física encontrada para os critérios informados.")

st.markdown("---")
st.subheader("📋 Consolidado Analítico por Unidade Presencial")
st.dataframe(df_tabela_mapa[['Unidade', 'Estado', 'Total_Disponibilidades', 'Professores_Unicos']], use_container_width=True, hide_index=True)
