# Decisões Metodológicas

Registro das decisões tomadas ao longo do projeto, com justificativa. Alterar qualquer item aqui requer confirmação explícita do usuário.

---

## D-01 — Série de PIB: usar Tabela 6613 (com ajuste sazonal)

**Decisão:** Usar o PIB real com ajuste sazonal (IBGE Tabela 6613), não a 6612 (sem ajuste).

**Motivo:** A Lei de Okun foca na relação entre o ciclo econômico e o desemprego cíclico. O ajuste sazonal remove flutuações previsíveis (ex: maior atividade no fim do ano), que o mercado de trabalho já antecipa. Usar a série ajustada isola o componente cíclico que é o verdadeiro objeto de análise. A comparação gráfica no `PIB.ipynb` confirmou o "padrão de serra" na série não ajustada.

---

## D-02 — Unificação das séries de desemprego: prioridade pela metodologia mais recente

**Decisão:** Nos períodos de sobreposição, prevalece: PNADc > PME Nova > PME Antiga.

**Motivo:** A metodologia mais recente é mais abrangente e representativa. A PME Nova ampliou a cobertura em 2002; a PNADc expandiu para cobertura nacional em 2012. Usar a série mais recente disponível garante consistência com as estimativas do Banco Central.

---

## D-03 — Trimestralização das séries mensais PME: média simples

**Decisão:** As séries mensais da PME Antiga e PME Nova foram convertidas para frequência trimestral pela média simples dos 3 meses.

**Motivo:** Abordagem preliminar padrão. **Ajuste pendente:** Revisar notas técnicas das 3 pesquisas para validar se média simples é o método adequado ou se ponderação por semanas do período é preferível.

---

## D-04 — Defasagem ótima: Lag 1 trimestre

**Decisão:** Os modelos de curto prazo usam crescimento do PIB defasado em 1 trimestre (Lag 1).

**Motivo:** Convergência de três evidências independentes:
1. Correlação cruzada mais forte no Lag 1 (r = −0.26, p = 0.005)
2. Teste de Causalidade de Granger mais significativo no Lag 1 (SSR F-test p = 0.0099)
3. AIC/BIC: BIC=0 foi rejeitado por contradizer a teoria (custos de ajuste do mercado de trabalho); AIC=6 foi rejeitado por overfitting (amsotra de ~115 obs)

---

## D-05 — Tratamento dos outliers identificados (1998-T1, 2002-T2, 2012-T1)

**Decisão:** Tratamento diferenciado por natureza do choque:
- **1998-T1**: interpolação linear (choque econômico real — Crise Asiática)
- **2002-T2**: pulse dummy (artefato metodológico — transição PME Antiga → PME Nova)
- **2012-T1**: pulse dummy (artefato metodológico — transição PME Nova → PNADc)

**Motivo:** A distinção é fundamental. 1998-T1 representa uma resposta econômica real do mercado de trabalho, porém deslocada temporalmente em relação à especificação de Lag 1 — a interpolação substitui o valor observado pelo esperado pela dinâmica do período. 2002-T2 e 2012-T1 são ruídos de medição causados pela troca de survey; a pulse dummy isola esses pontos sem distorcer os demais.

---

## D-06 — Modelo 1 final: Modelo C (Especificação da análise comparativa)

**Decisão:** Modelo C selecionado como especificação final do Modelo 1, dentre 4 alternativas testadas.

**Especificação:** `Δu_t = β₀ + β₁·crescimento_pib_{t-1} + δ₂·d_2002_t2 + δ₃·d_2012_t1 + ε_t` (com 1998-T1 interpolado)

**Motivo:** Menor AIC (214.8 vs 216.8 do Modelo A), aprovação no Jarque-Bera (p=0.607), coerência econômica no tratamento de 1998-T1. Coeficiente de Okun virtualmente idêntico ao Modelo A (−0.1728 vs −0.1729).

---

## D-07 — Step dummies descartadas no Modelo 1

**Decisão:** As step dummies de metodologia (PME Nova e PNADc) foram descartadas do Modelo 1.

**Motivo:** O modelo é estimado em primeira diferença (variação trimestral). Quebras de nível nas séries afetam apenas o trimestre exato da transição — já controlado pelas pulse dummies. As step dummies foram testadas e não apresentaram significância estatística, confirmando a expectativa teórica.

---

## D-08 — Filtro Hamilton (2018) como modelo principal no Modelo 2

**Decisão:** Filtro Hamilton (h=8, p=4) selecionado sobre HP (λ=1600) e CF (bandpass 6–32 tri.) para estimação do produto potencial.

**Motivo:** 
1. AIC substancialmente menor (441.8 vs 500.2 do HP — 58 pontos de diferença)
2. R² ajustado maior (0.349 vs 0.303)
3. Aprovação folgada no Jarque-Bera (p=0.276 vs p=0.057 marginal do HP)
4. Ausência do end-of-sample bias que afeta o HP nas últimas observações (2022-2024)
5. CF descartado por β₁ não significante (p=0.18)

---

## D-09 — Step dummies empilhadas no Modelo 2 (modelo de nível)

**Decisão:** `d_PMENova` permanece 1 mesmo após 2012 (quando `d_PNADc` entra como 1).

**Motivo:** Abordagem padrão de step dummies empilhadas para quebras sequenciais. Mantém a decomposição incremental: γ₁ captura o shift PME Antiga→PME Nova; γ₂ captura apenas o deslocamento adicional PME Nova→PNADc. Se d_PMENova voltasse a 0 em 2012, γ₂ representaria o shift total desde PME Antiga — algebricamente equivalente mas menos interpretável.

---

## D-10 — Correção HAC Newey-West (maxlags=4) em todos os modelos

**Decisão:** Todos os modelos são estimados com erros-padrão HAC (Heteroskedasticity and Autocorrelation Consistent), usando a correção de Newey-West com maxlags=4.

**Motivo:** Autocorrelação serial é detectada pelo Breusch-Godfrey em todos os modelos (esperada em séries temporais trimestrais de desemprego, que possui forte inércia). O HAC corrige os erros-padrão sem alterar os coeficientes estimados. maxlags=4 = 1 ano de dados trimestrais, seguindo heurística padrão da literatura.

---

## D-11 — Cointegração (Engle-Granger) validada para o Modelo 4

**Decisão:** O Modelo 4 (Elasticidade) é considerado válido, não espúrio, após confirmação de cointegração.

**Motivo:** Teste ADF nos resíduos da regressão em nível: estatística −3.5574 (p = 0.0004), rejeitando H₀ de raiz unitária nos resíduos. As variáveis são cointegradas — a relação de longo prazo entre ln_pib e u_t é genuína.

---

## D-12 — Amostra restrita até 2024-T4

**Decisão:** A amostra final foi truncada em dezembro de 2024 (2024-T4), descartando dados de 2025.

**Motivo:** A série de PIB disponível incluía projeções/dados incompletos de 2025. Para garantir a integridade da análise econométrica, apenas dados efetivamente realizados até 2024-T4 foram utilizados.
