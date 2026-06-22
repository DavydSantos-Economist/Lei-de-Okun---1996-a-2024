# AI Coding Agents Configuration — TCC: Lei de Okun no Brasil (UFRPE)

Instruções para assistentes de IA ao trabalhar neste projeto.

---

## Contexto do Projeto

**TCC de Economia** — análise econométrica da **Lei de Okun para o Brasil**, cobrindo o período 1996-T1 a 2024-T4 (dados trimestrais).

O objetivo é estimar a relação entre crescimento do PIB e variação do desemprego via quatro especificações:
1. **Modelo 1** — Primeira Diferença (curto prazo)
2. **Modelo 2** — Hiato do Produto por filtros estatísticos (HP, Hamilton, CF)
3. **Modelo 3** — Hiato FGV/IBRE (função de produção)
4. **Modelo 4** — Elasticidade do Produto (tendência ajustada + cointegração)

Toda a lógica econométrica e resultados obtidos estão em `docs/documentacao_econometrica.md`.
Decisões metodológicas consolidadas ficam em `docs/project_notes/decisions.md`.

---

## Estrutura de Pastas

```
Dados/                                     ← raiz do git repo
├── AGENTS.md                              ← este arquivo
├── dados/                                 ← dados brutos e intermediários (não modificar xlsx/pkl originais)
│   ├── Desemprego.xlsx                    ← séries PME Antiga, PME Nova e PNADc
│   ├── Tabela 6613 - com ajuste sazonal.xlsx  ← PIB real dessazonalizado (IBGE)
│   ├── Tabela 6612 - sem ajuste sazonal.xlsx  ← PIB sem ajuste (referência, não usado nos modelos)
│   ├── hiato_do_pib_3t25_final_FGV.xlsx   ← hiato FGV/IBRE (1982-T3 a 2025-T3)
│   ├── desemprego_tratado.pkl / .csv      ← série unificada gerada por Desemprego.ipynb
│   └── pib_tratado.pkl / .csv             ← ln_pib gerado por PIB.ipynb
├── notebooks/
│   ├── Desemprego.ipynb                   ← tratamento e unificação das séries de desemprego (concluído)
│   ├── PIB.ipynb                          ← tratamento do PIB, criação de ln_pib (concluído)
│   ├── Tratamento econonometrico.ipynb    ← integração dos dados, testes ADF/KPSS/Granger (concluído)
│   ├── 1.modelo de primeira diferença.ipynb  ← Modelo 1 (concluído)
│   ├── 2.modelo de hiato.ipynb            ← Modelo 2 — HP, Hamilton, CF (concluído)
│   ├── 3.modelo de hiato FGV.ipynb        ← Modelo 3 — FGV/IBRE (concluído)
│   └── 4.modelo de elasticidade.ipynb     ← Modelo 4 (concluído; extensões pendentes)
├── figuras/
│   ├── fase1_tratamento/                  ← fig_01 a fig_06
│   ├── fase2_modelo1/                     ← fig_07 a fig_09b
│   ├── fase3_modelo2/                     ← fig_10 a fig_16
│   └── fase4_modelo4/                     ← fig_17 a fig_20
└── docs/
    ├── documentacao_econometrica.md       ← documentação principal (fonte da verdade)
    ├── bugs.md                            ← bugs ativos
    └── project_notes/                     ← memória institucional do projeto
        ├── decisions.md                   ← decisões metodológicas e seus motivos
        ├── key_facts.md                   ← constantes numéricas, resultados, parâmetros fixados
        ├── issues.md                      ← tarefas concluídas e pendentes
        └── theory.md                      ← conceitos teóricos e referências bibliográficas
```

---

## Guardrails

- **Nunca sobrescrever** os arquivos `.xlsx` em `dados/` — são os dados originais coletados
- **Nunca sobrescrever** os arquivos `.pkl` sem re-executar o notebook que os gera (eles são outputs intermediários)
- Ao editar notebooks, usar a ferramenta `NotebookEdit` do Claude Code (edição direta é segura e preferível a gerar blocos para copiar)
- Novas figuras seguem a convenção `fig_{NN}_{descricao}.png` dentro da subpasta de fase correspondente
- Toda alteração metodológica relevante deve ser documentada em `docs/project_notes/decisions.md`
- A documentação principal (`docs/documentacao_econometrica.md`) é a fonte da verdade — manter sempre atualizada com resultados finais

---

## Fontes de Dados

| Arquivo | Fonte | Conteúdo |
|---|---|---|
| `Desemprego.xlsx` | IBGE (PME / PNADc) | 3 séries de desemprego: PME Antiga, PME Nova, PNADc |
| `Tabela 6613 - com ajuste sazonal.xlsx` | IBGE SIDRA Tab. 6613 | PIB real trimestral dessazonalizado (R$ milhões encadeados, ref. 1995) |
| `Tabela 6612 - sem ajuste sazonal.xlsx` | IBGE SIDRA Tab. 6612 | PIB real sem ajuste sazonal (referência, não usado nos modelos) |
| `hiato_do_pib_3t25_final_FGV.xlsx` | FGV/IBRE | Hiato do produto por função de produção, 1982-T3 a 2025-T3 |

---

## Padrão de Nomeação

| Tipo | Padrão | Exemplo |
|---|---|---|
| Figuras | `fig_{NN}_{descricao}.png` | `fig_07c_modelo_C.png` |
| Figuras por fase | Subpasta `figuras/fase{N}_{nome}/` | `figuras/fase2_modelo1/` |
| Notebooks | `{N}.{descricao}.ipynb` | `1.modelo de primeira diferença.ipynb` |
| Dados intermediários | `{variavel}_tratado.{ext}` | `desemprego_tratado.pkl` |

---

## Escalation Rules (Requer Confirmação)

O agente DEVE pausar e pedir confirmação antes de:

- Alterar metodologia de cálculo documentada em `docs/project_notes/decisions.md`
- Sobrescrever qualquer arquivo `.xlsx` em `dados/`
- Instalar dependências Python além de: `pandas`, `numpy`, `matplotlib`, `seaborn`, `statsmodels`, `scipy`
- Mudar a especificação final de qualquer modelo já validado (Modelos 1, 2, 3, 4)
- Enviar ou compartilhar dados ou figuras fora do ambiente local

---

## Status dos Modelos

| Modelo | Notebook | Status | Modelo Selecionado |
|---|---|---|---|
| Fase 1 — Tratamento | `Tratamento econonometrico.ipynb` | ✅ Concluído | — |
| Modelo 1 — Primeira Diferença | `1.modelo de primeira diferença.ipynb` | ✅ Concluído | Modelo C (interpolação 1998-T1 + pulse dummies) |
| Modelo 2 — Hiato Estatístico | `2.modelo de hiato.ipynb` | ✅ Concluído | Filtro Hamilton (2018) |
| Modelo 3 — Hiato FGV | `3.modelo de hiato FGV.ipynb` | ✅ Concluído | Referência comparativa |
| Modelo 4 — Elasticidade | `4.modelo de elasticidade.ipynb` | ✅ Base concluída | Extensões pendentes (ver issues) |
| Fase 5 — Síntese Final | — | ⏳ Pendente | — |

---

## Próximos Passos (ordem de prioridade)

### 1. Extensões do Modelo 4
- Implementar quebras estruturais na tendência (*trend breaks*) para 2015-T1 e 2020-T2
- Re-estimar cointegração (Engle-Granger) nos novos resíduos
- Implementar o Modelo de Correção de Erros (ECM) para estimar velocidade de ajuste λ

### 2. Ajuste pendente na trimestralização do desemprego
- Revisar as notas técnicas das 3 pesquisas (PME Antiga, PME Nova, PNADc) para validar se média simples é a melhor forma de trimestralizar as séries mensais da PME

### 3. Dados de informalidade (Ipeadata)
- Coletar série de informalidade do Ipeadata para enriquecer a análise das inversões históricas (Seção 1.6.1)

### 4. Fase 5 — Análise Comparativa e Conclusões
- Construir quadro comparativo final (todos os modelos)
- Redigir texto das conclusões

### 5. Redigir o texto do TCC
- Introdução, Revisão de Literatura, Metodologia, Resultados, Conclusão

---

## Configuração do Ambiente Python

```bash
pip install pandas numpy matplotlib seaborn statsmodels scipy openpyxl
```

Não há banco de dados nem credenciais envolvidas.
