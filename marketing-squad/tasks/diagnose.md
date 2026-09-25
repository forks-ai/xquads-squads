---
task: diagnose()
responsavel: "@marketing-chief"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: request
    tipo: string
    origem: User Input
    obrigatorio: true

Saida:
  - campo: diagnosis
    tipo: string
    destino: Console
    persistido: false

Checklist:
  - "[ ] Objetivo e disciplina(s) identificados"
  - "[ ] Nível de consciência do mercado avaliado (Schwartz)"
  - "[ ] Especialista(s) roteado(s) com o brief"
---

# Task: Diagnosticar Demanda de Marketing

**Task ID:** MKT-CHIEF-001
**Version:** 1.0.0
**Command:** `*diagnose`
**Orchestrator:** Marketing Chief (Mira)
**Purpose:** Fazer a triagem de qualquer demanda de marketing, identificar a(s) disciplina(s) e rotear para o especialista certo — ou disparar um workflow quando for campanha completa.

---

## Inputs

| Field | Type | Source | Required |
|-------|------|--------|----------|
| request | string | User | Yes |

## Execution Phases

1. **Parse** — extrair da demanda: objetivo, oferta, público, mídia e prazo.
2. **Estágio** — a mensagem/posicionamento já existe? Se NÃO, começar por Donald Miller.
3. **Consciência** — avaliar o nível de consciência do mercado (Unaware → Most Aware), que orienta copy e criativo.
4. **Rotear** — cruzar com `discipline_routing` / `objective_routing`:
   - Mensagem/funil → `donald-miller`
   - Copy (headline, sales page, VSL, ads, e-mail) → `eugene-schwartz`
   - Criativo/visual → `visual-generator`
   - Tráfego/lançamento → `pedro-sobral`
   - Campanha completa → disparar `*campaign`; lançamento → `*launch`
5. **Briefar** — entregar ao especialista: público, nível de consciência, oferta, métrica primária, restrições.

## Output Format

```
🎯 DIAGNÓSTICO — Marketing Chief

Objetivo:            {objetivo}
Disciplina(s):       {brand | copy | visual | traffic | campanha}
Nível de consciência:{Unaware → Most Aware}
Especialista(s):     @{agente(s)}
Métrica primária:    {métrica}

▶ Encaminhamento: {resumo do brief para o especialista}
```

## Veto Conditions

- NUNCA rotear copy antes de definir o nível de consciência do mercado.
- NUNCA pular a mensagem quando o posicionamento ainda está confuso.

## Completion Criteria

- [ ] Disciplina(s) e especialista(s) identificados com confiança ALTA
- [ ] Nível de consciência avaliado
- [ ] Brief entregue ao especialista (ou workflow disparado)
