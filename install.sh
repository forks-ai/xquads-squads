#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# Xquads — instalador universal
#
# Instala os squads como Agent Skills (padrão aberto agentskills.io) e os
# disponibiliza em todos os clientes agênticos presentes na máquina:
# Claude Code, Codex, Gemini CLI, Cursor, OpenCode, Factory, Goose e afins.
#
# Uso:
#   bash <(curl -sL https://raw.githubusercontent.com/ohmyjahh/xquads-squads/main/install.sh)
#   bash install.sh                        # instala todos os squads
#   bash install.sh copy-squad brand-squad # instala só os squads indicados
#   bash install.sh --project              # instala em ./.agents/skills (este projeto)
#   bash install.sh --list                 # lista os squads disponíveis
#   bash install.sh --claude-commands      # instala também o formato legado
#                                          #   de slash command do Claude Code
#   bash install.sh --copy                 # copia em vez de criar symlink
#   bash install.sh --uninstall            # remove os links criados
# ═══════════════════════════════════════════════════════════════════════════
set -euo pipefail

REPO="https://github.com/ohmyjahh/xquads-squads.git"

# Fonte de verdade das skills: o diretório neutro do padrão Agent Skills.
# Os demais clientes apontam para cá por symlink, então atualizar uma vez
# atualiza todo mundo.
HUB="$HOME/.agents/skills"

# Destinos por cliente. Cada linha: "rótulo|marcador de presença|diretório de skills".
# O marcador é o que denuncia que o cliente está instalado nesta máquina.
DESTINOS=(
  "Claude Code|$HOME/.claude|$HOME/.claude/skills"
  "Codex|$HOME/.codex|$HOME/.codex/skills"
  "Gemini CLI|$HOME/.gemini|$HOME/.gemini/skills"
  "Cursor|$HOME/.cursor|$HOME/.cursor/skills"
  "OpenCode|$HOME/.config/opencode|$HOME/.config/opencode/skills"
  "Factory|$HOME/.factory|$HOME/.factory/skills"
  "Goose|$HOME/.config/goose|$HOME/.config/goose/skills"
  "Amp|$HOME/.amp|$HOME/.amp/skills"
  "Kiro|$HOME/.kiro|$HOME/.kiro/skills"
  "Roo Code|$HOME/.roo|$HOME/.roo/skills"
  "Trae|$HOME/.trae|$HOME/.trae/skills"
)

MODO_PROJETO=0
MODO_COPIA=0
CLAUDE_COMMANDS=0
DESINSTALAR=0
SELECIONADOS=()  # nomes passados na linha de comando

# ── Saída ──────────────────────────────────────────────────────────────────
if [ -t 1 ]; then
  VERDE=$'\033[32m'; AMARELO=$'\033[33m'; CINZA=$'\033[90m'
  NEGRITO=$'\033[1m'; FIM=$'\033[0m'
else
  VERDE=""; AMARELO=""; CINZA=""; NEGRITO=""; FIM=""
fi
ok()    { printf '  %s✓%s %s\n' "$VERDE" "$FIM" "$1"; }
aviso() { printf '  %s!%s %s\n' "$AMARELO" "$FIM" "$1"; }
nota()  { printf '  %s%s%s\n' "$CINZA" "$1" "$FIM"; }
erro()  { printf 'ERRO: %s\n' "$1" >&2; exit 1; }

ajuda() {
  cat <<'AJUDA'
Xquads — instalador universal

Instala os squads como Agent Skills (padrão aberto agentskills.io) e os
disponibiliza em todos os clientes agênticos presentes na máquina:
Claude Code, Codex, Gemini CLI, Cursor, OpenCode, Factory, Goose e afins.

Uso:
  bash install.sh                        instala todos os squads
  bash install.sh copy-squad brand-squad instala só os squads indicados
  bash install.sh --list                 lista os squads disponíveis
  bash install.sh --project              instala em ./.agents/skills (este projeto)
  bash install.sh --copy                 copia em vez de criar symlink
  bash install.sh --claude-commands      instala também o formato legado de
                                         slash command do Claude Code
  bash install.sh --uninstall            remove o que foi instalado

Instalação remota, sem clonar:
  bash <(curl -sL https://raw.githubusercontent.com/ohmyjahh/xquads-squads/main/install.sh)
AJUDA
}

# ── Argumentos ─────────────────────────────────────────────────────────────
for arg in "$@"; do
  case "$arg" in
    --project|-p)        MODO_PROJETO=1 ;;
    --copy)              MODO_COPIA=1 ;;
    --claude-commands)   CLAUDE_COMMANDS=1 ;;
    --uninstall)         DESINSTALAR=1 ;;
    --list|-l)           LISTAR=1 ;;
    --help|-h)           ajuda; exit 0 ;;
    -*)                  erro "opção desconhecida: $arg (use --help)" ;;
    *)                   SELECIONADOS+=("$arg") ;;
  esac
done

# ── Origem: repo local se já estiver clonado, senão clona num temporário ───
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -d "$AQUI/xquads" ] && [ -f "$AQUI/xquads/squad.yaml" ]; then
  ORIGEM="$AQUI"
else
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  printf '  clonando o repositório...\n'
  git clone --depth 1 "$REPO" "$TMP/xquads-squads" >/dev/null 2>&1 \
    || erro "não consegui clonar $REPO — verifique a conexão e se o git está instalado"
  ORIGEM="$TMP/xquads-squads"
fi

# Um squad é toda pasta com SKILL.md na raiz.
# Sem mapfile: precisa rodar no bash 3.2 que o macOS ainda entrega em /bin/bash.
DISPONIVEIS=()
while IFS= read -r nome; do
  [ -n "$nome" ] && DISPONIVEIS+=("$nome")
done < <(
  find "$ORIGEM" -maxdepth 2 -name SKILL.md -not -path '*/.git/*' \
    -exec dirname {} \; | while IFS= read -r d; do basename "$d"; done | sort
)
[ ${#DISPONIVEIS[@]} -gt 0 ] || erro "nenhum SKILL.md encontrado em $ORIGEM — rode scripts/gerar-skills.py primeiro"

if [ "${LISTAR:-0}" = "1" ]; then
  printf '%sSquads disponíveis (%d):%s\n\n' "$NEGRITO" "${#DISPONIVEIS[@]}" "$FIM"
  for s in "${DISPONIVEIS[@]}"; do
    desc=$(sed -n '/^description:/,/^[a-z]/p' "$ORIGEM/$s/SKILL.md" \
           | sed '1d;$d' | tr -d '\n' | sed 's/  */ /g' | cut -c1-90)
    printf '  %-22s %s...\n' "$s" "${desc# }"
  done
  exit 0
fi

# Nada especificado = tudo.
if [ ${#SELECIONADOS[@]} -eq 0 ]; then
  SQUADS=("${DISPONIVEIS[@]}")
else
  SQUADS=()
  for s in ${SELECIONADOS[@]+"${SELECIONADOS[@]}"}; do
    encontrado=0
    for d in "${DISPONIVEIS[@]}"; do [ "$s" = "$d" ] && encontrado=1 && break; done
    [ "$encontrado" = "1" ] || erro "squad desconhecido: $s (use --list para ver os disponíveis)"
    SQUADS+=("$s")
  done
fi

# ── Desinstalação ──────────────────────────────────────────────────────────
if [ "$DESINSTALAR" = "1" ]; then
  printf '\n%sRemovendo o Xquads%s\n\n' "$NEGRITO" "$FIM"
  for squad in "${SQUADS[@]}"; do
    for linha in "${DESTINOS[@]}"; do
      IFS='|' read -r _ _ dir <<< "$linha"
      alvo="${dir:?}/${squad:?}"
      # Só remove o que aponta para o hub ou o próprio hub — nunca toca em
      # skills de terceiros que por acaso tenham o mesmo nome.
      if [ -L "$alvo" ]; then
        destino_link="$(readlink "$alvo")"
        case "$destino_link" in
          "$HUB"/*|*/.agents/skills/*) rm -f "$alvo" ;;
        esac
      fi
    done
    rm -rf "${HUB:?}/$squad"
    # Formato legado de slash command, quando foi instalado por nos.
    legado="$HOME/.claude/commands/${squad:?}"
    [ -f "$legado/SKILL.md" ] && rm -rf "$legado"
  done
  [ -f "$HOME/.claude/commands/xquads.md" ] && [ ! -d "$HOME/.claude/commands/xquads" ] \
    && rm -f "$HOME/.claude/commands/xquads.md"
  ok "removido"
  exit 0
fi

# ── Instalação por projeto ─────────────────────────────────────────────────
if [ "$MODO_PROJETO" = "1" ]; then
  DIR_PROJETO="$PWD/.agents/skills"
  printf '\n%sInstalando no projeto%s  %s\n\n' "$NEGRITO" "$FIM" "$DIR_PROJETO"
  mkdir -p "$DIR_PROJETO"
  for squad in "${SQUADS[@]}"; do
    rm -rf "${DIR_PROJETO:?}/$squad"
    cp -R "$ORIGEM/$squad" "$DIR_PROJETO/$squad"
    ok "$squad"
  done
  printf '\n'
  nota "Commite .agents/skills/ para o time inteiro herdar os squads."
  exit 0
fi

# ── Instalação global ──────────────────────────────────────────────────────
printf '\n%sXquads — instalação universal%s\n\n' "$NEGRITO" "$FIM"

mkdir -p "$HUB"
printf '%sSkills%s  %s\n' "$NEGRITO" "$FIM" "$HUB"
for squad in "${SQUADS[@]}"; do
  rm -rf "${HUB:?}/$squad"
  cp -R "$ORIGEM/$squad" "$HUB/$squad"
  ok "$squad"
done

# Liga cada cliente detectado ao hub.
printf '\n%sClientes%s\n' "$NEGRITO" "$FIM"
detectados=0
for linha in "${DESTINOS[@]}"; do
  IFS='|' read -r rotulo marcador dir <<< "$linha"
  [ -d "$marcador" ] || continue
  detectados=$((detectados + 1))
  mkdir -p "$dir"
  falhas=0
  for squad in "${SQUADS[@]}"; do
    alvo="${dir:?}/${squad:?}"
    # Preserva o que não foi instalado por nós: só substituímos um symlink
    # nosso ou um diretório que já veio de uma instalação anterior do Xquads.
    if [ -e "$alvo" ] && [ ! -L "$alvo" ] && [ ! -f "$alvo/SKILL.md" ]; then
      falhas=$((falhas + 1)); continue
    fi
    rm -rf "$alvo"
    if [ "$MODO_COPIA" = "1" ]; then
      cp -R "$HUB/$squad" "$alvo"
    else
      ln -s "$HUB/$squad" "$alvo" 2>/dev/null || cp -R "$HUB/$squad" "$alvo"
    fi
  done
  if [ "$falhas" -gt 0 ]; then
    aviso "$rotulo — $((${#SQUADS[@]} - falhas))/${#SQUADS[@]} (pulei $falhas já existentes)"
  else
    ok "$rotulo"
  fi
done

if [ "$detectados" -eq 0 ]; then
  aviso "nenhum cliente detectado — as skills ficaram em $HUB"
  nota "Aponte seu agente para esse diretório, ou rode de novo depois de instalar um cliente."
fi

# ── Formato legado do Claude Code (slash commands) ─────────────────────────
if [ "$CLAUDE_COMMANDS" = "1" ]; then
  COMANDOS="$HOME/.claude/commands"
  printf '\n%sSlash commands do Claude Code (legado)%s\n' "$NEGRITO" "$FIM"
  mkdir -p "$COMANDOS"
  for squad in "${SQUADS[@]}"; do
    rm -rf "${COMANDOS:?}/$squad"
    cp -R "$ORIGEM/$squad" "$COMANDOS/$squad"
  done
  [ -f "$ORIGEM/xquads/command-entry.md" ] \
    && cp "$ORIGEM/xquads/command-entry.md" "$COMANDOS/xquads.md"
  ok "$COMANDOS"
fi

# ── Fechamento ─────────────────────────────────────────────────────────────
printf '\n%s%d squads instalados.%s\n\n' "$NEGRITO" "${#SQUADS[@]}" "$FIM"
printf 'Reinicie seu agente e peça por um squad em linguagem natural.\n'
printf 'Ex.: %s"usa o xquads pra montar a campanha de lançamento"%s\n\n' "$CINZA" "$FIM"
