---
### **Observações para a IA (Instruções do Projeto)**

**LEIA ANTES DE PROSSEGUIR:** Estas são as diretrizes para trabalhar neste projeto.

1.  **NÃO EDITAR NOTEBOOKS DIRETAMENTE:** Nunca modifique os arquivos `.ipynb` (como `Desemprego.ipynb`, `PIB.ipynb`, etc.) usando as ferramentas de edição de arquivo. A edição direta pela IA está corrompendo os arquivos. Em vez disso, **gere o código Python em blocos de código**, e o usuário irá copiá-lo e colá-lo no notebook correspondente.

2.  **FOCO NA DOCUMENTAÇÃO ECONÔMICA:** O objetivo final é um TCC. Ao atualizar este arquivo (`documentacao_econometrica.md`), a prioridade é detalhar a **lógica econômica e estatística** por trás de cada etapa. Explique *por que* uma técnica foi escolhida (ex: *por que usar o filtro HP?*), *qual a interpretação econômica* dos resultados e *quais as hipóteses* sendo testadas. Os detalhes da implementação do código são secundários; o "porquê" é essencial.

3.  **ESTRUTURA MODULAR:** O trabalho está organizado em partes, com um notebook para cada grande etapa:
    *   `Desemprego.ipynb`: Tratamento dos dados de desemprego (concluído).
    *   `PIB.ipynb`: Tratamento dos dados do PIB (em andamento).
    *   Futuros notebooks para cada modelo econométrico (Modelo 1, Modelo 2, etc.).

---

# Documentação do Processo Econométrico: Análise da Lei de Okun para o Brasil (Estrutura Vertical)

Este documento detalha o passo a passo para a análise econométrica da Lei de Okun, utilizando dados brasileiros. A estrutura segue uma abordagem "vertical", onde cada modelo é analisado do início ao fim em sua própria seção.

---

## Fase 1: Preparação dos Dados e Análise Preliminar (Etapas Comuns)

Esta fase inicial é comum a todos os modelos e prepara as variáveis que serão utilizadas na análise.

### 1.1 Tratamento e Unificação dos Dados

1.  **Série de Desemprego:**
    *   Carregar as três séries de desemprego do arquivo `Desemprego.xlsx`: PME Antiga (desde 1994), PME Nova e PNAD Contínua.
    *   Padronizar as datas e os valores de cada série.
    *   Converter as séries mensais (PME) para a frequência trimestral, utilizando a média do período.
    *   Unificar as três séries em uma única série de desemprego trimestral. O critério de unificação nos períodos de sobreposição será a **prioridade pela metodologia mais recente** (PNADc > PME Nova > PME Antiga).
    *   Criar uma coluna `metodologia` para identificar a origem de cada dado, que será usada como candidata a dummy para testes de quebra estrutural.

2.  **Série do Produto Interno Bruto (PIB):**
    *   Carregar a série de PIB Real trimestral. Para a análise da Lei de Okun, a série **com ajuste sazonal** (`Tabela 6613`) foi a escolhida.
    *   **Justificativa da Escolha:** A sua intuição está correta. Séries econômicas como o PIB possuem flutuações sazonais previsíveis (por exemplo, maior atividade econômica no final do ano). O mercado de trabalho, em grande medida, antecipa e se ajusta a esses movimentos regulares. A Lei de Okun, no entanto, foca na relação entre o **ciclo econômico** (desvios não previsíveis da tendência de crescimento) e o desemprego cíclico. Utilizar a série com ajuste sazonal remove o "ruído" da sazonalidade, permitindo isolar o componente cíclico que é o verdadeiro objeto de interesse. A comparação gráfica entre as séries com e sem ajuste no notebook `PIB.ipynb` valida essa escolha, mostrando o padrão de "serra" da sazonalidade na série não ajustada, que é ausente na série ajustada.
    *   Aplicar o logaritmo natural (`ln`) na série do PIB para trabalhar com taxas de crescimento e elasticidades.

#### Status da Implementação no Notebook (`PIB.ipynb`)

As etapas de preparação da variável de PIB foram concluídas no notebook `PIB.ipynb`. O processo executado foi:

1.  **Carregamento e Correção:**
    *   A série de PIB com ajuste sazonal foi carregada a partir do arquivo `Tabela 6613 - com ajuste sazonal.xlsx`.
    *   Foi necessário corrigir o `DataFrame`, pois a primeira linha de dados foi lida como cabeçalho. A estrutura foi reajustada para incorporar essa linha aos dados e as colunas foram renomeadas para `data_raw` e `pib`.

2.  **Tratamento da Data:**
    *   A coluna de data, originalmente em formato de texto (ex: `"1º trimestre de 1996"`), foi processada por uma função para convertê-la em objetos `datetime` do pandas, padronizados para o final de cada trimestre (ex: `1996-03-31`).
    *   A coluna de data foi definida como o índice do `DataFrame`.

3.  **Criação das Variáveis:**
    *   A coluna `ln_pib` foi criada aplicando o logaritmo natural (`np.log`) à série de PIB.
    *   A coluna `crescimento_pib` foi gerada a partir da primeira diferença da série em log, multiplicada por 100 para representar a variação percentual.

3.  **Criação das Variáveis de Análise:**
    *   `u_t`: A série final unificada da taxa de desemprego (em nível).
    *   `Δu_t`: A variação trimestral da taxa de desemprego (`u_t - u_{t-1}`).
    *   `ln_pib_t`: A série do log do PIB real dessazonalizado.
    *   `crescimento_pib_t`: A taxa de crescimento do PIB (`(ln_pib_t - ln_pib_{t-1}) * 100`).

#### 1.1.1 Status da Implementação no Notebook (`Desemprego.ipynb`)

As etapas de preparação da variável de desemprego foram concluídas no notebook `Desemprego.ipynb`. O processo executado foi:

1.  **Carregamento e Tratamento Individual:**
    *   As três séries (`PME Antiga`, `PME Nova`, `PNADc`) foram carregadas a partir do arquivo Excel.
    *   As colunas de data de cada série foram padronizadas para o formato `datetime` do pandas (ex: o formato numérico `1994.03` foi convertido; o formato de texto `'mar-abr-mai 2012'` foi interpretado para uma data de fim de trimestre).
    *   As colunas de taxa foram devidamente convertidas para formato numérico.

2.  **Conversão de Frequência:**
    *   As séries da PME Antiga e PME Nova, que possuem frequência original **mensal**, foram convertidas para a frequência **trimestral**.
    *   A conversão foi feita calculando a **média simples** da taxa de desemprego para cada trimestre, através do comando `.resample('QE').mean()`.
    *   A série da PNADc, por sua vez, já possui uma natureza de média móvel trimestral e foi apenas alinhada para as datas de fim de trimestre.

3.  **Unificação:** Utilizando `pd.concat` e ordenação categórica, os três DataFrames trimestrais foram unificados em uma única série temporal (`desemprego_unificado`), garantindo a prioridade da metodologia mais recente nos períodos de sobreposição.

4.  **Visualização:** Foi gerado um gráfico de linha da série unificada, com o fundo sombreado para indicar os períodos de vigência de cada metodologia, facilitando a análise visual de quebras estruturais.

#### 1.1.2 Análise Visual e Hipótese de Quebra Estrutural

A inspeção visual do gráfico revelou fortes indícios de, no mínimo, uma quebra estrutural na série:

*   **Transição PME Antiga -> PME Nova (~2002):** Observa-se um "salto" nítido no nível da taxa de desemprego, indicando que a mudança metodológica introduziu uma quebra estrutural significativa na série.
*   **Transição PME Nova -> PNADc (~2012):** A quebra, se existente, é visualmente mais sutil.

Essa análise visual preliminar reforça a necessidade dos testes formais de quebra estrutural (como o Teste de Chow) que serão aplicados aos modelos de regressão, conforme detalhado na metodologia. A variável `metodologia` foi mantida no DataFrame unificado para facilitar esses testes.

#### 1.1.3 Unificação Final e Geração de Variáveis (`Tratamento econonometrico.ipynb`)

Com os arquivos `pib_tratado.pkl` e `desemprego_tratado.pkl` devidamente preparados, a próxima etapa, executada no notebook `Tratamento econonometrico.ipynb`, foi a consolidação final do dataset para a análise.

1.  **Unificação:** Os dois `DataFrames` foram unidos por seu índice de data (`join` com `how='inner'`), garantindo que a base de dados final contivesse apenas observações para as quais tanto os dados de PIB quanto de desemprego estivessem disponíveis.
2.  **Criação de Variáveis:** Foram geradas as variáveis necessárias para os modelos de regressão:
    *   `u_t`: Taxa de desemprego (em nível).
    *   `ln_pib`: Logaritmo natural do PIB (em nível).
    *   `delta_u_t`: A variação trimestral na taxa de desemprego (`u_t - u_{t-1}`), para o modelo de primeira diferença.
    *   `crescimento_pib`: A variação percentual do PIB, calculada como a primeira diferença da série de `ln_pib`.

O `DataFrame` resultante, após a remoção de valores `NaN` (gerados no cálculo da primeira diferença), contém 115 observações trimestrais, de Junho de 1996 a Dezembro de 2024, prontas para a análise.

### 1.2 Testes de Estacionariedade (Raiz Unitária)

**Objetivo:** Garantir que as séries são estacionárias para evitar regressões espúrias. Para isso, foram aplicados os testes ADF e KPSS às variáveis em nível e em primeira diferença. O resultado esperado é que as séries em nível sejam não-estacionárias (integradas de ordem 1, ou I(1)) e as séries em primeira diferença sejam estacionárias (I(0)).

**Resultados Obtidos no Notebook (`Tratamento econonometrico.ipynb`) para o período 1996-2024:**

*   **`ln_pib` (Log do PIB em Nível):**
    *   **ADF:** Não rejeitou H₀ (p-valor = 0.6258). A série é **não estacionária**.
    *   **KPSS:** Rejeitou H₀ (p-valor = 0.0100). A série é **não estacionária**.
    *   **Conclusão:** Ambos os testes concordam. A série é **I(1)**, como esperado.

*   **`u_t` (Desemprego em Nível):**
    *   **ADF:** Não rejeitou H₀ (p-valor = 0.2371). A série é **não estacionária**.
    *   **KPSS:** Não rejeitou H₀ (p-valor = 0.1000). A série é **estacionária**.
    *   **Conclusão:** Os testes discordam. Essa ambiguidade é comum em séries de desemprego, que podem exibir comportamento de "longa memória" ou quebras estruturais. Dado o forte resultado do ADF e a teoria econômica, a série será tratada como **I(1)**, justificando o uso de modelos de primeira diferença e cointegração.

*   **`crescimento_pib` (Primeira Diferença do `ln_pib`):**
    *   **ADF:** Rejeitou H₀ (p-valor = 0.0000). A série é **estacionária**.
    *   **KPSS:** Não rejeitou H₀ (p-valor = 0.1000). A série é **estacionária**.
    *   **Conclusão:** Ambos os testes confirmam que a série é **I(0)**.

*   **`delta_u_t` (Primeira Diferença do `u_t`):**
    *   **ADF:** Rejeitou H₀ (p-valor = 0.0001). A série é **estacionária**.
    *   **KPSS:** Não rejeitou H₀ (p-valor = 0.1000). A série é **estacionária**.
    *   **Conclusão:** Ambos os testes confirmam que a série é **I(0)**.

A confirmação de que as variáveis em nível são I(1) e suas primeiras diferenças são I(0) valida a abordagem econométrica de usar o **modelo de primeira diferença** (Fase 3) para analisar a relação de curto prazo e modelos baseados em **nível e hiato** (Fases 4 e 5) para investigar a relação de longo prazo.

### 1.3 Análise de Componentes com Filtro Hodrick-Prescott (HP)

Antes de prosseguir para os modelos de regressão, foi realizada uma análise exploratória para decompor as séries em nível (`ln_pib` e `u_t`) em seus dois componentes principais: **tendência** e **ciclo**. Para isso, utilizou-se o filtro Hodrick-Prescott (HP), uma ferramenta padrão em macroeconomia para essa finalidade, com `lambda=1600`, o valor recomendado para dados trimestrais.

O notebook `Tratamento econonometrico.ipynb` gera um dashboard 2x2 que visualiza essa decomposição:

1.  **Gráficos Superiores (Nível e Tendência):** Mostram as séries originais (PIB e desemprego) sobrepostas às suas tendências de longo prazo extraídas pelo filtro HP. Isso permite uma clara visualização dos períodos em que a economia operou acima ou abaixo de sua tendência (ciclos de expansão e recessão) e como o desemprego se moveu em relação à sua própria tendência.

2.  **Gráficos Inferiores (Séries Estacionárias):** Mostram as séries já diferenciadas (`crescimento_pib` e `delta_u_t`). Visualmente, confirma-se o que os testes de raiz unitária apontaram: as séries flutuam em torno de uma média zero, sem uma tendência clara, caracterizando um comportamento estacionário.

Esta análise visual reforça a adequação dos dados para os modelos propostos e fornece um primeiro vislumbre da relação cíclica inversa entre PIB e desemprego, que é o cerne da Lei de Okun.

### 1.4 Teste de Causalidade de Granger

**Objetivo:** Verificar a direção da relação temporal entre as variáveis. A Lei de Okun postula que o crescimento do produto causa variações no desemprego. O teste de Granger nos ajuda a confirmar se essa precedência temporal é estatisticamente significante nos dados brasileiros.

**Lógica do Teste:**
O teste verifica se valores passados de uma variável (X) ajudam a prever o valor atual de outra variável (Y), mais do que apenas os valores passados de Y.
*   **H₀ (Hipótese Nula):** X *não* causa Granger Y.
*   **H₁ (Hipótese Alternativa):** X causa Granger Y.

**Aplicação:**
Testamos a causalidade bidirecional entre `crescimento_pib` e `delta_u_t` (Variação do Desemprego).
1.  **Crescimento do PIB -> Variação do Desemprego:** Esperamos rejeitar H₀ (p-valor < 0.05), confirmando que o PIB ajuda a prever o desemprego.
2.  **Variação do Desemprego -> Crescimento do PIB:** A teoria econômica também sugere que o desemprego pode afetar o PIB (via demanda agregada), então a causalidade pode ser bidirecional.

**Interpretação para o TCC:**
A confirmação da causalidade no sentido PIB -> Desemprego é um pré-requisito importante para validar a especificação dos modelos de Okun que serão estimados nas fases seguintes, onde o Desemprego é a variável dependente.

**Resultados Obtidos (1996-2024):**

*   **Crescimento do PIB -> Variação do Desemprego:**
    *   **Resultado:** Rejeitamos H₀ em todos os lags testados (1 a 4 trimestres), com p-valores significativos (ex: p=0.0099 no lag 1, p=0.0039 no lag 4).
    *   **Conclusão:** Há forte evidência estatística de que o crescimento do PIB antecede e ajuda a prever as variações na taxa de desemprego. Isso corrobora a direção de causalidade assumida pela Lei de Okun.

*   **Variação do Desemprego -> Crescimento do PIB:**
    *   **Resultado:** Não rejeitamos H₀ em nenhum dos lags (p-valores > 0.05, variando de 0.27 a 0.85).
    *   **Conclusão:** Não encontramos evidências estatísticas de que a variação do desemprego cause o crescimento do PIB nesta amostra. A relação parece ser unidirecional (PIB -> Desemprego) para os dados trimestrais brasileiros neste período.

### 1.5 Discussão: Por que a relação é Unidirecional?

**Dúvida:** Teoricamente, o desemprego também não deveria afetar o PIB (menos renda gera menos consumo)?
**Resposta:** Sim, no longo prazo ou em modelos estruturais. Porém, o teste de Granger captura a **precedência temporal no curto prazo**.

1.  **Mercado de Trabalho como Indicador Defasado (Lagging Indicator):**
    *   As empresas não demitem ou contratam imediatamente após uma mudança na demanda.
    *   **Na queda:** Primeiro o PIB cai (vendas diminuem). As empresas seguram os funcionários (custos de demissão). Só depois o desemprego sobe.
    *   **Na alta:** Primeiro o PIB sobe (uso de capacidade ociosa). Só quando a alta é sustentada, elas voltam a contratar.
    *   **Resultado:** O movimento do PIB *antecede* o movimento do desemprego.

2.  **Isso é um problema para o TCC?**
    *   **Não, é uma vantagem.** Para estimar a Lei de Okun via regressão simples (OLS), precisamos assumir que o PIB explica o desemprego.
    *   Se houvesse forte causalidade reversa simultânea, teríamos viés nos coeficientes. A unidirecionalidade (PIB -> Desemprego) valida estatisticamente o uso do Crescimento do PIB como variável explicativa.

---

## Fase 2: Metodologia de Validação e Análise (Caixa de Ferramentas)

Esta seção descreve os testes que serão aplicados a **cada um** dos modelos estimados nas fases seguintes.

### 2.1 Diagnóstico dos Resíduos

Após cada regressão, os resíduos (`model.resid`) serão submetidos aos seguintes testes:

*   **Autocorrelação Serial (Teste de Breusch-Godfrey):** Verifica se os erros são correlacionados entre si.
    *   **H₀:** Não há autocorrelação. **Objetivo: Não rejeitar H₀.**
*   **Heterocedasticidade (Teste de White):** Verifica se a variância dos erros é constante.
    *   **H₀:** A variância é constante (Homocedasticidade). **Objetivo: Não rejeitar H₀.**
*   **Normalidade (Teste de Jarque-Bera):** Verifica se os erros seguem uma distribuição normal.
    *   **H₀:** Os resíduos são normais. **Objetivo: Não rejeitar H₀.**

### 2.2 Teste de Estabilidade (Quebra Estrutural)

*   **Teste de Chow:** Testa se há uma quebra nos coeficientes em uma **data específica** (ex: 2015).
    *   **H₀:** Os coeficientes são estáveis. **Objetivo: Um p-valor > 0.05 indica estabilidade.**
*   **Teste CUSUM:** Analisa graficamente a estabilidade dos coeficientes ao longo de toda a amostra.

### 2.3 Correção de Erros Padrão (HAC)

Se os testes de diagnóstico da Seção 2.1 falharem (o que é provável), isso não invalida o modelo. A solução é re-estimar a mesma regressão utilizando **erros padrão robustos à heterocedasticidade e autocorrelação (HAC)**, com o estimador de Newey-West.

*   **Comando:** `model.fit(cov_type='HAC', cov_kwds={'maxlags': 4})`
*   **Efeito:** Os coeficientes não mudam, mas seus p-valores e intervalos de confiança são corrigidos para se tornarem confiáveis.

---

## Fase 3: Modelo 1 - Primeira Diferença (Curto Prazo)

Este modelo captura a relação de curto prazo entre o crescimento da economia e a variação do desemprego.

### 3.1 Estimação e Interpretação

*   **Equação:** `Δu_t = β₀ + β₁ * crescimento_pib_t + ε_t`
*   **Estimação:** Rodar a regressão OLS de `Δu_t` contra `crescimento_pib_t`.
*   **Interpretação:**
    *   `β₁`: É o **coeficiente de Okun de curto prazo**. Mostra em quantos pontos percentuais a taxa de desemprego varia para cada 1 p.p. de crescimento do PIB. Espera-se que seja negativo.
    *   `β₀`: O intercepto. Indica qual seria a variação do desemprego se o PIB não crescesse.
    *   Taxa de crescimento para estabilizar o desemprego: `-β₀ / β₁`.

### 3.2 Validação e Análise de Estabilidade

1.  Aplicar os testes de diagnóstico de resíduos (Seção 2.1).
2.  Aplicar os testes de estabilidade/quebra estrutural (Seção 2.2).

### 3.3 Conclusão do Modelo 1

Com base nos resultados, re-estimar o modelo com correção HAC (Seção 2.3), se necessário. Apresentar a equação final com os coeficientes e p-valores robustos e interpretar o resultado econômico.

---

## Fase 4: Modelo 2 - Relação de Nível com o Hiato do Produto

Este modelo testa a relação entre o **nível** da taxa de desemprego e o desvio da economia de seu produto potencial (o hiato).

### 4.1 Estimação do Produto Potencial e do Hiato

1.  **Hiato com Tendência Linear:** Estimar `ln_pib_t = α + β * t + ε_t`. O hiato será o resíduo (`ε_t`) dessa regressão.
2.  **Hiato com Filtro Hodrick-Prescott (HP):** Aplicar o filtro HP na série `ln_pib_t` (com `λ=1600`). O hiato é o componente cíclico retornado pela função. O filtro HP é preferível por sua flexibilidade em capturar mudanças na tendência de crescimento da economia.

### 4.2 Estimação e Interpretação

*   **Equação:** `u_t = β₀ + β₁ * hiato_t + ε_t`
*   **Estimação:** Rodar duas versões da regressão, uma com cada hiato calculado.
*   **Interpretação:** `β₁` mede em quantos pontos percentuais a taxa de desemprego aumenta quando o PIB efetivo fica 1% abaixo do seu potencial. Espera-se que seja negativo.

### 4.3 Validação e Análise de Estabilidade

1.  Aplicar os testes de diagnóstico (Seção 2.1) e estabilidade (Seção 2.2) para as duas versões do modelo.

### 4.4 Conclusão do Modelo 2

Re-estimar as regressões com correção HAC, se preciso. Comparar os resultados (R², significância, etc.) do modelo com hiato linear vs. hiato HP e concluir qual deles se mostra mais robusto.

---

## Fase 5: Modelo 3 - Elasticidade e Tendência Ajustada

Este modelo estima a tendência do PIB e o efeito do desemprego sobre ele simultaneamente.

### 5.1 Estimação e Interpretação

*   **Equação:** `ln_pib_t = β₀ + β₁ * t + β₂ * u_t + ε_t`
*   **Estimação:** Rodar a regressão OLS de `ln_pib_t` contra uma tendência de tempo (`t`) e a taxa de desemprego em nível (`u_t`).
*   **Interpretação:** `β₂` mede a **elasticidade** do produto em relação ao desemprego. Informa em quantos por cento o PIB muda para cada variação de 1 ponto percentual na taxa de desemprego. Espera-se que seja negativo.

### 5.2 Validação e Análise de Estabilidade

1.  Aplicar os testes de diagnóstico (Seção 2.1) e estabilidade (Seção 2.2).
2.  **Teste de Multicolinearidade (VIF):** Por termos duas variáveis explicativas (`t` e `u_t`), é importante verificar se elas não são altamente correlacionadas, o que poderia inflar a variância dos coeficientes. Calcular o *Variance Inflation Factor* (VIF). Um VIF > 10 é um sinal de alerta.

### 5.3 Conclusão do Modelo 3

Re-estimar com correção HAC, se necessário. Apresentar a equação final robusta e interpretar a elasticidade encontrada.

---

## Fase 6: Análise Comparativa e Conclusões Finais

1.  **Quadro Comparativo:** Construir uma tabela resumindo os coeficientes de Okun encontrados em cada um dos modelos robustos (Modelos 1, 2 e 3).
2.  **Discussão dos Resultados:** Discutir as diferenças entre os coeficientes de curto prazo (Modelo 1) e de longo prazo (Modelos 2 e 3).
3.  **Conclusão Final:** Apresentar uma síntese dos achados, respondendo qual a relação de Okun para o Brasil no período analisado e qual modelo se mostrou mais adequado para descrevê-la.
