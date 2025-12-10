"""
VISIA CALCULATORS - Calculadoras de Impacto Social
===================================================
Módulo com funções de cálculo para:
- SROI (Social Return on Investment)
- Impacto em redução de criminalidade
- Recuperação ambiental
- Retorno fiscal para governo
- Multiplicador social

Autor: IBEDIS
Versão: 1.0.0
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import json

# Importar base de dados
from visia_database import (
    EDUCACAO, TRABALHO, PROGRAMAS_SOCIAIS, SISTEMA_PRISIONAL,
    SEGURANCA_CRIME, MEIO_AMBIENTE, SROI_REFERENCIAS, TERCEIRO_SETOR,
    MACROECONOMIA, get_custo_recuperacao, get_sroi_referencia,
    get_custo_crime, get_custo_preso_anual, get_arrecadacao_trabalhador,
    get_economia_bolsa_familia_ano, calcular_multiplicador_social
)

# =============================================================================
# DATACLASSES PARA RESULTADOS
# =============================================================================

@dataclass
class ResultadoSROI:
    """Resultado do cálculo de SROI."""
    investimento: float
    valor_social_bruto: float
    valor_social_liquido: float
    sroi: float
    sroi_range: Tuple[float, float]
    componentes: Dict[str, float]
    metodologia: str
    observacoes: List[str]

@dataclass
class ResultadoCrime:
    """Resultado do cálculo de impacto em criminalidade."""
    investimento: float
    crimes_evitados: Dict[str, int]
    economia_total: float
    economia_encarceramento: float
    economia_seguranca: float
    economia_saude: float
    roi_seguranca: float
    observacoes: List[str]

@dataclass
class ResultadoAmbiental:
    """Resultado do cálculo de impacto ambiental."""
    investimento: float
    hectares_recuperados: float
    bioma: str
    custo_por_hectare: float
    beneficios_carbono: float
    beneficios_psa: float
    beneficios_biodiversidade: float
    valor_total_beneficios: float
    roi_ambiental: float
    toneladas_co2_sequestradas: float
    observacoes: List[str]

@dataclass
class ResultadoFiscal:
    """Resultado do cálculo de retorno fiscal."""
    investimento_publico: float
    arrecadacao_gerada: float
    economia_programas_sociais: float
    economia_saude: float
    economia_seguranca: float
    retorno_fiscal_total: float
    roi_fiscal: float
    tempo_payback_anos: float
    observacoes: List[str]

@dataclass
class ResultadoIntegrado:
    """Resultado integrado de todos os cálculos VISIA."""
    projeto: str
    investimento_total: float
    beneficiarios_diretos: int
    impacto_total_pessoas: int
    sroi: ResultadoSROI
    crime: Optional[ResultadoCrime]
    ambiental: Optional[ResultadoAmbiental]
    fiscal: ResultadoFiscal
    uisv: float  # Unidade de Impacto Social VISIA
    tcs_recomendados: int  # Tokens de Crédito Social
    classificacao: str  # A, B, C, D
    observacoes: List[str]

# =============================================================================
# CALCULADORA SROI
# =============================================================================

def calcular_sroi(
    investimento: float,
    tipo_projeto: str,
    beneficiarios_diretos: int,
    duracao_anos: int = 1,
    empregos_gerados: int = 0,
    familias_saem_vulnerabilidade: int = 0,
    alunos_evitam_evasao: int = 0,
    hectares_recuperados: float = 0,
    customizacoes: Optional[Dict] = None
) -> ResultadoSROI:
    """
    Calcula o SROI (Social Return on Investment) de um projeto.
    
    Args:
        investimento: Valor total investido no projeto
        tipo_projeto: Tipo do projeto (educacao, qualificacao_profissional, etc.)
        beneficiarios_diretos: Número de beneficiários diretos
        duracao_anos: Duração do projeto em anos
        empregos_gerados: Número de empregos formais gerados
        familias_saem_vulnerabilidade: Famílias que saem de programas assistenciais
        alunos_evitam_evasao: Alunos que evitam evasão escolar
        hectares_recuperados: Hectares de área recuperada
        customizacoes: Dicionário com valores customizados
    
    Returns:
        ResultadoSROI com todos os cálculos
    """
    observacoes = []
    componentes = {}
    
    # Obter referência SROI para o tipo de projeto
    sroi_ref = get_sroi_referencia(tipo_projeto)
    
    # 1. Valor do impacto em empregabilidade
    if empregos_gerados > 0:
        arrecadacao_por_emprego = get_arrecadacao_trabalhador(2)  # ~2 SM
        valor_empregos = empregos_gerados * arrecadacao_por_emprego * duracao_anos
        componentes["empregos_gerados"] = valor_empregos
        observacoes.append(f"{empregos_gerados} empregos gerando R$ {valor_empregos:,.2f} em arrecadação")
    
    # 2. Valor da saída de vulnerabilidade
    if familias_saem_vulnerabilidade > 0:
        economia_bf = get_economia_bolsa_familia_ano()
        valor_vulnerabilidade = familias_saem_vulnerabilidade * economia_bf * duracao_anos
        componentes["saida_vulnerabilidade"] = valor_vulnerabilidade
        observacoes.append(f"{familias_saem_vulnerabilidade} famílias saem do Bolsa Família")
    
    # 3. Valor da prevenção de evasão escolar
    if alunos_evitam_evasao > 0:
        economia_evasao = EDUCACAO["impacto"]["economia_evasao_evitada_min"]
        valor_evasao = alunos_evitam_evasao * economia_evasao * 0.1  # 10% do valor total
        componentes["prevencao_evasao"] = valor_evasao
        observacoes.append(f"{alunos_evitam_evasao} alunos evitam evasão")
    
    # 4. Valor da recuperação ambiental
    if hectares_recuperados > 0:
        valor_carbono = hectares_recuperados * MEIO_AMBIENTE["carbono"]["sequestro_floresta_ton_ha_ano"]
        valor_carbono *= MEIO_AMBIENTE["carbono"]["preco_tonelada_co2_usd_medio"] * MACROECONOMIA["cotacao_dolar"]
        valor_carbono *= duracao_anos
        componentes["recuperacao_ambiental"] = valor_carbono
        observacoes.append(f"{hectares_recuperados} ha recuperados")
    
    # 5. Valor base por beneficiário (usando referência SROI)
    if not componentes:
        # Se não há componentes específicos, usar estimativa baseada em SROI de referência
        valor_base_beneficiario = investimento * sroi_ref["medio"] / beneficiarios_diretos
        valor_beneficiarios = beneficiarios_diretos * valor_base_beneficiario * 0.5
        componentes["impacto_direto_beneficiarios"] = valor_beneficiarios
    
    # Calcular valor social total
    valor_social_bruto = sum(componentes.values())
    valor_social_liquido = valor_social_bruto - investimento
    
    # Calcular SROI
    if investimento > 0:
        sroi = valor_social_liquido / investimento
    else:
        sroi = 0
    
    # Ajustar SROI para ficar dentro da faixa de referência se necessário
    sroi_ajustado = max(sroi_ref["min"] * 0.5, min(sroi, sroi_ref["max"] * 1.5))
    
    return ResultadoSROI(
        investimento=investimento,
        valor_social_bruto=valor_social_bruto,
        valor_social_liquido=valor_social_liquido,
        sroi=round(sroi_ajustado, 2),
        sroi_range=(sroi_ref["min"], sroi_ref["max"]),
        componentes=componentes,
        metodologia="VISIA-SROI v1.0",
        observacoes=observacoes
    )

# =============================================================================
# CALCULADORA IMPACTO CRIMINALIDADE
# =============================================================================

def calcular_impacto_crime(
    investimento: float,
    beneficiarios_jovens: int,
    duracao_anos: int = 1,
    taxa_reducao_crime: float = 0.70,  # 60-80% padrão
    tipo_area: str = "urbana",
    populacao_area: int = 100000
) -> ResultadoCrime:
    """
    Calcula o impacto econômico da redução de criminalidade.
    
    Args:
        investimento: Valor investido no projeto
        beneficiarios_jovens: Número de jovens atendidos
        duracao_anos: Duração do projeto
        taxa_reducao_crime: Taxa de redução de envolvimento com crime (0.6-0.8)
        tipo_area: Tipo da área (urbana, periurbana, rural)
        populacao_area: População da área de impacto
    
    Returns:
        ResultadoCrime com economia gerada
    """
    observacoes = []
    
    # Estimar crimes evitados baseado em estatísticas
    # Taxa base de envolvimento criminal jovens em vulnerabilidade: ~5%
    taxa_envolvimento_base = 0.05 if tipo_area == "urbana" else 0.03
    
    jovens_evitam_crime = int(beneficiarios_jovens * taxa_envolvimento_base * taxa_reducao_crime)
    
    # Distribuição típica de crimes evitados
    crimes_evitados = {
        "homicidios": max(1, int(jovens_evitam_crime * 0.02)),  # 2% seriam vítimas/autores homicídio
        "roubos": int(jovens_evitam_crime * 0.15),
        "furtos": int(jovens_evitam_crime * 0.25),
        "trafico": int(jovens_evitam_crime * 0.10),
        "outros": int(jovens_evitam_crime * 0.48),
    }
    
    # Calcular economia por tipo de crime
    economia_homicidios = crimes_evitados["homicidios"] * get_custo_crime("homicidio")
    economia_roubos = crimes_evitados["roubos"] * get_custo_crime("roubo_carga_medio")
    economia_furtos = crimes_evitados["furtos"] * get_custo_crime("furto")
    economia_trafico = crimes_evitados["trafico"] * 100000  # Estimativa custo social
    economia_outros = crimes_evitados["outros"] * 20000
    
    economia_total_crimes = (economia_homicidios + economia_roubos + 
                            economia_furtos + economia_trafico + economia_outros)
    
    # Economia com encarceramento evitado
    encarcerados_evitados = int(jovens_evitam_crime * 0.30)  # 30% seriam presos
    economia_encarceramento = encarcerados_evitados * get_custo_preso_anual() * min(duracao_anos, 5)
    
    # Economia com segurança pública (menos policiamento, menos processos)
    economia_seguranca = economia_total_crimes * 0.15  # 15% adicional
    
    # Economia com saúde (menos atendimentos violência)
    economia_saude = crimes_evitados["homicidios"] * 50000  # Custo médico por vítima
    economia_saude += (crimes_evitados["roubos"] + crimes_evitados["outros"]) * 5000
    
    economia_total = economia_total_crimes + economia_encarceramento + economia_seguranca + economia_saude
    
    # ROI em segurança
    roi_seguranca = economia_total / investimento if investimento > 0 else 0
    
    observacoes.append(f"{beneficiarios_jovens} jovens atendidos")
    observacoes.append(f"{jovens_evitam_crime} jovens evitam envolvimento criminal")
    observacoes.append(f"{encarcerados_evitados} encarceramentos evitados")
    observacoes.append(f"Economia total: R$ {economia_total:,.2f}")
    
    return ResultadoCrime(
        investimento=investimento,
        crimes_evitados=crimes_evitados,
        economia_total=economia_total,
        economia_encarceramento=economia_encarceramento,
        economia_seguranca=economia_seguranca,
        economia_saude=economia_saude,
        roi_seguranca=round(roi_seguranca, 2),
        observacoes=observacoes
    )

# =============================================================================
# CALCULADORA IMPACTO AMBIENTAL
# =============================================================================

def calcular_impacto_ambiental(
    investimento: float,
    hectares: float,
    bioma: str = "mata_atlantica",
    metodo_recuperacao: str = "plantio_total",
    anos_projeto: int = 10,
    incluir_psa: bool = True,
    incluir_carbono: bool = True
) -> ResultadoAmbiental:
    """
    Calcula o impacto e retorno de projetos de recuperação ambiental.
    
    Args:
        investimento: Valor investido
        hectares: Área em hectares
        bioma: Bioma (amazonia, mata_atlantica, cerrado, etc.)
        metodo_recuperacao: Método (regeneracao_natural, regeneracao_assistida, plantio_total)
        anos_projeto: Horizonte de tempo para cálculo de benefícios
        incluir_psa: Incluir receitas de PSA
        incluir_carbono: Incluir receitas de créditos de carbono
    
    Returns:
        ResultadoAmbiental com todos os benefícios calculados
    """
    observacoes = []
    
    # Custo de recuperação
    custo_hectare = get_custo_recuperacao(bioma)
    if metodo_recuperacao in MEIO_AMBIENTE["custo_recuperacao_hectare"]:
        custo_hectare = MEIO_AMBIENTE["custo_recuperacao_hectare"][metodo_recuperacao]
    
    custo_total_recuperacao = hectares * custo_hectare
    
    # Benefícios de carbono
    beneficios_carbono = 0
    toneladas_co2 = 0
    if incluir_carbono:
        sequestro_anual = MEIO_AMBIENTE["carbono"]["sequestro_floresta_ton_ha_ano"]
        preco_tonelada_brl = (MEIO_AMBIENTE["carbono"]["preco_tonelada_co2_usd_medio"] * 
                              MACROECONOMIA["cotacao_dolar"])
        toneladas_co2 = hectares * sequestro_anual * anos_projeto
        beneficios_carbono = toneladas_co2 * preco_tonelada_brl
        observacoes.append(f"Sequestro: {toneladas_co2:,.0f} tCO2 em {anos_projeto} anos")
    
    # Benefícios de PSA
    beneficios_psa = 0
    if incluir_psa:
        valor_psa_hectare_ano = (MEIO_AMBIENTE["psa"]["valor_hectare_conservado_ano_min"] + 
                                  MEIO_AMBIENTE["psa"]["valor_hectare_conservado_ano_max"]) / 2
        beneficios_psa = hectares * valor_psa_hectare_ano * anos_projeto
        observacoes.append(f"PSA: R$ {valor_psa_hectare_ano:,.2f}/ha/ano")
    
    # Benefícios de biodiversidade (estimativa conservadora)
    beneficios_biodiversidade = hectares * 500 * anos_projeto  # R$ 500/ha/ano
    
    # Valor total de benefícios
    valor_total_beneficios = beneficios_carbono + beneficios_psa + beneficios_biodiversidade
    
    # ROI ambiental
    roi_ambiental = (valor_total_beneficios - investimento) / investimento if investimento > 0 else 0
    
    observacoes.append(f"Bioma: {bioma}")
    observacoes.append(f"Método: {metodo_recuperacao}")
    observacoes.append(f"Custo recuperação: R$ {custo_hectare:,.2f}/ha")
    
    return ResultadoAmbiental(
        investimento=investimento,
        hectares_recuperados=hectares,
        bioma=bioma,
        custo_por_hectare=custo_hectare,
        beneficios_carbono=beneficios_carbono,
        beneficios_psa=beneficios_psa,
        beneficios_biodiversidade=beneficios_biodiversidade,
        valor_total_beneficios=valor_total_beneficios,
        roi_ambiental=round(roi_ambiental, 2),
        toneladas_co2_sequestradas=toneladas_co2,
        observacoes=observacoes
    )

# =============================================================================
# CALCULADORA RETORNO FISCAL
# =============================================================================

def calcular_retorno_fiscal(
    investimento_publico: float,
    empregos_gerados: int = 0,
    familias_saem_bf: int = 0,
    crimes_evitados: int = 0,
    internacoes_evitadas: int = 0,
    anos_horizonte: int = 10
) -> ResultadoFiscal:
    """
    Calcula o retorno fiscal para o governo de um projeto social.
    
    Args:
        investimento_publico: Investimento público no projeto
        empregos_gerados: Número de empregos formais gerados
        familias_saem_bf: Famílias que saem do Bolsa Família
        crimes_evitados: Número de crimes evitados
        internacoes_evitadas: Internações hospitalares evitadas
        anos_horizonte: Horizonte de tempo para cálculo
    
    Returns:
        ResultadoFiscal com retorno calculado
    """
    observacoes = []
    
    # Arrecadação com empregos
    arrecadacao_empregos = 0
    if empregos_gerados > 0:
        arrecadacao_por_emprego = get_arrecadacao_trabalhador(2)
        arrecadacao_empregos = empregos_gerados * arrecadacao_por_emprego * anos_horizonte
        observacoes.append(f"{empregos_gerados} empregos → R$ {arrecadacao_empregos:,.2f} arrecadação")
    
    # Economia Bolsa Família
    economia_bf = 0
    if familias_saem_bf > 0:
        economia_bf = familias_saem_bf * get_economia_bolsa_familia_ano() * anos_horizonte
        observacoes.append(f"{familias_saem_bf} famílias saem BF → R$ {economia_bf:,.2f} economia")
    
    # Economia segurança
    economia_seguranca = 0
    if crimes_evitados > 0:
        # Média ponderada de custo por crime
        custo_medio_crime = 150000  # Mix de crimes
        economia_seguranca = crimes_evitados * custo_medio_crime
        observacoes.append(f"{crimes_evitados} crimes evitados → R$ {economia_seguranca:,.2f} economia")
    
    # Economia saúde
    economia_saude = 0
    if internacoes_evitadas > 0:
        custo_internacao_media = 3500  # Custo médio SUS
        economia_saude = internacoes_evitadas * custo_internacao_media
        observacoes.append(f"{internacoes_evitadas} internações evitadas")
    
    # Totais
    arrecadacao_gerada = arrecadacao_empregos
    economia_programas = economia_bf
    retorno_fiscal_total = arrecadacao_gerada + economia_programas + economia_seguranca + economia_saude
    
    # ROI fiscal
    roi_fiscal = retorno_fiscal_total / investimento_publico if investimento_publico > 0 else 0
    
    # Tempo de payback
    retorno_anual = retorno_fiscal_total / anos_horizonte if anos_horizonte > 0 else retorno_fiscal_total
    tempo_payback = investimento_publico / retorno_anual if retorno_anual > 0 else float('inf')
    
    return ResultadoFiscal(
        investimento_publico=investimento_publico,
        arrecadacao_gerada=arrecadacao_gerada,
        economia_programas_sociais=economia_programas,
        economia_saude=economia_saude,
        economia_seguranca=economia_seguranca,
        retorno_fiscal_total=retorno_fiscal_total,
        roi_fiscal=round(roi_fiscal, 2),
        tempo_payback_anos=round(tempo_payback, 1),
        observacoes=observacoes
    )

# =============================================================================
# CALCULADORA INTEGRADA VISIA
# =============================================================================

def calcular_visia_integrado(
    nome_projeto: str,
    investimento_total: float,
    tipo_projeto: str,
    beneficiarios_diretos: int,
    duracao_anos: int = 1,
    # Parâmetros específicos
    empregos_gerados: int = 0,
    familias_saem_vulnerabilidade: int = 0,
    alunos_evitam_evasao: int = 0,
    jovens_atendidos: int = 0,
    hectares_recuperados: float = 0,
    bioma: str = "mata_atlantica",
    # Controles
    calcular_crime: bool = True,
    calcular_ambiental: bool = True
) -> ResultadoIntegrado:
    """
    Cálculo integrado VISIA com todos os componentes.
    
    Retorna ResultadoIntegrado com:
    - SROI
    - Impacto criminalidade (se aplicável)
    - Impacto ambiental (se aplicável)
    - Retorno fiscal
    - UISV (Unidade de Impacto Social VISIA)
    - TCS recomendados
    """
    observacoes = []
    
    # 1. Calcular SROI
    resultado_sroi = calcular_sroi(
        investimento=investimento_total,
        tipo_projeto=tipo_projeto,
        beneficiarios_diretos=beneficiarios_diretos,
        duracao_anos=duracao_anos,
        empregos_gerados=empregos_gerados,
        familias_saem_vulnerabilidade=familias_saem_vulnerabilidade,
        alunos_evitam_evasao=alunos_evitam_evasao,
        hectares_recuperados=hectares_recuperados
    )
    
    # 2. Calcular impacto criminalidade (se houver jovens)
    resultado_crime = None
    if calcular_crime and jovens_atendidos > 0:
        resultado_crime = calcular_impacto_crime(
            investimento=investimento_total * 0.3,  # Proporção segurança
            beneficiarios_jovens=jovens_atendidos,
            duracao_anos=duracao_anos
        )
    
    # 3. Calcular impacto ambiental (se houver hectares)
    resultado_ambiental = None
    if calcular_ambiental and hectares_recuperados > 0:
        resultado_ambiental = calcular_impacto_ambiental(
            investimento=investimento_total * 0.4,
            hectares=hectares_recuperados,
            bioma=bioma,
            anos_projeto=max(duracao_anos, 10)
        )
    
    # 4. Calcular retorno fiscal
    crimes_evitados = 0
    if resultado_crime:
        crimes_evitados = sum(resultado_crime.crimes_evitados.values())
    
    resultado_fiscal = calcular_retorno_fiscal(
        investimento_publico=investimento_total,
        empregos_gerados=empregos_gerados,
        familias_saem_bf=familias_saem_vulnerabilidade,
        crimes_evitados=crimes_evitados,
        anos_horizonte=max(duracao_anos, 10)
    )
    
    # 5. Calcular multiplicador social
    multiplicador = calcular_multiplicador_social(beneficiarios_diretos)
    impacto_total_pessoas = multiplicador["impacto_total"]
    
    # 6. Calcular UISV (Unidade de Impacto Social VISIA)
    # Fórmula: UISV = (SROI × 2) + (ROI_fiscal × 3) + (impacto_pessoas / 100) + bonificações
    uisv_base = (resultado_sroi.sroi * 2) + (resultado_fiscal.roi_fiscal * 3)
    uisv_pessoas = impacto_total_pessoas / 100
    
    # Bonificações
    bonus_crime = resultado_crime.roi_seguranca * 0.5 if resultado_crime else 0
    bonus_ambiental = resultado_ambiental.roi_ambiental * 0.5 if resultado_ambiental else 0
    
    uisv = uisv_base + uisv_pessoas + bonus_crime + bonus_ambiental
    uisv = round(uisv, 2)
    
    # 7. Calcular TCS recomendados
    # Fórmula: TCS = UISV × fator_escala × (investimento / 10000)
    fator_escala = 0.3
    tcs_recomendados = int(uisv * fator_escala * (investimento_total / 10000))
    tcs_recomendados = max(100, tcs_recomendados)  # Mínimo 100 TCS
    
    # 8. Classificação
    if uisv >= 20:
        classificacao = "A"
        observacoes.append("Projeto de altíssimo impacto")
    elif uisv >= 12:
        classificacao = "B"
        observacoes.append("Projeto de alto impacto")
    elif uisv >= 6:
        classificacao = "C"
        observacoes.append("Projeto de médio impacto")
    else:
        classificacao = "D"
        observacoes.append("Projeto de baixo impacto - revisar estratégia")
    
    observacoes.append(f"Multiplicador social: {multiplicador['multiplicador_total']}x")
    observacoes.append(f"UISV: {uisv} → {tcs_recomendados} TCS recomendados")
    
    return ResultadoIntegrado(
        projeto=nome_projeto,
        investimento_total=investimento_total,
        beneficiarios_diretos=beneficiarios_diretos,
        impacto_total_pessoas=impacto_total_pessoas,
        sroi=resultado_sroi,
        crime=resultado_crime,
        ambiental=resultado_ambiental,
        fiscal=resultado_fiscal,
        uisv=uisv,
        tcs_recomendados=tcs_recomendados,
        classificacao=classificacao,
        observacoes=observacoes
    )

# =============================================================================
# FUNÇÃO DE EXPORTAÇÃO
# =============================================================================

def exportar_resultado_json(resultado: ResultadoIntegrado) -> str:
    """Exporta resultado integrado para JSON."""
    
    def dataclass_to_dict(obj):
        if hasattr(obj, '__dataclass_fields__'):
            return {k: dataclass_to_dict(v) for k, v in obj.__dict__.items()}
        elif isinstance(obj, list):
            return [dataclass_to_dict(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: dataclass_to_dict(v) for k, v in obj.items()}
        else:
            return obj
    
    return json.dumps(dataclass_to_dict(resultado), indent=2, ensure_ascii=False)

# =============================================================================
# TESTES
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("VISIA CALCULATORS - Teste das Calculadoras")
    print("=" * 70)
    
    # Teste 1: SROI simples
    print("\n📊 TESTE 1: SROI Projeto Educacional")
    sroi = calcular_sroi(
        investimento=500000,
        tipo_projeto="educacao",
        beneficiarios_diretos=200,
        duracao_anos=2,
        empregos_gerados=30,
        alunos_evitam_evasao=50
    )
    print(f"   Investimento: R$ {sroi.investimento:,.2f}")
    print(f"   Valor Social: R$ {sroi.valor_social_bruto:,.2f}")
    print(f"   SROI: {sroi.sroi}")
    print(f"   Range referência: {sroi.sroi_range}")
    
    # Teste 2: Impacto crime
    print("\n🔒 TESTE 2: Impacto Criminalidade")
    crime = calcular_impacto_crime(
        investimento=300000,
        beneficiarios_jovens=150,
        duracao_anos=3
    )
    print(f"   Crimes evitados: {crime.crimes_evitados}")
    print(f"   Economia total: R$ {crime.economia_total:,.2f}")
    print(f"   ROI Segurança: {crime.roi_seguranca}")
    
    # Teste 3: Impacto ambiental
    print("\n🌳 TESTE 3: Impacto Ambiental")
    ambiental = calcular_impacto_ambiental(
        investimento=200000,
        hectares=50,
        bioma="mata_atlantica",
        anos_projeto=10
    )
    print(f"   Hectares: {ambiental.hectares_recuperados}")
    print(f"   tCO2 sequestradas: {ambiental.toneladas_co2_sequestradas:,.0f}")
    print(f"   Benefícios totais: R$ {ambiental.valor_total_beneficios:,.2f}")
    print(f"   ROI Ambiental: {ambiental.roi_ambiental}")
    
    # Teste 4: Retorno fiscal
    print("\n💰 TESTE 4: Retorno Fiscal")
    fiscal = calcular_retorno_fiscal(
        investimento_publico=500000,
        empregos_gerados=40,
        familias_saem_bf=20,
        crimes_evitados=15
    )
    print(f"   Retorno fiscal total: R$ {fiscal.retorno_fiscal_total:,.2f}")
    print(f"   ROI Fiscal: {fiscal.roi_fiscal}")
    print(f"   Payback: {fiscal.tempo_payback_anos} anos")
    
    # Teste 5: Cálculo integrado
    print("\n🎯 TESTE 5: Cálculo VISIA Integrado")
    resultado = calcular_visia_integrado(
        nome_projeto="Projeto Modelo IBEDIS",
        investimento_total=500000,
        tipo_projeto="qualificacao_profissional",
        beneficiarios_diretos=100,
        duracao_anos=2,
        empregos_gerados=60,
        familias_saem_vulnerabilidade=40,
        jovens_atendidos=80,
        hectares_recuperados=20,
        bioma="mata_atlantica"
    )
    
    print(f"   Projeto: {resultado.projeto}")
    print(f"   Investimento: R$ {resultado.investimento_total:,.2f}")
    print(f"   Beneficiários diretos: {resultado.beneficiarios_diretos}")
    print(f"   Impacto total: {resultado.impacto_total_pessoas} pessoas")
    print(f"   SROI: {resultado.sroi.sroi}")
    print(f"   UISV: {resultado.uisv}")
    print(f"   TCS Recomendados: {resultado.tcs_recomendados}")
    print(f"   Classificação: {resultado.classificacao}")
    print(f"   Observações: {resultado.observacoes}")
    
    print("\n✅ Todos os testes executados com sucesso!")
