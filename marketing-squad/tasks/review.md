---
task: review()
responsavel: "@marketing-chief"
responsavel_type: Agent
atomic_layer: Task
elicit: false

Entrada:
  - campo: campaign_assets
    tipo: markdown
    origem: pipeline
    obrigatorio: true
Saida:
  - campo: quality_verdict
    tipo: string
    destino: Console
    persistido: false
Checklist:
  - "[ ] 8 critérios de qualidade avaliados"
  - "[ ] Coerência entre as 4 disciplinas verificada"
  - "[ ] Veredito PASS/REVISE emitido"
---

# Task: Revisão de Qualidade do Chief

**Task ID:** MKT-CHIEF-002 · **Command:** `*review` · **Agent:** Marketing Chief (Mira)
**Purpose:** Validar a campanha contra o padrão do squad e garantir COERÊNCIA entre mensagem, copy, criativo e tráfego.

## Execution — 8 critérios (checklist output-quality.md)
1. Mensagem passa no grunt test (5s)?
2. Headline casa com o nível de consciência?
3. Oferta e CTA claros e irresistíveis?
4. Criativo serve a Big Idea e para o scroll?
5. Criativo otimizado para o formato da plataforma?
6. Campanha estruturada por objetivo, com temperatura de público correta?
7. Mensagem + copy + criativo + segmentação contam UMA história?
8. Existe uma métrica primária definida?

## Output Format
```
✅ REVISÃO — {campanha}
Critérios:  {8/8 | falhas}
Coerência:  {OK | incoerência em ...}
Veredito:   PASS | REVISE → {@agente responsável + brief}
```

## Veto Conditions
- REVISE (bloqueia) se qualquer critério CRÍTICO falhar ou se houver incoerência entre disciplinas.

## Completion Criteria
- [ ] 8 critérios avaliados · [ ] Coerência verificada · [ ] Veredito emitido
