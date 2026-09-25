# Marketing Squad 🎯

**O melhor agente de cada disciplina de marketing, orquestrado numa linha de montagem.**

Este squad reúne os 4 especialistas mais completos dos squads do Xquads, sob um orquestrador (Marketing Chief), para conduzir uma campanha de ponta a ponta: **mensagem → copy → criativo → distribuição**.

---

## O time

| Tier | Agente | Disciplina | Vem de | O que faz |
|------|--------|-----------|--------|-----------|
| 0 | 🎯 **Marketing Chief** (Mira) | Orquestração | *novo* | Diagnostica, roteia, sequencia a campanha e revisa a qualidade entre handoffs |
| 1 | 📖 **Donald Miller** | Mensagem / Brand | brand-squad | StoryBrand SB7, one-liner, clareza de oferta, esqueleto do funil |
| 1 | 🧠 **Eugene Schwartz** | Copy | copy-squad | 5 Níveis de Consciência, headline, mecanismo, sales page, VSL |
| 1 | 🎨 **Visual Generator** | Criativo / Visual | design-squad | Prompts de IA, criativos de anúncio, identidade, thumbnails, assets sociais |
| 1 | 🚦 **Pedro Sobral** | Tráfego Pago | traffic-masters | Meta Ads (PT-BR), públicos, orçamento, teste, escala, lançamento |

> **Por que estes quatro?** Miller é o brand mais *acionável* (transforma posicionamento em assets). Schwartz é o copy *fundacional* (os níveis de consciência são o eixo de todo copywriting). Visual Generator é o design que *produz criativo de marketing* de verdade. Sobral é o tráfego *full-funnel em português*. Juntos formam uma linha de montagem coerente.

---

## Início rápido

Ative o orquestrador e deixe ele rotear:

```
@marketing-squad:marketing-chief
*help
```

Ou vá direto a um especialista:

```
@marketing-squad:donald-miller      # mensagem/posicionamento
@marketing-squad:eugene-schwartz    # copy
@marketing-squad:visual-generator   # criativo visual
@marketing-squad:pedro-sobral       # tráfego pago
```

---

## Workflows pré-definidos

O squad tem workflows que encadeiam as 4 disciplinas automaticamente, com portão de qualidade entre cada fase:

| Comando | Workflow | O que faz |
|---------|----------|-----------|
| `*campaign` | **Campanha Completa** | `diagnose → mensagem (Miller) → copy (Schwartz) → criativo (Visual) → tráfego (Sobral) → review`. A linha de montagem completa. |
| `*launch` | **Lançamento** | Campanha em ondas (pré-lançamento → aquecimento → abertura → escassez), com o tráfego montado por onda. |

Cada fase tem um `checkpoint` (gate/veto): input ruim a montante é barrado antes de desperdiçar verba a jusante.

---

## Como o Chief roteia

```
Demanda
  ├─ Mensagem indefinida?      → Donald Miller (comece pela espinha)
  ├─ Copy (headline/VSL/ads)?  → Eugene Schwartz
  ├─ Criativo/visual?          → Visual Generator
  ├─ Tráfego/escala?           → Pedro Sobral
  └─ Campanha/lançamento?      → *campaign / *launch (sequencia todos)
```

---

## Estrutura

```
marketing-squad/
├── squad.yaml                  # manifesto de componentes
├── config/config.yaml          # tiers, agentes, handoffs, roteamento
├── data/routing-catalog.yaml   # mapa demanda → especialista
├── agents/                     # marketing-chief + os 4 especialistas
├── tasks/                      # diagnose, build-message, write-copy, create-creatives, build-traffic, review
├── workflows/                  # wf-full-campaign, wf-launch
└── checklists/output-quality.md
```

---

## Comandos do Chief

| Comando | O que faz |
|---------|-----------|
| `*help` | Lista os comandos |
| `*diagnose` | Triagem da demanda e roteamento |
| `*campaign` | Dispara a campanha completa (4 disciplinas) |
| `*launch` | Dispara o lançamento em ondas |
| `*assign {agente}` | Atribui manualmente um especialista |
| `*review` | Revisão de qualidade (8 critérios) |
| `*roster` | Mostra o time |

---

*Marketing Squad v1.0.0 · Xquads · Linha de montagem: mensagem → copy → criativo → tráfego*
