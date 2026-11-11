import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Hub Executivo | UNA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS globais da aplicação
st.markdown("""
    <style>
        .stApp { background-color: #f4f6f9; }
        .main { background-color: #f4f6f9; }
        
        .hero-box {
            background-color: #DE0309;
            padding: 35px 40px;
            border-radius: 16px;
            color: #ffffff;
            box-shadow: 0 10px 25px rgba(222, 3, 9, 0.25);
            margin-bottom: 30px;
            text-align: center;
        }
        .card-exec {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            border-top: 4px solid #DE0309;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            height: 100%;
        }
        h2, h3 { color: #1e293b; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Função segura para carregar a logo em base64
def render_logo():
    if os.path.exists("logo_una.png"):
        with open("logo_una.png", "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(
            f'<div style="text-align: center;"><img src="data:image/png;base64,{encoded}" style="width: 130px; margin-bottom: 15px;"></div>',
            unsafe_allow_html=True
        )

# Bloco unificado com a logo centralizada e textos dentro da caixa vermelha #DE0309
st.markdown('<div class="hero-box">', unsafe_allow_html=True)
render_logo()
st.markdown("""
        <h1 style="color: #ffffff !important; font-size: 2.0rem; margin-top: 0px; margin-bottom: 8px;">Hub de Gestão de Corpo Docente & Aderências</h1>
        <h3 style="color: #ffe6e6 !important; font-weight: 400; font-size: 1.1rem; margin-bottom: 15px;">65 Anos Mudando Mundos • Inteligência Acadêmica & RH</h3>
        <p style="font-size: 1.0rem; color: #ffffff !important; max-width: 850px; margin: 0 auto; line-height: 1.4;">
            Plataforma executiva de alta precisão para monitoramento do corpo docente, cruzamentos oficiais com a base de Recursos Humanos, gestão avançada de titulações, aderências curriculares e otimização de disponibilidades horárias por unidade.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("## 🧭 Guia Operacional e Arquitetura do Painel")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
        <div class="card-exec">
            <h3>🎛️ 1. Filtros Globais Dinâmicos</h3>
            <p style="color: #64748b; font-size: 0.95rem;">
                Utilize a barra lateral para segmentar os dados por <b>Unidade</b>, <b>Titulação</b> ou <b>Área</b>. Os filtros adaptam instantaneamente os indicadores e gráficos.
            </p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="card-exec">
            <h3>📊 2. Módulos Aprofundados</h3>
            <p style="color: #64748b; font-size: 0.95rem;">
                Explore as novas abas analíticas: <b>Visão Geral & RH</b>, <b>Aderências, Cursos & Disciplinas</b> e <b>Matriz de Disponibilidades & Turnos</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
        <div class="card-exec">
            <h3>🔒 3. Governança e Compliance</h3>
            <p style="color: #64748b; font-size: 0.95rem;">
                Base reconciliada por inteligência semântica contra o cadastro oficial corporativo, garantindo unicidade de matrículas e auditoria completa.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.success("✨ **Pronto para começar?** Selecione uma das páginas no menu lateral esquerdo para explorar os painéis analíticos avançados.")
