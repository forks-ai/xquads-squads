---
name: cybersecurity
description: >-
  Squad de 15 agentes de seguranca ofensiva e defensiva (Georgia Weidman, Peter Kim, Jim Manico,
  Chris Sanders, Omar Santos, Marcus Carey) cobrindo pentest, red team, blue team, AppSec, recon e
  resposta a incidente. Use SOMENTE em contexto autorizado: teste de intrusao contratado, CTF,
  pesquisa de seguranca ou defesa da propria infraestrutura. Gatilhos: pentest, vulnerabilidade,
  OWASP, recon, hardening, incidente de seguranca, auditoria de seguranca, CVE, exploit, blue
  team, red team.
license: MIT
metadata:
  squad: "Cybersecurity Squad"
  version: "1.0.0"
  agents: "15"
  author: "Xquads by Synkra"
---

# Cybersecurity Squad

**Dominio:** Offensive & Defensive Security Operations

> **Uso autorizado apenas.** Este squad cobre tecnicas ofensivas. Ative somente em pentest contratado, CTF, pesquisa de seguranca ou defesa de infraestrutura propria. Confirme o contexto de autorizacao antes de executar qualquer operacao ofensiva.

## Como ativar

Todos os caminhos abaixo sao **relativos a raiz desta skill**. Leia os arquivos diretamente do disco com a ferramenta de leitura do seu ambiente. Nao existe dependencia de slash command, de plugin ou de qualquer cliente especifico.

1. Leia `agents/cyber-chief.md` por completo. E a definicao autocontida do chefe do
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

**Chefe do squad** — `agents/cyber-chief.md`

**Especialistas (14)**

- `agents/busterer.md`
- `agents/cartographer.md`
- `agents/chris-sanders.md`
- `agents/command-generator.md`
- `agents/dirber.md`
- `agents/fuzzer.md`
- `agents/georgia-weidman.md`
- `agents/jim-manico.md`
- `agents/marcus-carey.md`
- `agents/omar-santos.md`
- `agents/peter-kim.md`
- `agents/ripper.md`
- `agents/rogue.md`
- `agents/shannon-runner.md`

## Tasks (9)

- `tasks/analyze-vulnerability.md`
- `tasks/assess-security.md`
- `tasks/audit-app-security.md`
- `tasks/diagnose.md`
- `tasks/generate-commands.md`
- `tasks/respond-incident.md`
- `tasks/review.md`
- `tasks/run-pentest.md`
- `tasks/run-recon.md`

## Workflows (2)

Sequencias multi-agente ja encadeadas. Siga as fases na ordem declarada.

- `workflows/wf-incident-response.yaml`
- `workflows/wf-pentest-engagement.yaml`

## Checklists

Rode antes de entregar. Nao declare a entrega pronta com item em aberto.

- `checklists/output-quality.md`

## Dados de referencia

- `data/routing-catalog.yaml`
- `data/security-tools-catalog.yaml`

## Convencoes

- Comandos do agente usam o prefixo `*` (`*help`, `*exit`, e os declarados na persona).
- Responda em portugues (pt-BR), salvo pedido explicito em contrario.
- O chefe do squad nao executa o trabalho do especialista: ele diagnostica e delega.
- Um agente por vez. Troca de agente encerra a persona anterior.

---

*Parte do [Xquads](https://github.com/ohmyjahh/xquads-squads) — Agent Skills padrao aberto.*
