# Registro de Bugs e Pontos de Melhoria

Arquivo para rastrear problemas identificados no projeto. Cada bug é registrado para avaliação e correção posterior.

---

## BUG-001 — Caminho do usuário Windows exposto nos outputs dos notebooks

**Status:** Aberto
**Prioridade:** Baixa
**Descoberto em:** 2026-05-10
**Arquivo(s) afetado(s):**
- `notebooks/1.modelo de primeira diferença.ipynb`
- `notebooks/Desemprego.ipynb`
- `notebooks/2.modelo de hiato.ipynb`
- `notebooks/Tratamento econonometrico.ipynb`

**Descrição:**
As células de output dos notebooks contêm mensagens de aviso geradas automaticamente pelo Python (UserWarning, FutureWarning, SettingWithCopyWarning) que incluem o caminho local do sistema do usuário, expondo o nome de usuário do Windows:
```
C:\Users\davyd\anaconda3\Lib\site-packages\...
C:\Users\davyd\AppData\Local\Temp\ipykernel_...\...
```

**Impacto:**
Baixo. Revela o nome de usuário do Windows (`davyd`) publicamente no GitHub. Não é uma credencial, mas é uma informação de ambiente que idealmente não deveria estar em repositórios públicos.

**Solução proposta:**
Limpar os outputs de todas as células dos notebooks antes do próximo push (`Kernel > Restart & Clear Output` no Jupyter, ou via script `nbconvert --clear-output`). Os outputs serão regenerados normalmente ao executar os notebooks.

**Observação:**
Não causa nenhum erro de execução — é apenas uma questão de privacidade/limpeza no repositório público.

---

## ESTUDO-001 — Avaliar correção do viés de fim de amostra no Filtro HP

**Status:** Em avaliação
**Prioridade:** Média
**Registrado em:** 2026-05-10
**Arquivo(s) afetado(s):**
- `notebooks/2.modelo de hiato.ipynb`
- `docs/documentacao_econometrica.md`

**Descrição:**
O Filtro HP (λ=1600) sofre do problema de viés de fim de amostra (*end-of-sample bias*): por ser um estimador simétrico de médias móveis, ele carece de observações futuras para ancorar a tendência nas últimas observações da amostra (2024-T4). A solução clássica na literatura é estender artificialmente a série com previsões (via ARIMA ou outro modelo preditivo) antes de aplicar o filtro, e depois descartar os valores previstos, mantendo apenas o hiato estimado para o período observado.

**Questão a investigar:**
Vale a pena implementar essa correção para o modelo HP deste TCC? A pergunta tem duas dimensões:
1. **Técnica:** A extensão via ARIMA melhora significativamente as estimativas do hiato HP no período 2022-2024 (pós-COVID), reduzindo a distorção que infla o NAIRU implícito da série HP?
2. **Relevância para o TCC:** A correção alteraria as conclusões comparativas entre HP e Hamilton, ou o Hamilton permaneceria superior mesmo com HP corrigido?

**Impacto esperado:**
O HP corrigido tenderia a produzir estimativas de hiato mais próximas das do Hamilton no período recente, potencialmente reduzindo o NAIRU implícito do PNADc (hoje 10,04% no HP vs. 9,73% no Hamilton). Se a diferença cair substancialmente, o argumento a favor do Hamilton ficaria mais nuançado.

**Solução proposta (se decidir implementar):**
1. Ajustar um modelo ARIMA(p,d,q) sobre `ln_pib` (seleção automática por AIC).
2. Gerar 8 trimestres de previsão (2025-T1 a 2026-T4) como extensão artificial.
3. Aplicar o filtro HP sobre a série estendida (obs. originais + previsões).
4. Recortar o hiato HP apenas até 2024-T4 para uso na regressão Okun.
5. Comparar os resultados com o HP atual e verificar se muda a decisão de seleção de modelo.

**Observação:**
Este problema é um dos motivos centrais da crítica de Hamilton (2018) ao filtro HP. Se a correção não mudar substancialmente os resultados, isso reforça a escolha do Hamilton como modelo final.

---

## BUG-002 — `NameError: beta0` no Notebook 3 (FGV) — notebook não reproduzível

**Status:** ✅ CORRIGIDO em 2026-06-21
**Prioridade:** Crítica
**Descoberto em:** 2026-06-21
**Arquivo(s) afetado(s):**
- `notebooks/3.modelo de hiato FGV.ipynb`

**Descrição:**
A célula de estimação (`a7b8c9d0`) cria o objeto `modelo_fgv` mas **não extrai os coeficientes individuais** (`beta0`, `beta1`, `gamma1`, `gamma2`, `r2_adj`, `aic`). As duas células seguintes dependem dessas variáveis:
- Célula `d0e1f2a3` (resultados finais + NAIRU implícita) → **lança `NameError: name 'beta0' is not defined`**, interrompendo a execução.
- Célula `e1f2a3b4` (tabela comparativa Hamilton vs FGV) → também usa `beta1`, `r2_adj`, `aic`.

Na saída salva no `.ipynb`, a célula `e1f2a3b4` aparece como executada com sucesso apenas porque foi rodada numa sessão anterior em que essas variáveis ainda existiam no kernel (estado residual). Em um **Restart & Run All**, o notebook quebra a partir de `d0e1f2a3`.

**Impacto:**
Nenhum impacto nos resultados (os coeficientes salvos e documentados estão corretos: β₁ = −0.4714; NAIRU FGV 7.26% / 9.52% / 9.05%). O problema é de **reprodutibilidade**: o notebook não roda do zero.

**Solução aplicada:**
Adicionada à célula `a7b8c9d0`, logo após `.fit(...)`, a extração dos coeficientes:
```python
beta0  = modelo_fgv.params['const']
beta1  = modelo_fgv.params['hiato_fgv']
gamma1 = modelo_fgv.params['d_PMENova']
gamma2 = modelo_fgv.params['d_PNADc']
r2_adj = modelo_fgv.rsquared_adj
aic    = modelo_fgv.aic
```

---

## BUG-003 — Dashboard HP (fig_02) gerado com dados de 2025 (118 obs)

**Status:** Aberto
**Prioridade:** Média
**Descoberto em:** 2026-06-21
**Arquivo(s) afetado(s):**
- `notebooks/Tratamento econonometrico.ipynb` (célula `956ac35d`)
- `figuras/fase1_tratamento/fig_02_hp_filter_dashboard.png`

**Descrição:**
O dashboard do filtro HP chama `hpfilter(df_final['ln_pib'], lamb=1600)` e `hpfilter(df_final['u_t'], lamb=1600)` usando `df_final`, que tem **118 observações** (1996-T1 a **2025-T3**), incluindo as projeções de 2025-T1/T2/T3. A amostra correta (`df_final_ajustado`, 115 obs até 2024-T4, conforme decisão D-12) só é criada em célula posterior e não é aplicada retroativamente ao dashboard.

**Impacto:**
O `fig_02_hp_filter_dashboard.png` foi gerado com a amostra errada. Agravante: o HP é o filtro mais sensível ao *end-of-sample bias* (ver ESTUDO-001), então as últimas observações da tendência (2022-2024) são contaminadas pelos valores de 2025 que deveriam ter sido descartados. É uma figura ilustrativa da Fase 1, não entra nas regressões finais — por isso prioridade média, não crítica.

**Solução proposta:**
Mover a criação de `df_final_ajustado` (truncamento em 2024-T4) para antes da célula do dashboard HP, ou trocar `df_final` por `df_final_ajustado` na célula `956ac35d`, e regerar `fig_02`.

---

## BUG-004 — Célula `taxa_neutra` do Notebook 1 usa Modelo A em vez do Modelo C

**Status:** Aberto
**Prioridade:** Média
**Descoberto em:** 2026-06-21
**Arquivo(s) afetado(s):**
- `notebooks/1.modelo de primeira diferença.ipynb` (célula `acd25e6a`, dependente de `0a5e121d`)

**Descrição:**
A célula `acd25e6a` calcula a "taxa neutra de crescimento" a partir do objeto `modelo1_ajustado`. Esse objeto é definido pela célula configurável `0a5e121d` com `X_vars = ['crescimento_pib_lag1', 'd_1998_t1', 'd_2002_t2', 'd_2012_t1']` — ou seja, a especificação do **Modelo A** (3 pulse dummies, 1998-T1 tratado por dummy e não por interpolação), e **não** a do Modelo C (que interpola 1998-T1 e usa apenas 2 pulse dummies).

Saída da célula:
```
Equação: Δu_t = 0.0064 + (-0.1729) * crescimento_pib_t-1
```
A documentação registra β₀ = **0.0071** para o Modelo C (final). A diferença (0.0064 vs 0.0071) é exatamente o efeito de usar a especificação A.

**Impacto:**
O Modelo C correto (célula `90068706`) calcula sua própria taxa neutra internamente e está consistente com a documentação. A célula `acd25e6a` é um resquício de versão anterior que exibe um valor divergente no fluxo do notebook — risco de confundir o leitor / ser copiado para o texto do TCC por engano. Não contamina os resultados documentados.

**Solução proposta:**
Reapontar a célula `acd25e6a` para `modelo_C` (definido em `90068706`), ou removê-la, já que o Modelo C já reporta sua taxa neutra. Definir a ordem canônica de execução do notebook.

---

## BUG-005 — ADF de `u_t` no Notebook 4 conclui I(0) mas texto afirma I(1)

**Status:** Aberto
**Prioridade:** Média
**Descoberto em:** 2026-06-21
**Arquivo(s) afetado(s):**
- `notebooks/4.modelo de elasticidade.ipynb` (célula `a1b2c3d4-0005`)

**Descrição:**
A função `teste_adf` é chamada para `u_t` com `regression='c'`:
```python
p_ut = teste_adf(df['u_t'], 'u_t (nível, c)', regression='c')
# → ADF = -3.4524, p = 0.0093 → imprime "I(0) — Estacionária ✓"
```
Logo em seguida o notebook imprime: `"→ Ambas as variáveis são I(1): o teste de cointegração é necessário."` — em **contradição direta** com o resultado que ele mesmo acabou de gerar.

Comparação de especificação com o Notebook de Tratamento (célula `dddb2844`, que usa `regression='ct'`):
- Tratamento: ADF u_t = −2.1186, p = 0.2371 → I(1) (valor documentado em `key_facts.md`)
- Notebook 4: ADF u_t = −3.4524, p = 0.0093 → I(0) (inconsistente com a documentação)

A diferença vem da escolha de `regression` ('c' vs 'ct') e do `maxlag`/`autolag`.

**Impacto:**
A decisão final de tratar u_t como I(1) (por teoria econômica e padrão da literatura) está correta e a cointegração foi confirmada — mas o Notebook 4 exibe um resultado de ADF que contradiz seu próprio texto e a documentação. Inconsistência de apresentação; não invalida o teste de cointegração.

**Solução proposta:**
Padronizar a especificação do ADF de `u_t` para `regression='ct'` (coerente com o Notebook de Tratamento e com `key_facts.md`), ou adicionar nota explicando a ambiguidade ADF/KPSS e por que u_t é tratada como I(1) apesar do resultado limítrofe.

---

## BUG-006 — Primeira célula ADF/KPSS do Tratamento usa dados de 2025 e spec incorreta

**Status:** Aberto
**Prioridade:** Baixa
**Descoberto em:** 2026-06-21
**Arquivo(s) afetado(s):**
- `notebooks/Tratamento econonometrico.ipynb` (célula `987834ff`)

**Descrição:**
A primeira célula de testes ADF/KPSS roda sobre `df_final` completo (118 obs, inclui 2025) e usa `regression='ct'` para **todas** as variáveis, inclusive as séries já diferenciadas (que deveriam usar `regression='c'`, pois são I(0) sem tendência). A célula correta (`dddb2844`) aparece depois, usa `df_final_ajustado` (115 obs) e as especificações adequadas — é dela que vêm os valores documentados.

**Impacto:**
Baixo. A célula `987834ff` é redundante e supersedida pela `dddb2844`. Não afeta resultados finais, mas polui o notebook e pode confundir.

**Solução proposta:**
Remover a célula `987834ff` ou marcá-la explicitamente como exploratória/descartada.

---

## BUG-007 — Trailing space na lista de datas do teste de Chow

**Status:** Aberto
**Prioridade:** Baixa
**Descoberto em:** 2026-06-21
**Arquivo(s) afetado(s):**
- `notebooks/Tratamento econonometrico.ipynb` (célula `59dc9d06`)

**Descrição:**
A lista de datas de outliers contém um espaço em branco no final do primeiro elemento:
```python
datas_outliers = ['2012-T1 ', '2002-T2', '1998-T1']
```
O teste executou e os p-valores (0.94 / 0.75 / 0.47) batem com a documentação, então o parsing absorveu o espaço sem erro. Código frágil — pode quebrar se a string for usada em comparação exata ou indexação.

**Impacto:**
Nenhum impacto observável nos resultados. Apenas robustez de código.

**Solução proposta:**
Remover o espaço: `'2012-T1'`.

---

## BUG-008 — Múltiplos objetos de modelo coexistem no Notebook 1 (risco de execução fora de ordem)

**Status:** Aberto
**Prioridade:** Baixa
**Descoberto em:** 2026-06-21
**Arquivo(s) afetado(s):**
- `notebooks/1.modelo de primeira diferença.ipynb`

**Descrição:**
Ao longo do notebook são criados muitos objetos de modelo no mesmo escopo: `modelo_ols`, `modelo_hac`, `modelo1_ajustado`, `modelo_simples`, `modelo_interp`, `modelo_A`, `modelo_B`, `modelo_C`, `modelo_D`. Células de diagnóstico e comparação (`7ff58684`, `d8234d37`) dependem de vários deles estarem em memória simultaneamente. Re-executar uma célula isolada fora de ordem pode usar um objeto desatualizado ou inexistente.

**Impacto:**
Baixo se o notebook for sempre executado de cima para baixo (Restart & Run All). Risco apenas em edição interativa fora de ordem.

**Solução proposta:**
Documentar a ordem canônica de execução no topo do notebook, e/ou consolidar a definição dos 4 modelos (A–D) em uma única célula autocontida (`332250fe` já faz isso parcialmente).

---

## BUG-009 — Numeração `fig_10b` duplicada no Notebook 2

**Status:** Aberto
**Prioridade:** Baixa (cosmético)
**Descoberto em:** 2026-06-21
**Arquivo(s) afetado(s):**
- `notebooks/2.modelo de hiato.ipynb`
- `figuras/fase3_modelo2/fig_10b_ut_nivel_com_quebras.png`
- `figuras/fase3_modelo2/fig_10b_hiato_hamilton.png`

**Descrição:**
Duas figuras distintas compartilham o prefixo `fig_10b`: a visualização das step dummies (célula `fb9ff135`) e o hiato Hamilton (célula `0409c291`). Os nomes de arquivo completos diferem, então não há sobrescrita — mas a numeração `10b` viola a convenção de identificadores únicos por figura.

**Impacto:**
Cosmético. Pode confundir referências cruzadas no texto do TCC.

**Solução proposta:**
Renumerar uma das figuras (ex.: a de step dummies para `fig_10d`) e atualizar a referência na documentação.

---

## NOTA-001 — Kernel crash ao final do Notebook 4

**Status:** Observação
**Prioridade:** Baixa
**Descoberto em:** 2026-06-21
**Arquivo(s) afetado(s):**
- `notebooks/4.modelo de elasticidade.ipynb` (após célula `a1b2c3d4-0014`)

**Descrição:**
Após a última célula de output, a saída registra "The Kernel crashed while executing code". Todos os resultados finais foram exibidos corretamente antes do crash. Provável esgotamento de memória/recursos de display com múltiplas figuras matplotlib abertas.

**Impacto:**
Nenhum nos coeficientes estimados. Apenas exibição.

**Solução proposta:**
Adicionar `plt.close('all')` ao final das células que geram figuras para liberar memória; verificar versão do kernel/ambiente.

---
