"""
VISIA MROSC - Módulo de Documentação para Parcerias OSC-Governo
================================================================
Templates e geradores para documentação conforme Lei 13.019/2014 (MROSC)

Tipos de parceria:
- Termo de Colaboração: Poder público propõe, transfere recursos
- Termo de Fomento: OSC propõe, recebe recursos
- Acordo de Cooperação: Sem transferência de recursos

Autor: IBEDIS
Versão: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, date
from enum import Enum
import json

# =============================================================================
# ENUMS E TIPOS
# =============================================================================

class TipoParceria(Enum):
    TERMO_COLABORACAO = "termo_colaboracao"
    TERMO_FOMENTO = "termo_fomento"
    ACORDO_COOPERACAO = "acordo_cooperacao"

class AreaAtuacao(Enum):
    ASSISTENCIA_SOCIAL = "assistencia_social"
    EDUCACAO = "educacao"
    SAUDE = "saude"
    CULTURA = "cultura"
    ESPORTE = "esporte"
    MEIO_AMBIENTE = "meio_ambiente"
    DIREITOS_HUMANOS = "direitos_humanos"
    DESENVOLVIMENTO_AGRARIO = "desenvolvimento_agrario"
    CIENCIA_TECNOLOGIA = "ciencia_tecnologia"
    MORADIA = "moradia"
    TRABALHO_RENDA = "trabalho_renda"

class StatusOSC(Enum):
    REGULAR = "regular"
    PENDENTE = "pendente"
    IRREGULAR = "irregular"

# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class DadosOSC:
    """Dados cadastrais da OSC."""
    razao_social: str
    cnpj: str
    endereco: str
    cidade: str
    uf: str
    cep: str
    telefone: str
    email: str
    site: Optional[str] = None
    data_fundacao: Optional[date] = None
    representante_legal: str = ""
    cpf_representante: str = ""
    cargo_representante: str = "Presidente"
    areas_atuacao: List[AreaAtuacao] = field(default_factory=list)
    
@dataclass
class ChecklistElegibilidade:
    """Checklist de elegibilidade MROSC."""
    cnpj_ativo: bool = False
    estatuto_adequado: bool = False
    atas_atualizadas: bool = False
    certidao_federal: bool = False
    certidao_estadual: bool = False
    certidao_municipal: bool = False
    certidao_fgts: bool = False
    certidao_trabalhista: bool = False
    tempo_minimo_existencia: bool = False  # 1-3 anos
    experiencia_comprovada: bool = False
    capacidade_tecnica: bool = False
    infraestrutura_adequada: bool = False
    nao_impedida_cepim: bool = False
    
    def percentual_conformidade(self) -> float:
        """Retorna percentual de conformidade."""
        itens = [
            self.cnpj_ativo, self.estatuto_adequado, self.atas_atualizadas,
            self.certidao_federal, self.certidao_estadual, self.certidao_municipal,
            self.certidao_fgts, self.certidao_trabalhista, self.tempo_minimo_existencia,
            self.experiencia_comprovada, self.capacidade_tecnica, 
            self.infraestrutura_adequada, self.nao_impedida_cepim
        ]
        return sum(itens) / len(itens) * 100
    
    def itens_pendentes(self) -> List[str]:
        """Retorna lista de itens pendentes."""
        pendentes = []
        if not self.cnpj_ativo: pendentes.append("CNPJ ativo")
        if not self.estatuto_adequado: pendentes.append("Estatuto adequado ao MROSC")
        if not self.atas_atualizadas: pendentes.append("Atas de assembleia atualizadas")
        if not self.certidao_federal: pendentes.append("Certidão negativa federal")
        if not self.certidao_estadual: pendentes.append("Certidão negativa estadual")
        if not self.certidao_municipal: pendentes.append("Certidão negativa municipal")
        if not self.certidao_fgts: pendentes.append("Certidão FGTS")
        if not self.certidao_trabalhista: pendentes.append("Certidão trabalhista")
        if not self.tempo_minimo_existencia: pendentes.append("Tempo mínimo de existência (1-3 anos)")
        if not self.experiencia_comprovada: pendentes.append("Experiência comprovada na área")
        if not self.capacidade_tecnica: pendentes.append("Capacidade técnica da equipe")
        if not self.infraestrutura_adequada: pendentes.append("Infraestrutura adequada")
        if not self.nao_impedida_cepim: pendentes.append("Verificação CEPIM (não impedida)")
        return pendentes

@dataclass
class Meta:
    """Meta do plano de trabalho."""
    numero: int
    descricao: str
    indicador: str
    valor_meta: float
    unidade_medida: str
    meio_verificacao: str
    prazo_meses: int

@dataclass
class Etapa:
    """Etapa de execução."""
    numero: int
    descricao: str
    inicio_mes: int
    fim_mes: int
    responsavel: str
    recursos_necessarios: float

@dataclass
class ItemOrcamento:
    """Item do orçamento detalhado."""
    categoria: str  # pessoal, material, servicos, equipamentos, outros
    descricao: str
    unidade: str
    quantidade: float
    valor_unitario: float
    valor_total: float
    justificativa: str

@dataclass
class PlanoTrabalho:
    """Plano de trabalho completo para parceria MROSC."""
    # Identificação
    titulo_projeto: str
    osc: DadosOSC
    tipo_parceria: TipoParceria
    area_atuacao: AreaAtuacao
    
    # Período
    data_inicio: date
    data_fim: date
    duracao_meses: int
    
    # Objeto
    objeto: str
    justificativa: str
    publico_alvo: str
    beneficiarios_estimados: int
    area_abrangencia: str
    
    # Metas e etapas
    metas: List[Meta] = field(default_factory=list)
    etapas: List[Etapa] = field(default_factory=list)
    
    # Orçamento
    valor_total: float = 0
    valor_osc: float = 0  # Contrapartida em bens/serviços
    valor_parceiro: float = 0
    itens_orcamento: List[ItemOrcamento] = field(default_factory=list)
    
    # Equipe
    equipe_tecnica: List[Dict] = field(default_factory=list)
    
    # Impacto esperado
    impacto_esperado: str = ""
    ods_relacionados: List[int] = field(default_factory=list)  # ODS 1-17
    
    # Metodologia VISIA
    sroi_estimado: float = 0
    uisv_estimado: float = 0
    tcs_projetados: int = 0

# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATE_OBJETO = """
O presente {tipo_parceria} tem por objeto a execução do projeto "{titulo_projeto}", 
que visa {objetivo_geral}, beneficiando diretamente {beneficiarios} pessoas na região de 
{area_abrangencia}, durante o período de {duracao_meses} meses, em consonância com as 
diretrizes da Política Nacional de {politica_relacionada}.
"""

TEMPLATE_JUSTIFICATIVA = """
1. CONTEXTO E DIAGNÓSTICO

{diagnostico_problema}

2. RELEVÂNCIA DA INTERVENÇÃO

A presente proposta justifica-se pela necessidade de {necessidade_principal}, considerando que:

- {justificativa_1}
- {justificativa_2}
- {justificativa_3}

3. ALINHAMENTO COM POLÍTICAS PÚBLICAS

O projeto está alinhado com:
- {politica_municipal}
- {politica_estadual}
- {politica_federal}

4. CAPACIDADE INSTITUCIONAL

A {nome_osc} possui experiência comprovada na área de {area_atuacao}, tendo executado 
{quantidade_projetos} projetos similares nos últimos {anos_experiencia} anos, beneficiando 
mais de {beneficiarios_historico} pessoas.

5. RETORNO SOCIAL ESPERADO

Com base na metodologia VISIA de mensuração de impacto social:
- SROI estimado: {sroi_estimado} (cada R$ 1 investido gera R$ {sroi_estimado} em retorno social)
- Impacto direto: {beneficiarios_diretos} pessoas
- Impacto indireto (multiplicador): {impacto_multiplicador} pessoas
- TCS projetados: {tcs_projetados} Tokens de Crédito Social
"""

TEMPLATE_METODOLOGIA = """
METODOLOGIA DE EXECUÇÃO

1. ABORDAGEM METODOLÓGICA

{descricao_metodologia}

2. ESTRATÉGIAS DE IMPLEMENTAÇÃO

{estrategias}

3. MONITORAMENTO E AVALIAÇÃO

O projeto utilizará a metodologia VISIA (Valoração de Impacto Social e Investimento Aplicado) 
para mensuração contínua de resultados, incluindo:

- Indicadores de processo: acompanhamento mensal das atividades
- Indicadores de resultado: verificação trimestral das metas
- Indicadores de impacto: avaliação semestral dos efeitos na comunidade

Instrumentos de coleta:
- Formulários de cadastro e acompanhamento
- Questionários de satisfação
- Relatórios técnicos periódicos
- Registros fotográficos e audiovisuais

4. CRITÉRIOS DE ELEGIBILIDADE DOS BENEFICIÁRIOS

{criterios_elegibilidade}

5. PARCERIAS E ARTICULAÇÕES

{parcerias_previstas}
"""

TEMPLATE_CRONOGRAMA = """
CRONOGRAMA DE EXECUÇÃO

| Etapa | Descrição | Mês Início | Mês Fim | Responsável |
|-------|-----------|------------|---------|-------------|
{linhas_cronograma}

CRONOGRAMA DE DESEMBOLSO

| Parcela | Mês | Valor (R$) | % do Total |
|---------|-----|------------|------------|
{linhas_desembolso}
"""

# =============================================================================
# GERADORES
# =============================================================================

def gerar_checklist_elegibilidade(dados_osc: DadosOSC) -> ChecklistElegibilidade:
    """
    Gera checklist de elegibilidade baseado nos dados da OSC.
    Na prática, cada item deve ser verificado individualmente.
    """
    checklist = ChecklistElegibilidade()
    
    # Verificações automáticas básicas
    if dados_osc.cnpj and len(dados_osc.cnpj) == 18:  # XX.XXX.XXX/XXXX-XX
        checklist.cnpj_ativo = True
    
    if dados_osc.data_fundacao:
        anos_existencia = (date.today() - dados_osc.data_fundacao).days / 365
        checklist.tempo_minimo_existencia = anos_existencia >= 1
    
    if dados_osc.areas_atuacao:
        checklist.experiencia_comprovada = True
    
    return checklist

def gerar_objeto_parceria(
    tipo_parceria: TipoParceria,
    titulo_projeto: str,
    objetivo_geral: str,
    beneficiarios: int,
    area_abrangencia: str,
    duracao_meses: int,
    politica_relacionada: str
) -> str:
    """Gera texto do objeto da parceria."""
    
    tipo_nome = {
        TipoParceria.TERMO_COLABORACAO: "Termo de Colaboração",
        TipoParceria.TERMO_FOMENTO: "Termo de Fomento",
        TipoParceria.ACORDO_COOPERACAO: "Acordo de Cooperação"
    }
    
    return TEMPLATE_OBJETO.format(
        tipo_parceria=tipo_nome[tipo_parceria],
        titulo_projeto=titulo_projeto,
        objetivo_geral=objetivo_geral,
        beneficiarios=beneficiarios,
        area_abrangencia=area_abrangencia,
        duracao_meses=duracao_meses,
        politica_relacionada=politica_relacionada
    ).strip()

def gerar_justificativa(
    diagnostico_problema: str,
    necessidade_principal: str,
    justificativas: List[str],
    politicas: Dict[str, str],
    nome_osc: str,
    area_atuacao: str,
    quantidade_projetos: int,
    anos_experiencia: int,
    beneficiarios_historico: int,
    sroi_estimado: float,
    beneficiarios_diretos: int,
    impacto_multiplicador: int,
    tcs_projetados: int
) -> str:
    """Gera texto completo da justificativa."""
    
    # Preencher justificativas
    justificativa_1 = justificativas[0] if len(justificativas) > 0 else ""
    justificativa_2 = justificativas[1] if len(justificativas) > 1 else ""
    justificativa_3 = justificativas[2] if len(justificativas) > 2 else ""
    
    return TEMPLATE_JUSTIFICATIVA.format(
        diagnostico_problema=diagnostico_problema,
        necessidade_principal=necessidade_principal,
        justificativa_1=justificativa_1,
        justificativa_2=justificativa_2,
        justificativa_3=justificativa_3,
        politica_municipal=politicas.get("municipal", "Políticas municipais aplicáveis"),
        politica_estadual=politicas.get("estadual", "Políticas estaduais aplicáveis"),
        politica_federal=politicas.get("federal", "Políticas federais aplicáveis"),
        nome_osc=nome_osc,
        area_atuacao=area_atuacao,
        quantidade_projetos=quantidade_projetos,
        anos_experiencia=anos_experiencia,
        beneficiarios_historico=beneficiarios_historico,
        sroi_estimado=sroi_estimado,
        beneficiarios_diretos=beneficiarios_diretos,
        impacto_multiplicador=impacto_multiplicador,
        tcs_projetados=tcs_projetados
    ).strip()

def gerar_metas_indicadores(
    metas: List[Dict],
    tipo_projeto: str
) -> List[Meta]:
    """
    Gera lista de metas com indicadores baseado no tipo de projeto.
    
    Args:
        metas: Lista de dicts com descrição, valor_meta, prazo
        tipo_projeto: Tipo do projeto para sugerir indicadores
    
    Returns:
        Lista de objetos Meta
    """
    indicadores_sugeridos = {
        "educacao": {
            "indicador": "Taxa de aproveitamento/conclusão",
            "unidade": "percentual",
            "meio_verificacao": "Lista de presença e avaliações"
        },
        "qualificacao_profissional": {
            "indicador": "Taxa de inserção no mercado de trabalho",
            "unidade": "percentual",
            "meio_verificacao": "Registro de emprego/CTPS"
        },
        "meio_ambiente": {
            "indicador": "Área recuperada/plantada",
            "unidade": "hectares",
            "meio_verificacao": "Relatório técnico com georreferenciamento"
        },
        "assistencia_social": {
            "indicador": "Famílias atendidas com superação de vulnerabilidade",
            "unidade": "famílias",
            "meio_verificacao": "Prontuários SUAS e relatório social"
        },
        "saude": {
            "indicador": "Atendimentos realizados",
            "unidade": "atendimentos",
            "meio_verificacao": "Prontuários e registros de atendimento"
        }
    }
    
    sugestao = indicadores_sugeridos.get(tipo_projeto.lower(), {
        "indicador": "Meta alcançada",
        "unidade": "unidades",
        "meio_verificacao": "Relatório de execução"
    })
    
    metas_geradas = []
    for i, meta_dict in enumerate(metas, 1):
        meta = Meta(
            numero=i,
            descricao=meta_dict.get("descricao", f"Meta {i}"),
            indicador=meta_dict.get("indicador", sugestao["indicador"]),
            valor_meta=meta_dict.get("valor_meta", 100),
            unidade_medida=meta_dict.get("unidade", sugestao["unidade"]),
            meio_verificacao=meta_dict.get("meio_verificacao", sugestao["meio_verificacao"]),
            prazo_meses=meta_dict.get("prazo_meses", 12)
        )
        metas_geradas.append(meta)
    
    return metas_geradas

def gerar_orcamento_detalhado(
    valor_total: float,
    duracao_meses: int,
    tipo_projeto: str,
    equipe_necessaria: int = 3
) -> List[ItemOrcamento]:
    """
    Gera orçamento detalhado sugerido baseado no tipo de projeto.
    
    Args:
        valor_total: Valor total do projeto
        duracao_meses: Duração em meses
        tipo_projeto: Tipo do projeto
        equipe_necessaria: Número de profissionais
    
    Returns:
        Lista de itens de orçamento
    """
    itens = []
    
    # Distribuição típica de recursos (MROSC)
    # Pessoal: 40-60%, Material: 10-20%, Serviços: 15-25%, Outros: 10-20%
    
    valor_pessoal = valor_total * 0.50
    valor_material = valor_total * 0.15
    valor_servicos = valor_total * 0.20
    valor_outros = valor_total * 0.15
    
    # Pessoal
    salario_medio = valor_pessoal / equipe_necessaria / duracao_meses
    itens.append(ItemOrcamento(
        categoria="pessoal",
        descricao="Coordenador(a) do Projeto",
        unidade="mês",
        quantidade=duracao_meses,
        valor_unitario=salario_medio * 1.5,
        valor_total=salario_medio * 1.5 * duracao_meses,
        justificativa="Profissional responsável pela gestão geral do projeto"
    ))
    
    itens.append(ItemOrcamento(
        categoria="pessoal",
        descricao="Técnico(s) de referência",
        unidade="mês",
        quantidade=duracao_meses * (equipe_necessaria - 1),
        valor_unitario=salario_medio,
        valor_total=salario_medio * duracao_meses * (equipe_necessaria - 1),
        justificativa="Profissionais para execução das atividades"
    ))
    
    # Material de consumo
    itens.append(ItemOrcamento(
        categoria="material",
        descricao="Material de escritório e consumo",
        unidade="mês",
        quantidade=duracao_meses,
        valor_unitario=valor_material * 0.3 / duracao_meses,
        valor_total=valor_material * 0.3,
        justificativa="Insumos necessários para as atividades administrativas"
    ))
    
    itens.append(ItemOrcamento(
        categoria="material",
        descricao="Material específico para atividades",
        unidade="verba",
        quantidade=1,
        valor_unitario=valor_material * 0.7,
        valor_total=valor_material * 0.7,
        justificativa="Materiais específicos conforme plano de atividades"
    ))
    
    # Serviços de terceiros
    itens.append(ItemOrcamento(
        categoria="servicos",
        descricao="Serviços contábeis",
        unidade="mês",
        quantidade=duracao_meses,
        valor_unitario=valor_servicos * 0.2 / duracao_meses,
        valor_total=valor_servicos * 0.2,
        justificativa="Prestação de contas e contabilidade da parceria"
    ))
    
    itens.append(ItemOrcamento(
        categoria="servicos",
        descricao="Consultoria técnica especializada",
        unidade="serviço",
        quantidade=2,
        valor_unitario=valor_servicos * 0.4 / 2,
        valor_total=valor_servicos * 0.4,
        justificativa="Apoio técnico para qualificação das atividades"
    ))
    
    itens.append(ItemOrcamento(
        categoria="servicos",
        descricao="Comunicação e divulgação",
        unidade="verba",
        quantidade=1,
        valor_unitario=valor_servicos * 0.4,
        valor_total=valor_servicos * 0.4,
        justificativa="Materiais de comunicação e visibilidade do projeto"
    ))
    
    # Outros
    itens.append(ItemOrcamento(
        categoria="outros",
        descricao="Custos indiretos (até 15%)",
        unidade="verba",
        quantidade=1,
        valor_unitario=valor_outros,
        valor_total=valor_outros,
        justificativa="Custos administrativos conforme permitido pela Lei 13.019/2014"
    ))
    
    return itens

def gerar_plano_trabalho_completo(
    # Dados básicos
    titulo_projeto: str,
    osc: DadosOSC,
    tipo_parceria: TipoParceria,
    area_atuacao: AreaAtuacao,
    
    # Período
    data_inicio: date,
    duracao_meses: int,
    
    # Escopo
    objetivo_geral: str,
    justificativa_resumida: str,
    publico_alvo: str,
    beneficiarios_estimados: int,
    area_abrangencia: str,
    
    # Metas
    metas: List[Dict],
    
    # Financeiro
    valor_total: float,
    valor_contrapartida_bens: float = 0,
    
    # Equipe
    equipe_necessaria: int = 3,
    
    # Impacto VISIA
    sroi_estimado: float = 2.0,
    uisv_estimado: float = 10.0,
    tcs_projetados: int = 1000,
    
    # ODS
    ods_relacionados: List[int] = None
) -> PlanoTrabalho:
    """
    Gera plano de trabalho completo para parceria MROSC.
    """
    from datetime import timedelta
    
    # Calcular data fim
    data_fim = data_inicio + timedelta(days=duracao_meses * 30)
    
    # Gerar metas
    metas_geradas = gerar_metas_indicadores(metas, area_atuacao.value)
    
    # Gerar etapas baseadas nas metas
    etapas = []
    for i, meta in enumerate(metas_geradas, 1):
        etapa = Etapa(
            numero=i,
            descricao=f"Execução da {meta.descricao}",
            inicio_mes=1 if i == 1 else (i - 1) * (duracao_meses // len(metas_geradas)) + 1,
            fim_mes=i * (duracao_meses // len(metas_geradas)),
            responsavel="Coordenação do Projeto",
            recursos_necessarios=valor_total / len(metas_geradas)
        )
        etapas.append(etapa)
    
    # Gerar orçamento
    itens_orcamento = gerar_orcamento_detalhado(
        valor_total=valor_total,
        duracao_meses=duracao_meses,
        tipo_projeto=area_atuacao.value,
        equipe_necessaria=equipe_necessaria
    )
    
    # Gerar objeto
    objeto = gerar_objeto_parceria(
        tipo_parceria=tipo_parceria,
        titulo_projeto=titulo_projeto,
        objetivo_geral=objetivo_geral,
        beneficiarios=beneficiarios_estimados,
        area_abrangencia=area_abrangencia,
        duracao_meses=duracao_meses,
        politica_relacionada=area_atuacao.value.replace("_", " ").title()
    )
    
    return PlanoTrabalho(
        titulo_projeto=titulo_projeto,
        osc=osc,
        tipo_parceria=tipo_parceria,
        area_atuacao=area_atuacao,
        data_inicio=data_inicio,
        data_fim=data_fim,
        duracao_meses=duracao_meses,
        objeto=objeto,
        justificativa=justificativa_resumida,
        publico_alvo=publico_alvo,
        beneficiarios_estimados=beneficiarios_estimados,
        area_abrangencia=area_abrangencia,
        metas=metas_geradas,
        etapas=etapas,
        valor_total=valor_total,
        valor_osc=valor_contrapartida_bens,
        valor_parceiro=valor_total - valor_contrapartida_bens,
        itens_orcamento=itens_orcamento,
        impacto_esperado=f"SROI {sroi_estimado}, beneficiando {beneficiarios_estimados} pessoas diretamente",
        ods_relacionados=ods_relacionados or [],
        sroi_estimado=sroi_estimado,
        uisv_estimado=uisv_estimado,
        tcs_projetados=tcs_projetados
    )

# =============================================================================
# EXPORTAÇÃO
# =============================================================================

def exportar_plano_markdown(plano: PlanoTrabalho) -> str:
    """Exporta plano de trabalho em formato Markdown."""
    
    md = f"""# PLANO DE TRABALHO

## {plano.titulo_projeto}

---

## 1. IDENTIFICAÇÃO DA OSC

| Campo | Informação |
|-------|------------|
| Razão Social | {plano.osc.razao_social} |
| CNPJ | {plano.osc.cnpj} |
| Endereço | {plano.osc.endereco} |
| Cidade/UF | {plano.osc.cidade}/{plano.osc.uf} |
| Telefone | {plano.osc.telefone} |
| E-mail | {plano.osc.email} |
| Representante Legal | {plano.osc.representante_legal} |
| CPF | {plano.osc.cpf_representante} |
| Cargo | {plano.osc.cargo_representante} |

---

## 2. IDENTIFICAÇÃO DA PARCERIA

| Campo | Informação |
|-------|------------|
| Tipo de Parceria | {plano.tipo_parceria.value.replace('_', ' ').title()} |
| Área de Atuação | {plano.area_atuacao.value.replace('_', ' ').title()} |
| Data Início | {plano.data_inicio.strftime('%d/%m/%Y')} |
| Data Fim | {plano.data_fim.strftime('%d/%m/%Y')} |
| Duração | {plano.duracao_meses} meses |
| Valor Total | R$ {plano.valor_total:,.2f} |

---

## 3. OBJETO

{plano.objeto}

---

## 4. JUSTIFICATIVA

{plano.justificativa}

---

## 5. PÚBLICO-ALVO E BENEFICIÁRIOS

| Campo | Informação |
|-------|------------|
| Público-Alvo | {plano.publico_alvo} |
| Beneficiários Diretos | {plano.beneficiarios_estimados} |
| Área de Abrangência | {plano.area_abrangencia} |

---

## 6. METAS E INDICADORES

"""

    for meta in plano.metas:
        md += f"""
### Meta {meta.numero}: {meta.descricao}

| Aspecto | Descrição |
|---------|-----------|
| Indicador | {meta.indicador} |
| Valor da Meta | {meta.valor_meta} {meta.unidade_medida} |
| Meio de Verificação | {meta.meio_verificacao} |
| Prazo | {meta.prazo_meses} meses |

"""

    md += """
---

## 7. CRONOGRAMA DE EXECUÇÃO

| Etapa | Descrição | Início | Fim | Responsável |
|-------|-----------|--------|-----|-------------|
"""

    for etapa in plano.etapas:
        md += f"| {etapa.numero} | {etapa.descricao} | Mês {etapa.inicio_mes} | Mês {etapa.fim_mes} | {etapa.responsavel} |\n"

    md += """
---

## 8. ORÇAMENTO DETALHADO

| Categoria | Descrição | Qtd | Valor Unit. | Valor Total |
|-----------|-----------|-----|-------------|-------------|
"""

    total_orcamento = 0
    for item in plano.itens_orcamento:
        md += f"| {item.categoria.title()} | {item.descricao} | {item.quantidade} {item.unidade} | R$ {item.valor_unitario:,.2f} | R$ {item.valor_total:,.2f} |\n"
        total_orcamento += item.valor_total

    md += f"| **TOTAL** | | | | **R$ {total_orcamento:,.2f}** |\n"

    md += f"""
---

## 9. IMPACTO SOCIAL ESPERADO (Metodologia VISIA)

| Indicador | Valor |
|-----------|-------|
| SROI Estimado | {plano.sroi_estimado} |
| UISV (Unidade de Impacto Social VISIA) | {plano.uisv_estimado} |
| TCS Projetados | {plano.tcs_projetados} |
| ODS Relacionados | {', '.join([f'ODS {ods}' for ods in plano.ods_relacionados]) or 'A definir'} |

---

## 10. DECLARAÇÕES

Declaro que as informações prestadas são verdadeiras e que a OSC está apta a executar 
o objeto proposto, possuindo condições materiais e capacidade técnica e operacional para 
o desenvolvimento das atividades previstas.

Local e Data: _________________________, ___/___/_____

_____________________________________________
{plano.osc.representante_legal}
{plano.osc.cargo_representante}
{plano.osc.razao_social}

---

*Documento gerado pela metodologia VISIA - IBEDIS*
"""

    return md

# =============================================================================
# TESTES
# =============================================================================

if __name__ == "__main__":
    from datetime import date
    
    print("=" * 70)
    print("VISIA MROSC - Teste de Geração de Documentos")
    print("=" * 70)
    
    # Criar OSC de teste
    osc_teste = DadosOSC(
        razao_social="IBEDIS - Instituto Brasileiro de Educação e Desenvolvimento em Inovação Sustentável",
        cnpj="XX.XXX.XXX/0001-XX",
        endereco="Endereço da Sede",
        cidade="São Paulo",
        uf="SP",
        cep="00000-000",
        telefone="(11) 0000-0000",
        email="contato@ibedis.org.br",
        site="www.ibedis.org.br",
        data_fundacao=date(2020, 1, 1),
        representante_legal="Nome do Representante",
        cpf_representante="000.000.000-00",
        cargo_representante="Presidente",
        areas_atuacao=[AreaAtuacao.EDUCACAO, AreaAtuacao.MEIO_AMBIENTE, AreaAtuacao.TRABALHO_RENDA]
    )
    
    # Testar checklist
    print("\n📋 TESTE 1: Checklist de Elegibilidade")
    checklist = gerar_checklist_elegibilidade(osc_teste)
    print(f"   Conformidade: {checklist.percentual_conformidade():.1f}%")
    print(f"   Itens pendentes: {len(checklist.itens_pendentes())}")
    
    # Testar geração de plano
    print("\n📄 TESTE 2: Geração de Plano de Trabalho")
    
    metas_teste = [
        {"descricao": "Capacitar 100 jovens em competências digitais", "valor_meta": 100, "prazo_meses": 6},
        {"descricao": "Inserir 60% dos capacitados no mercado de trabalho", "valor_meta": 60, "prazo_meses": 12},
        {"descricao": "Acompanhar permanência no emprego por 6 meses", "valor_meta": 80, "prazo_meses": 18}
    ]
    
    plano = gerar_plano_trabalho_completo(
        titulo_projeto="Qualifica Futuro - Capacitação Digital para Jovens",
        osc=osc_teste,
        tipo_parceria=TipoParceria.TERMO_FOMENTO,
        area_atuacao=AreaAtuacao.TRABALHO_RENDA,
        data_inicio=date(2025, 3, 1),
        duracao_meses=18,
        objetivo_geral="capacitar jovens em situação de vulnerabilidade social em competências digitais para inserção no mercado de trabalho",
        justificativa_resumida="O projeto justifica-se pela alta taxa de desemprego juvenil e necessidade de qualificação profissional para a economia digital.",
        publico_alvo="Jovens de 16 a 29 anos em situação de vulnerabilidade social",
        beneficiarios_estimados=100,
        area_abrangencia="Município de São Paulo - Zona Sul",
        metas=metas_teste,
        valor_total=500000.00,
        valor_contrapartida_bens=50000.00,
        equipe_necessaria=4,
        sroi_estimado=3.5,
        uisv_estimado=15.0,
        tcs_projetados=4500,
        ods_relacionados=[1, 4, 8, 10]
    )
    
    print(f"   Projeto: {plano.titulo_projeto}")
    print(f"   Tipo: {plano.tipo_parceria.value}")
    print(f"   Valor: R$ {plano.valor_total:,.2f}")
    print(f"   Metas: {len(plano.metas)}")
    print(f"   Etapas: {len(plano.etapas)}")
    print(f"   Itens orçamento: {len(plano.itens_orcamento)}")
    
    # Exportar markdown
    print("\n📝 TESTE 3: Exportação Markdown")
    md_output = exportar_plano_markdown(plano)
    print(f"   Tamanho do documento: {len(md_output)} caracteres")
    print(f"   Primeiras linhas:")
    print("   " + "\n   ".join(md_output.split("\n")[:10]))
    
    print("\n✅ Todos os testes executados com sucesso!")
