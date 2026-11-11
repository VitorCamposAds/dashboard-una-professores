import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visão Geral & RH | UNA", page_icon="📊", layout="wide")
st.title("📊 Visão Geral: Corpo Docente & Indicadores de RH")
st.markdown("Monitoramento integrado do quadro de professores, titulações acadêmicas e tempo de casa.")
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

c1, c2, c3, c4 = st.columns(4)
c1.metric("👨‍🏫 Total Professores Únicos", len(df_prof_filtrado), delta="Base Sincronizada")
c2.metric("🎓 Mestres e Doutores", len(df_prof_filtrado[df_prof_filtrado['Titulacao'].isin(['Mestrado', 'Doutorado', 'Pós-Doutorado'])]))
c3.metric("📚 Aderências Ativas", len(df_ader))
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
st.subheader("📋 Detalhamento do Corpo Docente")
st.dataframe(df_prof_filtrado[['Matricula', 'Nome', 'Formacao', 'Titulacao', 'CurriculoLattes']], use_container_width=True, hide_index=True)