import streamlit as st

st.set_page_config(
    page_title="Hub Executivo | UNA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stApp { background-color: #f4f6f9; }
        .main { background-color: #f4f6f9; }
        
        .hero-box {
            background-color: #DE0309;
            padding: 40px;
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

# Bloco unificado: Logo centralizada e textos dentro da mesma caixa vermelha #DE0309
col_l, col_c, col_r = st.columns([1, 1.2, 1])
with col_c:
    st.image("logo_una.png", use_container_width=True)

st.markdown("""
    <div class="hero-box">
        <h1 style="color: #ffffff !important; font-size: 2.3rem; margin-top: 5px; margin-bottom: 10px;">Hub de Gestão de Corpo Docente & Aderências</h1>
        <h3 style="color: #ffe6e6 !important; font-weight: 400; margin-bottom: 20px;">65 Anos Mudando Mundos • Inteligência Acadêmica & RH</h3>
        <p style="font-size: 1.1rem; color: #ffffff !important; max-width: 900px; margin: 0 auto; line-height: 1.5;">
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
