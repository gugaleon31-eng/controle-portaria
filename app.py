import datetime
import pandas as pd
import streamlit as st

# URL da Logo do Grupo Status
LOGO_URL = "https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/logo.png"

# Configuração da página e ícone da aba
st.set_page_config(
    page_title="Bougainville Belém | Controle de Portaria",
    page_icon=LOGO_URL,
    layout="centered"
)

# Inicialização da memória de registros na sessão
if "registros_portaria" not in st.session_state:
    st.session_state["registros_portaria"] = []

# CSS Customizado (Ajuste visual e regras de impressão)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(rgba(0, 28, 56, 0.70), rgba(0, 28, 56, 0.85)), 
                    url("https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/fundo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF;
    }

    .brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }

    .brand-logo {
        height: 120px;
        width: auto;
        object-fit: contain;
    }

    .portal-tag {
        background-color: rgba(255, 255, 255, 0.15);
        border: 1px solid #FFFFFF;
        color: #FFFFFF;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stTextInput > label, .stSelectbox > label {
        color: #FFFFFF !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    @media print {
        [data-testid="stSidebar"], .stTextInput, .stButton, .stSelectbox, header, footer {
            display: none !important;
        }
        .stApp {
            background: #FFFFFF !important;
            color: #000000 !important;
        }
        .hero-title, label, h1, h2, h3, span, div, td, th {
            color: #000000 !important;
            text-shadow: none !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho da aplicação
st.markdown(f"""
    <div class="brand-bar">
        <img src="{LOGO_URL}" class="brand-logo" alt="Grupo Status">
        <div class="portal-tag">CONTROLE DE PORTARIA</div>
    </div>
""", unsafe_allow_html=True)

st.title("📦 Registro de Entrada e Saída")
st.markdown("---")

# Form de Cadastro de Movimentação
with st.form(key="form_portaria", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        lote_quadra = st.text_input("Lote / Quadra (Ex: 28-47)").strip().upper()
        empresa_nome = st.text_input("Empresa / Nome do Visitante")
        descricao = st.text_input("Descrição (Material / Motivo)")

    with col2:
        condutor = st.text_input("Nome do Motorista / Entregador")
        placa_veiculo = st.text_input("Placa do Veículo").strip().upper()
        tipo_movimento = st.selectbox("Tipo de Movimentação", ["Entrada", "Saída"])

    btn_salvar = st.form_submit_button("💾 Registrar Movimentação")

    if btn_salvar:
        if lote_quadra and empresa_nome:
            agora = datetime.datetime.now()
            st.session_state["registros_portaria"].append({
                "Data": agora.strftime("%d/%m/%Y"),
                "Hora": agora.strftime("%H:%M:%S"),
                "Lote/Quadra": lote_quadra,
                "Origem/Empresa": empresa_nome,
                "Descrição": descricao,
                "Responsável": condutor,
                "Placa": placa_veiculo,
                "Movimento": tipo_movimento
            })
            st.success("✅ Entrada registrada com sucesso!")
        else:
            st.error("⚠️ Os campos 'Lote / Quadra' e 'Empresa / Nome' são obrigatórios.")

st.markdown("---")

# Exibição da Tabela e Relatório
st.subheader("📋 Movimentações Registradas Hoje")

if st.session_state["registros_portaria"]:
    df_registros = pd.DataFrame(st.session_state["registros_portaria"])
    st.dataframe(df_registros, use_container_width=True)

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        # Botão para acionar a janela de impressão
        st.components.v1.html(
            """
            <button onclick="window.parent.print()" style="
                background-color: #0284C7;
                color: white;
                padding: 10px 18px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
            ">🖨️ Imprimir Relatório Diário</button>
            """,
            height=50
        )

    with col_btn2:
        csv = df_registros.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar Planilha (CSV)",
            data=csv,
            file_name=f"relatorio_portaria_{datetime.datetime.now().strftime('%d_%m_%Y')}.csv",
            mime="text/csv",
            use_container_width=True
        )
else:
    st.info("Nenhuma movimentação registrada no momento.")
