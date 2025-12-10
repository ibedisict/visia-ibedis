"""
VISIA REPORTS - Gerador de Relatórios de Impacto Social
========================================================
Módulo para geração de relatórios completos de impacto social
incluindo análise VISIA, recomendações e projeções.

Autor: IBEDIS
Versão: 1.0.0
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime, date
import json

# Importar módulos VISIA
from visia_database import (
    EDUCACAO, TRABALHO, PROGRAMAS_SOCIAIS, SISTEMA_PRISIONAL,
    SEGURANCA_CRIME, MEIO_AMBIENTE, SROI_REFERENCIAS, TERCEIRO_SETOR,
    MACROECONOMIA, METADATA
)

from visia_calculators import (
    calcular_sroi, calcular_impacto_crime, calcular_impacto_ambiental,
    calcular_retorno_fiscal, calcular_visia_integrado,
    ResultadoSROI, ResultadoCrime, ResultadoAmbiental, 
    ResultadoFiscal, ResultadoIntegrado
)

# =============================================================================
# TEMPLATES DE RELATÓRIO
# =============================================================================

TEMPLATE_RELATORIO_EXECUTIVO = """
# RELATÓRIO EXECUTIVO DE IMPACTO SOCIAL

## {nome_projeto}

**Data de Emissão:** {data_emissao}
**Metodologia:** VISIA - Valoração de Impacto Social e Investimento Aplicado
**Elaborado por:** IBEDIS - Instituto Brasileiro de Educação e Desenvolvimento em Inovação Sustentável

---

## RESUMO EXECUTIVO

| Indicador | Valor |
|-----------|-------|
| **Investimento Total** | R$ {investimento:,.2f} |
| **Beneficiários Diretos** | {beneficiarios_diretos:,} pessoas |
| **Impacto Total (multiplicador)** | {impacto_total:,} pessoas |
| **SROI** | {sroi:.2f} |
| **UISV** | {uisv:.2f} |
| **TCS Recomendados** | {tcs:,} |
| **Classificação** | {classificacao} |

---

## ANÁLISE DE IMPACTO

### Retorno Social do Investimento (SROI)

O projeto apresenta SROI de **{sroi:.2f}**, significando que cada R$ 1,00 investido 
gera R$ {sroi:.2f} em valor social.

{analise_sroi}

### Impacto Fiscal

| Componente | Valor |
|------------|-------|
| Arrecadação gerada | R$ {arrecadacao:,.2f} |
| Economia em programas sociais | R$ {economia_programas:,.2f} |
| Economia em segurança | R$ {economia_seguranca:,.2f} |
| Economia em saúde | R$ {economia_saude:,.2f} |
| **Retorno Fiscal Total** | R$ {retorno_fiscal:,.2f} |
| **ROI Fiscal** | {roi_fiscal:.2f} |
| **Payback** | {payback:.1f} anos |

{secao_crime}

{secao_ambiental}

---

## TOKENS DE CRÉDITO SOCIAL (TCS)

Com base na análise VISIA, recomenda-se a emissão de **{tcs:,} TCS** para este projeto.

### Composição do UISV

| Componente | Contribuição |
|------------|--------------|
| SROI (peso 2x) | {contrib_sroi:.2f} |
| ROI Fiscal (peso 3x) | {contrib_fiscal:.2f} |
| Impacto em pessoas | {contrib_pessoas:.2f} |
| Bônus segurança | {contrib_crime:.2f} |
| Bônus ambiental | {contrib_ambiental:.2f} |
| **UISV Total** | **{uisv:.2f}** |

### Fórmula TCS

```
TCS = UISV × 0.3 × (Investimento / 10.000)
TCS = {uisv:.2f} × 0.3 × ({investimento:,.0f} / 10.000)
TCS = {tcs:,}
```

---

## RECOMENDAÇÕES

{recomendacoes}

---

## CONSIDERAÇÕES FINAIS

{consideracoes_finais}

---

## METODOLOGIA

Este relatório foi elaborado utilizando a metodologia **VISIA** (Valoração de Impacto 
Social e Investimento Aplicado), desenvolvida pelo IBEDIS.

### Base de Dados de Referência

- FUNDEB (MEC)
- Anuário Brasileiro de Segurança Pública (FBSP)
- Painel Custo do Preso (Senappen/MJSP)
- Censo GIFE
- IBGE / IPEA
- Banco Mundial / BID

### Versão da Metodologia

- Versão: {versao}
- Data de Atualização: {data_atualizacao}

---

*Documento gerado automaticamente pelo sistema VISIA - IBEDIS*
*{data_emissao}*
"""

TEMPLATE_SECAO_CRIME = """
### Impacto em Segurança Pública

O projeto demonstra potencial de redução de criminalidade:

| Indicador | Valor |
|-----------|-------|
| Jovens afastados do crime | {jovens_afastados} |
| Homicídios evitados | {homicidios_evitados} |
| Encarceramentos evitados | {encarceramentos_evitados} |
| **Economia total** | R$ {economia_crime:,.2f} |
| **ROI Segurança** | {roi_seguranca:.2f} |

**Referência:** Cada homicídio custa em média R$ 1 milhão ao poder público, 
e cada preso custa R$ {custo_preso:,.2f}/ano ao sistema prisional.
"""

TEMPLATE_SECAO_AMBIENTAL = """
### Impacto Ambiental

O projeto contribui para a recuperação ambiental:

| Indicador | Valor |
|-----------|-------|
| Hectares recuperados | {hectares:,.2f} ha |
| Bioma | {bioma} |
| CO₂ sequestrado | {co2:,.0f} toneladas |
| Benefícios de carbono | R$ {beneficio_carbono:,.2f} |
| Benefícios PSA | R$ {beneficio_psa:,.2f} |
| **Valor total benefícios** | R$ {valor_total:,.2f} |
| **ROI Ambiental** | {roi_ambiental:.2f} |

**Referência:** Custo médio de recuperação no bioma: R$ {custo_hectare:,.2f}/ha
"""

# =============================================================================
# FUNÇÕES DE GERAÇÃO
# =============================================================================

def gerar_analise_sroi(resultado_sroi: ResultadoSROI) -> str:
    """Gera texto de análise do SROI."""
    
    sroi = resultado_sroi.sroi
    sroi_min, sroi_max = resultado_sroi.sroi_range
    
    if sroi >= sroi_max:
        qualificacao = "excepcional"
        complemento = "superando significativamente as referências do setor"
    elif sroi >= (sroi_min + sroi_max) / 2:
        qualificacao = "muito bom"
        complemento = "acima da média para projetos similares"
    elif sroi >= sroi_min:
        qualificacao = "adequado"
        complemento = "dentro da faixa esperada para o tipo de projeto"
    else:
        qualificacao = "abaixo do esperado"
        complemento = "sugerindo necessidade de otimização"
    
    componentes_texto = ""
    if resultado_sroi.componentes:
        componentes_texto = "\n**Componentes do valor social:**\n"
        for comp, valor in resultado_sroi.componentes.items():
            componentes_texto += f"- {comp.replace('_', ' ').title()}: R$ {valor:,.2f}\n"
    
    return f"""
O SROI de {sroi:.2f} é considerado **{qualificacao}**, {complemento}.

A faixa de referência para projetos desta natureza é de {sroi_min:.1f} a {sroi_max:.1f}.
{componentes_texto}
"""

def gerar_recomendacoes(resultado: ResultadoIntegrado) -> str:
    """Gera recomendações baseadas na análise."""
    
    recomendacoes = []
    
    # Baseado no SROI
    if resultado.sroi.sroi < resultado.sroi.sroi_range[0]:
        recomendacoes.append(
            "**Otimizar SROI:** Considerar aumentar o número de beneficiários ou "
            "incluir componentes de maior impacto como qualificação profissional."
        )
    
    # Baseado na classificação
    if resultado.classificacao == "D":
        recomendacoes.append(
            "**Revisar estratégia:** O projeto apresenta baixo impacto. "
            "Recomenda-se revisão da teoria de mudança e dos indicadores de resultado."
        )
    elif resultado.classificacao == "C":
        recomendacoes.append(
            "**Potencial de melhoria:** O projeto tem espaço para ampliar seu impacto. "
            "Considerar parcerias estratégicas e ampliação da abrangência."
        )
    
    # Baseado no ROI fiscal
    if resultado.fiscal.tempo_payback_anos > 5:
        recomendacoes.append(
            "**Acelerar retorno fiscal:** O tempo de payback está elevado. "
            "Considerar estratégias de geração de emprego e renda para acelerar o retorno."
        )
    
    # Baseado no impacto em criminalidade
    if resultado.crime and resultado.crime.roi_seguranca > 2:
        recomendacoes.append(
            "**Destacar impacto em segurança:** O projeto tem forte impacto na "
            "prevenção à criminalidade, o que pode ser valorizado em editais de segurança pública."
        )
    
    # Baseado no impacto ambiental
    if resultado.ambiental and resultado.ambiental.roi_ambiental > 1:
        recomendacoes.append(
            "**Potencial de créditos de carbono:** O componente ambiental apresenta "
            "retorno positivo. Considerar certificação para venda de créditos de carbono."
        )
    
    # TCS
    if resultado.tcs_recomendados > 5000:
        recomendacoes.append(
            f"**Emissão de TCS:** Com {resultado.tcs_recomendados:,} TCS recomendados, "
            "o projeto é elegível para tokenização e captação via investimento de impacto."
        )
    
    if not recomendacoes:
        recomendacoes.append(
            "**Manter a estratégia atual:** O projeto apresenta bom desempenho em "
            "todos os indicadores. Recomenda-se manutenção da abordagem com monitoramento contínuo."
        )
    
    return "\n\n".join([f"{i+1}. {r}" for i, r in enumerate(recomendacoes)])

def gerar_consideracoes_finais(resultado: ResultadoIntegrado) -> str:
    """Gera considerações finais do relatório."""
    
    classificacao_texto = {
        "A": "altíssimo impacto social",
        "B": "alto impacto social", 
        "C": "médio impacto social",
        "D": "baixo impacto social, necessitando revisão"
    }
    
    return f"""
O projeto **{resultado.projeto}** apresenta **{classificacao_texto[resultado.classificacao]}**, 
com potencial de beneficiar diretamente {resultado.beneficiarios_diretos:,} pessoas e 
indiretamente {resultado.impacto_total_pessoas:,} pessoas considerando o efeito multiplicador.

O investimento de R$ {resultado.investimento_total:,.2f} tem retorno fiscal projetado de 
R$ {resultado.fiscal.retorno_fiscal_total:,.2f} em {max(1, int(resultado.fiscal.tempo_payback_anos * 2))} anos, 
representando ROI de {resultado.fiscal.roi_fiscal:.2f}.

A emissão de **{resultado.tcs_recomendados:,} Tokens de Crédito Social (TCS)** é recomendada, 
permitindo a captação de recursos via investidores de impacto e a rastreabilidade do 
impacto social gerado.

Este relatório atesta a viabilidade social do projeto e sua adequação aos critérios 
da metodologia VISIA para financiamento e parcerias.
"""

def gerar_relatorio_completo(
    resultado: ResultadoIntegrado,
    nome_elaborador: str = "IBEDIS"
) -> str:
    """
    Gera relatório completo de impacto social.
    
    Args:
        resultado: ResultadoIntegrado do cálculo VISIA
        nome_elaborador: Nome de quem elabora o relatório
    
    Returns:
        String com relatório em Markdown
    """
    
    # Análise SROI
    analise_sroi = gerar_analise_sroi(resultado.sroi)
    
    # Seção de crime (se aplicável)
    secao_crime = ""
    if resultado.crime:
        crimes = resultado.crime.crimes_evitados
        secao_crime = TEMPLATE_SECAO_CRIME.format(
            jovens_afastados=sum(crimes.values()),
            homicidios_evitados=crimes.get("homicidios", 0),
            encarceramentos_evitados=int(sum(crimes.values()) * 0.30),
            economia_crime=resultado.crime.economia_total,
            roi_seguranca=resultado.crime.roi_seguranca,
            custo_preso=SISTEMA_PRISIONAL["custos"]["custo_preso_estadual_medio_ano"]
        )
    
    # Seção ambiental (se aplicável)
    secao_ambiental = ""
    if resultado.ambiental:
        secao_ambiental = TEMPLATE_SECAO_AMBIENTAL.format(
            hectares=resultado.ambiental.hectares_recuperados,
            bioma=resultado.ambiental.bioma.replace("_", " ").title(),
            co2=resultado.ambiental.toneladas_co2_sequestradas,
            beneficio_carbono=resultado.ambiental.beneficios_carbono,
            beneficio_psa=resultado.ambiental.beneficios_psa,
            valor_total=resultado.ambiental.valor_total_beneficios,
            roi_ambiental=resultado.ambiental.roi_ambiental,
            custo_hectare=resultado.ambiental.custo_por_hectare
        )
    
    # Recomendações
    recomendacoes = gerar_recomendacoes(resultado)
    
    # Considerações finais
    consideracoes = gerar_consideracoes_finais(resultado)
    
    # Calcular contribuições UISV
    contrib_sroi = resultado.sroi.sroi * 2
    contrib_fiscal = resultado.fiscal.roi_fiscal * 3
    contrib_pessoas = resultado.impacto_total_pessoas / 100
    contrib_crime = resultado.crime.roi_seguranca * 0.5 if resultado.crime else 0
    contrib_ambiental = resultado.ambiental.roi_ambiental * 0.5 if resultado.ambiental else 0
    
    # Montar relatório
    relatorio = TEMPLATE_RELATORIO_EXECUTIVO.format(
        nome_projeto=resultado.projeto,
        data_emissao=datetime.now().strftime("%d/%m/%Y às %H:%M"),
        investimento=resultado.investimento_total,
        beneficiarios_diretos=resultado.beneficiarios_diretos,
        impacto_total=resultado.impacto_total_pessoas,
        sroi=resultado.sroi.sroi,
        uisv=resultado.uisv,
        tcs=resultado.tcs_recomendados,
        classificacao=resultado.classificacao,
        analise_sroi=analise_sroi,
        arrecadacao=resultado.fiscal.arrecadacao_gerada,
        economia_programas=resultado.fiscal.economia_programas_sociais,
        economia_seguranca=resultado.fiscal.economia_seguranca,
        economia_saude=resultado.fiscal.economia_saude,
        retorno_fiscal=resultado.fiscal.retorno_fiscal_total,
        roi_fiscal=resultado.fiscal.roi_fiscal,
        payback=resultado.fiscal.tempo_payback_anos,
        secao_crime=secao_crime,
        secao_ambiental=secao_ambiental,
        contrib_sroi=contrib_sroi,
        contrib_fiscal=contrib_fiscal,
        contrib_pessoas=contrib_pessoas,
        contrib_crime=contrib_crime,
        contrib_ambiental=contrib_ambiental,
        recomendacoes=recomendacoes,
        consideracoes_finais=consideracoes,
        versao=METADATA["versao"],
        data_atualizacao=METADATA["data_atualizacao"]
    )
    
    return relatorio

def gerar_relatorio_resumido(resultado: ResultadoIntegrado) -> str:
    """Gera relatório resumido de uma página."""
    
    return f"""
# RESUMO DE IMPACTO SOCIAL - {resultado.projeto}

## Indicadores Principais

| Métrica | Valor | Classificação |
|---------|-------|---------------|
| Investimento | R$ {resultado.investimento_total:,.2f} | - |
| Beneficiários | {resultado.beneficiarios_diretos:,} diretos / {resultado.impacto_total_pessoas:,} total | - |
| SROI | {resultado.sroi.sroi:.2f} | {'✅ Bom' if resultado.sroi.sroi >= 2 else '⚠️ Regular'} |
| UISV | {resultado.uisv:.2f} | {resultado.classificacao} |
| TCS | {resultado.tcs_recomendados:,} tokens | - |
| Retorno Fiscal | R$ {resultado.fiscal.retorno_fiscal_total:,.2f} | ROI {resultado.fiscal.roi_fiscal:.2f} |

## Síntese

O projeto é classificado como **{resultado.classificacao}** pela metodologia VISIA, 
com SROI de **{resultado.sroi.sroi:.2f}** e recomendação de emissão de **{resultado.tcs_recomendados:,} TCS**.

---
*IBEDIS - {datetime.now().strftime("%d/%m/%Y")}*
"""

def gerar_certificado_impacto(
    resultado: ResultadoIntegrado,
    numero_certificado: str = None
) -> str:
    """Gera certificado de impacto social."""
    
    if not numero_certificado:
        numero_certificado = f"VISIA-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      CERTIFICADO DE IMPACTO SOCIAL                           ║
║                         Metodologia VISIA - IBEDIS                           ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Certificado Nº: {numero_certificado:<54} ║
║                                                                              ║
║  Certificamos que o projeto:                                                 ║
║                                                                              ║
║  "{resultado.projeto:<66}" ║
║                                                                              ║
║  Foi avaliado pela metodologia VISIA e apresenta os seguintes resultados:    ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │  UISV (Unidade de Impacto Social VISIA): {resultado.uisv:>10.2f}                    │  ║
║  │  SROI (Retorno Social do Investimento):  {resultado.sroi.sroi:>10.2f}                    │  ║
║  │  Classificação:                          {resultado.classificacao:>10}                    │  ║
║  │  TCS Recomendados:                       {resultado.tcs_recomendados:>10,}                    │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
║  Investimento: R$ {resultado.investimento_total:>15,.2f}                                     ║
║  Beneficiários Diretos: {resultado.beneficiarios_diretos:>10,} pessoas                              ║
║  Impacto Total: {resultado.impacto_total_pessoas:>10,} pessoas                                      ║
║                                                                              ║
║  Data de Emissão: {datetime.now().strftime("%d/%m/%Y"):<54} ║
║  Validade: 12 meses                                                          ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Este certificado atesta a avaliação do impacto social potencial do          ║
║  projeto segundo a metodologia VISIA, desenvolvida pelo IBEDIS.              ║
║                                                                              ║
║                    _______________________________________________           ║
║                              IBEDIS - Assinatura Digital                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

def exportar_dados_json(resultado: ResultadoIntegrado) -> str:
    """Exporta dados do resultado em JSON para integração com sistemas."""
    
    dados = {
        "certificado": {
            "numero": f"VISIA-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "data_emissao": datetime.now().isoformat(),
            "metodologia": "VISIA v1.0",
            "emissor": "IBEDIS"
        },
        "projeto": {
            "nome": resultado.projeto,
            "investimento": resultado.investimento_total,
            "beneficiarios_diretos": resultado.beneficiarios_diretos,
            "impacto_total": resultado.impacto_total_pessoas
        },
        "indicadores": {
            "uisv": resultado.uisv,
            "sroi": resultado.sroi.sroi,
            "sroi_range": list(resultado.sroi.sroi_range),
            "classificacao": resultado.classificacao,
            "tcs_recomendados": resultado.tcs_recomendados
        },
        "fiscal": {
            "retorno_total": resultado.fiscal.retorno_fiscal_total,
            "roi": resultado.fiscal.roi_fiscal,
            "payback_anos": resultado.fiscal.tempo_payback_anos,
            "arrecadacao_gerada": resultado.fiscal.arrecadacao_gerada,
            "economia_programas": resultado.fiscal.economia_programas_sociais
        },
        "crime": None,
        "ambiental": None
    }
    
    if resultado.crime:
        dados["crime"] = {
            "economia_total": resultado.crime.economia_total,
            "roi": resultado.crime.roi_seguranca,
            "crimes_evitados": resultado.crime.crimes_evitados
        }
    
    if resultado.ambiental:
        dados["ambiental"] = {
            "hectares": resultado.ambiental.hectares_recuperados,
            "bioma": resultado.ambiental.bioma,
            "co2_toneladas": resultado.ambiental.toneladas_co2_sequestradas,
            "valor_beneficios": resultado.ambiental.valor_total_beneficios,
            "roi": resultado.ambiental.roi_ambiental
        }
    
    return json.dumps(dados, indent=2, ensure_ascii=False)

# =============================================================================
# TESTES
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("VISIA REPORTS - Teste de Geração de Relatórios")
    print("=" * 70)
    
    # Criar resultado de teste
    resultado = calcular_visia_integrado(
        nome_projeto="Programa Cubatão Verde 2026",
        investimento_total=1500000,
        tipo_projeto="meio_ambiente",
        beneficiarios_diretos=500,
        duracao_anos=3,
        empregos_gerados=50,
        familias_saem_vulnerabilidade=100,
        jovens_atendidos=200,
        hectares_recuperados=100,
        bioma="mata_atlantica"
    )
    
    # Teste 1: Relatório completo
    print("\n📄 TESTE 1: Relatório Completo")
    relatorio = gerar_relatorio_completo(resultado)
    print(f"   Tamanho: {len(relatorio)} caracteres")
    print(f"   Primeiras 500 caracteres:")
    print("   " + relatorio[:500].replace("\n", "\n   "))
    
    # Teste 2: Relatório resumido
    print("\n📋 TESTE 2: Relatório Resumido")
    resumo = gerar_relatorio_resumido(resultado)
    print(resumo)
    
    # Teste 3: Certificado
    print("\n🏆 TESTE 3: Certificado de Impacto")
    certificado = gerar_certificado_impacto(resultado)
    print(certificado)
    
    # Teste 4: JSON
    print("\n💾 TESTE 4: Exportação JSON")
    dados_json = exportar_dados_json(resultado)
    print(dados_json[:500] + "...")
    
    print("\n✅ Todos os testes executados com sucesso!")
