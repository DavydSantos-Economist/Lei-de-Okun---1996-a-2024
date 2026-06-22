# Fundamentação Teórica

Conceitos econômicos e econométricos que embasam as escolhas metodológicas do projeto. Inclui referências bibliográficas relevantes.

---

## A Lei de Okun

**Referência original:** Okun, A. M. (1962). *Potential GNP: Its Measurement and Significance*. Proceedings of the Business and Economic Statistics Section. American Statistical Association.

Okun (1962) documentou empiricamente uma relação negativa estável entre variações no produto e variações no desemprego nos EUA. A regra empírica original sugeria que para cada 1% de crescimento do PIB acima do potencial, o desemprego cai ~0.3 p.p.

### Três Especificações Originais de Okun (1962)

1. **Modelo de Primeira Diferença**: `Δu_t = α + β · Δln_pib_t + ε_t`
   - Captura a relação de **curto prazo** (trimestral) entre variações no produto e no desemprego
   - Variáveis em primeira diferença: I(0) → sem risco de regressão espúria

2. **Modelo de Hiato do Produto**: `u_t = α + β · hiato_t + ε_t`
   - Captura a relação de **longo prazo** entre o nível do desemprego e o desvio do produto do seu potencial
   - Requer estimação do produto potencial (via filtros ou modelos estruturais)

3. **Modelo de Elasticidade (Tendência Ajustada)**: `ln_pib_t = α + β₁·t + β₂·u_t + ε_t`
   - Especificação direta da relação produto-desemprego em nível com tendência determinística
   - Requer verificação de cointegração para validar relação de longo prazo

A literatura brasileira contemporânea concentrou-se quase exclusivamente na abordagem de Hiato (com Filtro HP), negligenciando as demais especificações. Este TCC recupera a triangulação original de Okun.

### Resultados Esperados pela Literatura Internacional

- Coeficiente de curto prazo (primeira diferença): tipicamente **−0.3 a −0.5** p.p. de Δu por 1% de crescimento em economias desenvolvidas
- Coeficiente de longo prazo (nível): maior em valor absoluto que o de curto prazo
- Brasil apresenta coeficientes menores que economias desenvolvidas, refletindo maior rigidez e lentidão de ajuste

---

## NAIRU — Taxa de Desemprego que Não Acelera a Inflação

**Referências fundamentais:**
- Friedman, M. (1968). The Role of Monetary Policy. *American Economic Review*, 58(1), 1–17.
- Phelps, E. S. (1968). Money-Wage Dynamics and Labor-Market Equilibrium. *Journal of Political Economy*, 76(4), 678–711.

A NAIRU é o nível de desemprego compatível com inflação estável. Abaixo da NAIRU, pressões inflacionárias emergem; acima, pressões deflacionárias. Friedman denominou este conceito de *taxa natural de desemprego*.

**Derivação neste TCC:** A NAIRU é extraída diretamente dos interceptos das regressões de nível, fazendo hiato = 0:
- `NAIRU_PME_Antiga = β₀`
- `NAIRU_PME_Nova = β₀ + γ₁`
- `NAIRU_PNADc = β₀ + γ₁ + γ₂`

**Fatores estruturais da NAIRU elevada no Brasil:**
1. Custos de demissão (FGTS + multa 40% + aviso prévio proporcional)
2. Segmentação formal-informal (~40% de informalidade na PNADc)
3. Baixa mobilidade geográfica e setorial
4. Efeitos de histerese após recessão 2015-2019 (*scarring effect*)

---

## Filtros de Extração do Ciclo Econômico

### Hodrick-Prescott (HP)
**Referência:** Hodrick, R. J., & Prescott, E. C. (1997). Postwar U.S. Business Cycles: An Empirical Investigation. *Journal of Money, Credit and Banking*, 29(1), 1–16.

Minimiza a soma de uma penalidade pela variação da tendência e do desvio da série em relação à tendência. Para dados trimestrais, λ = 1600 é o valor padrão da literatura.

**Crítica principal (end-of-sample bias):** Por ser um estimador de médias móveis simétricas, o HP carece de observações futuras nas últimas datas da amostra, gerando estimativas de tendência distorcidas. Hamilton (2018) documenta matematicamente esse problema.

### Filtro de Hamilton (2018)
**Referência:** Hamilton, J. D. (2018). Why You Should Never Use the Hodrick-Prescott Filter. *Review of Economics and Statistics*, 100(5), 831–843.

Propõe a projeção de $y_t$ sobre $[1, y_{t-h}, y_{t-h+1}, \ldots, y_{t-h+p-1}]$ via OLS. O resíduo dessa regressão é o componente cíclico. Para dados trimestrais, recomenda h=8 (2 anos) e p=4 (4 defasagens).

**Vantagens sobre HP:**
- Sem end-of-sample bias (usa apenas observações passadas)
- Componente cíclico resultante é estacionário por construção
- Evita a correlação serial espúria que o HP introduz no ciclo estimado

**Parâmetros usados neste TCC:** h=8, p=4.

### Filtro Christiano-Fitzgerald (CF)
**Referência:** Christiano, L. J., & Fitzgerald, T. J. (2003). The Band Pass Filter. *International Economic Review*, 44(2), 435–465.

Filtro passa-banda assimétrico que extrai componentes com periodicidade entre 6 e 32 trimestres (1.5 a 8 anos). Preserva todas as observações (diferença do Baxter-King, que perde k observações nas extremidades).

**Resultado neste TCC:** CF descartado — β₁ não significante (p=0.18), falha marginal no JB.

---

## Séries Temporais e Estacionariedade

### Processo I(1) — Integrado de Ordem 1
Uma série é I(1) se possui raiz unitária em nível (não-estacionária) mas sua primeira diferença é I(0) (estacionária). Regressões entre variáveis I(1) em nível podem ser espúrias (Granger & Newbold, 1974).

**Referências:**
- Granger, C. W. J., & Newbold, P. (1974). Spurious Regressions in Econometrics. *Journal of Econometrics*, 2(2), 111–120.

### Teste ADF (Augmented Dickey-Fuller)
Testa H₀: raiz unitária presente (série não-estacionária). Rejeitar H₀ → série estacionária.

### Teste KPSS (Kwiatkowski-Phillips-Schmidt-Shin)
Testa H₀: série estacionária. Rejeitar H₀ → série não-estacionária. Complementar ao ADF: quando os dois discordam, prevalece a interpretação teórica.

---

## Cointegração

**Referência fundamental:** Engle, R. F., & Granger, C. W. J. (1987). Co-Integration and Error Correction: Representation, Estimation, and Testing. *Econometrica*, 55(2), 251–276.

Variáveis I(1) são cointegradas quando existe uma combinação linear entre elas que é I(0). Isso implica uma relação de equilíbrio de longo prazo genuína — não espúria.

**Procedimento de Engle-Granger (2 etapas):**
1. Estimar a regressão em nível (OLS) e salvar os resíduos
2. Aplicar teste ADF nos resíduos (sem constante): se os resíduos são I(0) → cointegração confirmada

**Resultado no Modelo 4:** ADF nos resíduos = −3.5574, p = 0.0004 → cointegração confirmada.

### Modelo de Correção de Erros (ECM)
**Referência:** Engle & Granger (1987), citado acima.

Quando variáveis são cointegradas, a dinâmica de curto prazo pode ser modelada como:
`Δy_t = α₀ + α₁·Δx_t + λ·ε̂_{t-1} + ν_t`

Onde λ (velocidade de ajuste, −1 < λ < 0) mede a fração do desvio do equilíbrio corrigida a cada período.

**Status:** Pendente de implementação (ver issues.md).

---

## Testes Diagnósticos

### Jarque-Bera (JB)
Testa normalidade dos resíduos com base em assimetria e curtose. H₀: resíduos normais. **Deseja-se não rejeitar H₀** (p > 0.05) para que testes t/F em amostras finitas sejam válidos.

**Referência:** Jarque, C. M., & Bera, A. K. (1980). Efficient Tests for Normality, Homoscedasticity and Serial Independence of Regression Residuals. *Economics Letters*, 6(3), 255–259.

### Breusch-Godfrey (BG)
Testa autocorrelação serial nos resíduos até ordem p. Preferível ao Durbin-Watson quando há variáveis defasadas como regressores.

**Referência:** Godfrey, L. G. (1978). Testing Against General Autoregressive and Moving Average Error Models When the Regressors Include Lagged Dependent Variables. *Econometrica*, 46(6), 1293–1301.

### Teste de White
Testa heterocedasticidade sem assumir forma funcional específica. H₀: resíduos homocedásticos.

**Referência:** White, H. (1980). A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity. *Econometrica*, 48(4), 817–838.

### Correção HAC (Newey-West)
Fornece erros-padrão consistentes na presença de autocorrelação e heterocedasticidade, sem alterar os coeficientes estimados. Usado em todos os modelos com maxlags=4.

**Referência:** Newey, W. K., & West, K. D. (1987). A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix. *Econometrica*, 55(3), 703–708.

### Teste de Chow
Testa estabilidade dos parâmetros de uma regressão em torno de uma data específica. H₀: parâmetros estáveis.

**Referência:** Chow, G. C. (1960). Tests of Equality Between Sets of Coefficients in Two Linear Regressions. *Econometrica*, 28(3), 591–605.

---

## Causalidade de Granger

**Referência:** Granger, C. W. J. (1969). Investigating Causal Relations by Econometric Models and Cross-spectral Methods. *Econometrica*, 37(3), 424–438.

X causa Granger Y se os valores passados de X ajudam a prever Y além do que os valores passados de Y sozinhos fariam.

**Resultado neste TCC:** Causalidade unidirecional PIB → Desemprego confirmada. Desemprego não causa Granger PIB (p > 0.27 para todos os lags). Isso valida o crescimento do PIB como variável explicativa nos modelos OLS, reduzindo preocupações com endogeneidade simultânea.

---

## Rigidez do Mercado de Trabalho (Justificativa do Lag)

A defasagem de 1 trimestre entre variações do PIB e variações do desemprego é explicada por:

1. **Custos de ajuste** (*adjustment costs*): contratar e demitir é caro — multas rescisórias, treinamento, risco processual
2. **Incerteza** (*uncertainty*): firmas aguardam confirmar se a variação na demanda é permanente antes de ajustar o emprego
3. **Hoarding de mão de obra** (*labor hoarding*): em recessões curtas, firmas mantêm trabalhadores qualificados para evitar custos futuros de re-contratação

Esses mecanismos fazem o mercado de trabalho ser um *lagging indicator* do ciclo econômico.

---

## Histerese no Mercado de Trabalho

**Conceito:** Períodos prolongados de alto desemprego podem elevar permanentemente a NAIRU (efeito *scarring*):
- Trabalhadores desempregados por longo tempo perdem capital humano
- Empregadores usam o tempo de desemprego como sinal negativo de produtividade
- Redução da mobilidade e do capital de busca

**Relevância no Brasil:** A recessão 2015-2019 (desemprego de pico ~14% em 2017) é candidata a ter gerado efeitos de histerese, sustentando a NAIRU elevada mesmo após a recuperação pós-2020.
