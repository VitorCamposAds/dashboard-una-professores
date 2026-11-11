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

# Dicionário de coordenadas
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

if 'Unidade' in df_disp.columns:
    df_disp_presencial = df_disp[
        ~df_disp['Unidade'].astype(str).str.contains("digital|ead|virtual|online", case=False, na=False)
    ].copy()

    df_map_resumo = df_disp_presencial.groupby('Unidade').agg(
        Total_Disponibilidades=('Professor', 'count'),
        Professores_Unicos=('Professor', 'nunique')
    ).reset_index()

    def buscar_coord(unidade_str, tipo):
        for k, v in coordenadas_unidades.items():
            if k.lower() in str(unidade_str).lower():
                return v[tipo]
        return None

    df_map_resumo['lat'] = df_map_resumo['Unidade'].apply(lambda x: buscar_coord(x, 'lat'))
    df_map_resumo['lon'] = df_map_resumo['Unidade'].apply(lambda x: buscar_coord(x, 'lon'))
    df_map_resumo['Estado'] = df_map_resumo['Unidade'].apply(lambda x: buscar_coord(x, 'estado') or 'Outros')

    df_map_resumo = df_map_resumo.dropna(subset=['lat', 'lon'])
else:
    df_map_resumo = pd.DataFrame(columns=['Unidade', 'Total_Disponibilidades', 'Professores_Unicos', 'lat', 'lon', 'Estado'])

c1, c2, c3 = st.columns(3)
c1.metric("🏫 Campi Presenciais Mapeados", len(df_map_resumo))
c2.metric("📌 Total de Vagas nos Polos Físicos", int(df_map_resumo['Total_Disponibilidades'].sum()) if not df_map_resumo.empty else 0)
c3.metric("🌍 Estados Abrangidos", df_map_resumo['Estado'].nunique() if not df_map_resumo.empty else 0)

st.markdown("##")

busca_mapa = st.text_input("🔍 Filtrar unidade no mapa e na tabela:", key="busca_mapa", placeholder="Digite o nome da unidade...")
df_tabela_mapa = df_map_resumo.copy()
if busca_mapa and busca_mapa.strip() != "":
    mask = df_tabela_mapa.astype(str).apply(lambda x: x.str.contains(busca_mapa, case=False, na=False)).any(axis=1)
    df_tabela_mapa = df_tabela_mapa[mask]

if not df_tabela_mapa.empty:
    st.subheader("📍 Mapa Interativo dos Campi (Passe o mouse para ver os dados)")
    
    # Usando style 'carto-positron' (fundo limpo, profissional, sem molduras toscas)
    fig_mapa = px.scatter_mapbox(
        df_tabela_mapa,
        lat="lat",
        lon="lon",
        size="Total_Disponibilidades",
        color="Estado",
        hover_name="Unidade",
        hover_data={
            "lat": False,
            "lon": False,
            "Total_Disponibilidades": True,
            "Professores_Unicos": True,
            "Estado": True
        },
        zoom=6.5,
        center={"lat": -18.5, "lon": -45.0},
        height=550,
        color_discrete_sequence=['#C8102E', '#E63946', '#8B0000', '#5C0601']
    )
    
    fig_mapa.update_layout(
        mapbox_style="carto-positron",
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            title="Estado",
            orientation="h",
            yanchor="bottom",
            y=0.02,
            xanchor="left",
            x=0.02,
            bgcolor="rgba(255,255,255,0.8)"
        )
    )
    
    st.plotly_chart(fig_mapa, use_container_width=True)
else:
    st.info("Nenhuma unidade física encontrada para os critérios informados.")

st.markdown("---")
st.subheader("📋 Consolidado Analítico por Unidade Presencial")
st.dataframe(df_tabela_mapa[['Unidade', 'Estado', 'Total_Disponibilidades', 'Professores_Unicos']], use_container_width=True, hide_index=True)
