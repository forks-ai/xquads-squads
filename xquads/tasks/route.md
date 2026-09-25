# Task: Route (Diagnosticar + Ativar)

**Agente:** xquads-chief
**Comando:** `*route` (padrão) · `*route-to {squad}` (pula o diagnóstico)
**Output:** chefe do squad ATIVADO com briefing estruturado
**Duração:** < 2 minutos

---

## Objetivo

Levar a demanda até o chefe do squad certo e **transferir o comando**. Esta é a task principal do Xquads Chief. Ela termina com outro agente no controle da conversa — não com um relatório.

---

## Passo 1 — Diagnóstico

Execute `diagnose.md` na íntegra. Se o usuário já disse qual squad quer (`*route-to`), pule direto ao Passo 2.

**Bloqueio:** não avance com confiança < 50 sem ter feito a pergunta de desambiguação e recebido a resposta.

---

## Passo 2 — Montar o Handoff Briefing

O chefe do squad nunca recebe a demanda crua. Monte este pacote (**máximo 500 tokens** — regra de compactação de handoff):

```markdown
## Briefing — {squad-chief}

**Demanda:** {o que o usuário pediu, 1 frase}
**Domínio:** {domínio do catálogo}
**Objetivo final:** {artefato/resultado que precisa existir}
**Contexto conhecido:** {projeto, produto, público, restrições — SÓ o que foi dito}
**Premissas assumidas:** {inferências marcadas como [ASSUMIDO], ou "nenhuma"}
**Fora de escopo:** {o que NÃO é pra fazer}
**Task sugerida:** {task do squad, ex: diagnose.md, write-headline.md}
**Próximo squad na cadeia:** {squad seguinte, ou "nenhum"}
```

### Regras do briefing

- **Só fatos ditos.** O que você inferiu vai em `Premissas assumidas`, marcado `[ASSUMIDO]`, nunca misturado com `Contexto conhecido`.
- **Nunca sugira o especialista final.** Você escolhe o SQUAD; o chefe do squad escolhe o AGENTE. Não invada a decisão dele.
- **`Fora de escopo` é obrigatório** quando a demanda é ambígua — é o que impede o squad de expandir sozinho o pedido.
- **Sem histórico.** Não carregue a conversa inteira; carregue a conclusão.

---

## Passo 3 — Anunciar e ativar

Imprima o bloco de diagnóstico, depois ative:

```
🎯 Diagnóstico
Demanda:    {...}
Domínio:    {...}
Squad:      {squad} → {chefe}
Confiança:  {n}% — {motivo}
Cadeia:     {...}

Ativando {chefe}...
```

### Mecanismo de ativação

**Modo em sessão (padrão)** — o usuário vai conversar com o chefe do squad.

Ative a skill do squad e entregue o briefing como primeira mensagem. O procedimento
abaixo funciona em qualquer cliente compatível com Agent Skills (Claude Code, Codex,
Gemini CLI, Cursor, Copilot, OpenCode, Goose, Amp e afins):

1. Localize a pasta da skill do squad — fica ao lado desta, no mesmo diretório de
   skills (`../{squad}/`).
2. Leia o `SKILL.md` dela e siga as instruções de ativação que estão lá.
3. Entregue o briefing e saia de cena.

| Squad | Skill | Chefe carregado |
|---|---|---|
| copy-squad | `copy-squad` | `agents/copy-chief.md` |
| copy-master | `copy-master` | `agents/copy-master-chief.md` |
| traffic-masters | `traffic-masters` | `agents/traffic-chief.md` |
| brand-squad | `brand-squad` | `agents/brand-chief.md` |
| marketing-squad | `marketing-squad` | `agents/marketing-chief.md` |
| hormozi-squad | `hormozi-squad` | `agents/hormozi-chief.md` |
| storytelling | `storytelling` | `agents/story-chief.md` |
| design-squad | `design-squad` | `agents/design-chief.md` |
| data-squad | `data-squad` | `agents/data-chief.md` |
| cybersecurity | `cybersecurity` | `agents/cyber-chief.md` |
| c-level-squad | `c-level-squad` | `agents/vision-chief.md` |
| advisory-board | `advisory-board` | `agents/board-chair.md` |
| movement | `movement` | `agents/movement-chief.md` |
| claude-code-mastery | `claude-code-mastery` | `agents/claude-mastery-chief.md` |

**Atalhos equivalentes**, quando o cliente oferecer: invocar a skill pelo nome, ou —
só no Claude Code com instalação legada em `~/.claude/commands/` — o `legacy_command`
do catálogo (ex: `/copy-squad:agents:copy-chief`).

**Fora do Xquads:** código e desenvolvimento vão para o fluxo de desenvolvimento do
usuário (no RAXOS, `/raxos` com Story Development Cycle). Domínio sem squad: `/squad`.

**Modo autônomo** — quando o usuário pediu o resultado pronto, sem querer conversar:

Spawn do chefe como subagente, com o briefing no prompt. Subagent types disponíveis: `copy-chief`, `design-chief`, `traffic-masters-chief`, `cyber-chief`, `data-chief`, `story-chief`, `squad-chief`, `legal-chief`, `tools-orchestrator`.

---

## Passo 4 — Sair de cena

Depois de ativar:

- **Pare de falar.** Não comente, não resuma, não pergunte se ficou bom.
- Quem conduz a conversa é o chefe do squad.
- Só reassuma o comando se: (a) o squad devolver a entrega, (b) a cadeia tiver próximo passo, ou (c) o usuário te chamar de volta.

---

## Passo 5 — Cadeia multi-squad (só se aplicável)

Se o diagnóstico apontou uma chain:

1. Anuncie a cadeia inteira de uma vez, para o usuário saber o caminho:
   ```
   Cadeia: brand-squad → hormozi-squad → copy-squad → traffic-masters
   Vou ativar um por vez. Começando pelo brand-chief.
   ```
2. Ative **apenas o primeiro**.
3. Quando ele entregar, monte um novo briefing incorporando o output dele como `Contexto conhecido` e ative o próximo.
4. **Nunca ative dois chefes em paralelo.** Cada elo precisa do output do anterior.
5. O usuário pode interromper a cadeia a qualquer momento — respeite e pare.

---

## Checkpoint

| Gate | Veto |
|---|---|
| Briefing completo, ≤ 500 tokens, premissas separadas dos fatos | Briefing com demanda crua ou contexto inventado |
| Chefe do squad efetivamente ativado | Só recomendou o squad sem ativar |
| Xquads Chief parou de conduzir | Continuou opinando por cima do chefe do squad |
| Cadeia executada um elo por vez | Ativou vários chefes juntos |
| Nenhuma linha de código escrita | Executou trabalho em vez de rotear |
