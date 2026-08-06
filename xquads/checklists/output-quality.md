# Checklist: Qualidade de Roteamento — Xquads Chief

Gate de qualidade do meta-orquestrador. Diferente dos outros squads, aqui **não se avalia o deliverable** — avalia-se o **roteamento**. Rode antes de considerar um roteamento concluído.

---

## 1. Diagnóstico

- [ ] A demanda real foi extraída (o que precisa EXISTIR no final), não só o rótulo que o usuário usou
- [ ] O domínio veio do `routing-catalog.yaml` — nenhum squad inventado
- [ ] A confiança foi calculada e **declarada em voz alta** com motivo em 1 linha
- [ ] Se houve empate entre domínios, o `tie_breakers` foi aplicado
- [ ] Se confiança < 50, foi feita **exatamente uma** pergunta de desambiguação
- [ ] Caso especial verificado: código → `/raxos`; sem squad → `/squad`

## 2. Briefing de Handoff

- [ ] Cabe em 500 tokens
- [ ] `Contexto conhecido` tem **só** o que o usuário disse
- [ ] Toda inferência está em `Premissas assumidas`, marcada `[ASSUMIDO]`
- [ ] `Fora de escopo` preenchido (obrigatório quando a demanda é ambígua)
- [ ] `Objetivo final` descreve um artefato concreto, não uma intenção vaga
- [ ] O **especialista final não foi pré-escolhido** — essa decisão é do chefe do squad

## 3. Ativação

- [ ] O chefe do squad foi **efetivamente ativado**, não apenas recomendado
- [ ] O comando de ativação bate com o do catálogo
- [ ] Apenas **um** chefe ativado por vez
- [ ] O Xquads Chief parou de conduzir depois da transferência
- [ ] Nenhum comentário por cima do trabalho do chefe do squad

## 4. Cadeia Multi-Squad (quando aplicável)

- [ ] A cadeia foi anunciada inteira ao usuário antes de começar
- [ ] A cadeia veio de `multi_squad_chains` — não foi inventada
- [ ] A cadeia é realmente necessária (o usuário pediu resultado de negócio, não um deliverable isolado)
- [ ] Elos executados **em sequência**, nunca em paralelo
- [ ] Output do elo N virou `Contexto conhecido` do elo N+1
- [ ] Máximo de 5 elos respeitado
- [ ] A cadeia foi interrompível — o usuário pôde parar

## 5. Limites (violação = falha do gate)

- [ ] **Nenhum trabalho de execução foi feito** — nem rascunho, nem "só pra adiantar"
- [ ] Nenhuma linha de código escrita
- [ ] Nenhuma copy, design, análise ou estratégia produzida
- [ ] Mais de uma pergunta de desambiguação **não** foi feita
- [ ] Resposta inteira em português (pt-BR)

---

## Veredito

| Resultado | Critério |
|---|---|
| **PASS** | Todos os itens das seções 1-3 e 5 marcados (+ seção 4 se houve cadeia) |
| **CONCERNS** | Roteamento correto, mas briefing incompleto ou confiança não declarada |
| **FAIL** | Squad errado, execução feita pelo próprio chefe geral, ou chefe do squad não ativado |

**FAIL em qualquer item da seção 5 é automático** — não importa quão bom foi o resto.
