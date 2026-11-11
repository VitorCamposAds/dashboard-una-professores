import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Disponibilidades | UNA", page_icon="🕒", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #f4f6f9; }
        .main { background-color: #f4f6f9; }
    </style>
""", unsafe_allow_html=True)

st.title("🕒 Matriz de Disponibilidades & Otimização de Turnos")
st.markdown("Cruzamento avançado de horários, dias da semana, distribuição espacial por unidade acadêmica e gargalos de alocação.")
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

st.sidebar.header("🎛️ Filtros de Disponibilidade")
unidades_disponiveis = sorted([str(x) for x in df_disp['Unidade'].dropna().unique()])
unidade_selecionada = st.sidebar.multiselect("Filtrar por Unidade(s):", unidades_disponiveis, default=unidades_disponiveis, key="uni_p3")

dias_disponiveis = sorted([str(x) for x in df_disp['Dia'].dropna().unique()])
dia_selecionado = st.sidebar.multiselect("Filtrar por Dia:", dias_disponiveis, default=dias_disponiveis, key="dia_p3")

df_disp_filtrado = df_disp[
    df_disp['Unidade'].astype(str).isin(unidade_selecionada) & 
    df_disp['Dia'].astype(str).isin(dia_selecionado)
]

c1, c2, c3 = st.columns(3)
c1.metric("📌 Total de Horários Disponíveis", len(df_disp_filtrado))
c2.metric("🏫 Unidades na Seleção", df_disp_filtrado['Unidade'].nunique())
c3.metric("👨‍🏫 Professores Envolvidos", df_disp_filtrado['Professor'].nunique())

st.markdown("##")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Volume de Disponibilidades por Unidade")
    df_uni = df_disp_filtrado['Unidade'].value_counts().reset_index()
    df_uni.columns = ['Unidade', 'Total']
    fig_uni = px.bar(df_uni, x='Total', y='Unidade', orientation='h', text='Total', color='Total', color_continuous_scale=['#8B0000', '#C8102E'])
    fig_uni.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_uni, use_container_width=True)

with col2:
    st.subheader("📅 Disponibilidade por Dia da Semana")
    dias_ordem = ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB']
    fig_dias = px.histogram(df_disp_filtrado, x='Dia', category_orders={'Dia': dias_ordem}, color='Dia', color_discrete_sequence=['#C8102E', '#E63946', '#FF6B6B', '#D90429', '#8D0801', '#5C0601'])
    fig_dias.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_dias, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("⏰ Distribuição por Turno / Horário")
    if 'Horario' in df_disp_filtrado.columns:
        fig_horario = px.pie(df_disp_filtrado, names='Horario', hole=0.5, color_discrete_sequence=['#C8102E', '#FF4D4D', '#A30000'])
        fig_horario.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_horario, use_container_width=True)

with col4:
    st.subheader("📊 Cruzamento Unidade x Período (Stack)")
    if 'Horario' in df_disp_filtrado.columns and 'Unidade' in df_disp_filtrado.columns:
        df_cruz = df_disp_filtrado.groupby(['Unidade', 'Horario']).size().reset_index(name='Total')
        fig_cruz = px.bar(df_cruz, x='Unidade', y='Total', color='Horario', barmode='stack', color_discrete_sequence=['#C8102E', '#FF6B6B', '#5C0601'])
        fig_cruz.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_cruz, use_container_width=True)

st.markdown("---")

st.subheader("🔥 Matriz de Calor: Intensidade de Horários por Unidade e Dia")
if 'Unidade' in df_disp_filtrado.columns and 'Dia' in df_disp_filtrado.columns:
    df_heat = df_disp_filtrado.groupby(['Unidade', 'Dia']).size().reset_index(name='Total')
    fig_heat = px.density_heatmap(df_heat, x='Dia', y='Unidade', z='Total', color_continuous_scale=['#ffffff', '#FF6B6B', '#C8102E', '#5C0601'], category_orders={'Dia': ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB']})
    fig_heat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")
st.subheader("📋 Registros Detalhados de Disponibilidades")
st.dataframe(df_disp_filtrado, use_container_width=True, hide_index=True)
