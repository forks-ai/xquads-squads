#!/usr/bin/env python3
"""
Gera o SKILL.md de cada squad do Xquads no padrao Agent Skills (agentskills.io).

Executa a partir da raiz do repositorio:
    python3 scripts/gerar-skills.py

Cada squad vira uma skill autocontida: a pasta ja tem agents/, tasks/, workflows/,
checklists/, config/ e data/ — falta apenas o SKILL.md na raiz, que e o ponto de
entrada lido por qualquer cliente compativel (Claude Code, Codex, Gemini CLI,
Cursor, Copilot, OpenCode, Goose, Amp, Factory, Kiro e afins).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────────────────────
# Descricoes de ativacao.
#
# A description e o unico texto que o agente le no startup para decidir se a
# skill e relevante. Por isso ela diz o que o squad faz E os gatilhos concretos
# que devem ativa-lo. Limite da spec: 1024 caracteres.
# ─────────────────────────────────────────────────────────────────────────────
DESCRICOES = {
    "xquads": (
        "Porta de entrada unica do Xquads: diagnostica a demanda em linguagem natural, "
        "identifica o dominio e ativa o squad certo entre os 14 disponiveis. Use quando o "
        "usuario pedir ajuda com marketing, copy, trafego, marca, oferta, narrativa, design, "
        "dados, seguranca, estrategia ou movimento mas nao souber qual especialista chamar, "
        "quando disser 'xquads', 'chama o time', 'monta o squad', ou quando a demanda "
        "atravessar varios dominios e precisar de uma cadeia multi-squad."
    ),
    "copy-squad": (
        "Squad de 23 copywriters lendarios (Gary Halbert, Eugene Schwartz, David Ogilvy, "
        "Dan Kennedy, Joe Sugarman e outros) com um chefe que roteia pela combinacao de midia, "
        "nivel de consciencia do mercado e objetivo. Use para escrever ou revisar headline, "
        "carta de vendas, roteiro de VSL, sequencia de email, copy de anuncio, landing page, "
        "bullets, copy de funil e arquitetura de oferta; tambem para critica e diagnostico de "
        "copy existente. Gatilhos: copy, copywriting, headline, VSL, carta de vendas, email "
        "marketing, anuncio, pagina de vendas, oferta, fascinations."
    ),
    "copy-master": (
        "Versao 2.0 do Copy Squad com 33 agentes: os copywriters classicos mais especialistas "
        "em persuasao, negociacao, pitch e copy de SaaS (Robert Cialdini, Chris Voss, Oren Klaff, "
        "Joanna Wiebe, Sabri Suby, Alex Hormozi). Use quando a demanda de copy exigir profundidade "
        "extra em psicologia da persuasao, negociacao, pitch deck, roteiro de webinario ou copy de "
        "produto SaaS, ou quando o Copy Squad basico ficar curto. Gatilhos: persuasao, pitch, "
        "negociacao, webinario, copy de SaaS, gatilhos mentais, storytelling de vendas."
    ),
    "traffic-masters": (
        "Squad de 16 especialistas em trafego pago (Pedro Sobral, Kasim Aslam, Molly Pittman, "
        "Depesh Mandalia, Ralph Burns, Tom Breeze, Nicholas Kusmich) cobrindo Meta Ads, Google Ads, "
        "YouTube Ads, media buying, analise de criativos, escala e tracking. Use para montar "
        "estrategia de campanha, auditar conta de anuncios, criar criativos, analisar performance, "
        "gerir orcamento, escalar campanha e configurar rastreamento. Gatilhos: trafego pago, "
        "Meta Ads, Facebook Ads, Google Ads, ROAS, CPA, CPM, pixel, escala, media buyer, criativo."
    ),
    "brand-squad": (
        "Squad de 15 agentes de estrategia de marca (David Aaker, Marty Neumeier, Al Ries, "
        "Byron Sharp, Jean-Noel Kapferer, Kevin Keller, Donald Miller, Emily Heyward, Alina Wheeler, "
        "Denise Yohn) mais especialistas em naming, arquetipos e dominio. Use para posicionamento, "
        "auditoria de marca, identidade visual e verbal, arquitetura de marca, historia de marca, "
        "mapeamento de arquetipo e geracao de nomes. Gatilhos: marca, branding, posicionamento, "
        "naming, identidade, arquetipo, brand equity, tagline, proposito de marca."
    ),
    "marketing-squad": (
        "Squad enxuto que reune o melhor agente de cada disciplina de marketing: mensagem "
        "(Donald Miller/StoryBrand), copy (Eugene Schwartz), trafego (Pedro Sobral) e criativos. "
        "Use para campanha integrada ponta a ponta, quando a demanda atravessa mensagem, copy, "
        "criativo e midia paga ao mesmo tempo e nao vale abrir um squad especializado para cada "
        "etapa. Gatilhos: campanha, marketing integrado, lancamento, funil completo, "
        "mensagem de marca, one-liner, StoryBrand."
    ),
    "hormozi-squad": (
        "Squad de 16 agentes implementando os frameworks de Alex Hormozi (100M Offers, 100M Leads). "
        "Use para arquitetura de oferta irresistivel, precificacao, geracao de leads, fechamento de "
        "venda, ganchos, retencao, modelos de negocio, planejamento de lancamento, design de "
        "workshop e auditoria completa de negocio. Gatilhos: oferta, grand slam offer, precificacao, "
        "geracao de leads, LTV, CAC, escala, fechamento, retencao, modelo de negocio, Hormozi."
    ),
    "storytelling": (
        "Squad de 12 mestres da narrativa (Joseph Campbell, Blake Snyder, Dan Harmon, Nancy Duarte, "
        "Oren Klaff, Matthew Dicks, Kindra Hall, Marshall Ganz, Shawn Coyne, Park Howell, "
        "Keith Johnstone). Use para construir narrativa, escrever manifesto, montar pitch, estruturar "
        "apresentacao, analisar uma historia existente e destravar bloqueio criativo. Gatilhos: "
        "storytelling, narrativa, historia, jornada do heroi, pitch, apresentacao, manifesto, "
        "arco narrativo, roteiro."
    ),
    "design-squad": (
        "Squad de 8 agentes de design e design operations (Brad Frost/Atomic Design, Dan Mall, "
        "Dave Malouf) mais especialistas em UX, UI, design system e geracao visual. Use para criar "
        "ou auditar design system, especificar componente, desenhar fluxo de UX, montar handoff para "
        "desenvolvimento e estruturar DesignOps. Gatilhos: design system, tokens, componente, UX, UI, "
        "wireframe, acessibilidade, atomic design, handoff, DesignOps, biblioteca de padroes."
    ),
    "data-squad": (
        "Squad de 7 estrategistas data-driven: analytics (Avinash Kaushik), valor de cliente "
        "(Peter Fader), growth (Sean Ellis), comunidade (David Spinks), customer success "
        "(Nick Mehta) e educacao (Wes Kao). Use para analisar dados, construir audiencia, medir "
        "growth, otimizar retencao e desenhar estrategia de comunidade. Gatilhos: analytics, "
        "metricas, growth, churn, retencao, LTV, coorte, KPI, dashboard, north star, comunidade."
    ),
    "cybersecurity": (
        "Squad de 15 agentes de seguranca ofensiva e defensiva (Georgia Weidman, Peter Kim, "
        "Jim Manico, Chris Sanders, Omar Santos, Marcus Carey) cobrindo pentest, red team, blue team, "
        "AppSec, recon e resposta a incidente. Use SOMENTE em contexto autorizado: teste de intrusao "
        "contratado, CTF, pesquisa de seguranca ou defesa da propria infraestrutura. Gatilhos: "
        "pentest, vulnerabilidade, OWASP, recon, hardening, incidente de seguranca, auditoria de "
        "seguranca, CVE, exploit, blue team, red team."
    ),
    "c-level-squad": (
        "C-suite virtual de 6 executivos: CEO (Vision Chief), COO, CMO, CTO, CIO e CAIO. Use para "
        "definir visao e estrategia de empresa, planejar go-to-market, avaliar decisao de tecnologia, "
        "desenhar operacoes e preparar captacao de investimento. Gatilhos: visao, estrategia de "
        "empresa, go-to-market, captacao, investidor, board, decisao executiva, operacoes, "
        "escolha de stack, roadmap de empresa."
    ),
    "advisory-board": (
        "Board de 11 conselheiros estrategicos clonados como agentes (Ray Dalio, Charlie Munger, "
        "Naval Ravikant, Peter Thiel, Reid Hoffman, Simon Sinek, Brene Brown, Patrick Lencioni, "
        "Derek Sivers, Yvon Chouinard) com um chair que convoca, provoca tensao produtiva e "
        "sintetiza. Use para decisao dificil de fundador, dilema de escala, crise de cultura, "
        "conselho de investimento e questoes que merecem varias perspectivas em conflito. Gatilhos: "
        "conselho, decisao dificil, dilema, segunda opiniao, board, mentoria estrategica."
    ),
    "movement": (
        "Squad de 7 agentes para construcao de movimentos e tribos: fenomenologia, identidade "
        "coletiva, manifesto, arquitetura de movimento, ciclos de crescimento e medicao de impacto. "
        "Use quando o objetivo for reunir pessoas em torno de uma causa, criar senso de pertencimento "
        "e transformar publico em comunidade militante. Gatilhos: movimento, tribo, causa, manifesto, "
        "pertencimento, comunidade, identidade coletiva, mobilizacao."
    ),
    "claude-code-mastery": (
        "Squad de 8 agentes especializados em dominar ferramentas agenticas de desenvolvimento: "
        "hooks, skills, subagents, MCP, plugins, times de agentes, engenharia de contexto e "
        "integracao com projetos existentes. Use para configurar o ambiente do agente, auditar "
        "settings e permissoes, desenhar hooks, planejar integracao de MCP, escrever arquivos de "
        "instrucao do projeto, decompor trabalho em paralelo e reduzir context rot. Gatilhos: hooks, "
        "MCP, subagent, skill, plugin, settings, permissoes, CLAUDE.md, AGENTS.md, context rot, "
        "worktree, configuracao do agente."
    ),
}

# Squads cujo conteudo pressupoe cautela adicional na ativacao.
AVISOS = {
    "cybersecurity": (
        "> **Uso autorizado apenas.** Este squad cobre tecnicas ofensivas. Ative somente em "
        "pentest contratado, CTF, pesquisa de seguranca ou defesa de infraestrutura propria. "
        "Confirme o contexto de autorizacao antes de executar qualquer operacao ofensiva."
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# Roteamento do chefe geral.
#
# Skills nao tem namespacing por slash command. O Xquads Chief ativa um squad
# lendo o SKILL.md dele e seguindo suas proprias instrucoes de ativacao — o que
# funciona identico em qualquer cliente.
# ─────────────────────────────────────────────────────────────────────────────
ROTEAMENTO = [
    ("Copy, headline, VSL, email, carta de vendas", "copy-squad"),
    ("Copy avancado, persuasao, pitch, negociacao, SaaS", "copy-master"),
    ("Trafego pago, Meta Ads, Google Ads, escala, tracking", "traffic-masters"),
    ("Marca, posicionamento, naming, arquetipo", "brand-squad"),
    ("Campanha integrada de marketing ponta a ponta", "marketing-squad"),
    ("Oferta, precificacao, leads, fechamento, escala", "hormozi-squad"),
    ("Narrativa, pitch, apresentacao, manifesto", "storytelling"),
    ("UX, UI, design system, componente, handoff", "design-squad"),
    ("Analytics, growth, retencao, comunidade", "data-squad"),
    ("Seguranca, pentest, AppSec, incidente", "cybersecurity"),
    ("Visao, go-to-market, captacao, decisao executiva", "c-level-squad"),
    ("Conselho estrategico, decisao dificil, dilema", "advisory-board"),
    ("Movimento, tribo, causa, pertencimento", "movement"),
    ("Hooks, MCP, subagents, configuracao do agente", "claude-code-mastery"),
]


def bloco_roteamento() -> list[str]:
    linhas = ["## Squads que ele ativa", ""]
    linhas.append("| Dominio da demanda | Skill a ativar |")
    linhas.append("|---|---|")
    for dominio, squad in ROTEAMENTO:
        linhas.append(f"| {dominio} | `{squad}` |")
    linhas += [
        "",
        "**Como ativar um squad.** Skills nao tem namespacing por slash command, e cada",
        "cliente expoe a invocacao de um jeito. O procedimento abaixo funciona em todos:",
        "",
        "1. Localize a pasta da skill do squad. Ela fica ao lado desta, no mesmo diretorio",
        "   de skills (`../<squad>/`), ou no diretorio de skills do ambiente.",
        "2. Leia o `SKILL.md` do squad e siga as instrucoes de ativacao que estao la.",
        "3. Entregue ao chefe do squad o briefing de handoff (maximo 500 tokens) e saia de",
        "   cena. O chefe do squad conduz dali em diante.",
        "",
        "Se o cliente expuser as skills por nome (comando, menu ou invocacao implicita),",
        "use esse caminho — e equivalente e mais direto.",
        "",
        "> **Squad nao instalado = rota indisponivel.** Antes de ativar, confirme que a pasta",
        "> do squad existe. Se nao existir, diga isso ao usuario, indique como instalar",
        "> (`install.sh <squad>`) e ofereca a alternativa mais proxima entre as instaladas.",
        "> Nunca finja ter ativado um squad ausente.",
        "",
        "**Fora do escopo do Xquads:** desenvolvimento de software e codigo. Isso vai para o",
        "fluxo de desenvolvimento do usuario (no RAXOS, o Story Development Cycle), nunca",
        "para um squad de marketing.",
        "",
    ]
    return linhas


def ler(caminho: Path) -> str:
    try:
        return caminho.read_text(encoding="utf-8")
    except OSError:
        return ""


def campo(texto: str, chave: str) -> str | None:
    """Extrai um escalar de primeiro nivel de um YAML simples, sem dependencias."""
    m = re.search(rf"^\s*{re.escape(chave)}:\s*(.+?)\s*$", texto, re.M)
    if not m:
        return None
    valor = m.group(1).strip()
    if valor.startswith(("|", ">")):
        return None
    return valor.strip("\"'")


def metadados(squad: Path) -> dict:
    """Le squad.yaml e config.yaml, cobrindo os dois layouts em uso no repo."""
    manifesto = ler(squad / "squad.yaml")
    config = ler(squad / "config" / "config.yaml") or ler(squad / "config.yaml")
    juntos = manifesto + "\n" + config

    return {
        "nome": squad.name,
        "titulo": (
            campo(manifesto, "short-title")
            or campo(config, "display_name")
            or squad.name.replace("-", " ").title()
        ),
        "versao": campo(manifesto, "version") or campo(config, "version") or "1.0.0",
        "chefe": campo(juntos, "entry_agent"),
        "dominio": campo(config, "domain") or "",
    }


def listar(pasta: Path, sufixos: tuple[str, ...]) -> list[str]:
    if not pasta.is_dir():
        return []
    return sorted(
        f.name for f in pasta.iterdir()
        if f.is_file() and f.suffix in sufixos and not f.name.startswith(".")
    )


def montar_skill(squad: Path) -> str:
    meta = metadados(squad)
    nome = meta["nome"]
    descricao = DESCRICOES[nome]

    agentes = listar(squad / "agents", (".md",))
    tasks = listar(squad / "tasks", (".md",))
    workflows = listar(squad / "workflows", (".yaml", ".yml", ".md"))
    checklists = listar(squad / "checklists", (".md",))
    dados = listar(squad / "data", (".yaml", ".yml", ".md", ".json"))

    chefe = meta["chefe"]
    if chefe and f"{chefe}.md" not in agentes:
        chefe = None
    especialistas = [a for a in agentes if a != f"{chefe}.md"]

    linhas: list[str] = []
    add = linhas.append

    # ── Frontmatter ──────────────────────────────────────────────────────────
    add("---")
    add(f"name: {nome}")
    add(f"description: >-")
    for pedaco in quebrar(descricao, 96):
        add(f"  {pedaco}")
    add("license: MIT")
    add("metadata:")
    add(f'  squad: "{meta["titulo"]}"')
    add(f'  version: "{meta["versao"]}"')
    add(f'  agents: "{len(agentes)}"')
    add('  author: "Xquads by Synkra"')
    add("---")
    add("")

    # ── Corpo ────────────────────────────────────────────────────────────────
    add(f"# {meta['titulo']}")
    add("")
    if meta["dominio"]:
        add(f"**Dominio:** {meta['dominio']}")
        add("")
    if nome in AVISOS:
        add(AVISOS[nome])
        add("")

    add("## Como ativar")
    add("")
    add(
        "Todos os caminhos abaixo sao **relativos a raiz desta skill**. Leia os arquivos "
        "diretamente do disco com a ferramenta de leitura do seu ambiente. Nao existe "
        "dependencia de slash command, de plugin ou de qualquer cliente especifico."
    )
    add("")

    if chefe:
        add(f"1. Leia `agents/{chefe}.md` por completo. E a definicao autocontida do chefe do")
        add("   squad: persona, principios, logica de roteamento e limites. Adote-a.")
        if dados:
            catalogo = next((d for d in dados if "routing" in d or "catalog" in d), dados[0])
            add(f"2. Carregue `data/{catalogo}` como contexto de roteamento. Nao exiba o conteudo,")
            add("   apenas absorva.")
            n = 3
        else:
            n = 2
        add(f"{n}. Cumprimente com o `greeting` da persona e aguarde a demanda.")
        add(f"{n + 1}. Ao rotear para um especialista, leia `agents/<especialista>.md` e assuma")
        add("   aquela persona, mantendo o briefing que o chefe montou.")
        add(f"{n + 2}. Permaneca no squad ate receber `*exit`.")
    else:
        add("1. Leia o arquivo do agente desejado em `agents/` e adote a persona por completo.")
        add("2. Cumprimente com o `greeting` da persona e aguarde a demanda.")
        add("3. Permaneca no agente ate receber `*exit`.")
    add("")

    add("## Executando uma task")
    add("")
    add(
        "As tasks em `tasks/` sao roteiros executaveis com entradas, passos e formato de saida "
        "definidos. Leia o arquivo inteiro antes de comecar e siga os passos na ordem. Tasks "
        "marcadas com `elicit: true` exigem resposta do usuario em cada ponto de elicitacao — "
        "nao presuma respostas nem pule etapas."
    )
    add("")

    if nome == "xquads":
        linhas.extend(bloco_roteamento())

    if chefe:
        add("## Agentes")
        add("")
        add(f"**Chefe do squad** — `agents/{chefe}.md`")
        add("")
        if especialistas:
            add(f"**Especialistas ({len(especialistas)})**")
            add("")
            for a in especialistas:
                add(f"- `agents/{a}`")
            add("")
    elif agentes:
        add(f"## Agentes ({len(agentes)})")
        add("")
        for a in agentes:
            add(f"- `agents/{a}`")
        add("")

    if tasks:
        add(f"## Tasks ({len(tasks)})")
        add("")
        for t in tasks:
            add(f"- `tasks/{t}`")
        add("")

    if workflows:
        add(f"## Workflows ({len(workflows)})")
        add("")
        add("Sequencias multi-agente ja encadeadas. Siga as fases na ordem declarada.")
        add("")
        for w in workflows:
            add(f"- `workflows/{w}`")
        add("")

    if checklists:
        add("## Checklists")
        add("")
        add("Rode antes de entregar. Nao declare a entrega pronta com item em aberto.")
        add("")
        for c in checklists:
            add(f"- `checklists/{c}`")
        add("")

    if dados:
        add("## Dados de referencia")
        add("")
        for d in dados:
            add(f"- `data/{d}`")
        add("")

    add("## Convencoes")
    add("")
    add("- Comandos do agente usam o prefixo `*` (`*help`, `*exit`, e os declarados na persona).")
    add("- Responda em portugues (pt-BR), salvo pedido explicito em contrario.")
    add("- O chefe do squad nao executa o trabalho do especialista: ele diagnostica e delega.")
    add("- Um agente por vez. Troca de agente encerra a persona anterior.")
    add("")
    add("---")
    add("")
    add("*Parte do [Xquads](https://github.com/ohmyjahh/xquads-squads) — Agent Skills padrao aberto.*")

    return "\n".join(linhas) + "\n"


def quebrar(texto: str, largura: int) -> list[str]:
    palavras, linhas, atual = texto.split(), [], ""
    for p in palavras:
        if atual and len(atual) + 1 + len(p) > largura:
            linhas.append(atual)
            atual = p
        else:
            atual = f"{atual} {p}".strip()
    if atual:
        linhas.append(atual)
    return linhas


def main() -> int:
    squads = sorted(
        d for d in RAIZ.iterdir()
        if d.is_dir()
        and not d.name.startswith((".", "_"))
        and d.name not in {"scripts", "docs"}
        and (d / "agents").is_dir()
    )

    faltando = [d.name for d in squads if d.name not in DESCRICOES]
    if faltando:
        print(f"ERRO: squads sem description curada: {', '.join(faltando)}", file=sys.stderr)
        return 1

    for squad in squads:
        destino = squad / "SKILL.md"
        destino.write_text(montar_skill(squad), encoding="utf-8")
        print(f"  gerado  {destino.relative_to(RAIZ)}")

    print(f"\n{len(squads)} SKILL.md gerados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
