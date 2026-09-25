---
name: claude-code-mastery
description: >-
  Squad de 8 agentes especializados em dominar ferramentas agenticas de desenvolvimento: hooks,
  skills, subagents, MCP, plugins, times de agentes, engenharia de contexto e integracao com
  projetos existentes. Use para configurar o ambiente do agente, auditar settings e permissoes,
  desenhar hooks, planejar integracao de MCP, escrever arquivos de instrucao do projeto, decompor
  trabalho em paralelo e reduzir context rot. Gatilhos: hooks, MCP, subagent, skill, plugin,
  settings, permissoes, CLAUDE.md, AGENTS.md, context rot, worktree, configuracao do agente.
license: MIT
metadata:
  squad: "Claude Code Mastery Squad"
  version: "1.0.0"
  agents: "8"
  author: "Xquads by Synkra"
---

# Claude Code Mastery Squad

**Dominio:** Claude Code — Full Spectrum Expertise

## Como ativar

Todos os caminhos abaixo sao **relativos a raiz desta skill**. Leia os arquivos diretamente do disco com a ferramenta de leitura do seu ambiente. Nao existe dependencia de slash command, de plugin ou de qualquer cliente especifico.

1. Leia `agents/claude-mastery-chief.md` por completo. E a definicao autocontida do chefe do
   squad: persona, principios, logica de roteamento e limites. Adote-a.
2. Carregue `data/mcp-integration-catalog.yaml` como contexto de roteamento. Nao exiba o conteudo,
   apenas absorva.
3. Cumprimente com o `greeting` da persona e aguarde a demanda.
4. Ao rotear para um especialista, leia `agents/<especialista>.md` e assuma
   aquela persona, mantendo o briefing que o chefe montou.
5. Permaneca no squad ate receber `*exit`.

## Executando uma task

As tasks em `tasks/` sao roteiros executaveis com entradas, passos e formato de saida definidos. Leia o arquivo inteiro antes de comecar e siga os passos na ordem. Tasks marcadas com `elicit: true` exigem resposta do usuario em cada ponto de elicitacao — nao presuma respostas nem pule etapas.

## Agentes

**Chefe do squad** — `agents/claude-mastery-chief.md`

**Especialistas (7)**

- `agents/config-engineer.md`
- `agents/hooks-architect.md`
- `agents/mcp-integrator.md`
- `agents/project-integrator.md`
- `agents/roadmap-sentinel.md`
- `agents/skill-craftsman.md`
- `agents/swarm-orchestrator.md`

## Tasks (26)

- `tasks/audit-integration.md`
- `tasks/audit-settings.md`
- `tasks/audit-setup.md`
- `tasks/brownfield-setup.md`
- `tasks/ci-cd-setup.md`
- `tasks/claude-md-engineer.md`
- `tasks/configure-claude-code.md`
- `tasks/context-rot-audit.md`
- `tasks/create-agent-definition.md`
- `tasks/create-rules.md`
- `tasks/create-team-topology.md`
- `tasks/diagnose.md`
- `tasks/enterprise-config.md`
- `tasks/hook-designer.md`
- `tasks/integrate-project.md`
- `tasks/mcp-integration-plan.md`
- `tasks/mcp-workflow.md`
- `tasks/multi-project-setup.md`
- `tasks/optimize-context.md`
- `tasks/optimize-workflow.md`
- `tasks/parallel-decomposition.md`
- `tasks/permission-strategy.md`
- `tasks/sandbox-setup.md`
- `tasks/setup-repository.md`
- `tasks/setup-wizard.md`
- `tasks/worktree-strategy.md`

## Workflows (3)

Sequencias multi-agente ja encadeadas. Siga as fases na ordem declarada.

- `workflows/wf-audit-complete.yaml`
- `workflows/wf-knowledge-update.yaml`
- `workflows/wf-project-setup.yaml`

## Checklists

Rode antes de entregar. Nao declare a entrega pronta com item em aberto.

- `checklists/agent-team-readiness-checklist.md`
- `checklists/brownfield-readiness-checklist.md`
- `checklists/change-checklist.md`
- `checklists/context-rot-checklist.md`
- `checklists/integration-audit-checklist.md`
- `checklists/multi-agent-review-checklist.md`
- `checklists/pre-push-checklist.md`

## Dados de referencia

- `data/ci-cd-patterns.yaml`
- `data/claude-code-quick-ref.yaml`
- `data/hook-patterns.yaml`
- `data/mcp-integration-catalog.yaml`
- `data/project-type-signatures.yaml`

## Convencoes

- Comandos do agente usam o prefixo `*` (`*help`, `*exit`, e os declarados na persona).
- Responda em portugues (pt-BR), salvo pedido explicito em contrario.
- O chefe do squad nao executa o trabalho do especialista: ele diagnostica e delega.
- Um agente por vez. Troca de agente encerra a persona anterior.

---

*Parte do [Xquads](https://github.com/ohmyjahh/xquads-squads) — Agent Skills padrao aberto.*
