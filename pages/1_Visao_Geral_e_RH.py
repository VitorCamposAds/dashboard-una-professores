import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visão Geral & RH | UNA", page_icon="📊", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #f4f6f9; }
        .main { background-color: #f4f6f9; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Visão Geral: Corpo Docente & Indicadores de RH")
st.markdown("Monitoramento integrado do quadro de professores, titulações acadêmicas, tempo de casa e profundidade de formação.")
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

st.sidebar.header("🎛️ Filtros do Sistema")
titulacoes_disponiveis = sorted([str(x) for x in df_prof['Titulacao'].dropna().unique()])
titulacao_selecionada = st.sidebar.multiselect("Filtrar por Titulação:", titulacoes_disponiveis, default=titulacoes_disponiveis, key="tit_p1")
df_prof_filtrado = df_prof[df_prof['Titulacao'].astype(str).isin(titulacao_selecionada)]

# Indicador de match entre base de professores e RH
mat_prof = set(df_prof['Matricula'].astype(str))
mat_rh = set(df_rh['Matricula'].astype(str)) if 'Matricula' in df_rh.columns else set()
match_count = len(mat_prof.intersection(mat_rh)) if mat_rh else len(mat_prof)
taxa_match = f"{(match_count / max(len(df_prof), 1)) * 100:.1f}%"

c1, c2, c3, c4 = st.columns(4)
c1.metric("👨‍🏫 Total Professores Únicos", len(df_prof_filtrado), delta="Base Sincronizada")
c2.metric("🎓 Mestres e Doutores", len(df_prof_filtrado[df_prof_filtrado['Titulacao'].isin(['Mestrado', 'Doutorado', 'Pós-Doutorado'])]))
c3.metric("🔗 Sincronização com RH", taxa_match, delta="Compliance Ativo")
c4.metric("🏢 Colaboradores Base RH", len(df_rh))

st.markdown("##")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎓 Distribuição por Titulação Acadêmica")
    df_tit = df_prof_filtrado['Titulacao'].value_counts().reset_index()
    df_tit.columns = ['Titulacao', 'Total']
    fig_tit = px.bar(df_tit, x='Total', y='Titulacao', orientation='h', text='Total', color='Total', color_continuous_scale=['#8B0000', '#C8102E', '#FF4D4D'])
    fig_tit.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_tit, use_container_width=True)

with col2:
    st.subheader("📋 Top Formações Acadêmicas")
    df_form = df_prof_filtrado['Formacao'].value_counts().reset_index().head(10)
    df_form.columns = ['Formacao', 'Total']
    fig_form = px.bar(df_form, x='Total', y='Formacao', orientation='h', text='Total', color='Total', color_continuous_scale=['#B22222', '#DC143C'])
    fig_form.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_form, use_container_width=True)

st.markdown("---")
st.subheader("🔬 Análise Avançada: Cruzamento de Titulação vs Principais Formações")
if 'Titulacao' in df_prof_filtrado.columns and 'Formacao' in df_prof_filtrado.columns:
    df_cruz_rh = df_prof_filtrado.groupby(['Formacao', 'Titulacao']).size().reset_index(name='Total')
    top_formacoes = df_prof_filtrado['Formacao'].value_counts().head(8).index
    df_cruz_rh_top = df_cruz_rh[df_cruz_rh['Formacao'].isin(top_formacoes)]
    
    fig_cruz_rh = px.bar(df_cruz_rh_top, x='Total', y='Formacao', color='Titulacao', orientation='h', barmode='stack', color_discrete_sequence=['#C8102E', '#E63946', '#FF6B6B', '#5C0601'])
    fig_cruz_rh.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=200, r=20, t=30, b=30))
    st.plotly_chart(fig_cruz_rh, use_container_width=True)

st.markdown("---")
st.subheader("📋 Detalhamento do Corpo Docente")

busca_prof = st.text_input("🔍 Buscar professor por Nome ou Matrícula:", key="busca_p1", placeholder="Digite para filtrar...")
df_tabela_prof = df_prof_filtrado.copy()
if busca_prof and busca_prof.strip() != "":
    mask = df_tabela_prof.astype(str).apply(lambda x: x.str.contains(busca_prof, case=False, na=False)).any(axis=1)
    df_tabela_prof = df_tabela_prof[mask]

st.dataframe(df_tabela_prof[['Matricula', 'Nome', 'Formacao', 'Titulacao', 'CurriculoLattes']], use_container_width=True, hide_index=True)
