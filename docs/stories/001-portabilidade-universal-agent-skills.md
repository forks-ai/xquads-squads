# Story 001 — Portabilidade universal do Xquads via Agent Skills

**Epic:** Distribuição do Xquads
**Status:** Done
**Criada em:** 2026-09-25
**Agente criador:** @mestre

---

## Descrição

Hoje o Xquads só é instalável no Claude Code. O README manda copiar os squads para
`~/.claude/commands/`, diretório que nenhuma outra ferramenta agêntica lê, e o roteamento
do Xquads Chief usa a sintaxe `/squad:agents:agente`, que é namespacing exclusivo do
Claude Code. Usuários de Codex, Gemini CLI, Cursor, Copilot e afins não conseguem instalar
nem usar nada.

O conteúdo em si (371 arquivos de personas, tasks, workflows, checklists e catálogos) é
markdown e YAML puros, portanto já portável. O bloqueio é exclusivamente de empacotamento
e distribuição.

A solução é adotar o padrão aberto **Agent Skills** (agentskills.io), publicado pela
Anthropic em dez/2025 e adotado por 40+ clientes agênticos, incluindo Codex, Gemini CLI,
Cursor, GitHub Copilot, VS Code, OpenCode, Goose, Amp, Factory e Kiro. Cada squad vira uma
skill: pasta com `SKILL.md` na raiz (frontmatter `name` + `description`) mais os diretórios
auxiliares que já existem.

## Valor de negócio

Multiplica o público instalável do Xquads. Hoje o produto está restrito a usuários de uma
única ferramenta; com a mudança passa a rodar em qualquer cliente compatível com Agent
Skills, sem reescrever conteúdo. Também elimina o atrito de instalação manual via `cp -r`,
substituído por um comando único.

## Critérios de aceite

- **AC1** — Cada um dos 15 squads tem um `SKILL.md` válido na raiz, com frontmatter
  contendo `name` (kebab-case, igual ao nome da pasta, máx. 64 chars) e `description`
  (máx. 1024 chars, descrevendo o que faz e quando usar).
- **AC2** — O `SKILL.md` de cada squad instrui a ativação de forma agnóstica de ferramenta:
  lê os arquivos por **caminho relativo à raiz da skill** (ex.: `agents/copy-chief.md`),
  nunca por path absoluto `~/.claude/...` nem por slash command `/squad:agents:x`.
- **AC3** — O `SKILL.md` do squad `xquads` (chefe geral) roteia para os outros squads sem
  depender de slash commands, degradando com aviso quando um squad não está instalado.
- **AC4** — Existe um `install.sh` na raiz do repo que: detecta quais clientes agênticos
  estão presentes na máquina, instala em `~/.agents/skills/` como fonte de verdade,
  e liga os demais destinos (`~/.claude/skills/`, `~/.codex/skills/`, `~/.gemini/skills/`,
  `~/.cursor/skills/`) por symlink.
- **AC5** — O instalador aceita instalação seletiva (`install.sh copy-squad brand-squad`)
  e instalação por projeto (`--project`, gravando em `.agents/skills/`).
- **AC6** — A instalação legada no Claude Code via `~/.claude/commands/` continua
  funcionando, sem quebrar quem já instalou.
- **AC7** — Existe um `AGENTS.md` na raiz do repo, para clientes que leem esse arquivo.
- **AC8** — O `README.md` documenta a instalação universal, lista as ferramentas
  compatíveis e substitui as instruções antigas de `cp -r`.
- **AC9** — Todos os `SKILL.md` gerados passam em validação automatizada das regras de
  frontmatter da spec (name kebab-case sem hífen inicial/final nem duplo, bate com o nome
  da pasta; description não vazia e dentro do limite).

## Escopo

### IN
- Geração dos 15 arquivos `SKILL.md` (um por squad)
- `install.sh` universal com detecção de clientes
- `AGENTS.md` na raiz
- Reescrita do `README.md` principal
- Correção dos paths absolutos e das referências a slash commands nos arquivos do squad
  `xquads` (`command-entry.md`, `agents/xquads-chief.md`, `tasks/route.md`,
  `tasks/diagnose.md`, `data/routing-catalog.yaml`, `squad.yaml`)
- Script de validação dos `SKILL.md`

### OUT
- Reescrever o conteúdo das personas, tasks e workflows dos squads (já é agnóstico)
- Alterar o squad `claude-code-mastery` no mérito do conteúdo (é sobre Claude Code por
  assunto, o que é legítimo)
- Alterar o dashboard Next.js em `~/Desktop/Projetos/xquads` (o ZIP de download é regerado
  em story separada)
- Publicar em registries de skills de terceiros
- `git push` ou deploy

## Dependências

- Nenhuma story anterior. Depende apenas da spec Agent Skills, já estável e pública.

## Complexidade

**M** — volume alto de arquivos, mas a transformação é mecânica e gerável por script.
O trabalho de julgamento se concentra em 6 arquivos do squad `xquads` e no `install.sh`.

## Riscos

| Risco | Severidade | Mitigação |
|---|---|---|
| Quebrar a instalação de quem já usa o Claude Code | Alta | Manter o caminho `~/.claude/commands/` intacto e aditivo; o instalador só acrescenta |
| Descrição de skill mal calibrada faz o agente ativar o squad errado | Média | Derivar a `description` do `squad.yaml` (domain + keywords), que já foi curado |
| Divergência entre `~/xquads-squads` e `~/Desktop/Projetos/xquads/squads` | Média | Aplicar no repo instalável (`~/xquads-squads`) e sincronizar em story separada |
| Cliente agêntico ignora symlink | Baixa | Fallback de cópia real no instalador quando o symlink falhar |
| Path com espaço ou `$HOME` não-padrão quebra o instalador | Baixa | Aspas em todas as expansões e `set -euo pipefail` |

## Critérios de Done

- [x] Os 15 `SKILL.md` existem e passam no validador
- [x] `install.sh` roda limpo em macOS com zsh e é idempotente (rodar 2x não duplica)
- [x] Instalação seletiva e `--project` funcionam
- [x] `AGENTS.md` e `README.md` atualizados
- [x] Zero path `~/.claude/` hardcoded fora do squad `claude-code-mastery`
- [x] Zero referência a `/squad:agents:` nas instruções de ativação agnósticas
- [x] Instalação legada em `~/.claude/commands/` verificada como intacta
- [x] Nada commitado sem revisão; nenhum push sem autorização explícita do dono

## File List

### Criados
- `install.sh` — instalador universal com deteccao de clientes
- `AGENTS.md` — instrucoes de repositorio para agentes
- `scripts/gerar-skills.py` — gerador dos SKILL.md a partir dos manifestos
- `scripts/validar-skills.py` — validador contra a spec Agent Skills
- `scripts/testar.sh` — suite de 33 testes do empacotamento
- `docs/stories/001-portabilidade-universal-agent-skills.md` — esta story
- `.gitignore` — artefatos de build e lixo de sistema
- `advisory-board/SKILL.md`
- `brand-squad/SKILL.md`
- `c-level-squad/SKILL.md`
- `claude-code-mastery/SKILL.md`
- `copy-master/SKILL.md`
- `copy-squad/SKILL.md`
- `cybersecurity/SKILL.md`
- `data-squad/SKILL.md`
- `design-squad/SKILL.md`
- `hormozi-squad/SKILL.md`
- `marketing-squad/SKILL.md`
- `movement/SKILL.md`
- `storytelling/SKILL.md`
- `traffic-masters/SKILL.md`
- `xquads/SKILL.md`

### Modificados
- `README.md` — instalacao universal, tabela de squads corrigida (183 agentes)
- `xquads/squad.yaml` — `command` -> `legacy_command` nas rotas internas
- `xquads/data/routing-catalog.yaml` — idem, mais nota de ativacao agnostica
- `xquads/agents/xquads-chief.md` — protocolo de ativacao sem slash command
- `xquads/tasks/route.md` — tabela de ativacao por skill
- `xquads/tasks/diagnose.md` — saida do diagnostico sem slash command
- `xquads/command-entry.md` — marcado como formato legado

### Nao modificados (intencionalmente)
- Os 183 arquivos de persona em `*/agents/` — ja eram agnosticos
- As tasks, workflows e checklists dos demais squads — ja eram agnosticas
- O conteudo de `claude-code-mastery/` — fala de Claude Code por assunto

## Achados fora de escopo

- `copy-master/data/persuasion-psychology.yaml` nao e YAML valido (linha 177:
  `sugarman_30_triggers` mistura mapping e sequence). **Pre-existente**, veio no
  commit dcb32f3. Registrado como tarefa separada, nao corrigido aqui por estar
  fora do escopo declarado desta story.

## QA Loop — iteração 1 (2026-09-27)

**Gatilho:** verificação da documentação oficial de cada cliente, após a publicação.

### Defeito

O instalador criava `~/.codex/skills/` e ligava os squads ali. **O Codex nunca lê esse
diretório.** A documentação da OpenAI lista apenas `.agents/skills` (projeto e repo),
`$HOME/.agents/skills` (pessoal) e `/etc/codex/skills` (admin).

Severidade: baixa. Não quebrava nada — o hub `~/.agents/skills` já era o caminho correto e
o Codex encontrava as skills por lá. O efeito era uma pasta órfã que nenhum cliente abre e
uma mensagem de sucesso enganosa ("✓ Codex" sugeria que o symlink era o que fazia funcionar).

Mesma imprecisão, menor, em Gemini CLI e Cursor: ambos leem o hub **e** o diretório próprio,
com o hub tendo precedência, então o symlink era redundante.

### Correção

- Tabela `DESTINOS` ganhou a coluna "já lê o hub". Quem lê não recebe diretório próprio;
  a saída passa a dizer `Codex — lê o hub direto`, que é o que de fato acontece.
- `DESTINOS_OBSOLETOS` mantém `~/.codex/skills`, `~/.gemini/skills` e `~/.cursor/skills` na
  rotina de desinstalação, para limpar o resíduo de quem instalou a versão anterior.
- README passou a explicar a diferença entre ler o hub e receber symlink, e documenta a
  invocação no Codex (`/skills`, `$copy-squad`).

### Testes

Suíte foi de 33 para 40 asserções. As novas cobrem: ausência das pastas inúteis, presença
das skills no hub, texto da saída, e limpeza do resíduo de versão antiga.

Um falso negativo apareceu e foi corrigido no próprio teste: `grep -q` fecha o pipe no
primeiro match e o SIGPIPE derrubava o `install.sh` sob `pipefail`. O teste agora captura a
saída antes de filtrar. Mesmo padrão já tinha me enganado uma vez com `head`.

### Verdict

**PASS** — 40/40.

## QA Results

**Gate:** PASS
**Agente:** @qualidade
**Data:** 2026-09-25

### 7 quality checks

| # | Check | Resultado |
|---|---|---|
| 1 | Code review | OK — leitura manual do `install.sh` e dos dois scripts Python. `shellcheck` e `ruff` não estão instalados nesta máquina, então o lint automatizado **não** foi executado. Ambos os Python compilam. |
| 2 | Testes | OK — 33/33 em `scripts/testar.sh`, rodando em HOME descartável no bash 3.2 do macOS. |
| 3 | Critérios de aceite | OK — AC1 a AC9 verificados um a um. |
| 4 | Regressões | OK — apenas 1 arquivo de persona alterado (`xquads-chief.md`, previsto). Zero tasks alteradas fora do squad `xquads`. Formato legado do Claude Code instala e desinstala. |
| 5 | Performance | OK com ressalva — ~2.382 tokens de metadados no startup com os 15 squads instalados. Documentado no README com recomendação de instalação seletiva. Todos os corpos de `SKILL.md` abaixo de 500 linhas (máx. 128). |
| 6 | Segurança | OK — `set -euo pipefail`; todo `rm -rf` blindado com `${var:?}`; zero expansão sem aspas; sem `eval`, sem pipe-to-shell, sem segredo hardcoded; diretório temporário removido no trap EXIT; guarda que preserva skills de terceiros com nome coincidente. |
| 7 | Documentação | OK — README, AGENTS.md e story atualizados; `command-entry.md` marcado como legado. |

### Issues

```yaml
issues:
  - severity: low
    category: tests
    description: "shellcheck e ruff ausentes na maquina — o lint estatico nao rodou"
    recommendation: "Instalar shellcheck e ruff e adicionar ambos a scripts/testar.sh"
  - severity: low
    category: code
    description: "Instalacao remota depende de git; nao ha fallback para tarball"
    recommendation: "Adicionar fallback via curl do tarball do GitHub quando git faltar"
  - severity: low
    category: performance
    description: "15 squads somam ~2.4k tokens de metadados permanentes no contexto"
    recommendation: "Mitigado por documentacao. Instalacao seletiva ja e suportada."
```

### Bloqueadores para a publicação (exigem commit e push, não autorizados)

1. **`marketing-squad/` nunca foi commitado.** Está untracked no local e ausente de
   `origin/main`. Consequência direta: a instalação remota (`curl | bash`, que clona o
   repositório) entrega **14 squads, não 15**, e a rota `marketing-squad` do chefe geral
   fica indisponível para todo mundo que instalar de fora desta máquina. Pré-existente.
2. **`.next/` está commitado no repositório público** — artefatos de build de um projeto
   Next.js que não pertencem a um repo de skills. Adicionado `.gitignore` e removido do
   índice; a remoção só vale após commit.

Nenhum dos dois foi introduzido por esta story, mas o primeiro invalida o AC4 na prática
para usuários remotos. A story fica Done quanto ao código; a **publicação** depende de
autorização do dono para commit e push.

### Fora do escopo desta story

- `copy-master/data/persuasion-psychology.yaml` não é YAML válido. **Pré-existente**
  (commit dcb32f3), não introduzido aqui. Registrado como tarefa separada. A suíte de
  testes atual não valida os YAML de `data/` — a tarefa separada cobre isso também.

### Pendente de autorização do dono

- Nada foi commitado. Nada foi enviado. A instalação **não** foi executada no ambiente
  real do usuário — todos os testes rodaram em HOME descartável.

## Change Log

| Data | Agente | Ação |
|---|---|---|
| 2026-09-25 | @mestre | Story criada (Draft) |
| 2026-09-25 | @produto | Validação 10/10 — GO. Status Draft -> Ready |
| 2026-09-25 | @desenvolvedor | Implementação concluída. 33 testes passando. Status Ready -> InReview |
| 2026-09-25 | @qualidade | QA gate PASS (7/7, 3 issues low). Status InReview -> Done |
| 2026-09-25 | @devops | Publicado em origin/main (b4610d0) com autorização do dono |
| 2026-09-27 | @qualidade | QA loop it.1: destinos do instalador imprecisos (Codex não lê ~/.codex/skills) |
| 2026-09-27 | @desenvolvedor | Correção aplicada. Suíte 33 -> 40 asserções |
| 2026-09-27 | @qualidade | Re-review PASS (40/40) |
