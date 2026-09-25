---
task: writeCopy()
responsavel: "@eugene-schwartz"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: brandscript
    tipo: markdown
    origem: donald-miller
    obrigatorio: true
Saida:
  - campo: campaign_copy
    tipo: markdown
    destino: Console
    persistido: false
Checklist:
  - "[ ] Nível de consciência e sofisticação diagnosticados"
  - "[ ] Headline calibrada ao nível de consciência"
  - "[ ] Mecanismo, bullets e CTA definidos"
---

# Task: Escrever a Copy

**Task ID:** MKT-COPY-001 · **Command:** `*write-copy` · **Agent:** Eugene Schwartz (@eugene-schwartz)
**Purpose:** Produzir a copy da campanha ancorada na mensagem, calibrada ao nível de consciência do mercado.

## Execution Phases
1. **Diagnóstico** — nível de consciência (Unaware → Most Aware) e estágio de sofisticação do mercado. "Copy is not written, it is assembled."
2. **Headline** — casada ao nível de consciência: Unaware → história/curiosidade; Most Aware → oferta/preço/urgência.
3. **Lead & Mecanismo** — os primeiros parágrafos e o mecanismo único que explica por que funciona.
4. **Corpo** — sales page / VSL / ad copy / e-mails conforme a mídia; bullets de fascinação; prova.
5. **Oferta & CTA** — oferta irresistível e chamada clara.

## Output Format
```
✍️ COPY — {peça}
Consciência: {nível} | Sofisticação: {estágio}
Headline:  {headline}
Big Idea:  {ideia central}
Lead:      {abertura}
Mecanismo: {por que funciona}
Corpo:     {texto}
CTA:       {chamada}
```

## Veto Conditions
- NUNCA escrever sem definir o nível de consciência do mercado.
- NUNCA entregar sem uma oferta clara e um CTA.

## Completion Criteria
- [ ] Headline alinhada à consciência · [ ] Mecanismo/prova presentes · [ ] Oferta + CTA claros
