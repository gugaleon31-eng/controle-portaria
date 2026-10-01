import datetime
import sqlite3
from zoneinfo import ZoneInfo
import pandas as pd
import streamlit as st

# URL da Logo do Grupo Status
LOGO_URL = "https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/logo.png"

# Fuso horário de Brasília/Belém
FUSO_BELEM = ZoneInfo("America/Belem")

# Configuração da página
st.set_page_config(
    page_title="Bougainville Belém | Controle de Portaria",
    page_icon=LOGO_URL,
    layout="wide"
)

# ------------------------------------------------------------------------------
# CONEXÃO E CRIAÇÃO DO BANCO DE DADOS (PERSISTÊNCIA AO DAR F5)
# ------------------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect("portaria.db", check_same_thread=False)
    cursor = conn.cursor()
    # Tabela principal de movimentações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_entrada TEXT,
            hora_entrada TEXT,
            hora_saida TEXT,
            lote_quadra TEXT,
            visitante_empresa TEXT,
            motorista TEXT,
            placa TEXT,
            autorizado_por TEXT,
            descricao TEXT,
            status TEXT
        )
    """)
    # Tabela de histórico de alterações/exclusões (Audit Log)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_alteracoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movimentacao_id INTEGER,
            tipo_acao TEXT,
            detalhes TEXT,
            data_hora TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_connection():
    return sqlite3.connect("portaria.db", check_same_thread=False)

def carregar_movimentacoes():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM movimentacoes ORDER BY id DESC", conn)
    conn.close()
    return df

def carregar_historico():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM historico_alteracoes ORDER BY id DESC", conn)
    conn.close()
    return df

def registrar_historico(mov_id, tipo_acao, detalhes):
    agora = datetime.datetime.now(FUSO_BELEM).strftime("%d/%m/%Y %H:%M:%S")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO historico_alteracoes (movimentacao_id, tipo_acao, detalhes, data_hora)
        VALUES (?, ?, ?, ?)
    """, (mov_id, tipo_acao, detalhes, agora))
    conn.commit()
    conn.close()

# ------------------------------------------------------------------------------
# CSS ESTILIZADO (LOGO EM DESTAQUE E IMPRESSÃO COM FUNDO BRANCO)
# ------------------------------------------------------------------------------
st.markdown(f"""
    <style>
    #MainMenu, footer, header {{ visibility: hidden; }}
    
    .stApp {{
        background: linear-gradient(rgba(0, 28, 56, 0.70), rgba(0, 28, 56, 0.85)), 
                    url("https://raw.githubusercontent.com/gugaleon036-byte/app-portaria/main/fundo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF;
    }}

    /* Barra Superior de Identificação com Logo Grande e Escura */
    .brand-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 25px;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    }}

    .brand-logo {{
        height: 110px;
        width: auto;
        object-fit: contain;
    }}

    .portal-tag {{
        background-color: #001C38;
        border: 2px solid #001C38;
        color: #FFFFFF;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 15px;
        font-weight: bold;
    }}

    .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}

    .stTextInput > label, .stSelectbox > label {{
        color: #FFFFFF !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }}

    .print-only {{
        display: none;
    }}

    /* REGRAS DE IMPRESSÃO */
    @media print {{
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {{
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            background-image: none !important;
            color: #000000 !important;
        }}

        [data-testid="stSidebar"], 
        .stButton, 
        .stForm, 
        form, 
        iframe, 
        button, 
        header, 
        footer,
        .brand-bar,
        .stTabs,
        .hide-on-print,
        [data-testid="stDataFrame"] {{
            display: none !important;
        }}

        .print-only {{
            display: block !important;
            width: 100% !important;
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }}

        .print-header-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #000000;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}

        .print-logo {{
            height: 90px;
            width: auto;
        }}

        .print-title-box {{
            text-align: right;
        }}

        .print-title-box h2 {{
            margin: 0;
            font-size: 18px;
            font-weight: bold;
            color: #000000 !important;
        }}

        .print-title-box p {{
            margin: 3px 0 0 0;
            font-size: 12px;
            color: #333333 !important;
        }}

        table.print-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        table.print-table th, table.print-table td {{
            border: 1px solid #000000;
            padding: 6px 8px;
            font-size: 10px;
            text-align: left;
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }}

        table.print-table th {{
            background-color: #F0F0F0 !important;
            font-weight: bold;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Principal no Painel
st.markdown(f"""
    <div class="brand-bar">
        <img src="{LOGO_URL}" class="brand-logo" alt="Grupo Status">
        <div class="portal-tag">BOUGAINVILLE BELÉM | CONTROLE DE PORTARIA</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="hide-on-print">Controle de Portaria - Entrada e Saída</h1>', unsafe_allow_html=True)
st.markdown('<hr class="hide-on-print">', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Nova Entrada", 
    "🚪 Registrar Saída", 
    "✏️ Editar Movimentação", 
    "❌ Excluir Movimentação",
    "📜 Histórico de Modificações"
])

# ------------------------------------------------------------------------------
# TAB 1: REGISTRAR ENTRADA
# ------------------------------------------------------------------------------
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
                agora = datetime.datetime.now(FUSO_BELEM)
                data_e = agora.strftime("%d/%m/%Y")
                hora_e = agora.strftime("%H:%M:%S")
                
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO movimentacoes 
                    (data_entrada, hora_entrada, hora_saida, lote_quadra, visitante_empresa, motorista, placa, autorizado_por, descricao, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (data_e, hora_e, "Em Aberto", lote_quadra, empresa_nome, condutor, placa_veiculo, autorizado_por, descricao, "Dentro do Condomínio"))
                mov_id = cursor.lastrowid
                conn.commit()
                conn.close()

                registrar_historico(mov_id, "CRIAÇÃO", f"Entrada registrada para {empresa_nome} (Lote: {lote_quadra}, Placa: {placa_veiculo}).")
                st.success("✅ Entrada registrada com sucesso!")
                st.rerun()
            else:
                st.error("⚠️ Os campos 'Lote / Quadra', 'Empresa / Nome' e 'Autorizado Por' são obrigatórios.")

# ------------------------------------------------------------------------------
# TAB 2: REGISTRAR SAÍDA
# ------------------------------------------------------------------------------
with tab2:
    df_mov = carregar_movimentacoes()
    em_aberto = df_mov[df_mov["status"] == "Dentro do Condomínio"]
    
    if not em_aberto.empty:
        st.subheader("Veículos / Visitantes no Condomínio")
        
        opcoes = {f"ID #{row['id']} - {row['placa']} ({row['visitante_empresa']} - Lote {row['lote_quadra']})": row["id"] for _, row in em_aberto.iterrows()}
        selecionado_label = st.selectbox("Selecione o registro para dar saída:", list(opcoes.keys()))
        
        if st.button("🚪 Confirmar Saída"):
            registro_id = opcoes[selecionado_label]
            hora_saida = datetime.datetime.now(FUSO_BELEM).strftime("%H:%M:%S")
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE movimentacoes 
                SET hora_saida = ?, status = 'Finalizado' 
                WHERE id = ?
            """, (hora_saida, registro_id))
            conn.commit()
            conn.close()

            registrar_historico(registro_id, "SAÍDA", f"Saída registrada às {hora_saida}.")
            st.success(f"✅ Saída registrada com sucesso às {hora_saida}!")
            st.rerun()
    else:
        st.info("Nenhum veículo/visitante com entrada pendente de saída no momento.")

# ------------------------------------------------------------------------------
# TAB 3: EDITAR MOVIMENTAÇÃO
# ------------------------------------------------------------------------------
with tab3:
    df_mov = carregar_movimentacoes()
    if not df_mov.empty:
        opcoes_edit = {f"ID #{row['id']} - {row['data_entrada']} - {row['visitante_empresa']} (Lote {row['lote_quadra']})": row["id"] for _, row in df_mov.iterrows()}
        edit_label = st.selectbox("Selecione a movimentação que deseja editar:", list(opcoes_edit.keys()), key="select_edit")
        
        selected_id = opcoes_edit[edit_label]
        item = df_mov[df_mov["id"] == selected_id].iloc[0]

        with st.form(key="form_editar_mov"):
            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                e_lote = st.text_input("Lote / Quadra", value=item["lote_quadra"]).strip().upper()
                e_visitante = st.text_input("Empresa / Nome", value=item["visitante_empresa"])
                e_motorista = st.text_input("Motorista", value=item["motorista"])
            with col_e2:
                e_placa = st.text_input("Placa", value=item["placa"]).strip().upper()
                e_autorizado = st.text_input("Autorizado Por", value=item["autorizado_por"])
                e_descricao = st.text_input("Descrição", value=item["descricao"])
            with col_e3:
                e_entrada = st.text_input("Hora Entrada", value=item["hora_entrada"])
                e_saida = st.text_input("Hora Saída", value=item["hora_saida"])
                e_status = st.selectbox("Status", ["Dentro do Condomínio", "Finalizado"], index=0 if item["status"] == "Dentro do Condomínio" else 1)

            btn_update = st.form_submit_button("💾 Salvar Alterações")

            if btn_update:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE movimentacoes 
                    SET lote_quadra=?, visitante_empresa=?, motorista=?, placa=?, autorizado_por=?, descricao=?, hora_entrada=?, hora_saida=?, status=?
                    WHERE id=?
                """, (e_lote, e_visitante, e_motorista, e_placa, e_autorizado, e_descricao, e_entrada, e_saida, e_status, selected_id))
                conn.commit()
                conn.close()

                detalhes = f"Edição realizada. Lote: {e_lote}, Visitante: {e_visitante}, Placa: {e_placa}, Status: {e_status}."
                registrar_historico(selected_id, "EDIÇÃO", detalhes)
                st.success("✅ Movimentação atualizada com sucesso!")
                st.rerun()
    else:
        st.info("Nenhuma movimentação registrada para edição.")

# ------------------------------------------------------------------------------
# TAB 4: EXCLUIR MOVIMENTAÇÃO
# ------------------------------------------------------------------------------
with tab4:
    df_mov = carregar_movimentacoes()
    if not df_mov.empty:
        opcoes_del = {f"ID #{row['id']} - {row['data_entrada']} - {row['visitante_empresa']} (Lote {row['lote_quadra']})": row["id"] for _, row in df_mov.iterrows()}
        del_label = st.selectbox("Selecione o registro para excluir:", list(opcoes_del.keys()), key="select_del")
        
        del_id = opcoes_del[del_label]
        item_del = df_mov[df_mov["id"] == del_id].iloc[0]

        st.warning(f"⚠️ **Atenção:** Você está prestes a excluir o registro ID #{del_id} ({item_del['visitante_empresa']} - Placa {item_del['placa']}).")
        
        if st.button("🗑️ Confirmar Exclusão Permanetemente"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM movimentacoes WHERE id=?", (del_id,))
            conn.commit()
            conn.close()

            registrar_historico(del_id, "EXCLUSÃO", f"Registro ID #{del_id} ({item_del['visitante_empresa']}, Lote {item_del['lote_quadra']}) foi excluído.")
            st.success("✅ Movimentação excluída com sucesso!")
            st.rerun()
    else:
        st.info("Nenhuma movimentação disponível para exclusão.")

# ------------------------------------------------------------------------------
# TAB 5: HISTÓRICO DE AUDITORIA
# ------------------------------------------------------------------------------
with tab5:
    st.subheader("📜 Log de Alterações e Exclusões")
    df_hist = carregar_historico()
    if not df_hist.empty:
        df_hist.columns = ["ID Log", "ID Movimentação", "Ação", "Detalhes", "Data/Hora"]
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.info("Nenhum histórico de alteração registrado ainda.")

st.markdown('<hr class="hide-on-print">', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# RELATÓRIO PRINCIPAL E IMPRESSÃO (FUNDO 100% BRANCO)
# ------------------------------------------------------------------------------
st.subheader("📋 Relatório Geral de Movimentações")

df_registros = carregar_movimentacoes()

if not df_registros.empty:
    # Ajustar nomes para exibição na tela
    df_exibicao = df_registros.rename(columns={
        "id": "ID",
        "data_entrada": "Data Entrada",
        "hora_entrada": "Hora Entrada",
        "hora_saida": "Hora Saída",
        "lote_quadra": "Lote/Quadra",
        "visitante_empresa": "Visitante/Empresa",
        "motorista": "Motorista",
        "placa": "Placa",
        "autorizado_por": "Autorizado Por",
        "descricao": "Descrição",
        "status": "Status"
    })

    st.dataframe(df_exibicao, use_container_width=True)

    # Construção limpa da tabela de impressão sem caixa preta ou erros
    agora_fmt = datetime.datetime.now(FUSO_BELEM).strftime("%d/%m/%Y às %H:%M")
    
    linhas_html = ""
    for _, row in df_exibicao.iterrows():
        linhas_html += f"<tr><td>{row['ID']}</td><td>{row['Data Entrada']}</td><td>{row['Hora Entrada']}</td><td>{row['Hora Saída']}</td><td>{row['Lote/Quadra']}</td><td>{row['Visitante/Empresa']}</td><td>{row['Motorista']}</td><td>{row['Placa']}</td><td>{row['Autorizado Por']}</td><td>{row['Descrição']}</td><td>{row['Status']}</td></tr>"

    html_impressao = f"""<div class="print-only"><div class="print-header-container"><img src="{LOGO_URL}" class="print-logo" alt="Grupo Status"><div class="print-title-box"><h2>RELATÓRIO DE CONTROLE DE PORTARIA</h2><p><strong>Empreendimento:</strong> Bougainville Belém</p><p><strong>Gerado em:</strong> {agora_fmt}</p></div></div><table class="print-table"><thead><tr><th>ID</th><th>Data</th><th>Entrada</th><th>Saída</th><th>Lote/Quadra</th><th>Visitante/Empresa</th><th>Motorista</th><th>Placa</th><th>Autorizado Por</th><th>Descrição</th><th>Status</th></tr></thead><tbody>{linhas_html}</tbody></table></div>"""

    st.markdown(html_impressao, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
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
            ">🖨️ Imprimir / Salvar PDF (Fundo Branco)</button>
            """,
            height=50
        )

    with col_btn2:
        csv = df_exibicao.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar Planilha (CSV)",
            data=csv,
            file_name=f"relatorio_portaria_{datetime.datetime.now(FUSO_BELEM).strftime('%d_%m_%Y')}.csv",
            mime="text/csv",
            use_container_width=True
        )
else:
    st.info("Nenhuma movimentação registrada até o momento.")
