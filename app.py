"""
================================================================================
VISIA PLATFORM - Interface Principal
================================================================================
Sistema completo de análise de impacto de projetos públicos
Metodologia VISIA - IBEDIS
================================================================================
"""

import streamlit as st
import json
import os
import sys
from datetime import datetime
import hashlib

# Adiciona diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importações dos módulos VISIA
from core.visia_engine import (
    VisiaEngine, DadosProjetoVISIA, DadosDimensaoEducacional,
    DadosDimensaoEconomica, DadosDimensaoSocialAmbiental,
    DadosDimensaoPoliticoPublica, ResultadoVISIA
)
from services.ai_extractor import VisiaAIExtractor, DadosExtraidos
from database.visia_db import (
    VisiaDatabase, TipoUsuario, StatusProjeto, StatusAnalise
)

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================

st.set_page_config(
    page_title="VISIA - Plataforma de Análise de Impacto",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CSS CUSTOMIZADO
# ==============================================================================

st.markdown("""
<style>
    /* Cores da marca */
    :root {
        --visia-primary: #1E3A5F;
        --visia-secondary: #2E86AB;
        --visia-accent: #A23B72;
        --visia-success: #28A745;
        --visia-warning: #FFC107;
        --visia-danger: #DC3545;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, var(--visia-primary), var(--visia-secondary));
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        color: var(--visia-primary);
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9em;
    }
    
    /* Classificações */
    .classificacao-excelente {
        background: linear-gradient(135deg, #28A745, #20c997);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        font-size: 1.3em;
        font-weight: bold;
        text-align: center;
    }
    
    .classificacao-bom {
        background: linear-gradient(135deg, #2E86AB, #17a2b8);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        font-size: 1.3em;
        font-weight: bold;
        text-align: center;
    }
    
    .classificacao-regular {
        background: linear-gradient(135deg, #FFC107, #fd7e14);
        color: #333;
        padding: 15px 25px;
        border-radius: 10px;
        font-size: 1.3em;
        font-weight: bold;
        text-align: center;
    }
    
    .classificacao-insuficiente {
        background: linear-gradient(135deg, #DC3545, #c82333);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        font-size: 1.3em;
        font-weight: bold;
        text-align: center;
    }
    
    /* Dimensões */
    .dimensao-card {
        border-left: 4px solid var(--visia-secondary);
        padding: 15px;
        background: #f8f9fa;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    
    /* Login box */
    .login-box {
        max-width: 400px;
        margin: 50px auto;
        padding: 30px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    /* Sidebar */
    .sidebar-info {
        padding: 10px;
        background: #f0f2f6;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.85em;
    }
    
    /* Tabelas */
    .dataframe {
        font-size: 0.9em !important;
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, var(--visia-primary), var(--visia-secondary));
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--visia-secondary), var(--visia-primary));
    }
    
    /* Upload area */
    .uploadedFile {
        border: 2px dashed var(--visia-secondary) !important;
        border-radius: 10px !important;
    }
    
    /* Alertas customizados */
    .alert-visia {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .alert-info {
        background: #e7f3ff;
        border-left: 4px solid #2196F3;
    }
    
    .alert-success {
        background: #e8f5e9;
        border-left: 4px solid #4CAF50;
    }
    
    .alert-warning {
        background: #fff3e0;
        border-left: 4px solid #FF9800;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# INICIALIZAÇÃO
# ==============================================================================

# Inicializa banco de dados
@st.cache_resource
def get_database():
    return VisiaDatabase("visia_platform.db")

# Inicializa motor VISIA
@st.cache_resource
def get_engine():
    return VisiaEngine()

# Inicializa extrator
@st.cache_resource
def get_extractor():
    return VisiaAIExtractor()

db = get_database()
engine = get_engine()
extractor = get_extractor()

# ==============================================================================
# GERENCIAMENTO DE SESSÃO
# ==============================================================================

def init_session():
    """Inicializa variáveis de sessão"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'projeto_atual' not in st.session_state:
        st.session_state.projeto_atual = None
    if 'dados_extraidos' not in st.session_state:
        st.session_state.dados_extraidos = None
    if 'resultado_analise' not in st.session_state:
        st.session_state.resultado_analise = None
    if 'pagina' not in st.session_state:
        st.session_state.pagina = 'inicio'

init_session()

# ==============================================================================
# FUNÇÕES DE AUTENTICAÇÃO
# ==============================================================================

def login(email: str, senha: str) -> bool:
    """Realiza login do usuário"""
    user = db.autenticar_usuario(email, senha)
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user
        db.registrar_auditoria(
            usuario_id=user['id'],
            acao="LOGIN",
            entidade="usuario",
            entidade_id=user['id']
        )
        return True
    return False

def logout():
    """Realiza logout"""
    if st.session_state.user:
        db.registrar_auditoria(
            usuario_id=st.session_state.user['id'],
            acao="LOGOUT",
            entidade="usuario",
            entidade_id=st.session_state.user['id']
        )
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.projeto_atual = None
    st.session_state.dados_extraidos = None
    st.session_state.resultado_analise = None

# ==============================================================================
# COMPONENTES DE UI
# ==============================================================================

def render_header():
    """Renderiza header principal"""
    st.markdown("""
    <div class="main-header">
        <h1>📊 VISIA - Plataforma de Análise de Impacto</h1>
        <p>Valoração Integrada de Sustentabilidade e Impacto Aplicado | IBEDIS</p>
    </div>
    """, unsafe_allow_html=True)

def render_login():
    """Renderiza página de login"""
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1>📊 VISIA</h1>
        <h3>Plataforma de Análise de Impacto</h3>
        <p>Metodologia proprietária do IBEDIS</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Acesso ao Sistema")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="seu@email.com")
            senha = st.text_input("🔑 Senha", type="password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submitted = st.form_submit_button("Entrar", use_container_width=True)
            with col_btn2:
                cadastrar = st.form_submit_button("Cadastrar", use_container_width=True)
            
            if submitted:
                if login(email, senha):
                    st.success("✅ Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Email ou senha incorretos")
            
            if cadastrar:
                st.session_state.pagina = 'cadastro'
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.85em;">
            <p>📚 Metodologia baseada no livro "VISIA" de Wemerson Marinho</p>
            <p>ISBN: 978-65-01-58740-0</p>
        </div>
        """, unsafe_allow_html=True)

def render_cadastro():
    """Renderiza página de cadastro"""
    st.markdown("### 📝 Cadastro de Novo Usuário")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("cadastro_form"):
            nome = st.text_input("👤 Nome completo*")
            email = st.text_input("📧 Email*")
            senha = st.text_input("🔑 Senha*", type="password")
            senha_confirm = st.text_input("🔑 Confirmar senha*", type="password")
            organizacao = st.text_input("🏛️ Organização/Órgão")
            cargo = st.text_input("💼 Cargo")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submitted = st.form_submit_button("Cadastrar", use_container_width=True)
            with col_btn2:
                voltar = st.form_submit_button("Voltar", use_container_width=True)
            
            if submitted:
                if not nome or not email or not senha:
                    st.error("Preencha todos os campos obrigatórios (*)")
                elif senha != senha_confirm:
                    st.error("As senhas não conferem")
                elif len(senha) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres")
                else:
                    try:
                        user_id = db.criar_usuario(
                            nome=nome,
                            email=email,
                            senha=senha,
                            tipo=TipoUsuario.USUARIO,
                            organizacao=organizacao,
                            cargo=cargo
                        )
                        st.success("✅ Cadastro realizado! Faça login para continuar.")
                        st.session_state.pagina = 'login'
                        st.rerun()
                    except ValueError as e:
                        st.error(f"Erro: {e}")
            
            if voltar:
                st.session_state.pagina = 'login'
                st.rerun()

def render_sidebar():
    """Renderiza sidebar com navegação"""
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-info">
            <strong>👤 {st.session_state.user['nome']}</strong><br>
            <small>{st.session_state.user['tipo'].upper()}</small><br>
            <small>🏛️ {st.session_state.user.get('organizacao', 'N/A')}</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Menu de navegação
        menu_items = {
            "🏠 Início": "inicio",
            "📤 Upload de Projeto": "upload",
            "📝 Nova Análise Manual": "analise_manual",
            "📋 Meus Projetos": "projetos",
            "📊 Relatórios": "relatorios",
        }
        
        # Menu admin
        if st.session_state.user['tipo'] == 'administrador':
            menu_items["⚙️ Administração"] = "admin"
            menu_items["👥 Usuários"] = "usuarios"
            menu_items["🔑 API Keys"] = "api"
        
        # Menu auditor
        if st.session_state.user['tipo'] in ['administrador', 'auditor']:
            menu_items["📜 Auditoria"] = "auditoria"
        
        menu_items["ℹ️ Sobre VISIA"] = "sobre"
        
        for label, pagina in menu_items.items():
            if st.button(label, key=f"menu_{pagina}", use_container_width=True):
                st.session_state.pagina = pagina
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Sair", use_container_width=True):
            logout()
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; font-size: 0.75em; color: #888;">
            <p>VISIA v1.0.0</p>
            <p>© 2024 IBEDIS</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# PÁGINAS PRINCIPAIS
# ==============================================================================

def pagina_inicio():
    """Página inicial com dashboard"""
    render_header()
    
    st.markdown("### 📊 Dashboard")
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    # Conta projetos do usuário
    projetos = db.listar_projetos(usuario_id=st.session_state.user['id'])
    total_projetos = len(projetos)
    
    with col1:
        st.metric("📁 Meus Projetos", total_projetos)
    
    with col2:
        analisados = len([p for p in projetos if p['status'] == 'analisado'])
        st.metric("✅ Analisados", analisados)
    
    with col3:
        # Média de impacto
        if analisados > 0:
            media = sum([db.obter_ultima_analise(p['id'])['impacto_total'] 
                        for p in projetos if p['status'] == 'analisado'
                        and db.obter_ultima_analise(p['id'])]) / analisados
            st.metric("📈 Impacto Médio", f"{media:.1f}%")
        else:
            st.metric("📈 Impacto Médio", "N/A")
    
    with col4:
        # Último acesso
        st.metric("🕐 Último Acesso", 
                 datetime.now().strftime("%d/%m %H:%M"))
    
    st.markdown("---")
    
    # Ações rápidas
    st.markdown("### ⚡ Ações Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📤 Upload de Projeto</h4>
            <p>Faça upload de PDF ou Word para análise automática</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Fazer Upload", key="btn_upload", use_container_width=True):
            st.session_state.pagina = 'upload'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>📝 Nova Análise</h4>
            <p>Preencha os dados manualmente para análise VISIA</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Nova Análise", key="btn_analise", use_container_width=True):
            st.session_state.pagina = 'analise_manual'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📋 Meus Projetos</h4>
            <p>Visualize e gerencie seus projetos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver Projetos", key="btn_projetos", use_container_width=True):
            st.session_state.pagina = 'projetos'
            st.rerun()
    
    # Últimos projetos
    if projetos:
        st.markdown("---")
        st.markdown("### 📋 Últimos Projetos")
        
        for projeto in projetos[:5]:
            with st.expander(f"📁 {projeto['nome']} - {projeto['status'].upper()}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Criado em:** {projeto['data_criacao'][:10]}")
                    st.write(f"**Status:** {projeto['status']}")
                with col2:
                    if st.button("Ver Detalhes", key=f"ver_{projeto['id']}"):
                        st.session_state.projeto_atual = projeto
                        st.session_state.pagina = 'detalhe_projeto'
                        st.rerun()

def pagina_upload():
    """Página de upload de projetos"""
    render_header()
    
    st.markdown("### 📤 Upload de Projeto para Análise")
    
    st.info("""
    📋 **Formatos aceitos:** PDF, DOCX, TXT
    
    O sistema irá extrair automaticamente os dados do projeto e preencher 
    os campos da análise VISIA. Você poderá revisar e completar os dados 
    antes de executar a análise.
    """)
    
    uploaded_file = st.file_uploader(
        "Arraste ou selecione o arquivo do projeto",
        type=['pdf', 'docx', 'txt'],
        help="Faça upload do documento do projeto para análise automática"
    )
    
    if uploaded_file:
        st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
        
        # Salva arquivo temporariamente
        temp_path = f"/tmp/{uploaded_file.name}"
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("🔍 Analisando documento..."):
            try:
                # Extrai dados do documento
                dados = extractor.extrair_de_arquivo(temp_path)
                st.session_state.dados_extraidos = dados
                
                # Verifica se é documento já analisado
                projeto_existente = db.buscar_projeto_por_hash(dados.hash_documento)
                
                if projeto_existente:
                    st.warning("""
                    ⚠️ **Documento já analisado anteriormente!**
                    
                    Este mesmo documento já foi enviado e analisado. 
                    Você pode ver a análise anterior ou criar uma nova versão.
                    """)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📊 Ver Análise Anterior"):
                            st.session_state.projeto_atual = projeto_existente
                            st.session_state.pagina = 'detalhe_projeto'
                            st.rerun()
                    with col2:
                        if st.button("🔄 Criar Nova Versão"):
                            st.session_state.dados_extraidos = dados
                            st.session_state.pagina = 'revisar_extracao'
                            st.rerun()
                else:
                    # Mostra resumo da extração
                    st.markdown("### 📋 Dados Extraídos")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Nome do Projeto:** {dados.nome_projeto or 'Não identificado'}")
                        st.write(f"**Investimento:** R$ {dados.investimento_total:,.2f}" if dados.investimento_total else "**Investimento:** Não identificado")
                        st.write(f"**Beneficiários:** {dados.beneficiarios:,}" if dados.beneficiarios else "**Beneficiários:** Não identificado")
                    
                    with col2:
                        st.write(f"**Local:** {dados.municipio or 'N/A'} - {dados.estado or 'N/A'}")
                        st.write(f"**Órgão:** {dados.orgao_responsavel or 'Não identificado'}")
                        st.write(f"**Confiança:** {dados.confianca_extracao}%")
                    
                    # Mostra campos para preenchimento manual
                    if dados.campos_manuais_necessarios:
                        st.warning(f"⚠️ {len(dados.campos_manuais_necessarios)} campo(s) precisam ser preenchidos manualmente")
                    
                    if st.button("📝 Revisar e Completar Dados", use_container_width=True):
                        st.session_state.pagina = 'revisar_extracao'
                        st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Erro ao processar documento: {str(e)}")
                st.info("💡 Tente fazer uma análise manual com os dados do projeto.")
        
        # Remove arquivo temporário
        if os.path.exists(temp_path):
            os.remove(temp_path)

def pagina_revisar_extracao():
    """Página para revisar e completar dados extraídos"""
    render_header()
    
    st.markdown("### 📝 Revisar e Completar Dados")
    
    dados = st.session_state.dados_extraidos
    
    if not dados:
        st.warning("Nenhum dado para revisar. Faça upload de um documento primeiro.")
        return
    
    with st.form("form_revisao"):
        st.markdown("#### 📋 Identificação do Projeto")
        
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Projeto*", value=dados.nome_projeto or "")
            orgao = st.text_input("Órgão Responsável", value=dados.orgao_responsavel or "")
            municipio = st.text_input("Município", value=dados.municipio or "")
        with col2:
            descricao = st.text_area("Descrição", value=dados.descricao or "", height=100)
            estado = st.text_input("Estado (UF)", value=dados.estado or "")
            investimento_total = st.number_input(
                "Investimento Total (R$)*", 
                min_value=0.0,
                value=float(dados.investimento_total) if dados.investimento_total else 0.0,
                format="%.2f"
            )
        
        st.markdown("---")
        st.markdown("#### 📚 Dimensão Educacional")
        
        col1, col2 = st.columns(2)
        indicadores_edu = dados.indicadores_encontrados.get('educacional', {})
        
        with col1:
            alunos = st.number_input(
                "Alunos/Jovens Impactados",
                min_value=0,
                value=int(indicadores_edu.get('alunos_beneficiados', 0) or indicadores_edu.get('jovens_capacitados', 0))
            )
            melhoria = st.number_input(
                "Melhoria no Desempenho (%)",
                min_value=0.0, max_value=100.0,
                value=float(indicadores_edu.get('melhoria_desempenho', 0))
            )
        with col2:
            empregabilidade = st.number_input(
                "Taxa de Empregabilidade (%)",
                min_value=0.0, max_value=100.0,
                value=float(indicadores_edu.get('taxa_empregabilidade', 0))
            )
            invest_edu = st.number_input(
                "Investimento Educacional (R$)",
                min_value=0.0,
                value=0.0
            )
        
        st.markdown("---")
        st.markdown("#### 💰 Dimensão Econômica")
        
        col1, col2 = st.columns(2)
        indicadores_eco = dados.indicadores_encontrados.get('economico', {})
        
        with col1:
            empregos = st.number_input(
                "Empregos Gerados",
                min_value=0,
                value=int(dados.empregos or 0)
            )
            renda = st.number_input(
                "Renda Média (R$)",
                min_value=0.0,
                value=float(indicadores_eco.get('renda_media', 0))
            )
        with col2:
            microcreditos = st.number_input(
                "Microcréditos Concedidos",
                min_value=0,
                value=int(indicadores_eco.get('microcreditos', 0))
            )
            valor_credito = st.number_input(
                "Valor Médio do Crédito (R$)",
                min_value=0.0,
                value=float(indicadores_eco.get('valor_credito', 0))
            )
        
        st.markdown("---")
        st.markdown("#### 🌱 Dimensão Social e Ambiental")
        
        col1, col2 = st.columns(2)
        indicadores_soc = dados.indicadores_encontrados.get('social_ambiental', {})
        
        with col1:
            populacao = st.number_input(
                "População Beneficiada",
                min_value=0,
                value=int(dados.beneficiarios or 0)
            )
            melhoria_vida = st.number_input(
                "Melhoria Qualidade de Vida (%)",
                min_value=0.0, max_value=100.0,
                value=float(indicadores_soc.get('melhoria_qualidade_vida', 0))
            )
        with col2:
            carbono = st.number_input(
                "Créditos de Carbono Gerados",
                min_value=0,
                value=int(indicadores_soc.get('creditos_carbono', 0))
            )
            economia_circular = st.number_input(
                "Impacto Economia Circular (%)",
                min_value=0.0, max_value=100.0,
                value=0.0
            )
        
        st.markdown("---")
        st.markdown("#### 🏛️ Dimensão Político-Pública")
        
        col1, col2 = st.columns(2)
        indicadores_pol = dados.indicadores_encontrados.get('politico', {})
        
        with col1:
            gestores = st.number_input(
                "Gestores Capacitados",
                min_value=0,
                value=int(indicadores_pol.get('gestores_capacitados', 0))
            )
            transparencia = st.number_input(
                "Aumento Transparência (%)",
                min_value=0.0, max_value=100.0,
                value=float(indicadores_pol.get('aumento_transparencia', 0))
            )
        with col2:
            captacao = st.number_input(
                "Investimentos Captados (R$)",
                min_value=0.0,
                value=float(indicadores_pol.get('investimentos_captados', 0))
            )
            politicas = st.number_input(
                "Políticas/Leis Criadas",
                min_value=0,
                value=int(indicadores_pol.get('politicas_criadas', 0))
            )
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            submitted = st.form_submit_button("🔍 EXECUTAR ANÁLISE VISIA", use_container_width=True)
        
        if submitted:
            if not nome:
                st.error("Informe o nome do projeto")
            elif investimento_total <= 0:
                st.error("Informe o investimento total")
            else:
                # Monta dados do projeto
                projeto = DadosProjetoVISIA(
                    nome_projeto=nome,
                    descricao=descricao,
                    orgao_responsavel=orgao,
                    municipio=municipio,
                    estado=estado,
                    investimento_total=investimento_total
                )
                
                # Define investimentos por dimensão (distribui se não informado)
                invest_dimensao = investimento_total / 4 if invest_edu == 0 else invest_edu
                
                projeto.educacional = DadosDimensaoEducacional(
                    alunos_impactados=alunos,
                    melhoria_desempenho=melhoria,
                    jovens_capacitados=alunos,
                    taxa_empregabilidade=empregabilidade,
                    investimento=invest_edu if invest_edu > 0 else invest_dimensao
                )
                
                projeto.economica = DadosDimensaoEconomica(
                    empregos_gerados=empregos,
                    renda_media=renda,
                    microcreditos_concedidos=microcreditos,
                    valor_medio_credito=valor_credito,
                    investimento=invest_dimensao
                )
                
                projeto.social_ambiental = DadosDimensaoSocialAmbiental(
                    populacao_beneficiada=populacao,
                    taxa_melhoria_qualidade_vida=melhoria_vida,
                    creditos_carbono_gerados=carbono,
                    impacto_economia_circular=economia_circular,
                    investimento=invest_dimensao
                )
                
                projeto.politico_publica = DadosDimensaoPoliticoPublica(
                    gestores_capacitados=gestores,
                    transparencia_aumento=transparencia,
                    investimentos_captados=captacao,
                    numero_politicas_criadas=politicas,
                    investimento=invest_dimensao
                )
                
                # Executa análise
                resultado = engine.analisar_projeto(projeto)
                
                # Salva no banco
                dados_salvar = {
                    "nome": nome,
                    "descricao": descricao,
                    "investimento_total": investimento_total,
                    "educacional": projeto.educacional.__dict__,
                    "economica": projeto.economica.__dict__,
                    "social_ambiental": projeto.social_ambiental.__dict__,
                    "politico_publica": projeto.politico_publica.__dict__
                }
                
                projeto_id = db.criar_projeto(
                    nome=nome,
                    dados=dados_salvar,
                    usuario_id=st.session_state.user['id'],
                    descricao=descricao,
                    arquivo_origem=dados.arquivo_origem if dados else ""
                )
                
                # Salva análise
                resultado_dict = {
                    "impacto_total": resultado.impacto_total,
                    "classificacao": resultado.classificacao,
                    "recomendacao": resultado.recomendacao,
                    "indice_educacional": resultado.indice_educacional,
                    "indice_economico": resultado.indice_economico,
                    "indice_social_ambiental": resultado.indice_social_ambiental,
                    "indice_politico_publico": resultado.indice_politico_publico,
                    "detalhes_educacional": resultado.detalhes_educacional,
                    "detalhes_economico": resultado.detalhes_economico,
                    "detalhes_social_ambiental": resultado.detalhes_social_ambiental,
                    "detalhes_politico_publico": resultado.detalhes_politico_publico,
                    "recomendacoes": resultado.recomendacoes,
                    "hash_resultado": resultado.hash_resultado
                }
                
                db.criar_analise(
                    projeto_id=projeto_id,
                    resultado=resultado_dict,
                    usuario_id=st.session_state.user['id']
                )
                
                st.session_state.resultado_analise = resultado
                st.session_state.projeto_atual = db.obter_projeto(projeto_id)
                st.session_state.pagina = 'resultado_analise'
                st.rerun()

def pagina_resultado_analise():
    """Página com resultado da análise VISIA"""
    render_header()
    
    resultado = st.session_state.resultado_analise
    projeto = st.session_state.projeto_atual
    
    if not resultado:
        st.warning("Nenhuma análise para exibir")
        return
    
    st.markdown("### 📊 Resultado da Análise VISIA")
    
    # Classificação principal
    classe_css = f"classificacao-{resultado.classificacao.lower()}"
    st.markdown(f"""
    <div class="{classe_css}">
        🏆 CLASSIFICAÇÃO: {resultado.classificacao}<br>
        <small>Impacto Total: {resultado.impacto_total}%</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"> {resultado.recomendacao}")
    
    st.markdown("---")
    
    # Índices por dimensão
    st.markdown("### 📈 Índices por Dimensão")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📚 Educacional",
            f"{resultado.indice_educacional}%",
            delta=f"{'↑' if resultado.indice_educacional >= 20 else '↓'}"
        )
    
    with col2:
        st.metric(
            "💰 Econômico",
            f"{resultado.indice_economico}%",
            delta=f"{'↑' if resultado.indice_economico >= 20 else '↓'}"
        )
    
    with col3:
        st.metric(
            "🌱 Social-Ambiental",
            f"{resultado.indice_social_ambiental}%",
            delta=f"{'↑' if resultado.indice_social_ambiental >= 20 else '↓'}"
        )
    
    with col4:
        st.metric(
            "🏛️ Político-Público",
            f"{resultado.indice_politico_publico}%",
            delta=f"{'↑' if resultado.indice_politico_publico >= 20 else '↓'}"
        )
    
    # Gráfico de barras
    st.markdown("---")
    
    import pandas as pd
    
    dados_grafico = pd.DataFrame({
        'Dimensão': ['Educacional', 'Econômico', 'Social-Ambiental', 'Político-Público'],
        'Índice (%)': [
            resultado.indice_educacional,
            resultado.indice_economico,
            resultado.indice_social_ambiental,
            resultado.indice_politico_publico
        ]
    })
    
    st.bar_chart(dados_grafico.set_index('Dimensão'))
    
    # Recomendações de melhoria
    if resultado.recomendacoes:
        st.markdown("---")
        st.markdown("### 💡 Recomendações de Melhoria")
        
        for rec in resultado.recomendacoes:
            prioridade_emoji = "🔴" if rec['prioridade'] == 'ALTA' else "🟡"
            st.markdown(f"""
            <div class="dimensao-card">
                <strong>{prioridade_emoji} {rec['dimensao']}</strong> [{rec['prioridade']}]<br>
                📌 {rec['acao']}<br>
                <small>📈 Impacto esperado: {rec['impacto_estimado']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Hash de consistência
    st.markdown("---")
    st.markdown(f"""
    <div class="sidebar-info">
        <strong>🔑 Hash de Verificação:</strong> {resultado.hash_resultado}<br>
        <small>Este código garante que a mesma entrada produzirá sempre o mesmo resultado.</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Gerar Relatório PDF", use_container_width=True):
            st.info("Funcionalidade em desenvolvimento")
    
    with col2:
        if st.button("📤 Exportar JSON", use_container_width=True):
            json_str = json.dumps({
                "projeto": projeto['nome'] if projeto else "N/A",
                "resultado": {
                    "impacto_total": resultado.impacto_total,
                    "classificacao": resultado.classificacao,
                    "indices": {
                        "educacional": resultado.indice_educacional,
                        "economico": resultado.indice_economico,
                        "social_ambiental": resultado.indice_social_ambiental,
                        "politico_publico": resultado.indice_politico_publico
                    }
                },
                "hash": resultado.hash_resultado
            }, ensure_ascii=False, indent=2)
            st.download_button("⬇️ Download JSON", json_str, "resultado_visia.json", "application/json")
    
    with col3:
        if st.button("🏠 Voltar ao Início", use_container_width=True):
            st.session_state.pagina = 'inicio'
            st.rerun()

def pagina_analise_manual():
    """Página para análise manual (sem upload)"""
    render_header()
    
    st.markdown("### 📝 Nova Análise Manual")
    st.info("Preencha os dados do projeto para executar a análise VISIA")
    
    # Cria dados vazios para usar o mesmo formulário
    st.session_state.dados_extraidos = DadosExtraidos()
    st.session_state.pagina = 'revisar_extracao'
    st.rerun()

def pagina_projetos():
    """Lista de projetos do usuário"""
    render_header()
    
    st.markdown("### 📋 Meus Projetos")
    
    projetos = db.listar_projetos(usuario_id=st.session_state.user['id'])
    
    if not projetos:
        st.info("Você ainda não tem projetos. Faça upload ou crie uma análise manual.")
        return
    
    for projeto in projetos:
        analise = db.obter_ultima_analise(projeto['id'])
        
        with st.expander(f"📁 {projeto['nome']} - {projeto['status'].upper()}", expanded=False):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**Criado em:** {projeto['data_criacao'][:10]}")
                st.write(f"**Versão:** {projeto['versao']}")
            
            with col2:
                if analise:
                    st.write(f"**Impacto:** {analise['impacto_total']}%")
                    st.write(f"**Classificação:** {analise['classificacao']}")
            
            with col3:
                if st.button("Ver", key=f"ver_{projeto['id']}"):
                    st.session_state.projeto_atual = projeto
                    if analise:
                        # Reconstrói resultado
                        resultado_dict = analise['resultado']
                        resultado = ResultadoVISIA(
                            indice_educacional=resultado_dict.get('indice_educacional', 0),
                            indice_economico=resultado_dict.get('indice_economico', 0),
                            indice_social_ambiental=resultado_dict.get('indice_social_ambiental', 0),
                            indice_politico_publico=resultado_dict.get('indice_politico_publico', 0),
                            impacto_total=resultado_dict.get('impacto_total', 0),
                            classificacao=resultado_dict.get('classificacao', ''),
                            recomendacao=resultado_dict.get('recomendacao', ''),
                            recomendacoes=resultado_dict.get('recomendacoes', []),
                            hash_resultado=resultado_dict.get('hash_resultado', '')
                        )
                        st.session_state.resultado_analise = resultado
                    st.session_state.pagina = 'resultado_analise'
                    st.rerun()

def pagina_sobre():
    """Página sobre a metodologia VISIA"""
    render_header()
    
    st.markdown("""
    ## ℹ️ Sobre a Metodologia VISIA
    
    ### O que é VISIA?
    
    **VISIA** (Valoração Integrada de Sustentabilidade e Impacto Aplicado) é uma 
    metodologia brasileira inovadora para mensuração de impacto de políticas públicas 
    e projetos governamentais.
    
    Desenvolvida por **Wemerson Marinho** e apresentada no livro "VISIA: Uma Nova 
    Abordagem Brasileira para Mensuração de Impacto no Setor Público" (ISBN: 978-65-01-58740-0).
    
    ---
    
    ### As 4 Dimensões da VISIA
    
    | Dimensão | Descrição |
    |----------|-----------|
    | 📚 **Educacional** | Avalia impacto em educação, capacitação e desenvolvimento humano |
    | 💰 **Econômica** | Mensura retorno financeiro, geração de empregos e renda |
    | 🌱 **Social e Ambiental** | Analisa qualidade de vida, inclusão social e sustentabilidade |
    | 🏛️ **Político-Pública** | Mede governança, transparência e captação de investimentos |
    
    ---
    
    ### Fórmulas da VISIA
    
    **Impacto Total:**
    ```
    I_total = (I_educacional + I_econômico + I_soc-amb + I_político) / 4
    ```
    
    **Classificação:**
    - ≥ 50%: **EXCELENTE** - Projeto aprovado com alto impacto
    - ≥ 30%: **BOM** - Projeto aprovado com ressalvas
    - ≥ 15%: **REGULAR** - Projeto requer ajustes
    - < 15%: **INSUFICIENTE** - Projeto não recomendado
    
    ---
    
    ### Diferenciais da VISIA vs Outras Metodologias
    
    | Característica | VISIA | SROI | IDH |
    |----------------|-------|------|-----|
    | Foco em políticas públicas | ✅ | ❌ | ❌ |
    | Avaliação integrada | ✅ | ❌ | ✅ |
    | Aplicabilidade no Brasil | Alta | Baixa | Média |
    | Facilidade de implementação | Alta | Média | Alta |
    
    ---
    
    ### Contato
    
    **IBEDIS** - Instituto Brasileiro de Desenvolvimento, Inovação e Sustentabilidade
    
    📧 contato@ibedis.org.br
    🌐 www.ibedis.org.br
    """)

def pagina_admin():
    """Página de administração"""
    render_header()
    
    st.markdown("### ⚙️ Administração do Sistema")
    
    tab1, tab2, tab3 = st.tabs(["📊 Estatísticas", "⚙️ Configurações", "🔑 API"])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_usuarios = len(db.listar_usuarios())
            st.metric("👥 Total Usuários", total_usuarios)
        
        with col2:
            total_projetos = len(db.listar_projetos())
            st.metric("📁 Total Projetos", total_projetos)
        
        with col3:
            st.metric("📊 Análises Hoje", "N/A")
        
        with col4:
            st.metric("🔄 Uso API/hora", "N/A")
    
    with tab2:
        st.markdown("#### Configurações do Sistema")
        
        configs = db.listar_configuracoes()
        
        with st.form("config_form"):
            limite_api = st.number_input(
                "Limite de requisições API/hora",
                min_value=10, max_value=10000,
                value=100
            )
            
            if st.form_submit_button("Salvar"):
                db.definir_configuracao("limite_api_hora", str(limite_api))
                st.success("Configurações salvas!")
    
    with tab3:
        st.markdown("#### Gerenciamento de API Keys")
        st.info("Configure aqui as chaves de API para integrações externas")

def pagina_usuarios():
    """Página de gerenciamento de usuários (admin)"""
    render_header()
    
    st.markdown("### 👥 Gerenciamento de Usuários")
    
    usuarios = db.listar_usuarios()
    
    # Filtros
    col1, col2 = st.columns([3, 1])
    with col2:
        filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos", "Administrador", "Usuário", "Auditor"])
    
    for usuario in usuarios:
        if filtro_tipo != "Todos" and usuario['tipo'] != filtro_tipo.lower():
            continue
        
        with st.expander(f"👤 {usuario['nome']} ({usuario['tipo']})"):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**Email:** {usuario['email']}")
                st.write(f"**Organização:** {usuario.get('organizacao', 'N/A')}")
            
            with col2:
                st.write(f"**Cadastro:** {usuario['data_criacao'][:10]}")
                st.write(f"**Status:** {'Ativo' if usuario['ativo'] else 'Inativo'}")
            
            with col3:
                if st.button("Editar", key=f"edit_{usuario['id']}"):
                    st.info("Edição em desenvolvimento")

def pagina_auditoria():
    """Página de logs de auditoria"""
    render_header()
    
    st.markdown("### 📜 Logs de Auditoria")
    
    logs = db.obter_logs_auditoria(limite=100)
    
    if not logs:
        st.info("Nenhum registro de auditoria encontrado")
        return
    
    for log in logs:
        st.markdown(f"""
        <div class="sidebar-info">
            <strong>{log['acao']}</strong> em <em>{log['entidade']}</em><br>
            <small>Usuário: {log.get('usuario_nome', 'Sistema')} | {log['data_hora'][:19]}</small>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# ROTEAMENTO DE PÁGINAS
# ==============================================================================

def main():
    """Função principal de roteamento"""
    
    # Se não está logado, mostra login ou cadastro
    if not st.session_state.logged_in:
        if st.session_state.pagina == 'cadastro':
            render_cadastro()
        else:
            render_login()
        return
    
    # Renderiza sidebar
    render_sidebar()
    
    # Roteia para página correta
    paginas = {
        'inicio': pagina_inicio,
        'upload': pagina_upload,
        'revisar_extracao': pagina_revisar_extracao,
        'resultado_analise': pagina_resultado_analise,
        'analise_manual': pagina_analise_manual,
        'projetos': pagina_projetos,
        'sobre': pagina_sobre,
        'admin': pagina_admin,
        'usuarios': pagina_usuarios,
        'auditoria': pagina_auditoria,
        'relatorios': pagina_inicio,  # TODO
        'api': pagina_admin,  # TODO
        'detalhe_projeto': pagina_resultado_analise,
    }
    
    pagina_func = paginas.get(st.session_state.pagina, pagina_inicio)
    pagina_func()

if __name__ == "__main__":
    main()
