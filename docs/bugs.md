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
