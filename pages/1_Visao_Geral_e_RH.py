import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Aderências & Cursos | UNA", page_icon="📚", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #f4f6f9; }
        .main { background-color: #f4f6f9; }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Módulo de Aderências & Alocação Curricular")
st.markdown("Análise profunda de cursos, grandes áreas de conhecimento e o ranking das disciplinas com maior demanda.")
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

st.sidebar.header("🎛️ Filtros de Aderência")
areas_disponiveis = sorted([str(x) for x in df_ader['Area'].dropna().unique()])
area_selecionada = st.sidebar.multiselect("Filtrar por Área:", areas_disponiveis, default=areas_disponiveis, key="area_p2")
df_ader_filtrado = df_ader[df_ader['Area'].astype(str).isin(area_selecionada)]

c1, c2, c3 = st.columns(3)
c1.metric("📚 Total de Aderências", len(df_ader_filtrado))
c2.metric("🏛️ Cursos Envolvidos", df_ader_filtrado['Curso'].nunique())
c3.metric("📖 Disciplinas Vinculadas", df_ader_filtrado['Disciplina'].nunique())

st.markdown("##")

st.subheader("🏛️ Top 10 Cursos com Mais Aderências")
df_cursos = df_ader_filtrado['Curso'].value_counts().reset_index().head(10)
df_cursos.columns = ['Curso', 'Total']
fig_cursos = px.bar(df_cursos, x='Total', y='Curso', orientation='h', text='Total', color='Total', color_continuous_scale=['#8B0000', '#C8102E'])
fig_cursos.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=200, r=20, t=30, b=30))
st.plotly_chart(fig_cursos, use_container_width=True)

st.markdown("---")

st.subheader("🌐 Distribuição por Grande Área de Conhecimento")
df_areas = df_ader_filtrado['Area'].value_counts().reset_index()
df_areas.columns = ['Area', 'Total']

fig_areas = px.bar(df_areas, x='Total', y='Area', orientation='h', text='Total', color='Total', color_continuous_scale=['#B22222', '#DC143C'])
fig_areas.update_layout(
    yaxis={'categoryorder':'total ascending'}, 
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=380, r=40, t=30, b=30),
    height=450
)
st.plotly_chart(fig_areas, use_container_width=True)

st.markdown("---")

st.subheader("📖 Top 10 Disciplinas com Maior Volume de Aderências")
if 'Disciplina' in df_ader_filtrado.columns:
    df_disc = df_ader_filtrado['Disciplina'].value_counts().reset_index().head(10)
    df_disc.columns = ['Disciplina', 'Total']
    fig_disc = px.bar(df_disc, x='Total', y='Disciplina', orientation='h', text='Total', color='Total', color_continuous_scale=['#900B1F', '#C8102E'])
    fig_disc.update_layout(
        yaxis={'categoryorder':'total ascending'}, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=280, r=20, t=30, b=30),
        height=450
    )
    st.plotly_chart(fig_disc, use_container_width=True)

st.markdown("---")
st.subheader("📋 Registros Detalhados de Aderências")

# Campo de busca interativo na tabela
busca_ader = st.text_input("🔍 Buscar por Curso, Disciplina ou Professor:", key="busca_p2")
df_tabela_ader = df_ader_filtrado.copy()
if busca_ader:
    mask = df_tabela_ader.astype(str).apply(lambda x: x.str.contains(busca_ader, case=False, na=False)).any(axis=1)
    df_tabela_ader = df_tabela_ader[mask]

st.dataframe(df_tabela_ader, use_container_width=True, hide_index=True)
