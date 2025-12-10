# 📊 VISIA Platform

## Valoração Integrada de Sustentabilidade e Impacto Aplicado

Plataforma completa para análise de impacto de projetos públicos utilizando a metodologia **VISIA** - uma abordagem brasileira inovadora desenvolvida por **Wemerson Marinho** (ISBN: 978-65-01-58740-0).

---

## 🎯 Visão Geral

A **VISIA** é uma metodologia proprietária do **IBEDIS** que se diferencia de outras metodologias globais (SROI, IDH) por:

- ✅ **Integração Multidimensional**: Analisa 4 dimensões simultaneamente
- ✅ **Foco no Brasil**: Desenvolvida para o contexto brasileiro
- ✅ **Padronização**: Fórmulas replicáveis e consistentes
- ✅ **Transparência**: Ênfase em governança pública

---

## 📐 As 4 Dimensões VISIA

| Dimensão | Descrição | Indicadores-chave |
|----------|-----------|-------------------|
| 📚 **Educacional** | Impacto em educação e capacitação | Alunos, melhoria desempenho, empregabilidade |
| 💰 **Econômica** | Retorno financeiro e geração de renda | Empregos, renda média, microcréditos |
| 🌱 **Social-Ambiental** | Qualidade de vida e sustentabilidade | Beneficiários, créditos carbono |
| 🏛️ **Político-Pública** | Governança e captação de recursos | Gestores, transparência, investimentos |

---

## 🧮 Fórmulas (Fiéis ao Livro)

### Impacto Total
```
I_total = (I_educacional + I_econômico + I_soc-amb + I_político) / 4
```

### Classificação

| Score | Classificação | Recomendação |
|-------|---------------|--------------|
| ≥ 50% | 🥇 EXCELENTE | Aprovado - Expansão recomendada |
| ≥ 30% | 🥈 BOM | Aprovado com ressalvas |
| ≥ 15% | 🥉 REGULAR | Aprovado com ajustes |
| < 15% | ❌ INSUFICIENTE | Não recomendado |

---

## 🚀 Funcionalidades

### Para Usuários
- 📤 Upload de projetos (PDF, Word)
- 🤖 Extração automática de dados com IA
- 📊 Análise VISIA completa
- 📄 Relatórios e certificados
- 📈 Dashboard de projetos

### Para Administradores
- 👥 Gestão de usuários
- 🔑 Gerenciamento de API Keys
- 📜 Logs de auditoria
- ⚙️ Configurações do sistema
- 📊 Estatísticas de uso

### Para Auditores
- ✅ Validação de análises
- 📜 Rastreabilidade completa
- 🔍 Verificação de consistência

---

## 🔒 Segurança e Consistência

- **Hash de Verificação**: Cada análise gera um hash único
- **Mesmo documento = Mesma análise**: Garantia de consistência
- **Versionamento**: Histórico completo de alterações
- **Auditoria**: Todas ações são registradas

---

## 🛠️ Instalação

### Requisitos
- Python 3.9+
- pip

### Instalação Local

```bash
# Clone ou baixe o projeto
cd visia_platform

# Instale as dependências
pip install -r requirements.txt

# Execute
streamlit run app.py
```

### Deploy no Streamlit Cloud

1. Faça upload para GitHub
2. Conecte ao Streamlit Cloud
3. Configure:
   - Main file: `app.py`
   - Python version: 3.9+

---

## 📁 Estrutura do Projeto

```
visia_platform/
├── app.py                    # Interface principal Streamlit
├── requirements.txt          # Dependências
├── core/
│   ├── __init__.py
│   └── visia_engine.py       # Motor de cálculos VISIA
├── database/
│   ├── __init__.py
│   ├── visia_db.py           # Banco de dados SQLite
│   └── reference_data.py     # Dados de referência
├── services/
│   ├── __init__.py
│   └── ai_extractor.py       # Extrator de PDFs/Word
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
└── uploads/
```

---

## 🔑 API (Em Desenvolvimento)

### Autenticação
```python
headers = {
    "Authorization": "Bearer visia_sua_api_key_aqui"
}
```

### Endpoints

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/v1/analise` | POST | Nova análise VISIA |
| `/api/v1/projeto/{id}` | GET | Detalhes do projeto |
| `/api/v1/projetos` | GET | Lista projetos |

---

## 👤 Credenciais Padrão

⚠️ **ALTERE EM PRODUÇÃO!**

| Tipo | Email | Senha |
|------|-------|-------|
| Admin | admin@visia.ibedis.org.br | admin123 |

---

## 📚 Referências

- Livro: "VISIA: Uma Nova Abordagem Brasileira para Mensuração de Impacto no Setor Público"
- Autor: Wemerson Marinho
- ISBN: 978-65-01-58740-0
- Instituição: IBEDIS

---

## 📄 Licença

Este software implementa a metodologia VISIA, propriedade intelectual do IBEDIS.
Uso comercial requer autorização prévia.

---

## 📞 Contato

**IBEDIS** - Instituto Brasileiro de Desenvolvimento, Inovação e Sustentabilidade

📧 contato@ibedis.org.br
🌐 www.ibedis.org.br

---

*Desenvolvido com ❤️ para transformar a gestão pública brasileira*
