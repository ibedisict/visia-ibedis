"""
VISIA DATABASE - Base de Dados de Referência para Cálculo de Impacto Social
===========================================================================
Consolidação de 3 sessões de pesquisa (Dezembro 2025)
Fonte: Dados oficiais do governo brasileiro, IBGE, IPEA, FBSP, CNJ, MEC, MTE

Autor: IBEDIS - Instituto Brasileiro de Educação e Desenvolvimento em Inovação Sustentável
Versão: 1.0.0
Data: Dezembro 2025
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

# =============================================================================
# ENUMS E TIPOS
# =============================================================================

class Bioma(Enum):
    AMAZONIA = "amazonia"
    MATA_ATLANTICA = "mata_atlantica"
    CERRADO = "cerrado"
    CAATINGA = "caatinga"
    PANTANAL = "pantanal"
    PAMPA = "pampa"

class TipoProjeto(Enum):
    EDUCACAO = "educacao"
    QUALIFICACAO_PROFISSIONAL = "qualificacao_profissional"
    PRIMEIRA_INFANCIA = "primeira_infancia"
    MEIO_AMBIENTE = "meio_ambiente"
    SAUDE = "saude"
    SEGURANCA = "seguranca"
    ASSISTENCIA_SOCIAL = "assistencia_social"
    CULTURA = "cultura"
    ESPORTE = "esporte"

class TipoCrime(Enum):
    HOMICIDIO = "homicidio"
    ROUBO = "roubo"
    FURTO = "furto"
    ESTELIONATO = "estelionato"
    TRAFICO = "trafico"
    LATROCINIO = "latrocinio"

# =============================================================================
# CONSTANTES - EDUCAÇÃO (Sessão 1)
# =============================================================================

EDUCACAO = {
    # FUNDEB 2024-2025
    "fundeb": {
        "valor_aluno_ano_minimo_2024": 5559.00,
        "valor_aluno_ano_maximo_2024": 8539.00,
        "valor_aluno_ano_medio_2024": 7049.00,
        "valor_aluno_ano_minimo_2025": 5870.00,  # Estimativa
        "complementacao_uniao_2024_bilhoes": 35.8,
        "total_alunos_educacao_basica": 47_000_000,
    },
    
    # Piso e formação docente
    "docentes": {
        "piso_nacional_2025": 4867.77,
        "piso_nacional_2024": 4580.57,
        "total_professores_brasil": 2_300_000,
        "percentual_sem_formacao_adequada": 0.33,
        "custo_formacao_professor_min": 3500.00,
        "custo_formacao_professor_max": 5200.00,
        "custo_formacao_professor_medio": 4350.00,
        "alunos_impactados_por_professor": 150,
    },
    
    # Indicadores de impacto educacional
    "impacto": {
        "aumento_empregabilidade_por_10pct_melhoria": 0.06,  # 5-8%
        "economia_evasao_evitada_min": 50000.00,
        "economia_evasao_evitada_max": 80000.00,
        "retorno_pib_desvio_padrao_educacao": 0.015,  # 1-2.2 p.p./ano
    },
    
    # Ensino técnico
    "tecnico": {
        "aumento_salarial_vs_medio": 0.32,  # 32% a mais
        "taxa_desemprego_tecnico": 0.072,  # 7.2%
        "taxa_desemprego_medio": 0.102,  # 10.2%
        "taxa_empregabilidade_engenharia_computacao": 0.926,
    },
}

# =============================================================================
# CONSTANTES - TRABALHO E CLT (Sessão 2)
# =============================================================================

TRABALHO = {
    # Salário mínimo e encargos 2025
    "salario_minimo": {
        "valor_2025": 1518.00,
        "valor_2024": 1412.00,
        "reajuste_2025": 0.075,  # 7.5%
    },
    
    # Encargos trabalhistas CLT
    "encargos_clt": {
        "inss_empregador": 0.20,
        "fgts": 0.08,
        "ferias_13o_proporcional": 0.1111,
        "terco_ferias": 0.0370,
        "multa_fgts_provisao": 0.04,
        "sistema_s_total": 0.058,
        "total_minimo": 0.67,
        "total_maximo": 1.10,
        "total_medio": 0.85,
    },
    
    # Arrecadação governo por trabalhador formal
    "arrecadacao_governo": {
        "por_salario_minimo_ano": 5004.00,
        "por_5_salarios_ano": 21804.00,
        "por_10_salarios_ano": 49420.00,
        "media_trabalhador_formal_ano": 15000.00,
    },
    
    # Qualificação profissional
    "qualificacao": {
        "custo_curso_senai_medio": 2500.00,
        "custo_curso_tecnico_medio": 8000.00,
        "taxa_colocacao_mercado": 0.65,  # 60-80%
        "aumento_renda_medio": 0.35,  # 25-45%
        "investimento_programa_manuel_querino": 4000.00,
        "bolsa_auxilio_qualificacao": 1000.00,
    },
}

# =============================================================================
# CONSTANTES - PROGRAMAS SOCIAIS (Sessão 1)
# =============================================================================

PROGRAMAS_SOCIAIS = {
    # Bolsa Família
    "bolsa_familia": {
        "familias_beneficiadas_milhoes": 20.5,
        "valor_medio_beneficio": 683.00,
        "valor_minimo_beneficio": 600.00,
        "investimento_anual_bilhoes": 168.0,
        "custo_familia_ano": 8196.00,  # 12 x R$ 683
    },
    
    # BPC - Benefício de Prestação Continuada
    "bpc": {
        "valor_beneficio": 1518.00,  # 1 salário mínimo
        "beneficiarios_milhoes": 5.8,
    },
    
    # CRAS/CREAS
    "assistencia_social": {
        "custo_atendimento_cras_pessoa_ano": 1200.00,
        "custo_atendimento_creas_pessoa_ano": 2400.00,
        "economia_saida_vulnerabilidade": 8196.00,  # Bolsa Família evitado
    },
}

# =============================================================================
# CONSTANTES - SISTEMA PRISIONAL (Sessão 3)
# =============================================================================

SISTEMA_PRISIONAL = {
    # Custos 2024 (Senappen/MJSP)
    "custos": {
        "custo_preso_federal_mes": 40800.00,
        "custo_preso_federal_ano": 489600.00,
        "custo_preso_estadual_medio_mes": 2331.49,
        "custo_preso_estadual_medio_ano": 27978.00,
        "custo_preso_estadual_min_mes": 1105.00,  # ES
        "custo_preso_estadual_max_mes": 4367.00,  # BA
        "investimento_total_2024_bilhoes": 20.7,
        "despesa_pessoal_bilhoes": 14.2,
        "outras_despesas_bilhoes": 6.5,
    },
    
    # População carcerária
    "populacao": {
        "total_presos_2023": 852010,
        "crescimento_2000_2023": 2.661,  # 266.1%
        "presos_federais": 520,  # Aproximado, 5 penitenciárias
        "taxa_reincidencia": 0.42,  # ~42%
    },
    
    # Economia com ressocialização
    "ressocializacao": {
        "economia_por_preso_ressocializado_ano": 27978.00,
        "reducao_reincidencia_projetos_sociais": 0.30,  # 30%
        "custo_programa_ressocializacao": 5000.00,
    },
}

# =============================================================================
# CONSTANTES - SEGURANÇA E CUSTO DO CRIME (Sessão 3)
# =============================================================================

SEGURANCA_CRIME = {
    # Custos totais da violência
    "custo_violencia": {
        "impacto_pib_percentual_min": 0.059,  # 5.9% IPEA
        "impacto_pib_percentual_max": 0.14,   # 11-14% estudos recentes
        "impacto_total_trilhoes": 1.3,  # R$ 1,3 trilhão
        "custo_homicidio_medio": 1000000.00,  # R$ 1 milhão
        "gastos_seguranca_publica_2023_bilhoes": 124.8,
        "gastos_estados_2023_bilhoes": 101.0,
        "gastos_seguranca_privada_bilhoes": 170.0,
        "percentual_pib_seguranca_privada": 0.017,
    },
    
    # Estatísticas criminais 2023-2024
    "estatisticas": {
        "homicidios_2023": 46328,
        "homicidios_2024": 38777,  # Recorde baixo
        "taxa_homicidio_2023_100mil": 22.8,
        "taxa_homicidio_2024_100mil": 17.8,
        "limite_oms_100mil": 10.0,
        "estelionatos_crescimento_2023": 0.082,
        "estelionatos_digitais_crescimento": 0.136,
        "tentativas_fraude_prejuizo_bilhoes": 51.6,
    },
    
    # Custos por tipo de crime (estimativas)
    "custo_por_crime": {
        "homicidio": 1000000.00,
        "latrocinio": 1200000.00,
        "roubo_carga_medio": 114000.00,  # R$ 1.2 bi / 10.478 ocorrências
        "roubo_veiculo_medio": 45000.00,
        "furto_medio": 5000.00,
        "estelionato_medio": 22000.00,  # R$ 51.6 bi potencial
    },
    
    # Impacto econômico
    "impacto_economico": {
        "reducao_produtividade_empresas": 0.09,  # até 9%
        "reducao_crescimento_latam_homicidios": 0.005,  # 0.5 p.p./ano
        "roubos_carga_2024": 10478,
        "perdas_roubos_carga_bilhoes": 1.2,
        "perdas_combustivel_fraude_bilhoes": 29.0,
    },
    
    # Prevenção e impacto projetos sociais
    "prevencao": {
        "reducao_crime_jovens_atendidos": 0.70,  # 60-80%
        "economia_homicidio_evitado": 1000000.00,
        "economia_encarceramento_evitado_ano": 27978.00,
    },
}

# =============================================================================
# CONSTANTES - MEIO AMBIENTE (Sessões 2 e 3)
# =============================================================================

MEIO_AMBIENTE = {
    # Custos recuperação por bioma (R$/hectare)
    "custo_recuperacao_hectare": {
        "amazonia": 2000.00,
        "mata_atlantica": 2100.00,
        "cerrado": 3000.00,
        "caatinga": 1800.00,
        "pantanal": 2200.00,
        "pampa": 1900.00,
        "regeneracao_natural": 800.00,
        "regeneracao_assistida": 1200.00,
        "plantio_total": 2500.00,
    },
    
    # Recuperação pastagens degradadas (Amazônia)
    "recuperacao_pastagem": {
        "moderadamente_degradada": 1330.66,
        "severamente_degradada": 1904.02,
        "manutencao_preventiva_ano": 298.10,
        "receita_moderada_recuperada": 2287.73,
        "receita_severa_recuperada": 2764.34,
    },
    
    # Metas nacionais
    "metas_nacionais": {
        "meta_acordo_paris_hectares": 12000000,
        "investimento_necessario_usd_ano_min": 700000000,
        "investimento_necessario_usd_ano_max": 1200000000,
        "eco_invest_brasil_bilhoes": 31.4,
        "restaura_amazonia_milhoes": 450,
        "meta_restaura_amazonia_hectares": 6000000,
    },
    
    # Educação ambiental impacto
    "educacao_ambiental": {
        "reducao_consumo_agua": 0.20,  # 10-30%
        "reducao_consumo_energia": 0.15,
        "reducao_residuos": 0.25,
    },
    
    # PSA - Pagamento Serviços Ambientais
    "psa": {
        "valor_hectare_conservado_ano_min": 500.00,
        "valor_hectare_conservado_ano_max": 1850.00,  # R$ 50k / 27 ha
        "programa_extrema_hectares": 7000,
        "programa_reflorestar_es_hectares": 10000,
        "investimento_reflorestar_milhoes": 52.0,
        "icms_ecologico_percentual": 0.05,  # 5% do ICMS
    },
    
    # Créditos de carbono
    "carbono": {
        "preco_tonelada_co2_usd_min": 10.00,
        "preco_tonelada_co2_usd_medio": 25.00,
        "preco_tonelada_co2_usd_max": 50.00,
        "sequestro_floresta_ton_ha_ano": 10.0,  # Média tropical
        "reducao_emissoes_produtos_ocde": 0.33,
    },
}

# =============================================================================
# CONSTANTES - SROI E RETORNO SOCIAL (Sessões 2 e 3)
# =============================================================================

SROI_REFERENCIAS = {
    # SROI por tipo de projeto
    "por_tipo_projeto": {
        "educacao_basica": {"min": 1.5, "max": 3.5, "medio": 2.5},
        "qualificacao_profissional": {"min": 3.5, "max": 6.8, "medio": 5.0},
        "primeira_infancia": {"min": 7.0, "max": 13.0, "medio": 10.0},
        "saude_preventiva": {"min": 2.0, "max": 4.0, "medio": 3.0},
        "meio_ambiente": {"min": 1.5, "max": 4.0, "medio": 2.5},
        "ressocializacao": {"min": 2.0, "max": 5.0, "medio": 3.5},
        "esporte_cultura": {"min": 1.2, "max": 2.5, "medio": 1.8},
    },
    
    # Casos reais brasileiros
    "casos_reais": {
        "gerando_falcoes": 3.5,
        "caer_ramacrisna": 3.62,
        "adolescente_aprendiz_ramacrisna": 3.50,
        "cursos_profissionalizantes_ramacrisna": 6.81,
        "formacao_professor_estimado": 130.0,  # Alto multiplicador
    },
    
    # Multiplicadores
    "multiplicadores": {
        "familiar": {"min": 3.0, "max": 4.0, "medio": 3.5},
        "comunitario": {"min": 1.5, "max": 2.5, "medio": 2.0},
        "total": {"min": 4.5, "max": 10.0, "medio": 7.0},
    },
}

# =============================================================================
# CONSTANTES - TERCEIRO SETOR E MROSC (Sessão 3)
# =============================================================================

TERCEIRO_SETOR = {
    # Dados gerais
    "dados_gerais": {
        "movimentacao_anual_bilhoes": 32.0,
        "isp_2022_bilhoes": 4.8,
        "isp_2021_bilhoes": 4.4,
        "isp_2020_bilhoes": 6.1,  # Pico pandemia
        "media_anual_gife_bilhoes": 3.0,
    },
    
    # Incentivos fiscais disponíveis
    "incentivos_fiscais": {
        "entidades_utilidade_publica_lucro": 0.02,  # 2% lucro operacional
        "fia_ir_devido": 0.01,  # 1% IR devido
        "limite_doacao_pj_lucro_real": 0.02,
        "limite_doacao_pf_base_calculo": 0.06,
    },
    
    # MROSC - Lei 13.019/2014
    "mrosc": {
        "vigencia": "2014-07-31",
        "alteracao_lei_13204": "2015-12-14",
        "tipos_parceria": ["termo_colaboracao", "termo_fomento", "acordo_cooperacao"],
        "exigencia_contrapartida_financeira": False,
        "tempo_minimo_existencia_anos": 1,  # 1-3 conforme edital
    },
}

# =============================================================================
# INDICADORES MACROECONÔMICOS 2025
# =============================================================================

MACROECONOMIA = {
    "pib_brasil_trilhoes": 11.2,
    "populacao_milhoes": 215.0,
    "taxa_desemprego": 0.068,
    "inflacao_ipca_acumulada": 0.048,
    "taxa_selic": 0.1225,
    "salario_medio_formal": 3200.00,
    "renda_per_capita_mensal": 1848.00,
    "taxa_pobreza": 0.315,  # 31.5% até 1/2 SM
    "taxa_extrema_pobreza": 0.055,  # 5.5%
    "cotacao_dolar": 5.75,  # Estimativa
}

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def get_custo_recuperacao(bioma: str) -> float:
    """Retorna custo de recuperação por hectare para um bioma específico."""
    bioma_lower = bioma.lower().replace(" ", "_")
    return MEIO_AMBIENTE["custo_recuperacao_hectare"].get(bioma_lower, 2500.00)

def get_sroi_referencia(tipo_projeto: str) -> Dict[str, float]:
    """Retorna faixa de SROI de referência para um tipo de projeto."""
    tipo_lower = tipo_projeto.lower().replace(" ", "_")
    return SROI_REFERENCIAS["por_tipo_projeto"].get(
        tipo_lower, 
        {"min": 1.0, "max": 3.0, "medio": 2.0}
    )

def get_custo_crime(tipo_crime: str) -> float:
    """Retorna custo econômico estimado por tipo de crime."""
    tipo_lower = tipo_crime.lower()
    return SEGURANCA_CRIME["custo_por_crime"].get(tipo_lower, 50000.00)

def get_custo_preso_anual(tipo: str = "estadual") -> float:
    """Retorna custo anual de um preso por tipo de unidade."""
    if tipo.lower() == "federal":
        return SISTEMA_PRISIONAL["custos"]["custo_preso_federal_ano"]
    return SISTEMA_PRISIONAL["custos"]["custo_preso_estadual_medio_ano"]

def get_arrecadacao_trabalhador(salarios_minimos: int = 1) -> float:
    """Retorna arrecadação anual estimada do governo por trabalhador."""
    if salarios_minimos <= 1:
        return TRABALHO["arrecadacao_governo"]["por_salario_minimo_ano"]
    elif salarios_minimos <= 5:
        return TRABALHO["arrecadacao_governo"]["por_5_salarios_ano"]
    else:
        return TRABALHO["arrecadacao_governo"]["por_10_salarios_ano"]

def get_economia_bolsa_familia_ano() -> float:
    """Retorna economia anual por família que sai do Bolsa Família."""
    return PROGRAMAS_SOCIAIS["bolsa_familia"]["custo_familia_ano"]

def calcular_multiplicador_social(beneficiarios_diretos: int) -> Dict[str, int]:
    """Calcula impacto total considerando multiplicadores familiares e comunitários."""
    mult = SROI_REFERENCIAS["multiplicadores"]
    
    impacto_familiar = int(beneficiarios_diretos * mult["familiar"]["medio"])
    impacto_comunitario = int(impacto_familiar * mult["comunitario"]["medio"])
    
    return {
        "beneficiarios_diretos": beneficiarios_diretos,
        "impacto_familiar": impacto_familiar,
        "impacto_comunitario": impacto_comunitario,
        "impacto_total": impacto_comunitario,
        "multiplicador_total": round(impacto_comunitario / beneficiarios_diretos, 2),
    }

# =============================================================================
# METADADOS
# =============================================================================

METADATA = {
    "versao": "1.0.0",
    "data_atualizacao": "2025-12-10",
    "fontes": [
        "MEC/FUNDEB",
        "MTE - Ministério do Trabalho e Emprego",
        "IBGE",
        "IPEA",
        "Fórum Brasileiro de Segurança Pública (FBSP)",
        "Anuário Brasileiro de Segurança Pública 2024",
        "CNJ - Conselho Nacional de Justiça",
        "Senappen/MJSP - Painel Custo do Preso",
        "GIFE - Censo do Investimento Social Privado",
        "Instituto Ramacrisna",
        "WRI Brasil",
        "The Conversation / Exame",
    ],
    "autor": "IBEDIS - Instituto Brasileiro de Educação e Desenvolvimento em Inovação Sustentável",
    "metodologia": "VISIA - Valoração de Impacto Social e Investimento Aplicado",
}


if __name__ == "__main__":
    # Teste básico
    print("=" * 60)
    print("VISIA DATABASE - Teste de Constantes")
    print("=" * 60)
    
    print(f"\n📚 EDUCAÇÃO:")
    print(f"   FUNDEB médio 2024: R$ {EDUCACAO['fundeb']['valor_aluno_ano_medio_2024']:,.2f}/aluno/ano")
    print(f"   Piso professor 2025: R$ {EDUCACAO['docentes']['piso_nacional_2025']:,.2f}")
    
    print(f"\n💼 TRABALHO:")
    print(f"   Salário mínimo 2025: R$ {TRABALHO['salario_minimo']['valor_2025']:,.2f}")
    print(f"   Encargos CLT médio: {TRABALHO['encargos_clt']['total_medio']*100:.0f}%")
    
    print(f"\n🔒 SISTEMA PRISIONAL:")
    print(f"   Custo preso estadual/ano: R$ {SISTEMA_PRISIONAL['custos']['custo_preso_estadual_medio_ano']:,.2f}")
    print(f"   Custo preso federal/ano: R$ {SISTEMA_PRISIONAL['custos']['custo_preso_federal_ano']:,.2f}")
    
    print(f"\n🚨 SEGURANÇA:")
    print(f"   Custo homicídio: R$ {SEGURANCA_CRIME['custo_violencia']['custo_homicidio_medio']:,.2f}")
    print(f"   Gastos segurança pública 2023: R$ {SEGURANCA_CRIME['custo_violencia']['gastos_seguranca_publica_2023_bilhoes']:.1f} bi")
    
    print(f"\n🌳 MEIO AMBIENTE:")
    print(f"   Custo recuperação Amazônia: R$ {MEIO_AMBIENTE['custo_recuperacao_hectare']['amazonia']:,.2f}/ha")
    print(f"   Meta Acordo de Paris: {MEIO_AMBIENTE['metas_nacionais']['meta_acordo_paris_hectares']:,} ha")
    
    print(f"\n📊 SROI REFERÊNCIAS:")
    for tipo, valores in SROI_REFERENCIAS["por_tipo_projeto"].items():
        print(f"   {tipo}: {valores['min']:.1f} - {valores['max']:.1f} (médio: {valores['medio']:.1f})")
    
    print(f"\n✅ Database carregado com sucesso!")
    print(f"   Versão: {METADATA['versao']}")
    print(f"   Atualização: {METADATA['data_atualizacao']}")
