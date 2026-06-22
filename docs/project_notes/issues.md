# Tarefas — Status do Projeto

---

## Concluído

### Fase 1 — Preparação dos Dados e Análise Preliminar

- [x] Tratamento e unificação das três séries de desemprego (PME Antiga, PME Nova, PNADc) — `Desemprego.ipynb`
- [x] Tratamento da série de PIB com ajuste sazonal, criação de `ln_pib` e `crescimento_pib` — `PIB.ipynb`
- [x] Unificação final dos datasets e criação do DataFrame analítico (`Tratamento econonometrico.ipynb`)
- [x] Filtro de período: amostra truncada em 2024-T4
- [x] Testes de raiz unitária (ADF e KPSS) para ln_pib, u_t, crescimento_pib e delta_u_t
- [x] Análise visual com Filtro HP (dashboard 2×2)
- [x] Análise de correlação contemporânea (Lag 0: r = −0.21) e defasada (Lag 1: r = −0.26, p = 0.005)
- [x] Análise de correlação cruzada para Lags 0–8; identificação do Lag 1 como ótimo
- [x] Seleção formal de defasagens (VAR — AIC/BIC): decisão por Lag 1
- [x] Teste de Causalidade de Granger: PIB → Desemprego (unidirecional confirmado)
- [x] Identificação analítica de outliers por resíduos padronizados (Z > 2.0): 1998-T1, 2002-T2, 2012-T1
- [x] Teste de Chow nas 4 datas de choque: nenhuma quebra estrutural detectada
- [x] Interpretação econômica detalhada de cada outlier

### Fase 2 — Modelo 1 (Primeira Diferença)

- [x] Estimação de 4 especificações (A, B, C, D) e análise comparativa
- [x] Eliminação dos Modelos B e D (falha no Jarque-Bera)
- [x] Seleção do Modelo C como final (menor AIC, normalidade aprovada, coerência econômica)
- [x] Interpretação do coeficiente de Okun β₁ = −0.1728
- [x] Cálculo da taxa neutra de crescimento (~0.16% ao ano)
- [x] Diagnóstico completo: JB ✓ (0.607), BG → HAC, White ✓ (0.812)
- [x] Geração de todas as figuras da Fase 2 (fig_07 a fig_09b)

### Fase 3 — Modelo 2 (Hiato Estatístico)

- [x] Estimação com Filtro HP (λ=1600)
- [x] Estimação com Filtro Hamilton (h=8, p=4)
- [x] Estimação com Filtro Christiano-Fitzgerald (bandpass 6–32 tri.)
- [x] Análise comparativa dos 3 filtros; seleção do Hamilton como modelo final
- [x] Implementação das step dummies empilhadas (d_PMENova e d_PNADc)
- [x] Diagnóstico completo dos resíduos (Hamilton e HP)
- [x] Derivação da NAIRU implícita por período (Hamilton: 6.63% / 9.91% / 9.73%)
- [x] Redação da análise comparativa HP vs Hamilton vs FGV
- [x] Discussão econômica sobre dicotomia JB/White entre filtros e FGV
- [x] Geração de todas as figuras da Fase 3 (fig_10 a fig_16)

### Fase 3b — Modelo 3 (Hiato FGV/IBRE)

- [x] Carregamento e análise da série FGV/IBRE (1982-T3 a 2025-T3)
- [x] Estimação do modelo com hiato FGV; β₁ = −0.4714
- [x] Diagnóstico dos resíduos (JB falha p=0.007; White aprovado p=0.186)
- [x] Derivação da NAIRU implícita (FGV): 7.26% / 9.52% / 9.05%
- [x] Quadro comparativo geral (todos os modelos)
- [x] Seção 3.8 — análise completa da NAIRU: teoria, derivação algébrica, implicações

### Fase 4 — Modelo 4 (Elasticidade)

- [x] Estimação base: `ln_pib ~ t + u_t + D_PMENova + D_PNADc` com HAC
- [x] Todos os coeficientes significativos a 5%; β₂ = −0.0195 (elasticidade)
- [x] Teste de cointegração Engle-Granger: p = 0.0004 — relação válida, não espúria
- [x] Derivação do produto potencial e hiato implícito (σ = 5.72 p.p.)
- [x] Comparação hiato Modelo 4 vs hiato Hamilton: correlação = 0.52
- [x] Diagnóstico completo (JB, BG, White, VIF)
- [x] Redação da análise de robustez e validade (Seção 4.3)
- [x] Discussão do contexto da literatura brasileira e contribuição do TCC (Seção 4.3.6)
- [x] Geração de todas as figuras da Fase 4 (fig_17 a fig_20)

---

## Pendente

### Extensões do Modelo 4 (alta prioridade)

- [ ] **Quebras estruturais na tendência** (*trend breaks*): implementar dummies de nível e inclinação para 2015-T1 (recessão) e 2020-T2 (pandemia) na equação de elasticidade
- [ ] **Re-estimar cointegração (Engle-Granger)** nos resíduos do modelo estendido com trend breaks
- [ ] **Modelo de Correção de Erros (ECM)**: estimar velocidade de ajuste λ e elasticidade de curto prazo α₁ a partir dos resíduos da regressão de cointegração do Modelo 4

### Ajuste de Dados

- [ ] **Revisão da trimestralização** das séries mensais PME: revisar notas técnicas das 3 pesquisas para validar ou corrigir o método de média simples (ver D-03 em decisions.md)
- [ ] **Coleta de dados de informalidade** via Ipeadata: série de taxa de informalidade para enriquecer a discussão das inversões históricas (Seção 1.6.1 da documentação)

### Fase 5 — Análise Comparativa e Conclusões

- [ ] Quadro comparativo final consolidado (todos os 4 modelos, incluindo extensões)
- [ ] Discussão das diferenças curto prazo vs longo prazo
- [ ] Síntese: qual a Lei de Okun para o Brasil (1996-2024)?

### Redação do TCC

- [ ] Introdução — contextualização e justificativa
- [ ] Revisão de Literatura — Lei de Okun, NAIRU, estudos brasileiros
- [ ] Metodologia — descrever todas as decisões de D-01 a D-12
- [ ] Resultados — apresentar os 4 modelos com tabelas e figuras
- [ ] Conclusão — resposta às perguntas de pesquisa, limitações, agenda futura
- [ ] Abstract, referências bibliográficas, apêndices
