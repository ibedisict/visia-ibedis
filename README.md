# VISIA - Valoração de Impacto Social e Investimento Aplicado

## Sistema de Mensuração de Impacto Social e Geração de TCS

**Versão:** 1.0.0  
**Autor:** IBEDIS - Instituto Brasileiro de Educação e Desenvolvimento em Inovação Sustentável  
**Data:** Dezembro 2025

---

## 📋 Visão Geral

O **VISIA** (Valoração de Impacto Social e Investimento Aplicado) é uma metodologia proprietária desenvolvida pelo IBEDIS para mensuração, valoração e certificação do impacto social de projetos e organizações.

### Principais Funcionalidades

- 📊 **Cálculo de SROI** (Social Return on Investment)
- 🔒 **Análise de Impacto em Segurança Pública**
- 🌳 **Valoração de Impacto Ambiental**
- 💰 **Projeção de Retorno Fiscal**
- 🎯 **Geração de UISV** (Unidade de Impacto Social VISIA)
- 🪙 **Recomendação de TCS** (Tokens de Crédito Social)
- 📄 **Geração de Documentação MROSC**
- 📑 **Relatórios de Impacto Certificados**

---

## 🏗️ Estrutura do Sistema

```
poc_visia/
├── visia_database.py      # Base de dados de referência (constantes)
├── visia_calculators.py   # Calculadoras de impacto
├── visia_mrosc.py         # Templates para parcerias OSC-Governo
├── visia_reports.py       # Gerador de relatórios
├── scorer_visia.py        # Scoring VE1-VE4 (original)
├── analisador_elegibilidade.py
├── gerador_parecer.py
├── models.py
├── config.py
├── main.py
└── README.md
```

---

## 📊 Base de Dados de Referência

O módulo `visia_database.py` contém dados oficiais consolidados de 3 sessões de pesquisa:

### Educação
| Indicador | Valor | Fonte |
|-----------|-------|-------|
| FUNDEB 2024 (médio) | R$ 7.049/aluno/ano | MEC |
| Piso Professor 2025 | R$ 4.867,77 | MEC |
| Custo formação professor | R$ 3.500-5.200 | IBGE |
| Aumento empregabilidade técnicos | +32% | IBGE |

### Trabalho
| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Salário mínimo 2025 | R$ 1.518 | Governo Federal |
| Encargos CLT | 67-110% | MTE |
| Arrecadação/trabalhador/ano | R$ 5.004-49.420 | Receita Federal |

### Sistema Prisional
| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Custo preso estadual/ano | R$ 27.978 | Senappen/MJSP |
| Custo preso federal/ano | R$ 489.600 | Senappen/MJSP |
| População carcerária | 852.010 | FBSP 2024 |

### Segurança e Crime
| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Custo homicídio | R$ 1.000.000 | IPEA |
| Gastos segurança pública 2023 | R$ 124,8 bi | FBSP |
| Impacto crime no PIB | 11-14% | The Conversation |

### Meio Ambiente
| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Custo recuperação Amazônia | R$ 2.000/ha | WRI Brasil |
| Custo recuperação Cerrado | R$ 3.000/ha | WRI Brasil |
| Sequestro CO₂ floresta | 10 ton/ha/ano | IPCC |

### SROI de Referência
| Tipo de Projeto | SROI Mínimo | SROI Máximo |
|-----------------|-------------|-------------|
| Educação básica | 1,5 | 3,5 |
| Qualificação profissional | 3,5 | 6,8 |
| Primeira infância | 7,0 | 13,0 |
| Meio ambiente | 1,5 | 4,0 |

---

## 🧮 Fórmulas Principais

### SROI (Social Return on Investment)

```
SROI = (Valor Social Total - Investimento) / Investimento
```

### UISV (Unidade de Impacto Social VISIA)

```
UISV = (SROI × 2) + (ROI_fiscal × 3) + (impacto_pessoas / 100) + bônus_crime + bônus_ambiental
```

### TCS (Tokens de Crédito Social)

```
TCS = UISV × 0.3 × (Investimento / 10.000)
TCS_mínimo = 100
```

### Classificação de Projetos

| UISV | Classificação | Descrição |
|------|---------------|-----------|
| ≥ 20 | A | Altíssimo impacto |
| ≥ 12 | B | Alto impacto |
| ≥ 6 | C | Médio impacto |
| < 6 | D | Baixo impacto |

---

## 🚀 Como Usar

### Instalação

```bash
cd poc_visia
pip install -r requirements.txt
```

### Exemplo de Uso - Cálculo Integrado

```python
from visia_calculators import calcular_visia_integrado

resultado = calcular_visia_integrado(
    nome_projeto="Projeto Exemplo",
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

print(f"UISV: {resultado.uisv}")
print(f"TCS Recomendados: {resultado.tcs_recomendados}")
print(f"Classificação: {resultado.classificacao}")
```

### Exemplo - Geração de Relatório

```python
from visia_calculators import calcular_visia_integrado
from visia_reports import gerar_relatorio_completo, gerar_certificado_impacto

resultado = calcular_visia_integrado(...)

# Relatório completo
relatorio = gerar_relatorio_completo(resultado)

# Certificado
certificado = gerar_certificado_impacto(resultado)
```

### Exemplo - Plano de Trabalho MROSC

```python
from visia_mrosc import (
    DadosOSC, TipoParceria, AreaAtuacao,
    gerar_plano_trabalho_completo, exportar_plano_markdown
)
from datetime import date

osc = DadosOSC(
    razao_social="Nome da OSC",
    cnpj="XX.XXX.XXX/0001-XX",
    # ... outros dados
)

plano = gerar_plano_trabalho_completo(
    titulo_projeto="Nome do Projeto",
    osc=osc,
    tipo_parceria=TipoParceria.TERMO_FOMENTO,
    area_atuacao=AreaAtuacao.EDUCACAO,
    data_inicio=date(2025, 3, 1),
    duracao_meses=12,
    valor_total=500000,
    beneficiarios_estimados=100,
    # ... outros parâmetros
)

markdown = exportar_plano_markdown(plano)
```

---

## 📄 Módulos

### visia_database.py
Base de dados com constantes oficiais de referência para cálculos de impacto social.

### visia_calculators.py
Calculadoras de impacto:
- `calcular_sroi()` - Retorno social do investimento
- `calcular_impacto_crime()` - Economia em segurança
- `calcular_impacto_ambiental()` - Valoração ambiental
- `calcular_retorno_fiscal()` - Retorno para governo
- `calcular_visia_integrado()` - Cálculo completo com UISV e TCS

### visia_mrosc.py
Templates e geradores para Lei 13.019/2014 (MROSC):
- `ChecklistElegibilidade` - Verificação de requisitos OSC
- `gerar_plano_trabalho_completo()` - Gerador automático
- `exportar_plano_markdown()` - Exportação formatada

### visia_reports.py
Geração de relatórios e certificados:
- `gerar_relatorio_completo()` - Relatório executivo detalhado
- `gerar_relatorio_resumido()` - Resumo executivo
- `gerar_certificado_impacto()` - Certificado oficial
- `exportar_dados_json()` - JSON para integração

---

## 🔗 Integração com TCS

O sistema VISIA é a base para a emissão de **Tokens de Crédito Social (TCS)** do IBEDIS:

1. Projeto é avaliado pela metodologia VISIA
2. UISV é calculado com base em todos os impactos
3. Quantidade de TCS é determinada pela fórmula
4. Relatório e certificado são emitidos
5. TCS são tokenizados com lastro no impacto verificado

---

## 📚 Fontes de Dados

- MEC / FUNDEB
- MTE - Ministério do Trabalho e Emprego  
- IBGE / IPEA
- Fórum Brasileiro de Segurança Pública (FBSP)
- Senappen/MJSP - Painel Custo do Preso
- CNJ - Conselho Nacional de Justiça
- GIFE - Censo do Investimento Social Privado
- WRI Brasil
- Banco Mundial / BID

---

## 📜 Licença

Metodologia proprietária do IBEDIS.  
Uso comercial requer autorização.

---

*IBEDIS - Dezembro 2025*
