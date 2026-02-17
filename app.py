import streamlit as st
import time
from datetime import datetime
from src.database import Database
from src.ai_engine import AIEngine
from src.utils import carregar_imagem_drive

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="Qualidade Injeção", layout="wide")

# --- 2. INICIALIZAÇÃO DO ESTADO E PERSISTÊNCIA ---
if "logout_realizado" not in st.session_state:
    st.session_state.logout_realizado = False
    
if not st.session_state.logout_realizado:
    params = st.query_params
    usuario_url = params.get("operador")
    turno_url = params.get("turno")

    if usuario_url and turno_url:
        if "identificado" not in st.session_state or not st.session_state.identificado:
            st.session_state.identificado = True
            st.session_state.input_operador = usuario_url
            st.session_state.input_turno = turno_url
else:
    usuario_url = None
    turno_url = None

if "identificado" not in st.session_state:
    st.session_state.identificado = False

if "input_operador" not in st.session_state:
    st.session_state.input_operador = ""

if "input_turno" not in st.session_state:
    st.session_state.input_turno = ""

if "confirmar_salvamento" not in st.session_state:
    st.session_state.confirmar_salvamento = False

if "msg_sucesso" not in st.session_state:
    st.session_state.msg_sucesso = False

# --- 3. CACHE ---
@st.cache_resource(show_spinner="Carregando sistema...")
def inicializar_componentes():
    try:

        db = Database(credentials_path="data/credenciais.json")
        ai = AIEngine()
        contexto = ai.extrair_texto_pdf("data/manual_processo.pdf")
        return db, ai, contexto
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        st.stop()

db, ai, contexto_manual = inicializar_componentes()

# --- 4. CSS PARA BOLINHA IA E REVISÃO  ---
st.markdown("""
<style>
    /* 1. LOCALIZA O CONTAINER DO POPOVER */
    div[data-testid=stPopover] {
        position: fixed;
        bottom: 50px;
        right: 50px;
        z-index: 999999;
        width: auto !important;
    }

    /* 2. ALVO DIRETO NO BOTÃO - TAMANHO PADRÃO (DESKTOP) */
    div[data-testid=stPopover] button {
        border-radius: 35% !important;
        width: 50px !important;
        height: 50px !important;
        min-width: 65px !important;
        min-height: 65px !important;
        background-color: #002D62 !important;
        color: white !important;
        border: 2px solid #ffffff !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4) !important;
        padding: 0px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease;
    }

    /* 3. REMOVE A SETINHA PARA FICAR LIMPO */
    div[data-testid=stPopover] button span svg {
        display: none !important;
    }

    /* Ajuste para o emoji ficar grande e centralizado */
    div[data-testid=stPopover] button p {
        font-size: 30px !important;
        margin: 0 !important;
    }

    /* MOBILE */
    @media (max-width: 600px) {
        div[data-testid=stPopover] button {
            width: 50px !important;
            height: 50px !important;
            min-width: 50px !important;
            min-height: 50px !important;
        }
        div[data-testid=stPopover] button p {
            font-size: 22px !important;
        }
        div[data-testid=stPopover] {
            bottom: 15px !important;
            right: 15px !important;
        }
    }

    /* Centralização dos inputs da tela principal */
    .stTextInput, .stSelectbox, .stNumberInput {
        max-width: 100% !important;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# --- 5. FUNÇÕES DE SUPORTE ---

def confirmar_identificacao():
    if st.session_state.input_operador and st.session_state.input_turno:
        st.session_state.identificado = True
        st.session_state.logout_realizado = False 
        st.query_params["operador"] = st.session_state.input_operador
        st.query_params["turno"] = st.session_state.input_turno

def reset_apenas_inspecao():
    """Limpa apenas os dados da peça, mantendo o operador logado."""

    if 'input_op' in st.session_state:
        st.session_state.input_op = "" 
    
    st.session_state.confirmar_salvamento = False
    
    if 'input_medida' in st.session_state:
        st.session_state.input_medida = 0.0
    if 'input_obs' in st.session_state:
        st.session_state.input_obs = ""
        
    chaves_para_deletar = [key for key in st.session_state.keys() if key.startswith("ch_")]
    for key in chaves_para_deletar:
        del st.session_state[key]

def callback_salvar_limpar(linha_dados):
    """Função chamada pelo botão (on_click) para salvar e limpar."""
    db.salvar_log(linha_dados)
    st.session_state['msg_sucesso'] = True
    reset_apenas_inspecao()

@st.dialog("Confirmar Salvamento")
def popup_salvar(linha_dados):
    st.write("Você está prestes a salvar esta inspeção no banco de dados.")
    st.info("Deseja prosseguir?")
    
    col_a, col_b = st.columns(2)
    
    if col_a.button("SALVAR NO SISTEMA", use_container_width=True, type="primary"):
        callback_salvar_limpar(linha_dados)
        st.rerun()
        
    if col_b.button("ALTERAR INSPEÇÃO", use_container_width=True):
        st.rerun() 

@st.dialog("Cancelar Operação")
def popup_cancelar():
    st.warning("⚠️ Tem certeza? Todos os dados preenchidos nesta peça serão perdidos.")
    
    col_a, col_b = st.columns(2)

    if col_a.button("🗑️ CONFIRMAR CANCELAMENTO", use_container_width=True, type="primary"):
        reset_apenas_inspecao()
        st.rerun()
        
    if col_b.button("✏️ ALTERAR INSPEÇÃO", use_container_width=True):
        st.rerun() 

# --- 6. FLUXO 1: TELA DE IDENTIFICAÇÃO (Login) ---
if not st.session_state.identificado:
    if st.query_params and st.session_state.logout_realizado:
        st.query_params.clear()

    _, col_login, _ = st.columns([1, 2, 1])
    with col_login:
        st.title("Identificação do Inspetor")
        st.text_input("Inspetor:", key="input_operador")
        st.selectbox("Turno:", ["", "1º Turno", "2º Turno", "3º Turno"], key="input_turno")
        st.button("ACESSAR SISTEMA", on_click=confirmar_identificacao, use_container_width=True)

# --- 7. FLUXO 2: SISTEMA DE INSPEÇÃO ATIVO ---
else:
    # SIDEBAR (Sanduíche com dados do login)
    with st.sidebar:
        st.header("👤 Inspetor Ativo")
        nome_inspetor = st.session_state.get('input_operador', 'Não identificado')
        turno_inspetor = st.session_state.get('input_turno', 'Não identificado')
        
        st.info(f"**Nome:** {nome_inspetor}\n\n**Turno:** {turno_inspetor}")

        if st.button("🔄 Trocar Operador"):
            st.session_state.identificado = False
            st.session_state.logout_realizado = True 
            st.session_state.input_operador = ""
            st.session_state.input_turno = ""
            st.query_params.clear() 
            st.rerun()
        
        st.divider()
        st.subheader("📋 Passagem de Turno")
        
        historico = db.obter_historico_recente(50)
        
        if historico:
            lista_ops = list(set([str(r['numero_op']) for r in historico]))[::-1]
            op_sel = st.selectbox("Analisar OP:", ["Selecione..."] + lista_ops)
            
            if st.button("🤖 Gerar Relatório de Turno", use_container_width=True):
                if op_sel != "Selecione...":
                    
                    dados_op = [r for r in historico if str(r['numero_op']) == op_sel]
                    
                    if dados_op:

                        total_inspecoes = len(dados_op)
       
                        total_reprovas = 0
                        for r in dados_op:
                            res = r.get('resultado') or r.get('resultado_final') or r.get('status')
                            if res == 'Reprovado':
                                total_reprovas += 1
             
                        lista_obs = []
                        for r in dados_op:
                            texto = r.get('observacao') or r.get('obs') or r.get('observacoes')
                            if texto and str(texto).strip():
                                lista_obs.append(str(texto))

                        texto_obs = "; ".join(lista_obs) if lista_obs else "Sem observações relevantes."

                        with st.spinner(f"Analisando {total_inspecoes} registros da OP {op_sel}..."):
                            try:
                                resumo = ai.gerar_relatorio_turno(
                                    op=op_sel, 
                                    total=total_inspecoes, 
                                    reprovas=total_reprovas, 
                                    observacoes=texto_obs
                                )

                                st.markdown("### 📢 Relatório do Supervisor")
                                st.info(resumo)
                                
                            except Exception as e:
                                st.error(f"Erro na IA: {e}")
                    else:
                        st.warning("Sem dados suficientes para esta OP.")
                else:
                    st.warning("Selecione uma OP primeiro.")

    # TELA PRINCIPAL
    _, col_main, _ = st.columns([0.1, 1, 0.1])
    with col_main:
        st.title("Inspeção Ativa")
        op_input = st.text_input("Número da OP:", key="input_op")
        
        if op_input:
            dados = db.buscar_dados_completos(op_input)
            if dados:
                st.subheader(f"Peça: {dados['nome_peca']}")
                tab1, tab2, tab3 = st.tabs(["📸 Referência", "📝 Checklist", "📊 Salvar"])
                
                with tab1:
                    st.subheader("Padrão Visual")
                    url_img = dados.get('url_imagem_padrao')
                    
                    if url_img:
                        img_pil = carregar_imagem_drive(url_img)
                        if img_pil:
                            st.image(img_pil, use_container_width=True)
                        else:
                            st.error("Erro ao carregar imagem. Verifique se o link é público.")
                    else:
                        st.info("Nenhuma imagem cadastrada para esta OP.")

                with tab2:
                    st.subheader("Conferência Visual")
                    checks = dados['checklist_visual'].split(";")
                    respostas = [st.checkbox(c.strip(), key=f"ch_{i}") for i, c in enumerate(checks) if c.strip()]
                    st.divider()
                    medida = st.number_input("Valor Medido (mm):", format="%.3f", key="input_medida")

                with tab3:

                    obs = st.text_area("Observações Técnicas:", key="input_obs", placeholder="Digite aqui se houver alguma observação...")
                    
                    status_v = "OK" if not any(respostas) else "NG (Defeito)"
                    limite_sup = float(dados['cota_nominal']) + float(dados['tolerancia_mais'])
                    limite_inf = float(dados['cota_nominal']) - float(dados['tolerancia_menos'])

                    status_dim = "Aprovado" if limite_inf <= medida <= limite_sup else "Reprovado"

                    if status_v == "OK" and status_dim == "Aprovado":
                        resultado_final = "Aprovado"
                        cor_resultado = "#28a745" 
                        icone_resultado = "✅"
                    else:
                        resultado_final = "Reprovado"
                        cor_resultado = "#dc3545" 
                        icone_resultado = "🚫"

                    st.divider()

                    st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid {cor_resultado};">
<h4 style="margin-top:0;">📝 Resumo da Inspeção</h4>
<p><b>OP:</b> {op_input}</p>
<p><b>Inspetor:</b> {nome_inspetor}</p>
<p><b>Turno:</b> {turno_inspetor}</p>
<p><b>Peça:</b> {dados['nome_peca']}</p>
<p><b>Visual:</b> {status_v}</p>
<p><b>Medição:</b> {medida} mm <span style="font-size:0.8em; color:gray">(Nominal: {dados['cota_nominal']})</span></p>
<p><b>Observação:</b> {obs if obs else "Nenhuma"}</p>
<hr style="margin: 5px 0;">
<h3 style="color: {cor_resultado}; text-align: center; margin-bottom: 0;">
    {icone_resultado} {resultado_final.upper()}
</h3>
</div>
""", unsafe_allow_html=True)

                    st.write("")

                    col_save, col_cancel = st.columns(2)

                    if col_save.button("CONFIRMAR E SALVAR", use_container_width=True, type="primary"):
                        linha_para_salvar = [
                            datetime.now().strftime("%d/%m/%Y %H:%M"), 
                            op_input, 
                            st.session_state.input_operador, 
                            st.session_state.input_turno, 
                            status_v, 
                            medida, 
                            resultado_final, 
                            obs
                        ]
                        popup_salvar(linha_para_salvar)


                    if col_cancel.button("CANCELAR", use_container_width=True):
                        popup_cancelar()

                    if st.session_state.get('msg_sucesso'):
                        st.success("REGISTRO SALVO COM SUCESSO!")
                        st.session_state['msg_sucesso'] = False
            else:
                st.error("OP não encontrada.")

# --- 8. ASSISTENTE IA (BOLINHA FIXA) ---
with st.popover("🤖"):
    st.subheader("🤖 Assistente IA")
    st.write("Consulte o manual técnico:")
    
    duvida_ia = st.text_input("Sua dúvida:", key="txt_duvida_ia")
    
    if st.button("Enviar Pergunta", key="btn_enviar_ia"):
        if duvida_ia:
            with st.spinner("Buscando no manual..."):
                try:
                    resposta = ai.consultar_manual(duvida_ia, contexto_manual)
                    st.info(resposta)
                except AttributeError:
                    st.error("Erro: A função 'consultar_manual' não existe no seu arquivo AI.")
                except Exception as e:
                    st.error(f"Erro inesperado: {e}")
        else:

            st.warning("Escreva algo antes de enviar.")
