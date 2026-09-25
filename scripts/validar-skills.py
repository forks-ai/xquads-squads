#!/usr/bin/env python3
"""
Valida os SKILL.md do repositorio contra a spec Agent Skills (agentskills.io).

    python3 scripts/validar-skills.py

Checa apenas o que a spec define como obrigatorio, mais as invariantes que o
Xquads assume: caminhos relativos e ausencia de acoplamento a um cliente.
Sai com codigo 1 se algo falhar, para uso em CI.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

MAX_NOME = 64
MAX_DESCRICAO = 1024
RE_NOME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Squads cujo conteudo fala de um cliente especifico por assunto, nao por
# acoplamento estrutural.
ISENTOS_DE_MENCAO = {"claude-code-mastery"}


def frontmatter(texto: str) -> tuple[dict[str, str], int] | None:
    """Extrai os escalares de primeiro nivel do frontmatter. Sem dependencias."""
    if not texto.startswith("---\n"):
        return None
    fim = texto.find("\n---\n", 4)
    if fim == -1:
        return None
    bruto = texto[4:fim]
    campos: dict[str, str] = {}
    chave: str | None = None
    for linha in bruto.split("\n"):
        if not linha.strip():
            continue
        m = re.match(r"^([a-zA-Z][\w-]*):\s*(.*)$", linha)
        if m:
            chave = m.group(1)
            valor = m.group(2).strip()
            campos[chave] = "" if valor in {">-", "|", ">", "|-"} else valor.strip("\"'")
        elif chave and linha.startswith((" ", "\t")):
            trecho = linha.strip()
            # Ignora os sub-campos de `metadata`, que sao um mapa aninhado.
            if not re.match(r"^[a-zA-Z][\w-]*:", trecho) or chave == "description":
                campos[chave] = (campos.get(chave, "") + " " + trecho).strip()
    return campos, texto[fim + 5:].count("\n")


def validar(skill: Path) -> list[str]:
    erros: list[str] = []
    arquivo = skill / "SKILL.md"
    texto = arquivo.read_text(encoding="utf-8")

    analisado = frontmatter(texto)
    if analisado is None:
        return ["frontmatter YAML ausente ou nao delimitado por ---"]
    campos, linhas_corpo = analisado

    # ── name ────────────────────────────────────────────────────────────────
    nome = campos.get("name", "")
    if not nome:
        erros.append("campo obrigatorio `name` ausente")
    else:
        if len(nome) > MAX_NOME:
            erros.append(f"`name` tem {len(nome)} chars (maximo {MAX_NOME})")
        if not RE_NOME.match(nome):
            erros.append(
                f"`name` = {nome!r}: so minusculas, numeros e hifens simples, "
                "sem hifen inicial, final ou duplo"
            )
        if nome != skill.name:
            erros.append(f"`name` = {nome!r} difere do nome da pasta {skill.name!r}")

    # ── description ─────────────────────────────────────────────────────────
    descricao = campos.get("description", "")
    if not descricao:
        erros.append("campo obrigatorio `description` ausente ou vazio")
    elif len(descricao) > MAX_DESCRICAO:
        erros.append(f"`description` tem {len(descricao)} chars (maximo {MAX_DESCRICAO})")

    # ── corpo ───────────────────────────────────────────────────────────────
    if linhas_corpo > 500:
        erros.append(f"corpo com {linhas_corpo} linhas (recomendado ate 500)")

    corpo = texto[texto.find("\n---\n", 4) + 5:]

    # ── invariantes do Xquads ───────────────────────────────────────────────
    if "~/.claude" in corpo and skill.name not in ISENTOS_DE_MENCAO:
        erros.append("corpo cita `~/.claude` — o caminho de ativacao deve ser relativo")

    for slash in re.findall(r"`?/[a-z][a-z0-9-]*:agents:[a-z-]+`?", corpo):
        if "legacy" not in corpo[max(0, corpo.find(slash) - 200):corpo.find(slash)]:
            erros.append(f"corpo cita o slash command {slash} fora de contexto legado")

    # Todo caminho citado entre crases deve existir na skill.
    for ref in set(re.findall(r"`((?:agents|tasks|workflows|checklists|data)/[^`]+)`", corpo)):
        if "<" in ref or "{" in ref:  # placeholder, nao caminho literal
            continue
        if not (skill / ref).exists():
            erros.append(f"referencia quebrada: {ref}")

    return erros


def main() -> int:
    skills = sorted(p.parent for p in RAIZ.glob("*/SKILL.md"))
    if not skills:
        print("ERRO: nenhum SKILL.md encontrado", file=sys.stderr)
        return 1

    falhas = 0
    for skill in skills:
        erros = validar(skill)
        if erros:
            falhas += 1
            print(f"FALHOU  {skill.name}")
            for e in erros:
                print(f"          {e}")
        else:
            print(f"ok      {skill.name}")

    print()
    if falhas:
        print(f"{falhas} de {len(skills)} skills com problema.")
        return 1
    print(f"{len(skills)} skills validas conforme a spec Agent Skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
