---
task: buildTraffic()
responsavel: "@pedro-sobral"
responsavel_type: Agent
atomic_layer: Task
elicit: true

Entrada:
  - campo: creative_assets
    tipo: markdown
    origem: visual-generator
    obrigatorio: true
Saida:
  - campo: media_plan
    tipo: markdown
    destino: Console
    persistido: false
Checklist:
  - "[ ] Estrutura de campanha por objetivo"
  - "[ ] Públicos por temperatura definidos"
  - "[ ] Orçamento (CBO/ABO) e plano de teste"
---

# Task: Montar o Tráfego

**Task ID:** MKT-TRAFFIC-001 · **Command:** `*build-traffic` · **Agent:** Pedro Sobral (@pedro-sobral)
**Purpose:** Distribuir e escalar a campanha via tráfego pago (foco Meta Ads), recebendo copy + criativos + oferta.

## Execution Phases
1. **Objetivo** — escolher o tipo de campanha entre os 3 essenciais: audiência, leads ou vendas ("90% dos resultados").
2. **Públicos** — segmentação por temperatura: frios (topo/captação), mornos e quentes (retargeting/conversão).
3. **Estrutura** — 4–8 conjuntos de anúncios; CBO vs ABO conforme a fase; "criativo é o novo público".
4. **Teste** — plano de teste de criativos/hooks; métricas e critérios de corte.
5. **Escala / Lançamento** — escala horizontal vs vertical; se lançamento, campanhas por onda.

## Output Format
```
🚦 PLANO DE MÍDIA — {campanha}
Objetivo:    {audiência | leads | vendas}
Estrutura:   {campanhas / ad sets / CBO-ABO}
Públicos:    {frio / morno / quente}
Criativos:   {variações a testar}
Orçamento:   {distribuição}
Teste:       {plano + critérios de corte}
```

## Veto Conditions
- NUNCA subir campanha sem objetivo claro ou com público mal segmentado.
- NUNCA escalar antes de validar o criativo vencedor.

## Completion Criteria
- [ ] Estrutura por objetivo · [ ] Públicos por temperatura · [ ] Orçamento + plano de teste
