#!/usr/bin/env bash
# Bateria de testes do empacotamento do Xquads.
#
#   bash scripts/testar.sh
#
# Roda tudo em um HOME descartável: nao toca na instalacao real da maquina.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

SANDBOX="$(mktemp -d)"
trap 'rm -rf "$SANDBOX"' EXIT
mkdir -p "$SANDBOX/.claude" "$SANDBOX/.codex" "$SANDBOX/.gemini" \
         "$SANDBOX/.cursor" "$SANDBOX/.config/opencode"

falhas=0
verificar() {
  local nome="$1"; shift
  if eval "$@" >/dev/null 2>&1; then
    printf '  ok      %s\n' "$nome"
  else
    printf '  FALHOU  %s\n' "$nome"
    falhas=$((falhas + 1))
  fi
}
secao() { printf '\n%s\n' "$1"; }

secao "Instalador"
verificar "sintaxe valida"                 "bash -n install.sh"
verificar "roda no bash 3.2 do macOS"      "HOME='$SANDBOX' /bin/bash install.sh"
verificar "15 skills no hub"               "[ \$(ls '$SANDBOX/.agents/skills' | wc -l) -eq 15 ]"
# Clientes que precisam de symlink porque nao leem ~/.agents/skills.
for cliente in ".claude" ".config/opencode"; do
  verificar "cliente $cliente ligado"      "[ -L '$SANDBOX/$cliente/skills/xquads' ]"
done
# Codex, Gemini e Cursor leem o hub: o instalador NAO deve criar diretorio
# proprio para eles. Codex em especial nunca le ~/.codex/skills.
for cliente in ".codex" ".gemini" ".cursor"; do
  verificar "cliente $cliente sem pasta inutil" "[ ! -d '$SANDBOX/$cliente/skills' ]"
done
verificar "Codex acha as skills no hub"    "[ -f '$SANDBOX/.agents/skills/xquads/SKILL.md' ]"
SAIDA_CODEX="$(HOME="$SANDBOX" /bin/bash install.sh xquads 2>&1)"
verificar "saida anuncia o hub para o Codex" "printf '%s' \"\$SAIDA_CODEX\" | grep -q 'lê o hub direto'"
verificar "symlink entrega o conteudo"     "grep -q '^name: xquads' '$SANDBOX/.claude/skills/xquads/SKILL.md'"
verificar "hub entrega o conteudo"         "grep -q '^name: xquads' '$SANDBOX/.agents/skills/xquads/SKILL.md'"
verificar "idempotente na 2a execucao"     "HOME='$SANDBOX' /bin/bash install.sh && [ \$(ls '$SANDBOX/.claude/skills' | wc -l) -eq 15 ]"
verificar "instalacao seletiva"            "HOME='$SANDBOX' /bin/bash install.sh copy-squad brand-squad"
verificar "rejeita squad inexistente"      "! HOME='$SANDBOX' /bin/bash install.sh nao-existe"
verificar "rejeita flag desconhecida"      "! HOME='$SANDBOX' /bin/bash install.sh --xyz"
verificar "--list nao instala nada"        "HOME='$SANDBOX/vazio' /bin/bash install.sh --list && [ ! -d '$SANDBOX/vazio/.agents' ]"

secao "Preservacao do que nao e nosso"
PRESERVA="$(mktemp -d)"
mkdir -p "$PRESERVA/.claude/skills/movement"
echo alheio > "$PRESERVA/.claude/skills/movement/outro.txt"
HOME="$PRESERVA" /bin/bash install.sh movement >/dev/null 2>&1
verificar "skill de terceiro intacta"      "[ -f '$PRESERVA/.claude/skills/movement/outro.txt' ]"
verificar "hub recebeu mesmo assim"        "[ -f '$PRESERVA/.agents/skills/movement/SKILL.md' ]"
rm -rf "$PRESERVA"

secao "Desinstalacao"
HOME="$SANDBOX" /bin/bash install.sh >/dev/null 2>&1
HOME="$SANDBOX" /bin/bash install.sh --claude-commands copy-squad >/dev/null 2>&1
verificar "instalou o formato legado"      "[ -d '$SANDBOX/.claude/commands/copy-squad' ]"
HOME="$SANDBOX" /bin/bash install.sh --uninstall >/dev/null 2>&1
verificar "hub limpo"                      "[ \$(ls '$SANDBOX/.agents/skills' 2>/dev/null | wc -l) -eq 0 ]"
verificar "skills dos clientes limpas"     "[ \$(ls '$SANDBOX/.claude/skills' 2>/dev/null | wc -l) -eq 0 ]"
verificar "formato legado limpo"           "[ ! -d '$SANDBOX/.claude/commands/copy-squad' ]"
# Quem instalou a versao antiga ficou com ~/.codex/skills; a limpeza deve pegar.
mkdir -p "$SANDBOX/.codex/skills"
ln -s "$SANDBOX/.agents/skills/xquads" "$SANDBOX/.codex/skills/xquads" 2>/dev/null
HOME="$SANDBOX" /bin/bash install.sh >/dev/null 2>&1
HOME="$SANDBOX" /bin/bash install.sh --uninstall >/dev/null 2>&1
verificar "residuo de versao antiga limpo"  "[ ! -e '$SANDBOX/.codex/skills/xquads' ]"

secao "Modo projeto"
PROJETO="$(mktemp -d)"
( cd "$PROJETO" && /bin/bash "$REPO/install.sh" --project copy-squad >/dev/null 2>&1 )
verificar "gravou em .agents/skills"       "[ -f '$PROJETO/.agents/skills/copy-squad/SKILL.md' ]"
verificar "copia real, nao symlink"        "[ ! -L '$PROJETO/.agents/skills/copy-squad' ]"
rm -rf "$PROJETO"

secao "Skills"
verificar "validador aprova todas"         "python3 scripts/validar-skills.py"
verificar "um SKILL.md por squad"          "[ \$(ls */SKILL.md | wc -l) -eq 15 ]"
# Gerar duas vezes tem de produzir exatamente o mesmo byte a byte.
ANTES="$(cat */SKILL.md | shasum)"
python3 scripts/gerar-skills.py >/dev/null 2>&1
verificar "gerador e deterministico"       "[ \"\$(cat */SKILL.md | shasum)\" = '$ANTES' ]"

secao "Desacoplamento de cliente"
verificar "nenhum SKILL.md cita ~/.claude" "[ -z \"\$(grep -l '~/\\.claude' */SKILL.md 2>/dev/null)\" ]"
verificar "nenhum SKILL.md usa :agents:"   "! grep -q ':agents:' */SKILL.md"
verificar "AGENTS.md presente"             "[ -f AGENTS.md ]"
verificar "README sem instrucao de cp -r"  "! grep -q 'cp -r xquads-squads' README.md"
verificar "README cita Codex"              "grep -q 'Codex' README.md"

secao "Nenhum cliente apresentado como requisito"
# Alunos de Codex relataram ver o Xquads como se fosse exclusivo do Claude Code.
# A causa estava na documentacao voltada ao usuario, nao no codigo. Estas
# verificacoes impedem a volta.
verificar "xquads/README nao manda copiar p/ ~/.claude" "! grep -q 'cp -r.*\.claude/commands' xquads/README.md"
verificar "xquads/README sem requisito de cliente"      "! sed -n '/^## Requisitos/,/^## /p' xquads/README.md | grep -q 'claude/commands'"
verificar "xquads/README ensina o install.sh"           "grep -q 'install.sh' xquads/README.md"
verificar "READMEs citam o padrao aberto"               "grep -ql 'agentskills.io' README.md xquads/README.md claude-code-mastery/README.md"
# Slash command so pode aparecer dentro de um bloco marcado como legado.
verificar "ativacao legada esta rotulada"               "[ \$(grep -c 'legad' claude-code-mastery/README.md) -ge 1 ]"
verificar "nenhum README exige um cliente"              "! grep -rlE 'Claude Code \\(Anthropic|requer Claude|apenas para o Claude|somente no Claude' --include='README.md' ."

secao "Regressao — Claude Code legado"
verificar "command-entry.md preservado"    "[ -f xquads/command-entry.md ]"
verificar "14 squads com legacy_command"   "[ \$(grep -c '^    legacy_command:' xquads/data/routing-catalog.yaml) -eq 14 ]"
verificar "2 rotas externas no catalogo"   "[ \$(grep -c '^    command:' xquads/data/routing-catalog.yaml) -eq 2 ]"
verificar "14 rotas internas legadas"      "[ \$(sed -n '/^  internal:/,/^  external:/p' xquads/squad.yaml | grep -c 'legacy_command:') -eq 14 ]"
verificar "2 rotas externas com command"   "[ \$(sed -n '/^  external:/,\$p' xquads/squad.yaml | grep -c 'command:') -eq 2 ]"
verificar "nenhum 'command:' em internal"  "[ \$(sed -n '/^  internal:/,/^  external:/p' xquads/squad.yaml | grep -cE '^      command:') -eq 0 ]"

printf '\n'
if [ "$falhas" -eq 0 ]; then
  printf 'Todos os testes passaram.\n'
else
  printf '%d teste(s) falharam.\n' "$falhas"
fi
exit "$falhas"
