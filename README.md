# Xquads Squads

**As maiores mentes trabalhando para você.**

15 squads de agentes de IA especializados — **183 agentes** — com workflows, tasks e
checklists prontos para uso.

Distribuídos no padrão aberto **[Agent Skills](https://agentskills.io)**, então funcionam
no agente que você já usa: Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, VS Code,
OpenCode, Goose, Amp, Factory, Kiro, Roo Code e outros 30+ clientes compatíveis.

## Instalação

Um comando, em qualquer máquina:

```bash
bash <(curl -sL https://raw.githubusercontent.com/ohmyjahh/xquads-squads/main/install.sh)
```

O instalador detecta quais agentes você tem instalados e disponibiliza os squads em todos
eles de uma vez. Reinicie o agente e peça em linguagem natural:

> "usa o xquads pra montar a campanha de lançamento"

### Outras formas

```bash
bash install.sh --list                     # ver os squads disponíveis
bash install.sh copy-squad traffic-masters # instalar só o que interessa
bash install.sh --project                  # instalar neste projeto (.agents/skills)
bash install.sh --copy                     # copiar em vez de criar symlink
bash install.sh --uninstall                # remover
```

A instalação global usa `~/.agents/skills/` como fonte de verdade e liga os outros
clientes por symlink — atualizar uma vez atualiza todos.

> **Sobre o custo de contexto.** Todo agente carrega o nome e a descrição de cada skill
> instalada no início da sessão. Os 15 squads somam cerca de 2.400 tokens permanentes. Não é
> muito, mas se você só usa dois ou três, instale só esses — o chefe geral avisa quando uma
> rota não está instalada e sugere a alternativa mais próxima. O corpo completo de um squad
> (personas, tasks, workflows) só entra no contexto quando ele é de fato ativado.

A instalação por projeto grava em `.agents/skills/`. Commite essa pasta e o time inteiro
herda os squads junto com o repositório.

### Já usava pelos slash commands do Claude Code?

Continua funcionando, nada quebrou. Para reinstalar também nesse formato:

```bash
bash install.sh --claude-commands
```

## Comece por aqui: o Chefe Geral

Não precisa saber qual squad chamar. O **Xquads Chief (Xander 🎯)** é a porta de entrada
única: você descreve o problema em linguagem natural, ele identifica a atividade, escolhe o
squad e ativa o chefe dele com um briefing pronto.

```
Você descreve o problema
        │
        ▼
  DIAGNOSTICA ....... classifica o domínio e calcula a confiança
        │
        ├── confiança < 50% ──► UMA pergunta de desambiguação
        │
        ▼
  BRIEFA ............ handoff estruturado (máx. 500 tokens)
        │
        ▼
  ATIVA ............. o chefe do squad assume a conversa
```

Ele nunca executa o trabalho — só identifica e delega. Quando a demanda atravessa domínios,
monta uma cadeia multi-squad e ativa um elo por vez.

Detalhes em [`xquads/README.md`](xquads/README.md).

## Squads disponíveis

| Squad | Agentes | Foco |
|-------|---------|------|
| Advisory Board | 11 | Conselheiros estratégicos (Ray Dalio, Charlie Munger, Naval Ravikant...) |
| Brand Squad | 15 | Branding e posicionamento (David Aaker, Marty Neumeier, Al Ries...) |
| C-Level Squad | 6 | Liderança executiva (CEO, CTO, CMO, COO, CIO, CAIO) |
| Claude Code Mastery | 8 | Configuração de agentes: hooks, MCP, subagents, contexto |
| Copy Master | 33 | Copywriting 2.0 — persuasão, pitch, negociação, SaaS |
| Copy Squad | 23 | Copywriting (Gary Halbert, Eugene Schwartz, David Ogilvy...) |
| Cybersecurity | 15 | Segurança ofensiva e defensiva |
| Data Squad | 7 | Analytics, growth e comunidade (Sean Ellis, Avinash Kaushik...) |
| Design Squad | 8 | UX/UI e design systems (Brad Frost, Dan Mall...) |
| Hormozi Squad | 16 | Negócios e escala (frameworks Alex Hormozi) |
| Marketing Squad | 5 | Campanha integrada — o melhor de cada disciplina |
| Movement | 7 | Construção de movimentos e comunidades |
| Storytelling | 12 | Narrativa e storytelling (Joseph Campbell, Oren Klaff...) |
| Traffic Masters | 16 | Tráfego pago e mídia (Pedro Sobral, Kasim Aslam...) |
| Xquads Chief | 1 | Porta de entrada — diagnostica e roteia para o squad certo |

## Estrutura de cada squad

```
squad-name/
├── SKILL.md            # Ponto de entrada (padrão Agent Skills)
├── squad.yaml          # Manifesto: agentes, tasks, workflows
├── agents/             # Personas autocontidas
├── tasks/              # Tasks executáveis com inputs/outputs
├── workflows/          # Workflows multi-agente
├── checklists/         # Checklists de qualidade
├── config/             # Tiers, ícones e metadados
└── data/               # Frameworks e catálogos de referência
```

## Desenvolvimento

Os `SKILL.md` são **gerados**, não editados à mão:

```bash
python3 scripts/gerar-skills.py     # regera os 15 SKILL.md
python3 scripts/validar-skills.py   # valida contra a spec Agent Skills
```

Convenções para quem contribui estão em [`AGENTS.md`](AGENTS.md).

## Dashboard

Veja todos os agentes, bios e especialidades em
[xquads.vercel.app/xquads](https://xquads.vercel.app/xquads).

---

**Xquads by Synkra** · MIT
