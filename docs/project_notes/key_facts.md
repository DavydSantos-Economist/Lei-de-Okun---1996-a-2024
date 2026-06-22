# Constantes e Fatos Críticos

Valores numéricos fixados, resultados obtidos e parâmetros que não devem ser alterados sem re-execução do notebook correspondente.

---

## Amostra e Período

| Parâmetro | Valor |
|---|---|
| Cobertura total | 1996-T1 a 2024-T4 |
| Frequência | Trimestral |
| **Modelo 1 (Δu_t)** | 1996-T3 a 2024-T4 — **114 observações** |
| **Modelo 2 (hiato Hamilton)** | 1996-T2 a 2024-T4 — **105 observações** |
| **Modelo 3 (hiato FGV)** | 1996-T1 a 2024-T4 — **116 observações** |
| **Modelo 4 (elasticidade)** | 1996-T1 a 2024-T4 — **116 observações** |

---

## Séries de Dados

| Variável | Descrição | Fonte |
|---|---|---|
| `u_t` | Taxa de desemprego unificada (% PEA) | PME Antiga + PME Nova + PNADc |
| `ln_pib` | Log natural do PIB real dessazonalizado | IBGE Tabela 6613 |
| `delta_u_t` | Variação trimestral: u_t − u_{t-1} | Derivada de u_t |
| `crescimento_pib` | (ln_pib_t − ln_pib_{t-1}) × 100 | Derivada de ln_pib |
| `hiato_hp` | Ciclo extraído pelo filtro HP (λ=1600) | Calculado sobre ln_pib |
| `hiato_hamilton` | Ciclo extraído pelo filtro Hamilton (h=8, p=4) | Calculado sobre ln_pib |
| `hiato_cf` | Ciclo extraído pelo filtro CF (bandpass 6–32 tri.) | Calculado sobre ln_pib |
| `hiato_fgv` | Hiato do produto FGV/IBRE | `dados/hiato_do_pib_3t25_final_FGV.xlsx` |

---

## Testes de Raiz Unitária (ADF e KPSS, período 1996-2024)

| Variável | ADF (estatística) | ADF (p-valor) | KPSS (p-valor) | Conclusão |
|---|:---:|:---:|:---:|---|
| `ln_pib` (nível) | -1.3073 | 0.6258 | 0.0100 | **I(1)** |
| `u_t` (nível) | -2.1186 | 0.2371 | 0.1000 | **I(1)** por convenção* |
| `crescimento_pib` (1ª dif.) | -8.6429 | 0.0000 | 0.1000 | **I(0)** |
| `delta_u_t` (1ª dif.) | -4.6522 | 0.0001 | 0.1000 | **I(0)** |

*u_t apresenta resultado ambíguo nos testes em nível; tratada como I(1) pela teoria econômica e pelo padrão da literatura.

---

## Outliers Identificados (resíduos padronizados |Z| > 2.0)

| Trimestre | Δu_t observado | Crescimento PIB (Lag 1) | Z-score | Natureza |
|---|:---:|:---:|:---:|---|
| **1998-T1** | +2.57 p.p. | +0.84% | 3.14 | Choque econômico real (Crise Asiática/Russa) |
| **2002-T2** | +4.31 p.p. | +2.46% | 5.53 | Artefato metodológico (transição PME Antiga → PME Nova) |
| **2012-T1** | +2.80 p.p. | +0.93% | 3.43 | Artefato metodológico (transição PME Nova → PNADc) |

Teste de Chow aplicado nas três datas: nenhum gerou quebra estrutural nos parâmetros (p-valores: 0.47, 0.75 e 0.94 respectivamente).

---

## Modelo 1 — Primeira Diferença (Modelo C Final)

**Equação:** `Δu_t = β₀ + β₁·crescimento_pib_{t-1} + δ₂·d_2002_t2 + δ₃·d_2012_t1 + ε_t`
(série Δu_t com 1998-T1 substituído por interpolação linear)

| Parâmetro | Coeficiente | P-valor |
|---|:---:|:---:|
| β₁ (coef. Okun) | **−0.1728** | < 0.001 |
| β₀ (constante) | +0.0071 | 0.914 (n.s.) |
| δ₂ (dummy 2002-T2) | +4.7307 | < 0.001 |
| δ₃ (dummy 2012-T1) | +2.9539 | < 0.001 |

- **R² Ajustado:** 0.455
- **Jarque-Bera:** p = 0.607 ✓
- **Breusch-Godfrey:** autocorrelação presente — corrigido com HAC
- **White:** p = 0.812 ✓
- **Taxa neutra de crescimento:** ~0.04% ao trimestre (~0.16% ao ano)

**Interpretação:** Para cada 1 p.p. de crescimento do PIB em t, a taxa de desemprego cai **0.17 p.p.** em t+1.

---

## Modelo 2 — Hiato do Produto (Filtro Hamilton, selecionado)

**Equação:** `u_t = β₀ + β₁·hiato_hamilton + γ₁·D_PMENova + γ₂·D_PNADc + ε_t`

| Parâmetro | Coeficiente | P-valor |
|---|:---:|:---:|
| β₁ (coef. Okun) | **−0.3168** | < 0.001 |
| β₀ (constante) | +6.6331 | < 0.001 |
| γ₁ (step PME Nova) | +3.2726 | < 0.001 |
| γ₂ (step PNADc) | −0.1783 | 0.829 (n.s.) |

- **R² Ajustado:** 0.349 | **AIC:** 441.8 | **BIC:** 452.4
- **Jarque-Bera:** p = 0.276 ✓ | **White:** p = 0.001 ✗ (HAC corrige)

**NAIRU Implícita (Hamilton):**

| Período | NAIRU |
|---|:---:|
| PME Antiga (pré-2002) | **6.63%** |
| PME Nova (2002–2012) | **9.91%** |
| PNADc (pós-2012) | **9.73%** |

---

## Modelo 2 — Hiato HP (referência comparativa)

| Parâmetro | Coeficiente | P-valor |
|---|:---:|:---:|
| β₁ (coef. Okun) | **−0.5038** | < 0.001 |
| β₀ | +7.2481 | < 0.001 |
| γ₁ | +1.8970 | 0.009 |
| γ₂ | +0.8949 | 0.306 (n.s.) |

- **R² Ajustado:** 0.303 | **AIC:** 500.2 | **Jarque-Bera:** p = 0.057 ✓ (marginal)

---

## Modelo 3 — Hiato FGV/IBRE (referência comparativa)

**Equação:** mesma estrutura do Modelo 2, substituindo hiato_hamilton por hiato_fgv.

| Parâmetro | Coeficiente | P-valor |
|---|:---:|:---:|
| β₁ (coef. Okun) | **−0.4714** | < 0.001 |
| β₀ | +7.2563 | < 0.001 |
| γ₁ (step PME Nova) | +2.2591 | < 0.001 |
| γ₂ (step PNADc) | −0.4643 | 0.499 (n.s.) |

- **R² Ajustado:** 0.552 | **AIC:** 449.0 | N = 116 obs.
- **Jarque-Bera:** p = 0.007 ✗ — não-normalidade; coeficientes OLS válidos por TLC (n=116)

**NAIRU Implícita (FGV):** PME Antiga: 7.26% | PME Nova: 9.52% | PNADc: 9.05%

---

## Modelo 4 — Elasticidade do Produto

**Equação:** `ln_pib_t = β₀ + β₁·t + β₂·u_t + γ₁·D_PMENova + γ₂·D_PNADc + ε_t`

| Parâmetro | Coeficiente | P-valor |
|---|:---:|:---:|
| β₀ (constante) | 12.2424 | < 0.001 |
| β₁ (tendência) | 0.003988 | < 0.001 |
| β₂ (elasticidade Okun) | **−0.0195** | < 0.001 |
| γ₁ (step PME Nova) | 0.1590 | < 0.001 |
| γ₂ (step PNADc) | 0.0596 | 0.030 |

- **R² Ajustado:** 0.967 | **AIC:** −434.52 | N = 116 obs.
- **Durbin-Watson:** 0.425 (ativa sinal de alerta — validado por cointegração)
- **Cointegração (Engle-Granger):** ADF nos resíduos = −3.5574, **p = 0.0004** ✓
- **Jarque-Bera:** p = 0.005 ✗ (assimetria leve −0.72; inferência assintótica válida com n=116)
- **Tendência implícita:** 0.40% ao trimestre = **1.60% ao ano** de crescimento potencial

**Interpretação:** Um aumento de 1 p.p. no desemprego está associado a uma **redução de 1.95% no PIB** no longo prazo (ceteris paribus).

---

## Quadro Comparativo — Coeficiente de Okun

| Modelo | Especificação | β Okun | Dimensão | Status |
|---|---|:---:|---|---|
| **Modelo 1 ★** | Primeira diferença (Modelo C) | **−0.1728** | Curto prazo | Final |
| Modelo 2a | Nível — Hiato HP | −0.5038 | Longo prazo | Referência |
| **Modelo 2b ★** | Nível — Hiato Hamilton | **−0.3168** | Longo prazo | Final |
| Modelo 3 | Nível — Hiato FGV/IBRE | −0.4714 | Longo prazo | Ref. comparativa |
| Modelo 4 | Elasticidade (ln_pib ~ u_t) | −0.0195 (log) | Longo prazo | Final |

**Intervalo de robustez (modelos de longo prazo selecionados):** −0.317 a −0.471

---

## Parâmetros dos Filtros

| Filtro | Parâmetros |
|---|---|
| Hodrick-Prescott | λ = 1600 (padrão para dados trimestrais) |
| Hamilton (2018) | h = 8 trimestres, p = 4 defasagens |
| Christiano-Fitzgerald | Bandpass: 6 a 32 trimestres |
