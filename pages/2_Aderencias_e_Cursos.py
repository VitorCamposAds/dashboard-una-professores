import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Aderências & Cursos | UNA", page_icon="📚", layout="wide")
st.title("📚 Módulo de Aderências & Alocação Curricular")
st.markdown("Análise profunda de cursos, áreas de conhecimento e disciplinas vinculadas aos docentes.")
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

# Gráfico 1: Top Cursos (Largura total)
st.subheader("🏛️ Top Cursos com Mais Aderências")
df_cursos = df_ader_filtrado['Curso'].value_counts().reset_index().head(10)
df_cursos.columns = ['Curso', 'Total']
fig_cursos = px.bar(df_cursos, x='Total', y='Curso', orientation='h', text='Total', color='Total', color_continuous_scale=['#8B0000', '#C8102E'])
fig_cursos.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=200, r=20, t=30, b=30))
st.plotly_chart(fig_cursos, use_container_width=True)

st.markdown("---")

# Gráfico 2: Distribuição por Grande Área (Com margem l=380 para o texto não cortar)
st.subheader("🌐 Distribuição por Grande Área")
df_areas = df_ader_filtrado['Area'].value_counts().reset_index()
df_areas.columns = ['Area', 'Total']

fig_areas = px.bar(df_areas, x='Total', y='Area', orientation='h', text='Total', color='Total', color_continuous_scale=['#B22222', '#DC143C'])
fig_areas.update_layout(
    yaxis={'categoryorder':'total ascending'}, 
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=380, r=40, t=30, b=30),
    height=500
)
st.plotly_chart(fig_areas, use_container_width=True)

st.markdown("---")
st.subheader("📋 Registros Detalhados de Aderências")
st.dataframe(df_ader_filtrado, use_container_width=True, hide_index=True)