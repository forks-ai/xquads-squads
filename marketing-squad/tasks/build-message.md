---
task: buildMessage()
responsavel: "@donald-miller"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: campaign_brief
    tipo: markdown
    origem: marketing-chief
    obrigatorio: true
Saida:
  - campo: brandscript
    tipo: markdown
    destino: Console
    persistido: false
Checklist:
  - "[ ] One-liner criado (Problema + Solução + Resultado)"
  - "[ ] BrandScript SB7 completo"
  - "[ ] Esqueleto do funil definido"
---

# Task: Construir a Mensagem (StoryBrand)

**Task ID:** MKT-BRAND-001 · **Command:** `*build-message` · **Agent:** Donald Miller (@donald-miller)
**Purpose:** Definir a espinha da campanha — o que dizemos e para quem — antes de qualquer copy, criativo ou tráfego.

## Execution Phases
1. **BrandScript SB7** — Personagem (cliente=herói) → Problema (externo/interno/filosófico) → Guia (a marca) → Plano → CTA → Sucesso → Fracasso evitado.
2. **One-liner** — fórmula Problema + Solução + Resultado, curta e memorável.
3. **Grunt test** — um estranho entende em 5 segundos: o que você oferece, como melhora minha vida, o que fazer para comprar?
4. **Esqueleto do funil** — one-liner → site/wireframe → isca digital → sequência de nurture → sequência de vendas.

## Output Format
```
🧭 BRANDSCRIPT — {marca}
One-liner:  {frase}
Herói:      {cliente}   | Problema: {ext/int/filo}
Guia:       {marca}     | Plano: {passos}
CTA:        {direto}    | Sucesso: {transformação}
Funil:      {esqueleto}
```

## Veto Conditions
- NUNCA posicionar a marca como o herói — o cliente é o herói, a marca é o guia.
- Se a mensagem confunde, refazer: "If you confuse, you lose."

## Completion Criteria
- [ ] One-liner passa no grunt test  · [ ] BrandScript SB7 completo · [ ] Funil esquematizado
