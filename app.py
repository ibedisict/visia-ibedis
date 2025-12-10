"""
VISIA - Interface Web
=====================
Aplicação Streamlit para análise de impacto social

Deploy gratuito: https://streamlit.io/cloud
"""

import streamlit as st
import json
from datetime import date, datetime

# Importar módulos VISIA
from visia_database import (
    EDUCACAO, TRABALHO, PROGRAMAS_SOCIAIS, SISTEMA_PRISIONAL,
    SEGURANCA_CRIME, MEIO_AMBIENTE, SROI_REFERENCIAS, METADATA
)
from visia_calculators import (
    calcular_visia_integrado, calcular_sroi, 
    calcular_impacto_crime, calcular_impacto_ambiental,
    calcular_retorno_fiscal
)
from visia_reports import (
    gerar_relatorio_completo, gerar_relatorio_resumido,
    gerar_certificado_impacto, exportar_dados_json
)

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================

st.set_page_config(
    page_title="VISIA - IBEDIS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
    }
    .classificacao-A { color: #28a745; font-size: 3rem; font-weight: bold; }
    .classificacao-B { color: #17a2b8; font-size: 3rem; font-weight: bold; }
    .classificacao-C { color: #ffc107; font-size: 3rem; font-weight: bold; }
    .classificacao-D { color: #dc3545; font-size: 3rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR - NAVEGAÇÃO
# =============================================================================

st.sidebar.image("https://via.placeholder.com/200x80?text=IBEDIS", width=200)
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "📌 Navegação",
    [
        "🏠 Início",
        "📊 Analisar Projeto",
        "📋 Base de Dados",
        "📄 Gerar Relatório",
        "ℹ️ Sobre a Metodologia"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Versão:** {METADATA['versao']}")
st.sidebar.markdown(f"**Atualização:** {METADATA['data_atualizacao']}")

# =============================================================================
# PÁGINA: INÍCIO
# =============================================================================

if pagina == "🏠 Início":
    st.markdown('<p class="main-header">📊 VISIA</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Valoração de Impacto Social e Investimento Aplicado</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Calcule o Impacto")
        st.write("Insira os dados do seu projeto e obtenha análise completa de SROI, retorno fiscal e TCS recomendados.")
        if st.button("Analisar Projeto", key="btn_analisar"):
            st.switch_page = "📊 Analisar Projeto"
    
    with col2:
        st.markdown("### 📄 Gere Relatórios")
        st.write("Produza relatórios executivos, certificados de impacto e documentação para parceiros e investidores.")
    
    with col3:
        st.markdown("### 🪙 Emita TCS")
        st.write("Calcule a quantidade de Tokens de Crédito Social baseado no UISV do seu projeto.")
    
    st.markdown("---")
    
    # Métricas rápidas da base de dados
    st.markdown("### 📈 Referências da Base de Dados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Custo Preso/Ano",
            f"R$ {SISTEMA_PRISIONAL['custos']['custo_preso_estadual_medio_ano']:,.0f}",
            "Estadual"
        )
    
    with col2:
        st.metric(
            "Custo Homicídio",
            f"R$ {SEGURANCA_CRIME['custo_violencia']['custo_homicidio_medio']/1000000:.0f}M",
            "Por ocorrência"
        )
    
    with col3:
        st.metric(
            "SROI Qualificação",
            f"{SROI_REFERENCIAS['por_tipo_projeto']['qualificacao_profissional']['medio']:.1f}x",
            "Referência"
        )
    
    with col4:
        st.metric(
            "Salário Mínimo",
            f"R$ {TRABALHO['salario_minimo']['valor_2025']:,.0f}",
            "2025"
        )

# =============================================================================
# PÁGINA: ANALISAR PROJETO
# =============================================================================

elif pagina == "📊 Analisar Projeto":
    st.markdown("## 📊 Análise de Impacto Social")
    st.markdown("Preencha os dados do projeto para obter a análise VISIA completa.")
    
    # Formulário de entrada
    with st.form("form_projeto"):
        st.markdown("### 📝 Dados do Projeto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_projeto = st.text_input(
                "Nome do Projeto *",
                placeholder="Ex: Programa Qualifica Jovem 2025"
            )
            
            tipo_projeto = st.selectbox(
                "Tipo de Projeto *",
                options=[
                    "qualificacao_profissional",
                    "educacao",
                    "meio_ambiente",
                    "assistencia_social",
                    "saude",
                    "primeira_infancia",
                    "esporte_cultura"
                ],
                format_func=lambda x: x.replace("_", " ").title()
            )
            
            investimento = st.number_input(
                "Investimento Total (R$) *",
                min_value=10000.0,
                max_value=100000000.0,
                value=500000.0,
                step=10000.0,
                format="%.2f"
            )
        
        with col2:
            beneficiarios = st.number_input(
                "Beneficiários Diretos *",
                min_value=1,
                max_value=1000000,
                value=100
            )
            
            duracao = st.slider(
                "Duração (anos)",
                min_value=1,
                max_value=10,
                value=2
            )
            
            area_abrangencia = st.text_input(
                "Área de Abrangência",
                placeholder="Ex: Município de São Paulo - Zona Sul"
            )
        
        st.markdown("---")
        st.markdown("### 📈 Impactos Estimados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            empregos = st.number_input(
                "Empregos Gerados",
                min_value=0,
                max_value=10000,
                value=0
            )
            
            familias_bf = st.number_input(
                "Famílias que saem do Bolsa Família",
                min_value=0,
                max_value=10000,
                value=0
            )
        
        with col2:
            jovens = st.number_input(
                "Jovens Atendidos (prevenção crime)",
                min_value=0,
                max_value=10000,
                value=0
            )
            
            alunos_evasao = st.number_input(
                "Alunos que evitam evasão",
                min_value=0,
                max_value=10000,
                value=0
            )
        
        with col3:
            hectares = st.number_input(
                "Hectares Recuperados",
                min_value=0.0,
                max_value=100000.0,
                value=0.0,
                step=1.0
            )
            
            bioma = st.selectbox(
                "Bioma",
                options=["mata_atlantica", "amazonia", "cerrado", "caatinga", "pantanal", "pampa"],
                format_func=lambda x: x.replace("_", " ").title()
            )
        
        submitted = st.form_submit_button("🚀 Calcular Impacto", use_container_width=True)
    
    # Processamento e exibição de resultados
    if submitted:
        if not nome_projeto:
            st.error("Por favor, preencha o nome do projeto.")
        else:
            with st.spinner("Calculando impacto social..."):
                # Calcular
                resultado = calcular_visia_integrado(
                    nome_projeto=nome_projeto,
                    investimento_total=investimento,
                    tipo_projeto=tipo_projeto,
                    beneficiarios_diretos=beneficiarios,
                    duracao_anos=duracao,
                    empregos_gerados=empregos,
                    familias_saem_vulnerabilidade=familias_bf,
                    jovens_atendidos=jovens,
                    alunos_evitam_evasao=alunos_evasao,
                    hectares_recuperados=hectares,
                    bioma=bioma
                )
                
                # Guardar na sessão para uso no relatório
                st.session_state['resultado'] = resultado
            
            st.success("✅ Análise concluída!")
            
            # Exibir resultados
            st.markdown("---")
            st.markdown("## 📊 Resultados da Análise")
            
            # Métricas principais
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("UISV", f"{resultado.uisv:.2f}")
            
            with col2:
                st.metric("SROI", f"{resultado.sroi.sroi:.2f}x")
            
            with col3:
                st.metric("TCS", f"{resultado.tcs_recomendados:,}")
            
            with col4:
                st.metric("ROI Fiscal", f"{resultado.fiscal.roi_fiscal:.2f}x")
            
            with col5:
                classe = resultado.classificacao
                cor = {"A": "🟢", "B": "🔵", "C": "🟡", "D": "🔴"}[classe]
                st.metric("Classificação", f"{cor} {classe}")
            
            st.markdown("---")
            
            # Detalhamento
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 👥 Impacto em Pessoas")
                st.write(f"**Beneficiários diretos:** {resultado.beneficiarios_diretos:,}")
                st.write(f"**Impacto total (multiplicador):** {resultado.impacto_total_pessoas:,}")
                
                st.markdown("### 💰 Retorno Fiscal")
                st.write(f"**Arrecadação gerada:** R$ {resultado.fiscal.arrecadacao_gerada:,.2f}")
                st.write(f"**Economia programas sociais:** R$ {resultado.fiscal.economia_programas_sociais:,.2f}")
                st.write(f"**Economia segurança:** R$ {resultado.fiscal.economia_seguranca:,.2f}")
                st.write(f"**Retorno total:** R$ {resultado.fiscal.retorno_fiscal_total:,.2f}")
                st.write(f"**Payback:** {resultado.fiscal.tempo_payback_anos:.1f} anos")
            
            with col2:
                st.markdown("### 📊 SROI Detalhado")
                st.write(f"**Investimento:** R$ {resultado.sroi.investimento:,.2f}")
                st.write(f"**Valor social bruto:** R$ {resultado.sroi.valor_social_bruto:,.2f}")
                st.write(f"**SROI:** {resultado.sroi.sroi:.2f}")
                st.write(f"**Range referência:** {resultado.sroi.sroi_range[0]:.1f} - {resultado.sroi.sroi_range[1]:.1f}")
                
                if resultado.crime:
                    st.markdown("### 🔒 Impacto em Segurança")
                    st.write(f"**Economia total:** R$ {resultado.crime.economia_total:,.2f}")
                    st.write(f"**ROI Segurança:** {resultado.crime.roi_seguranca:.2f}x")
                
                if resultado.ambiental:
                    st.markdown("### 🌳 Impacto Ambiental")
                    st.write(f"**CO₂ sequestrado:** {resultado.ambiental.toneladas_co2_sequestradas:,.0f} ton")
                    st.write(f"**Benefícios:** R$ {resultado.ambiental.valor_total_beneficios:,.2f}")
            
            # Observações
            st.markdown("---")
            st.markdown("### 📝 Observações")
            for obs in resultado.observacoes:
                st.info(obs)

# =============================================================================
# PÁGINA: BASE DE DADOS
# =============================================================================

elif pagina == "📋 Base de Dados":
    st.markdown("## 📋 Base de Dados de Referência")
    st.markdown("Constantes utilizadas nos cálculos VISIA, baseadas em fontes oficiais.")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📚 Educação",
        "💼 Trabalho",
        "🔒 Prisional",
        "🚨 Segurança",
        "🌳 Ambiente"
    ])
    
    with tab1:
        st.markdown("### Educação")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**FUNDEB 2024**")
            st.write(f"- Mínimo: R$ {EDUCACAO['fundeb']['valor_aluno_ano_minimo_2024']:,.2f}/aluno/ano")
            st.write(f"- Máximo: R$ {EDUCACAO['fundeb']['valor_aluno_ano_maximo_2024']:,.2f}/aluno/ano")
            st.write(f"- Médio: R$ {EDUCACAO['fundeb']['valor_aluno_ano_medio_2024']:,.2f}/aluno/ano")
        with col2:
            st.markdown("**Docentes**")
            st.write(f"- Piso 2025: R$ {EDUCACAO['docentes']['piso_nacional_2025']:,.2f}")
            st.write(f"- Custo formação: R$ {EDUCACAO['docentes']['custo_formacao_professor_min']:,.0f} - {EDUCACAO['docentes']['custo_formacao_professor_max']:,.0f}")
    
    with tab2:
        st.markdown("### Trabalho")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Salário Mínimo**")
            st.write(f"- 2025: R$ {TRABALHO['salario_minimo']['valor_2025']:,.2f}")
            st.write(f"- 2024: R$ {TRABALHO['salario_minimo']['valor_2024']:,.2f}")
        with col2:
            st.markdown("**Encargos CLT**")
            st.write(f"- Mínimo: {TRABALHO['encargos_clt']['total_minimo']*100:.0f}%")
            st.write(f"- Máximo: {TRABALHO['encargos_clt']['total_maximo']*100:.0f}%")
            st.write(f"- Médio: {TRABALHO['encargos_clt']['total_medio']*100:.0f}%")
    
    with tab3:
        st.markdown("### Sistema Prisional")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Custos 2024**")
            st.write(f"- Preso estadual/ano: R$ {SISTEMA_PRISIONAL['custos']['custo_preso_estadual_medio_ano']:,.2f}")
            st.write(f"- Preso federal/ano: R$ {SISTEMA_PRISIONAL['custos']['custo_preso_federal_ano']:,.2f}")
        with col2:
            st.markdown("**População**")
            st.write(f"- Total 2023: {SISTEMA_PRISIONAL['populacao']['total_presos_2023']:,}")
            st.write(f"- Taxa reincidência: {SISTEMA_PRISIONAL['populacao']['taxa_reincidencia']*100:.0f}%")
    
    with tab4:
        st.markdown("### Segurança e Crime")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Custos da Violência**")
            st.write(f"- Impacto PIB: {SEGURANCA_CRIME['custo_violencia']['impacto_pib_percentual_max']*100:.0f}%")
            st.write(f"- Custo homicídio: R$ {SEGURANCA_CRIME['custo_violencia']['custo_homicidio_medio']:,.0f}")
        with col2:
            st.markdown("**Estatísticas 2024**")
            st.write(f"- Homicídios: {SEGURANCA_CRIME['estatisticas']['homicidios_2024']:,}")
            st.write(f"- Taxa: {SEGURANCA_CRIME['estatisticas']['taxa_homicidio_2024_100mil']}/100 mil")
    
    with tab5:
        st.markdown("### Meio Ambiente")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Custo Recuperação/ha**")
            for bioma, valor in MEIO_AMBIENTE['custo_recuperacao_hectare'].items():
                if bioma not in ['regeneracao_natural', 'regeneracao_assistida', 'plantio_total']:
                    st.write(f"- {bioma.replace('_', ' ').title()}: R$ {valor:,.2f}")
        with col2:
            st.markdown("**Carbono**")
            st.write(f"- Preço mínimo: US$ {MEIO_AMBIENTE['carbono']['preco_tonelada_co2_usd_min']:.0f}/ton")
            st.write(f"- Preço médio: US$ {MEIO_AMBIENTE['carbono']['preco_tonelada_co2_usd_medio']:.0f}/ton")
            st.write(f"- Sequestro: {MEIO_AMBIENTE['carbono']['sequestro_floresta_ton_ha_ano']:.0f} ton/ha/ano")

# =============================================================================
# PÁGINA: GERAR RELATÓRIO
# =============================================================================

elif pagina == "📄 Gerar Relatório":
    st.markdown("## 📄 Gerador de Relatórios")
    
    if 'resultado' not in st.session_state:
        st.warning("⚠️ Nenhum projeto analisado. Vá para 'Analisar Projeto' primeiro.")
    else:
        resultado = st.session_state['resultado']
        
        st.success(f"✅ Projeto carregado: **{resultado.projeto}**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Relatório Completo", use_container_width=True):
                relatorio = gerar_relatorio_completo(resultado)
                st.download_button(
                    "⬇️ Baixar Relatório (MD)",
                    relatorio,
                    file_name=f"relatorio_{resultado.projeto.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
                st.markdown("### Prévia do Relatório")
                st.markdown(relatorio)
        
        with col2:
            if st.button("📋 Resumo Executivo", use_container_width=True):
                resumo = gerar_relatorio_resumido(resultado)
                st.download_button(
                    "⬇️ Baixar Resumo (MD)",
                    resumo,
                    file_name=f"resumo_{resultado.projeto.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
                st.markdown("### Prévia do Resumo")
                st.markdown(resumo)
        
        with col3:
            if st.button("🏆 Certificado", use_container_width=True):
                certificado = gerar_certificado_impacto(resultado)
                st.download_button(
                    "⬇️ Baixar Certificado (TXT)",
                    certificado,
                    file_name=f"certificado_{resultado.projeto.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                st.markdown("### Prévia do Certificado")
                st.code(certificado)
        
        st.markdown("---")
        
        if st.button("💾 Exportar JSON (API)", use_container_width=True):
            json_data = exportar_dados_json(resultado)
            st.download_button(
                "⬇️ Baixar JSON",
                json_data,
                file_name=f"dados_{resultado.projeto.replace(' ', '_')}.json",
                mime="application/json"
            )
            st.json(json.loads(json_data))

# =============================================================================
# PÁGINA: SOBRE
# =============================================================================

elif pagina == "ℹ️ Sobre a Metodologia":
    st.markdown("## ℹ️ Sobre a Metodologia VISIA")
    
    st.markdown("""
    ### O que é VISIA?
    
    **VISIA** (Valoração de Impacto Social e Investimento Aplicado) é uma metodologia 
    proprietária desenvolvida pelo **IBEDIS** para mensuração, valoração e certificação 
    do impacto social de projetos e organizações.
    
    ---
    
    ### 🧮 Fórmulas Principais
    
    #### SROI (Social Return on Investment)
    ```
    SROI = (Valor Social Total - Investimento) / Investimento
    ```
    
    #### UISV (Unidade de Impacto Social VISIA)
    ```
    UISV = (SROI × 2) + (ROI_fiscal × 3) + (impacto_pessoas / 100) + bônus
    ```
    
    #### TCS (Tokens de Crédito Social)
    ```
    TCS = UISV × 0.3 × (Investimento / 10.000)
    ```
    
    ---
    
    ### 📊 Classificação de Projetos
    
    | UISV | Classificação | Descrição |
    |------|---------------|-----------|
    | ≥ 20 | 🟢 A | Altíssimo impacto |
    | ≥ 12 | 🔵 B | Alto impacto |
    | ≥ 6 | 🟡 C | Médio impacto |
    | < 6 | 🔴 D | Baixo impacto |
    
    ---
    
    ### 📚 Fontes de Dados
    
    - MEC / FUNDEB
    - MTE - Ministério do Trabalho
    - IBGE / IPEA
    - Fórum Brasileiro de Segurança Pública
    - Senappen/MJSP
    - WRI Brasil
    - Banco Mundial / BID
    
    ---
    
    ### 📞 Contato
    
    **IBEDIS - Instituto Brasileiro de Educação e Desenvolvimento em Inovação Sustentável**
    
    - 🌐 www.ibedis.org.br
    - 📧 contato@ibedis.org.br
    """)

# =============================================================================
# RODAPÉ
# =============================================================================

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>"
    "VISIA © 2025 - IBEDIS | Todos os direitos reservados"
    "</p>",
    unsafe_allow_html=True
)
