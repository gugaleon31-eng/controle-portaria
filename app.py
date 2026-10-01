import datetime
import pandas as pd
import streamlit as st

# URL da Logo do Grupo Status
LOGO_URL = "https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/logo.png"

# Configuração da página e ícone da aba
st.set_page_config(
    page_title="Bougainville Belém | Controle de Portaria",
    page_icon=LOGO_URL,
    layout="wide"
)

# Inicialização da memória de registros na sessão
if "registros_portaria" not in st.session_state:
    st.session_state["registros_portaria"] = []

# CSS Customizado com suporte otimizado para Impressão/PDF
st.markdown("""
    <style>
    /* Ocultar elementos padrão do Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    
    .stApp {
        background: linear-gradient(rgba(0, 28, 56, 0.70), rgba(0, 28, 56, 0.85)), 
                    url("https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/fundo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF;
    }

    /* Barra Superior no Ecra */
    .brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }

    .brand-logo {
        height: 100px;
        width: auto;
        object-fit: contain;
    }

    .portal-tag {
        background-color: rgba(255, 255, 255, 0.15);
        border: 1px solid #FFFFFF;
        color: #FFFFFF;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    /* Estilização dos inputs no ecra */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stTextInput > label, .stSelectbox > label {
        color: #FFFFFF !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    /* Ocultar cabeçalho exclusivo de impressão no ecrã */
    .print-header {
        display: none;
    }

    /* ==========================================================================
       REGRAS DE IMPRESSÃO (PDF / IMPRESSORA) - ECONOMIA DE TINTA E ESTILO LIMPO
       ========================================================================== */
    @media print {
        /* Ocultar formulários, botões, barras e navegações */
        [data-testid="stSidebar"], 
        .stButton, 
        .stForm, 
        form, 
        iframe, 
        button, 
        header, 
        footer,
        .brand-bar {
            display: none !important;
        }

        /* Fundo limpo e texto escuro */
        .stApp {
            background: #FFFFFF !important;
            color: #000000 !important;
        }

        /* Mostrar cabeçalho institucional limpo */
        .print-header {
            display: flex !important;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #000;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }

        .print-header img {
            max-height: 80px;
            filter: grayscale(100%); /* Opcional: converte logo para PB se preferir */
        }

        .print-header-text {
            text-align: right;
            color: #000;
        }

        .print-header-text h2 {
            margin: 0;
            font-size: 20px;
            color: #000 !important;
        }

        .print-header-text p {
            margin: 2px 0 0 0;
            font-size: 12px;
            color: #333 !important;
        }

        h1, h2, h3, h4, span, div, p, td, th {
            color: #000000 !important;
            text-shadow: none !important;
        }

        /* Ajustes de tabelas para impressão */
        table {
            border-collapse: collapse !important;
            width: 100% !important;
        }

        th, td {
            border: 1px solid #666 !important;
            padding: 8px !important;
            font-size: 11px !important;
            color: #000 !important;
        }

        th {
            background-color: #f0f0f0 !important;
            font-weight: bold !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho na Tela
st.markdown(f"""
    <div class="brand-bar">
        <img src="{LOGO_URL}" class="brand-logo" alt="Grupo Status">
        <div class="portal-tag">BOUGAINVILLE BELÉM | CONTROLE DE PORTARIA</div>
    </div>
""", unsafe_allow_html=True)

# Cabeçalho exclusivo para Impressão/PDF
agora_fmt = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")
st.markdown(f"""
    <div class="print-header">
        <img src="{LOGO_URL}" alt="Logo">
        <div class="print-header-text">
            <h2>RELATÓRIO DE CONTROLE DE PORTARIA</h2>
            <p><strong>Empreendimento:</strong> Bougainville Belém</p>
            <p><strong>Gerado em:</strong> {agora_fmt}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.title("🚗 Controle de Portaria - Entrada e Saída")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Nova Entrada", "🚪 Registrar Saída"])

# Tab 1: Registrar Nova Entrada
with tab1:
    with st.form(key="form_portaria_entrada", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lote_quadra = st.text_input("Lote / Quadra (Ex: 28-47)").strip().upper()
            empresa_nome = st.text_input("Empresa / Nome do Visitante")
            
        with col2:
            condutor = st.text_input("Nome do Motorista / Entregador")
            placa_veiculo = st.text_input("Placa do Veículo").strip().upper()

        with col3:
            autorizado_por = st.text_input("Autorizado Por (Responsável)")
            descricao = st.text_input("Descrição / Motivo / Material")

        btn_salvar = st.form_submit_button("💾 Registrar Entrada")

        if btn_salvar:
            if lote_quadra and empresa_nome and autorizado_por:
                agora = datetime.datetime.now()
                novo_id = len(st.session_state["registros_portaria"]) + 1
                
                st.session_state["registros_portaria"].append({
                    "ID": novo_id,
                    "Data Entrada": agora.strftime("%d/%m/%Y"),
                    "Hora Entrada": agora.strftime("%H:%M:%S"),
                    "Hora Saída": "Em Aberto",
                    "Lote/Quadra": lote_quadra,
                    "Visitante/Empresa": empresa_nome,
                    "Motorista": condutor,
                    "Placa": placa_veiculo,
                    "Autorizado Por": autorizado_por,
                    "Descrição": descricao,
                    "Status": "Dentro do Condomínio"
                })
                st.success("✅ Entrada registrada com sucesso!")
            else:
                st.error("⚠️ Os campos 'Lote / Quadra', 'Empresa / Nome' e 'Autorizado Por' são obrigatórios.")

# Tab 2: Registrar Saída
with tab2:
    em_aberto = [r for r in st.session_state["registros_portaria"] if r["Status"] == "Dentro do Condomínio"]
    
    if em_aberto:
        st.subheader("Veículos / Visitantes no Condomínio")
        
        opcoes = {f"ID #{r['ID']} - {r['Placa']} ({r['Visitante/Empresa']} - Lote {r['Lote/Quadra']})": r["ID"] for r in em_aberto}
        selecionado_label = st.selectbox("Selecione o registro para dar saída:", list(opcoes.keys()))
        
        if st.button("🚪 Confirmar Saída"):
            registro_id = opcoes[selecionado_label]
            hora_saida = datetime.datetime.now().strftime("%H:%M:%S")
            
            for reg in st.session_state["registros_portaria"]:
                if reg["ID"] == registro_id:
                    reg["Hora Saída"] = hora_saida
                    reg["Status"] = "Finalizado"
                    break
            
            st.success(f"✅ Saída registrada com sucesso às {hora_saida}!")
            st.rerun()
    else:
        st.info("Nenhum veículo/visitante com entrada pendente de saída no momento.")

st.markdown("---")

# Exibição do Relatório
st.subheader("📋 Relatório de Movimentações")

if st.session_state["registros_portaria"]:
    df_registros = pd.DataFrame(st.session_state["registros_portaria"])
    
    # Reordenar colunas para exibição
    colunas_ordem = [
        "ID", "Data Entrada", "Hora Entrada", "Hora Saída", 
        "Lote/Quadra", "Visitante/Empresa", "Motorista", 
        "Placa", "Autorizado Por", "Descrição", "Status"
    ]
    df_registros = df_registros[colunas_ordem]
    
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
                font-size: 15px;
            ">🖨️ Imprimir / Guardar PDF (Modelo Limpo)</button>
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
    st.info("Nenhuma movimentação registrada até ao momento.")
