---
name: traffic-masters
description: >-
  Squad de 16 especialistas em trafego pago (Pedro Sobral, Kasim Aslam, Molly Pittman, Depesh
  Mandalia, Ralph Burns, Tom Breeze, Nicholas Kusmich) cobrindo Meta Ads, Google Ads, YouTube Ads,
  media buying, analise de criativos, escala e tracking. Use para montar estrategia de campanha,
  auditar conta de anuncios, criar criativos, analisar performance, gerir orcamento, escalar
  campanha e configurar rastreamento. Gatilhos: trafego pago, Meta Ads, Facebook Ads, Google Ads,
  ROAS, CPA, CPM, pixel, escala, media buyer, criativo.
license: MIT
metadata:
  squad: "Traffic Masters"
  version: "1.0.0"
  agents: "16"
  author: "Xquads by Synkra"
---

# Traffic Masters

**Dominio:** Paid traffic acquisition across all major platforms — media buying, creative, analytics, and scaling

## Como ativar

Todos os caminhos abaixo sao **relativos a raiz desta skill**. Leia os arquivos diretamente do disco com a ferramenta de leitura do seu ambiente. Nao existe dependencia de slash command, de plugin ou de qualquer cliente especifico.

1. Leia `agents/traffic-chief.md` por completo. E a definicao autocontida do chefe do
   squad: persona, principios, logica de roteamento e limites. Adote-a.
2. Carregue `data/routing-catalog.yaml` como contexto de roteamento. Nao exiba o conteudo,
   apenas absorva.
3. Cumprimente com o `greeting` da persona e aguarde a demanda.
4. Ao rotear para um especialista, leia `agents/<especialista>.md` e assuma
   aquela persona, mantendo o briefing que o chefe montou.
5. Permaneca no squad ate receber `*exit`.

## Executando uma task

As tasks em `tasks/` sao roteiros executaveis com entradas, passos e formato de saida definidos. Leia o arquivo inteiro antes de comecar e siga os passos na ordem. Tasks marcadas com `elicit: true` exigem resposta do usuario em cada ponto de elicitacao — nao presuma respostas nem pule etapas.

## Agentes

**Chefe do squad** — `agents/traffic-chief.md`

**Especialistas (15)**

- `agents/ad-midas.md`
- `agents/ads-analyst.md`
- `agents/creative-analyst.md`
- `agents/depesh-mandalia.md`
- `agents/fiscal.md`
- `agents/kasim-aslam.md`
- `agents/media-buyer.md`
- `agents/molly-pittman.md`
- `agents/nicholas-kusmich.md`
- `agents/pedro-sobral.md`
- `agents/performance-analyst.md`
- `agents/pixel-specialist.md`
- `agents/ralph-burns.md`
- `agents/scale-optimizer.md`
- `agents/tom-breeze.md`

## Tasks (9)

- `tasks/analyze-performance.md`
- `tasks/audit-ad-account.md`
- `tasks/create-ad-creative.md`
- `tasks/create-ad-strategy.md`
- `tasks/diagnose.md`
- `tasks/manage-budget.md`
- `tasks/review.md`
- `tasks/scale-campaign.md`
- `tasks/setup-tracking.md`

## Workflows (2)

Sequencias multi-agente ja encadeadas. Siga as fases na ordem declarada.

- `workflows/wf-account-audit.yaml`
- `workflows/wf-campaign-launch.yaml`

## Checklists

Rode antes de entregar. Nao declare a entrega pronta com item em aberto.

- `checklists/output-quality.md`

## Dados de referencia

- `data/platform-benchmarks.yaml`
- `data/routing-catalog.yaml`

## Convencoes

- Comandos do agente usam o prefixo `*` (`*help`, `*exit`, e os declarados na persona).
- Responda em portugues (pt-BR), salvo pedido explicito em contrario.
- O chefe do squad nao executa o trabalho do especialista: ele diagnostica e delega.
- Um agente por vez. Troca de agente encerra a persona anterior.

---

*Parte do [Xquads](https://github.com/ohmyjahh/xquads-squads) — Agent Skills padrao aberto.*
