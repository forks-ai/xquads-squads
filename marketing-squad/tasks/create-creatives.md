---
task: createCreatives()
responsavel: "@visual-generator"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: campaign_copy
    tipo: markdown
    origem: eugene-schwartz
    obrigatorio: true
Saida:
  - campo: creative_assets
    tipo: markdown
    destino: Console
    persistido: false
Checklist:
  - "[ ] Prompts de IA estruturados por asset"
  - "[ ] Criativos otimizados por plataforma"
  - "[ ] Visual serve a Big Idea da copy"
---

# Task: Criar os Assets Visuais

**Task ID:** MKT-VISUAL-001 · **Command:** `*create-creatives` · **Agent:** Visual Generator (@visual-generator)
**Purpose:** Transformar a Big Idea da copy em assets visuais de marketing — o visual serve à venda, não decora.

## Execution Phases
1. **Direção** — extrair a Big Idea e o tom da copy; definir estilo/paleta/identidade.
2. **Assets** — criativos de anúncio, thumbnails, banners, ícones, ilustrações, assets de social.
3. **Prompts de IA** — prompts estruturados (Midjourney/DALL-E/Flux): sujeito, estilo, composição, iluminação, paleta, parâmetros.
4. **Otimização por plataforma** — formatos e proporções por canal (Feed 1:1/4:5, Stories/Reels 9:16, YouTube 16:9, etc.).

## Output Format
```
🎨 CRIATIVOS — {campanha}
Big Idea:   {ideia servida}
Estilo:     {estilo/paleta}
Assets:     {lista}
Prompts IA: {prompts por asset}
Formatos:   {por plataforma}
```

## Veto Conditions
- NUNCA criar visual decorativo desconectado da copy/Big Idea.
- NUNCA entregar fora do formato/proporção da plataforma de destino.

## Completion Criteria
- [ ] Prompts estruturados · [ ] Formatos por plataforma · [ ] Visual serve a Big Idea
