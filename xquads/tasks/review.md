# Task: Review (Validação de Roteamento e Entrega)

**Agente:** xquads-chief
**Comando:** `*review`
**Output:** veredito de roteamento + próximo passo (encerrar ou encadear)
**Duração:** < 2 minutos

---

## Objetivo

Quando o squad devolve a entrega, o Xquads Chief valida **uma coisa só**: o roteamento acertou e a demanda original foi respondida. Ele **não** avalia a qualidade técnica do deliverable — isso é do chefe do squad, que tem o `output-quality.md` dele.

---

## Passo 1 — Conferir contra a demanda original

| Verificação | Pergunta |
|---|---|
| Aderência | A entrega responde ao que foi pedido, ou responde a outra coisa? |
| Escopo | Ficou dentro do `Fora de escopo` declarado no briefing? |
| Premissas | As premissas `[ASSUMIDO]` se confirmaram? |
| Completude | Falta alguma parte do pedido original sem justificativa? |

---

## Passo 2 — Veredito de roteamento

| Veredito | Critério | Ação |
|---|---|---|
| **ACERTO** | Entrega responde à demanda dentro do escopo | Encerrar ou seguir para o próximo elo da cadeia |
| **PARCIAL** | Responde, mas parte da demanda ficou de fora | Devolver ao mesmo chefe com o gap explícito |
| **ERRO DE ROTA** | O squad não era o certo | Re-rotear para o squad correto, com briefing corrigido e o aprendizado registrado |
| **FORA DE ESCOPO** | Squad expandiu o pedido sozinho | Sinalizar ao usuário o que foi entregue além do pedido |

---

## Passo 3 — Registrar o aprendizado (só em ERRO DE ROTA)

Erro de rota é informação. Registre em uma linha o que enganou o diagnóstico:

```
[ROTA] "{demanda}" → roteado p/ {squad errado}, correto era {squad certo}.
Sinal enganoso: {keyword ou premissa que induziu ao erro}.
```

Use isso para ajustar o `tie_breakers` do `routing-catalog.yaml` quando o padrão se repetir. Não reescreva o catálogo por um caso isolado.

---

## Passo 4 — Fechar ou encadear

- **Cadeia terminou** → entregue o consolidado e encerre. Sem resumo cerimonial.
- **Tem próximo elo** → monte o novo briefing com o output atual como `Contexto conhecido` e ative o próximo chefe.
- **Usuário quer parar** → pare. Não force o resto da cadeia.

---

## Checkpoint

| Gate | Veto |
|---|---|
| Veredito emitido em 1 dos 4 tipos | Avaliou qualidade técnica do deliverable (não é seu papel) |
| Gap explícito quando PARCIAL | Devolveu "melhora aí" sem apontar o quê |
| Erro de rota registrado | Re-roteou em silêncio, sem registrar o aprendizado |
