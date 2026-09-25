---
name: brand-squad
description: >-
  Squad de 15 agentes de estrategia de marca (David Aaker, Marty Neumeier, Al Ries, Byron Sharp,
  Jean-Noel Kapferer, Kevin Keller, Donald Miller, Emily Heyward, Alina Wheeler, Denise Yohn) mais
  especialistas em naming, arquetipos e dominio. Use para posicionamento, auditoria de marca,
  identidade visual e verbal, arquitetura de marca, historia de marca, mapeamento de arquetipo e
  geracao de nomes. Gatilhos: marca, branding, posicionamento, naming, identidade, arquetipo,
  brand equity, tagline, proposito de marca.
license: MIT
metadata:
  squad: "Brand Squad"
  version: "1.0.0"
  agents: "15"
  author: "Xquads by Synkra"
---

# Brand Squad

**Dominio:** Brand strategy, identity, positioning, architecture, naming, archetypes, and growth

## Como ativar

Todos os caminhos abaixo sao **relativos a raiz desta skill**. Leia os arquivos diretamente do disco com a ferramenta de leitura do seu ambiente. Nao existe dependencia de slash command, de plugin ou de qualquer cliente especifico.

1. Leia `agents/brand-chief.md` por completo. E a definicao autocontida do chefe do
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

**Chefe do squad** — `agents/brand-chief.md`

**Especialistas (14)**

- `agents/al-ries.md`
- `agents/alina-wheeler.md`
- `agents/archetype-consultant.md`
- `agents/byron-sharp.md`
- `agents/david-aaker.md`
- `agents/denise-yohn.md`
- `agents/domain-scout.md`
- `agents/donald-miller.md`
- `agents/emily-heyward.md`
- `agents/jean-noel-kapferer.md`
- `agents/kevin-keller.md`
- `agents/marty-neumeier.md`
- `agents/miller-sticky-brand.md`
- `agents/naming-strategist.md`

## Tasks (9)

- `tasks/audit-brand.md`
- `tasks/build-identity.md`
- `tasks/create-brand-story.md`
- `tasks/create-positioning.md`
- `tasks/design-architecture.md`
- `tasks/diagnose.md`
- `tasks/generate-names.md`
- `tasks/map-archetype.md`
- `tasks/review.md`

## Workflows (2)

Sequencias multi-agente ja encadeadas. Siga as fases na ordem declarada.

- `workflows/wf-brand-creation.yaml`
- `workflows/wf-rebrand.yaml`

## Checklists

Rode antes de entregar. Nao declare a entrega pronta com item em aberto.

- `checklists/output-quality.md`

## Dados de referencia

- `data/brand-frameworks.yaml`
- `data/routing-catalog.yaml`

## Convencoes

- Comandos do agente usam o prefixo `*` (`*help`, `*exit`, e os declarados na persona).
- Responda em portugues (pt-BR), salvo pedido explicito em contrario.
- O chefe do squad nao executa o trabalho do especialista: ele diagnostica e delega.
- Um agente por vez. Troca de agente encerra a persona anterior.

---

*Parte do [Xquads](https://github.com/ohmyjahh/xquads-squads) — Agent Skills padrao aberto.*
