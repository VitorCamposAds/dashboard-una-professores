import streamlit as st

st.set_page_config(
    page_title="Hub Executivo | UNA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main { background-color: #fcfcfc; }
        .hero-banner {
            background: linear-gradient(135deg, #C8102E 0%, #900B1F 100%);
            padding: 45px;
            border-radius: 16px;
            color: white;
            box-shadow: 0 10px 25px rgba(200, 16, 46, 0.2);
            margin-bottom: 30px;
        }
        .card-exec {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            border-top: 4px solid #C8102E;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            height: 100%;
        }
        h1, h2, h3 { color: #1e293b; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-banner">
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 10px;">🎓 Hub de Gestão de Corpo Docente & Aderências</h1>
        <h3 style="color: #ffcccc; font-weight: 400; margin-bottom: 20px;">65 Anos Mudando Mundos • Inteligência Acadêmica & RH</h3>
        <p style="font-size: 1.1rem; color: #f8d7da; max-width: 900px; line-height: 1.5;">
            Plataforma executiva de alta precisão para monitoramento do corpo docente, cruzamentos oficiais com a base de Recursos Humanos, gestão de titulações, aderências curriculares e otimização de disponibilidades horárias por unidade.
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
                Utilize a barra lateral para segmentar os dados por <b>Unidade</b>, <b>Titulação</b> ou <b>Vínculo</b>. Os filtros se aplicam simultaneamente a todas as páginas do sistema.
            </p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="card-exec">
            <h3>📊 2. Módulos de Análise</h3>
            <p style="color: #64748b; font-size: 0.95rem;">
                Navegue pelas abas do menu lateral esquerdo: <b>Visão Geral RH</b>, <b>Aderências e Cursos</b> e <b>Matriz de Disponibilidades</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
        <div class="card-exec">
            <h3>🔒 3. Governança e Compliance</h3>
            <p style="color: #64748b; font-size: 0.95rem;">
                Base reconciliada por algoritmos de similaridade semântica contra o cadastro oficial de colaboradores, garantindo unicidade de matrículas e histórico íntegro.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.success("✨ **Pronto para começar?** Selecione uma das páginas no menu lateral esquerdo para explorar os painéis analíticos.")